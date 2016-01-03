import datetime, hashlib, os, random, subprocess, time
from flask import abort, flash, jsonify, redirect, render_template, request, send_from_directory, session, url_for
from flask.ext.login import current_user, fresh_login_required, login_user, logout_user
from werkzeug import secure_filename

from config import config
from main import app, bcrypt, login_manager
from helpers import write_log
from models.db import session_factory
from models.invite import Invite
from models.upload import Upload
from models.user import requires_role, User
from login import Login
from register import Register

@app.route('/grill', methods=['GET'])
def grill():
	grill_dir = os.path.join(os.path.dirname(__file__), 'static/grill')
	grills = os.listdir(grill_dir)
	rand = int(random.random() * len(grills))

	return send_from_directory(grill_dir, grills[rand])

@login_manager.unauthorized_handler
def not_found():
	abort(404)

@app.route('/logout', methods=['GET'])
def logout():
	logout_user()
	flash('You have been logged out.')

	return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated():
		return redirect(url_for('index'))

	login = Login(request.form)

	if request.method == 'POST':
		user = login.validate()

	 	if user:
			flash('You are now logged in as ' + user.username + '.')

			login_user(user)

			return redirect(url_for('index'))

	return render_template('login.html', title='Log In', form=login)

@app.route('/invite/<name>', methods=['GET'])
@fresh_login_required
@requires_role(0)
def invite_new(name):
	with session_factory() as sess:
		if User.get_by_name(name):
			return 'User already exists.'

		try:
			h = hashlib.md5(name + str(time.time())).hexdigest()
			Invite(name=name, h=h).save()
		except:
			return 'Invite already exists.'

	return url_for('invite', name=name, h=h, _external=True)

@app.route('/invite/<name>/<h>', methods=['GET', 'POST'])
def invite(name, h):
	if current_user.is_authenticated():
		return redirect(url_for('index'))

	if not Invite.confirm_invite(name, h):
		flash(config.messages.BAD_INVITE, category='red')
		return redirect(url_for('index'))

	register = Register(request.form)
	register._action = request.path

	if request.method == 'POST' and register.validate():
		user = User(
			username=name,
			h=bcrypt.generate_password_hash(register.password.data),
			max_load=AUTH_PAYLOAD
		).save()

		Invite.delete_invite(name, h)

		flash('You are now registered.')

		return redirect(url_for('login'))

	return render_template('register.html', title='You\'re Invited', form=register)

@app.route('/build-url', methods=['GET'])
def build_url():	
	if 'filename' not in session or not session['filename']:
		return redirect(url_for('index'))

	filename = session['filename']
	session['filename'] = None
	now = datetime.datetime.utcnow()
	ip = get_ip if config.LOGGING else 'Logging Disabled'

	Upload(ip=ip, path=filename).save()

	return render_template('build.html', title='Access URL', hash=filename)

def process_file(file):
	filename = secure_filename(file.filename)

	if not filename:
		filename = hashlib.md5(time.time()).hexdigest()

	path = os.path.join(config.UPLOAD_FOLDER, hashlib.sha1(filename + str(now)).hexdigest()[:10] + os.path.splitext(filename)[1])
	
	file.save(path)

	# Strip meta-data if we can.
	exiftool = ''
	command = config.script.EXIF_TOOL.format(**locals())
	subprocess.call(command)

	# Scan for virus
	try:
		command = config.script.CLAMDSCAN.format(**locals())

		subprocess.check_call(command, shell=True)
	except subprocess.CalledProcessError:
		return jsonify({
			'mode': 'message',
			'message': config.messages.VIRUS,
			'color': 'red'
		})

	rel_path = path.replace(config.UPLOAD_FOLDER, '')

	subprocess.call(config.script.UPLOAD_AWS.format(**locals()), shell=True)

	write_log('Uploaded ' + path)

	session['filename'] = rel_path

	return None

@app.route('/upload', methods=['POST'])
def upload():
	content_length = request.content_length

	if not content_length:
		abort(500)

	if current_user.is_authenticated():
		max_payload = current_user.max_payload()
	else:
		max_payload = config.MAX_PAYLOAD

	max_payload *= 1024 ** 2

	if content_length > max_payload:
		return jsonify({
			'mode': 'message',
			'message': config.messages.TOO_BIG,
			'color': 'red'
		})

	now = time.time()

	if 'last' in session and now - session['last'] < UPLOAD_WAIT:
		return jsonify({
			'mode': 'message',
			'message': config.messages.SLOW_DOWN,
			'color': 'red'
		})
   
	session['last'] = now

	if 'upload' not in request.files:
		return jsonify({
			'mode': 'message',
			'message': config.messages.EMPTY,
			'color': 'red'
		})

	file = request.files['upload']

	error = process_file(file)

	if error is not None:
		return error

	return jsonify({
		'mode': 'redirect',
		'url': url_for('build_url')
	})

@app.route('/guidelines', methods=['GET'])
def guidelines():
	return render_template('guidelines.html', title='Guidelines')

@app.route('/', methods=['GET'])
def index():
	return render_template('upload.html')