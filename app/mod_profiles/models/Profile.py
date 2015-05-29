from app.mod_shared.models import db

class Profile(db.Model):
    # Attributes
    id         = db.Column(db.Integer, primary_key=True)
    last_name  = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    gender     = db.Column(db.Integer)
    birthday   = db.Column(db.Date)


    def __init__(self, last_name, first_name, gender, birthday):
        self.last_name  = last_name
        self.first_name = first_name
        self.gender     = gender
        self.birthday   = birthday

    def __repr__(self):
        return '<Profile: %r %r>' % (self.first_name, self.last_name)
