from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

