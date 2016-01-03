from wtforms import Form, TextField, PasswordField, validators

class Login(Form):
	_method = 'POST'
	_action = '/login'

	name = TextField('Username', validators = [
		validators.Required(message = 'You must enter a username.')
	])

	password = PasswordField('Password', validators = [
		validators.Required(message = 'You must enter a password.')
	])

	submit_text = 'Log In'