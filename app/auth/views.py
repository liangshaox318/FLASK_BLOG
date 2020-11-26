from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,login_required,logout_user,current_user
from . import auth
from ..models import User 
from .. import db
from .forms import LoginForm,RegistrationForm,ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from ..email import send_email


@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed \
				and request.endpoint \
				and request.blueprint != 'auth' \
				and request.endpoint != 'static' :
			return redirect(url_for('auth.unconfirmed'))

@auth.route('/login',methods = ['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			next = request.args.get('next')
			if next is None or not next.startswith('/'):
				next = url_for('main.index')
			return redirect(next)
		flash('用户名或密码无效.')
	return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('您已退出.')
	return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email,'验证您的账户',
					'auth/email/confirm',user=user,token=token)
		flash('验证邮件已发送至您的邮箱.')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		db.session.commit()
		flash('您已成功通过账号验证. 十分感谢!')
	else:
		flash('确认链接无效或已过期.')
	return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
	if current_user.confirmed is not True:
		token = current_user.generate_confirmation_token()
		send_email(current_user.email, '验证您的账户',
						'auth/email/confirm',user=current_user,token=token)
		flash('新的验证邮件已发送至您的邮箱.')
	return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			db.session.commit()
			flash('用户密码修改成功.')
			return redirect(url_for('main.index'))
		else:
			flash('密码无效.')
	return render_template("auth/change_password.html",form=form)


@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data.lower()).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email, '重置您的账户密码',
						'auth/email/reset_password',
						user = user ,token=token)
			flash('重置密码邮件已发送至您的邮箱.')
			return redirect(url_for('auth.login'))
		else:
			flash('抱歉，没有找的您的邮箱!')
	return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token,form.password.data):
            db.session.commit()
            flash('用户密码修改成功.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '重置您的邮箱',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('重置密码邮件已发送至您的邮箱.')
            return redirect(url_for('main.index'))
        else:
            flash('抱歉，没有找的您的邮箱!')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('用户邮箱修改成功.')
    else:
        flash('请求无效.')
    return redirect(url_for('main.index'))









