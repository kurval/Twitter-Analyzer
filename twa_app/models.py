from app import db

class Usertable(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String())
    oauth_token = db.Column(db.String())
    oauth_token_secret = db.Column(db.String())

    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return f"<User {self.screen_name}>"