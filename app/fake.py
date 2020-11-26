from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from .import db
from .models import User,Post,Comment

def users(count=100):
	fake = Faker(locale='zh_CN')
	i = 0
	while i < count:
		u = User(email = fake.email(),
				username = fake.user_name(),
				password = 'password',
				confirmed = True,
				name = fake.name(),
				location = fake.city(),
				about_me = fake.text(),
				member_since = fake.past_date())
		db.session.add(u)
		try:
			db.session.commit()
			i +=1
		except IntegrityError:
			db.session.rollbock()

def posts(count = 100):
	fake = Faker(locale='zh_CN')
	user_count = User.query.count()
	for i in range(count):
		u = User.query.offset(randint(0, user_count - 1)).first()
		p = Post(body = fake.text(),
				timestamp = fake.past_date(),
				author = u)
		db.session.add(p)
	db.session.commit()

def comments(count = 300):
	fake = Faker(locale='zh_CN')
	post_count = Post.query.count()
	for i in range(count):
		p = Post.query.offset(randint(0, post_count - 1)).first()
		c = Comment(body = fake.sentence(),
					timestamp = fake.past_date(),
					post = p,
					author = p.author)
		db.session.add(c)
	db.session.commit()