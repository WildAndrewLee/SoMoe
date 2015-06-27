from wtforms import Form, TextField, PasswordField, validators
from user import User

'''
Form for logging in.
'''
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

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.validate(self.name.data, self.password.data)

		if not user:
			# Quick hack to add a custom error post-form validation.
			self.name.errors.append('Invalid username or password specified.')
			return False

		return user