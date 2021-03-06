import os
import click
import sys
from flask_migrate import Migrate,upgrade
from app import create_app, db
from app.models import User, Role,Post,Comment
from dotenv import load_dotenv

dotenv_flaskenv_path = os.path.join(os.path.dirname(__file__),'.flaskenv')
if os.path.exists(dotenv_flaskenv_path):
	load_dotenv(dotenv_flaskenv_path)
dotenv_env_path = os.path.join(os.path.dirname(__file__),'.env')
if os.path.exists(dotenv_env_path):
	load_dotenv(dotenv_env_path)


COV = None
if os.environ.get('FLAKS_COVERAGE'):
	import coverage
	COV = coverage.coverage(branch = True, include = 'app/*')
	COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role,Post=Post,Comment=Comment)

@app.cli.command()
def deploy():
	"""Run deployment tasks"""
	#把数据库迁移到最新版本
	upgrade()
	#创建或更新角色
	Role.insert_roles()
	#确保所有用户都关注自己
	User.add_self_follows()


@app.cli.command()
@click.option('--coverage/--no-coverage',default=False,
				help = 'Run tests under code coverage.')
def test(coverage):
	"""Run the unit tests."""
	if coverage and not os.environ.get('FLAKS_COVERAGE'):
		os.environ['FLAKS_COVERAGE'] = '1'
		os.execvp(sys.executable,[sys.executable]+ sys.argv)
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)
	if COV:
		COV.stop()
		COV.save()
		print('Coverage Summary:')
		COV.report()
		basedir = os.path.abspath(os.path.dirname(__file__))
		covdir = os.path.join(basedir,'tmp/coverage')
		COV.html_report(directory=covdir)
		print('HTML version: file://%s/index.html' % covdir)
		COV.erase()

@app.cli.command()
@click.option('--length',default=25,
				help='Number of functions to include in the profiler report.')
@click.option('--profiler-dir',default=None,
				help='directory where profiler data files are saved.')
def profile(length,profile_dir):
	"""Start the application under the code profiler"""
	from werkzeug.contrib.profiler import ProfilerMiddleware
	app.wsgi_app = ProfilerMiddleware(app.wsgi_app,restrictions = [length],
									profile_dir=profile_dir)
	app.run(debug = False)