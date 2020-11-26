import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True if os.environ.get('MAIL_USE_TLS', False) == 'True' else False
    MAIL_USE_SSL = False if os.environ.get('MAIL_USE_SSL', True) == 'False' else True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <'+ str(MAIL_USERNAME) + '>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_POSTS_PER_PAGE = 10
    FLASKY_FOLLOWERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE =10
    SQLALCHEMY_RECORD_QUERIES = True
    FLASK_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        #出错时邮件通知管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME',None) is not None:
            credentials = (cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
            if getattr(cls,'MAIL_USE_TLS',None):
                secure=()
        mail_handler = SMTPHandler(
            mail_host = (cls.MAIL_SERVER,cls.MAIL_PASSWORD),
            formaddr = cls.FLASKY_MAIL_SENDER,
            toaddr = [cls.FLASKY_ADMIN],
            subject = cls.FLASKY_MAIL_SUBJECT_PREFIX + 'Application Error',
            credentials = credentials,
            secure = secure
            )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
