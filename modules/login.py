from wtforms import Form, TextField, PasswordField, validators

from main import app, bcrypt
from models.user import User

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

		user = User.get_by_name(self.name.data)

		if not user or not bcrypt.check_password_hash(user.h, self.password.data):
			# Quick hack to add a custom error post-form validation.
			self.name.errors.append('Invalid username or password specified.')
			return False

		return user