from wtforms import Form, validators, StringField, EmailField, PasswordField


class CreateSongForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=150)])
    artist = StringField('Artist', [validators.DataRequired(), validators.Length(min=1, max=150)])
    album = StringField('Album', [validators.DataRequired(), validators.Length(min=1, max=150)])
    track = StringField('Track', [validators.DataRequired(), validators.Length(min=1, max=150)],
                        default='Test')
    cover = StringField('Cover', [validators.DataRequired(), validators.Length(min=1, max=150)],
                        default='Test')


class LoginForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Length(min=1, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8, max=50)])


class CreateAccountForm(LoginForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=1, max=150)])
    confirm_password = PasswordField(
        'Confirm Password', [
            validators.DataRequired(),
            validators.EqualTo('password', message='Passwords must match')
        ]
    )
