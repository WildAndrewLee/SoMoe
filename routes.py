import os, time, hashlib, shutil, datetime
from flask import Flask, request, abort, render_template, session, redirect, url_for, send_from_directory, flash, jsonify
from werkzeug import secure_filename

from main import app

from config import config

conf = globals()
conf.update(config)

from helpers import write_log, get_path
from auth import requires_auth
from upload import Upload

'''
Endpoints
'''
@app.route('/login', methods=['GET'])
@requires_auth
def login():
	return redirect(url_for('index'))

# This endpoint is not made public due to all of the
# fucking things that could possibly happen.
#
# It's a good idea to make your entire uploads
# directory read and write only.
@app.route('/serve/<h>', methods=['GET'])
def serve(h):
	path = get_path(h)
	return send_from_directory(app.config['UPLOAD_FOLDER'], path)

@app.route('/fetch/<h>', methods=['GET'])
def fetch(h):
	path = get_path(h)
	return send_from_directory(app.config['UPLOAD_FOLDER'], path, as_attachment=True)

@app.route('/delete/<h>', methods=['GET'])
@requires_auth
def delete_url(h):
	if 'admin' not in session or not session['admin']:
		abort(404)

	try:
		path = Upload.query.filter(Upload.h == h).one()
	except:
		abort(404)

	sys_path = os.path.join(app.config['UPLOAD_FOLDER'], path.path)

	shutil.rmtree(os.path.dirname(sys_path))
	path.delete()

	msg = 'Deleted hash <{0}>.'.format(h)

	flash(msg)
	write_log('Removed file with hash ' + h)

	return redirect(url_for('index'))

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

	h = hashlib.md5(filename).hexdigest()
	h += hashlib.md5(str(now)).hexdigest()

	Upload(h, ip, filename, now).save()

	return render_template('build.html', title='Access URL', hash=h)

@app.route('/opps/<path:err>', methods=['GET'])
def oops(err):
	if not err:
		abort(404)

	if err not in MESSAGES:
		abort(404)

	return render_template('oops.html', title=MESSAGES[err], message=MESSAGES[err])

@app.route('/upload', methods=['POST'])
def upload():
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
	hashed_name = hashlib.md5(filename).hexdigest()
	hashed_time = hashlib.md5(str(now)).hexdigest()

	directory = os.path.join(app.config['UPLOAD_FOLDER'], hashed_time, hashed_name)

	# Highly unlikely that we need to check this due
	# to the nature of MD5 hashing but oh well.

	if not os.path.exists(directory):
		os.makedirs(directory)

	path = os.path.join(directory, filename)
	
	file.save(path)
	write_log('Uploaded ' + path)

	session['filename'] = path

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