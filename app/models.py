from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Bing(db.Model):
    __tablename__ = 'bings'

    id = db.Column(db.Integer, primary_key=True)
    hsh = db.Column(db.String(120), nullable=True, unique=True)
    pub_date = db.Column(db.DateTime, nullable=True, default=datetime.now)
    url = db.Column(db.String(120), nullable=True)
    urlbase = db.Column(db.String(120), nullable=True)
    copyright = db.Column(db.Text)
    title = db.Column(db.String(120))
    caption = db.Column(db.Text)
    description = db.Column(db.Text)

    def __repr__(self):
        return "<Bing:%r>" % self.id

    def get_json(self):
        return dict(
            hsh=self.hsh,
            pub_date=self.pub_date.strftime("%Y%m%d"),
            url=self.url,
            title=self.title,
            caption=self.caption,
            description=self.description
        )


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    pwd = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.name

    def generate_password_hash(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def check_password_hash(self, pwd):
        return check_password_hash(self.pwd, pwd)


class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return "<Visitor:%r>" % self.addr
