from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField,BooleanField ,SubmitField 
from wtforms.validators import DataRequired ,Length , Email ,Regexp ,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Length(1,64),Email(
                        message='请输入正确邮箱')])
	password = PasswordField('密码' , validators=[DataRequired()])
	remember_me = BooleanField('保持登录状态')
	submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Length(1,64),Email(
                        message='请输入正确邮箱')])
	username = StringField('用户名',validators=[
		DataRequired(),Length(1,64),
		Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
				'用户名必须只含字母、数字、点或下划线')])
	password = PasswordField('密码' , validators=[
		DataRequired(),EqualTo('password2',message='密码必须一致.')])
	password2 = PasswordField('再次输入',validators=[DataRequired()])
	submit = SubmitField('注册')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('邮箱已经注册.')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('用户名已使用.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须一致.')])
    password2 = PasswordField('再次输入',
                              validators=[DataRequired()])
    submit = SubmitField('修改密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email(
                                                message='请输入正确邮箱')])
    submit = SubmitField('重置密码')


class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须一致.')])
    password2 = PasswordField('再次输入', validators=[DataRequired()])
    submit = SubmitField('修改密码')


class ChangeEmailForm(FlaskForm):
    email = StringField('新Email地址', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('修改邮件地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('邮件地址已注册.')
