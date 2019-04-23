from datetime import datetime
from app import db


class Bing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hsh = db.Column(db.String(120), nullable=True, unique=True)
    datetime = db.Column(db.DateTime, nullable=True, default=datetime.now)
    url = db.Column(db.String(120), nullable=True)
    urlbase = db.Column(db.String(120), nullable=True)
    copyright = db.Column(db.Text)
    title = db.Column(db.String(120))
    caption = db.Column(db.Text)
    description = db.Column(db.Text)
    shares = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<Bing:%r>" % self.id

    def get_json(self):
        return dict(
            id=self.id,
            datetime=self.datetime,
            url=self.url,
            title=self.title,
            caption=self.caption,
            description=self.description
        )
