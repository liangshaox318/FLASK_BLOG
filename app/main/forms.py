from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField,BooleanField,SelectField
from wtforms.validators import DataRequired,Regexp,Length,Email,EqualTo
from wtforms import ValidationError
from ..models import User,Role,AnonymousUser
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('请输入你的名字?', validators=[DataRequired()])
    submit = SubmitField('提交')

class EditProfileForm(FlaskForm):
	name = StringField('真实姓名', validators=[Length(0,64)])
	location = StringField('地址',validators=[Length(0,64)])
	about_me = TextAreaField('个性签名')
	submit = SubmitField('提交')

class EditProfileAdminForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(), Length(1,64),
												Email(
													message='请输入正确邮箱')])
	username = StringField('用户名',validators=[
						DataRequired(),Length(1,64),
						Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
								'用户名必须只含字母、数字、点或下划线')])
	confirmed = BooleanField('是否通过验证')
	role = SelectField('角色',coerce=int)
	name = StringField('真实姓名',validators=[Length(0,64)])
	location = StringField('地址', validators=[Length(0,64)])
	about_me = TextAreaField('个性签名')
	submit = SubmitField('提交')

	def __init__(self,user,*arg,**kwargs):
		super(EditProfileAdminForm,self).__init__(*arg,**kwargs)
		self.role.choices = [(role.id,role.name)
								for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self,field):
		if field.data != self.user.email and \
				User.query.filter_by(email = field.data).first():
			raise ValidationError('Email已被注册.')
	def validate_username(self,field):
		if field.data != self.user.username  and \
				User.query.filter_by(username = field.data).first():
			raise ValidationError('用户名已被使用.')

class PostForm(FlaskForm):
	body = PageDownField("发布您的想法?",validators=[DataRequired()])
	submit = SubmitField('提交')

class CommentForm(FlaskForm):
	body = StringField('',validators=[DataRequired()])
	submit = SubmitField('提交')

