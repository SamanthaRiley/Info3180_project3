from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, Optional, NumberRange
from wtforms.fields.html5 import IntegerField
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User, Profile
from app import db


class RegForm(Form):
    email       = StringField('Email',              validators=[Required(), Length(1, 64), Email()])
    password    = PasswordField('Password',         validators=[Required(), EqualTo('confirmpassword', message='Passwords must match.')])
    confirmpassword   = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Submit')
     
    def validate_email(self, field):
        if db.session.query(User).filter(User.email == field.data).first():
            raise ValidationError('Email already registered.')

class LoginForm(Form):
    email       = StringField('Email',              validators=[Required(), Length(1, 64), Email()])
    password    = PasswordField('Password',         validators=[Required()])
    login       = SubmitField('Login'),
    remember_me = BooleanField('Keep me logged in')

    
class ItemForm(Form):
    itemUrl     = StringField('Url',                validators=[Required()])
    imgUrl      = StringField('Image',              validators=[Required()])
    title       = StringField('Title',              validators=[Required()])
    description = TextAreaField('Description',      validators=[Required(), Length(max=200)])

#class WishForm(Form):
#	title = StringField('Title', validators=[Required()])  # add per user validation
#	description = TextAreaField('Description', validators=[Required()]) # add per user validation
#	url = URLField('URL', validators=[url()]) # add per user validation
#	add = SubmitField('Add')

class WishListForm(Form):
	title = StringField('Title', validators=[Required()])  # add per user validation
	create = SubmitField('Create')
    
#class UrlForm(Form):
#    url = StringField('URL', validators=[url()])
#    submit = SubmitField('Select Thumbnail')    

#class ShareWishlistForm(Form):
#    email1      = StringField('Email',              validators=[Required(), Length(1, 64), Email()])
#    email2      = StringField('Email',              validators=[Optional(), Length(1, 64), Email()])
#    email3      = StringField('Email',              validators=[Optional(), Length(1, 64), Email()])
#    email4      = StringField('Email',              validators=[Optional(), Length(1, 64), Email()])
#    email5      = StringField('Email',              validators=[Optional(), Length(1, 64), Email()])
    
class UserProfileForm(Form):
    username    = StringField('Username',          validators=[Required()])
    firstname   = StringField('First Name',        validators=[Required()])
    lastname    = StringField('Last Name',         validators=[Required()])
    sex         = RadioField('Sex',                validators=[Required()], choices=[('Male','Male'),('Female','Female')])
    age         = IntegerField('Age',              validators=[Required(),NumberRange(min=0, max=100)])
    img         = FileField('Image',               validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    
    def validate_username(self, field):
        if db.session.query(Profile).filter(Profile.username == field.data).first():
            raise ValidationError('Username already in use.')

            