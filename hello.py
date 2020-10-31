import os 
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap 
from flask_moment import Moment 
from flask_wtf import FlaskForm 
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_mail import Mail,Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI']= \
	'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIT'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasktest318@163.com>' 
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer , primary_key = True)
	name = db.Column(db.String(64),unique = True)
	user = db.relationship('User',backref = 'role')

	def __repr__(self):
		return '<Role %r>' %self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key = True)
	username =  db.Column(db.String(64),unique = True,index =True)
	role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username 

def send_email(to,subject,template ,**kwargs):
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIT'] + ' ' +subject,
					sender = app.config['FLASKY_MAIL_SENDER'],recipients=[to])
	msg.body = render_template(template + '.txt' , **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	mail.send(msg)

class NameForm(FlaskForm):
	name = StringField('What\'s your name?',validators=[DataRequired()])
	submit = SubmitField('Submit')

@app.shell_context_processor
def make_shell_context():
	return dict(db=db,User=User, Role=Role)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'),500

@app.route('/',methods=['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			db.session.commit()
			session['known'] = False
			if app.config['FLASKY_ADMIN']:
				send_email(app.config['FLASKY_ADMIN'],'NEW USER',
						'mail/new_user',user = user)
		else:
			session['known'] = True

		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'),
							known=session.get('known',False))
	
