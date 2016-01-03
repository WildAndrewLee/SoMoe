from wtforms import Form, PasswordField, validators

class Register(Form):
	_method = 'POST'
	_action = '/invite'

	password = PasswordField('Password', validators = [
		validators.Required(message = 'You must enter a password.'),
		validators.EqualTo('confirm', message = 'Passwords do not match.')
	])

	confirm = PasswordField('Confirm Password')

	submit_text = 'Register'