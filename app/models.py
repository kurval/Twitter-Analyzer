from app import db

class Usertable(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String())
    oauth_token = db.Column(db.String())
    oauth_token_secret = db.Column(db.String())