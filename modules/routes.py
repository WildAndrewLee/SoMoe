import os, time, hashlib, shutil, datetime, random, subprocess
from flask import request, abort, render_template, session, redirect, url_for, send_from_directory, flash, jsonify, escape
from flask.ext.login import fresh_login_required, login_user, logout_user, current_user
from werkzeug import secure_filename

from main import app, login_manager

from config import config

conf = globals()
conf.update(config)

from modules.helpers import write_log, get_path
from models.db import session_factory
from modules.login import Login
from modules.register import Register
from models.user import requires_role, User
from models.upload import Upload
from models.invite import Invite

'''
Endpoints
'''

@login_manager.unauthorized_handler
def not_found():
	abort(404)

@app.route('/grill', methods=['GET'])
def grill():
	grill_dir = os.path.join(os.path.dirname(__file__), 'static/grill')
	grills = os.listdir(grill_dir)
	rand = int(random.random() * len(grills))

	return send_from_directory(grill_dir, grills[rand])

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
	 
		# Role 0 is admin so don't check
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
		try:
			user = sess.query(User).filter(User.username == name).one()
			return 'User already exists.'
		except:
			pass

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
		flash('Oops. Looks like somebody gave you a bad invite.', category='red')
		return redirect(url_for('index'))

	register = Register(request.form)
	register._action = request.path

	if request.method == 'POST' and register.validate():
		user = User(
			username=name,
			h=register.password.data,
			max_load=AUTH_PAYLOAD
		)

		user.save()

		with session_factory() as sess:
			sess.query(Invite).filter(
				Invite.name == name,
				Invite.h == h
			).delete()

		flash('You are now registered.')

		return redirect(url_for('login'))

	return render_template('register.html', title='You\'re Invited', form=register)

@app.route('/build-url', methods=['GET'])
def build_url():	
	if 'filename' not in session or not session['filename']:
		return redirect(url_for('index'))

	filename = session['filename'].replace(app.config['UPLOAD_FOLDER'] + '/', '')
	session['filename'] = None
	now = datetime.datetime.utcnow()
	
	ip = 'Logging Disabled'

	if LOGGING:
		ip = get_ip()

	Upload(h=filename, ip=ip, path=filename, last_update=now).save()

	return render_template('build.html', title='Access URL', hash=filename)

@app.route('/opps/<path:err>', methods=['GET'])
def oops(err):
	if not err:
		abort(404)

	if err not in MESSAGES:
		abort(404)

	flash(MESSAGES[err], category='red')

	return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
	content_length = request.content_length

	if not content_length:
		abort(500)

	if current_user.is_authenticated():
		max_payload = current_user.max_payload()
	else:
		max_payload = MAX_PAYLOAD

	max_payload *= 1024 ** 2

	if content_length > max_payload:
		if 'ajax' in request.form:
			return jsonify({
				'mode': 'message',
				'message': MESSAGES['too-big'],
				'color': 'red'
			})
		else:
			redirect(url_for('oops', err='too-big'))

	now = time.time()

	if 'last' in session and now - session['last'] < UPLOAD_WAIT:
		if 'ajax' in request.form:
			return jsonify({
				'mode': 'message',
				'message': MESSAGES['slow-down'],
				'color': 'red'
			})

		return redirect(url_for('oops', err='slow-down'))
   
	session['last'] = now

	if 'upload' not in request.files:
		if 'ajax' in request.form:
			return jsonify({
				'mode': 'message',
				'message': MESSAGES['empty'],
				'color': 'red'
			})

		return redirect(url_for('oops', err='empty'))

	file = request.files['upload']

	filename = secure_filename(file.filename)

	if not filename:
		filename = hashlib.md5(time.time()).hexdigest()

	path = os.path.join('/tmp/', hashlib.sha1(filename + str(now)).hexdigest()[:10] + os.path.splitext(filename)[1])
	
	file.save(path)

	# Strip meta-data if we can.
	exiftool = '/usr/bin/exiftool'
	command = '{exiftool} -q -all= {path}'.format(**locals())
	subprocess.call(command, shell=True)

	# Scan for virus
	try:
		clamdscan = '/usr/bin/clamdscan'
		command = '{clamdscan} {path} | {clamdscan} --remove -'.format(**locals())

		# true_path is sanitized already.
		subprocess.check_call(command, shell=True)
	except subprocess.CalledProcessError:
		return jsonify({
			'mode': 'message',
			'message': MESSAGES['virus'],
			'color': 'red'
		})

	rel_path = path.replace('/tmp/', '')

	print subprocess.check_output('/usr/local/bin/aws s3 cp {path} s3://neko.somoe.moe/{rel_path} && /bin/rm -r {path}'.format(**locals()), shell=True)

	write_log('Uploaded ' + path)

	session['filename'] = rel_path

	if 'ajax' in request.form:
		return jsonify({
			'mode': 'redirect',
			'url': url_for('build_url')
		})

	return redirect(url_for('build_url'))

@app.route('/guidelines', methods=['GET'])
def guidelines():
	return render_template('guidelines.html', title='Guidelines')

@app.route('/', methods=['GET'])
def index():
	return render_template('upload.html')
