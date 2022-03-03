from werkzeug.security import generate_password_hash, check_password_hash
from config import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(80), nullable=False)
    password = db.Column(db.String(128)) 
    email = db.Column(db.String(128), nullable=False) 
    roles = db.relationship('Role', backref = 'user', lazy= 'dynamic')
    
    def __repr__(self):
        return f'<User {self.id} {self.username} {self.email}>'

    @property
    def password(self):
        # Preventing password from being accessed
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        # Set password to a hashed password
        password = generate_password_hash(password)

    def verify_password(self, password):
        # Check if hashed password matches actual password
        return check_password_hash(self.password, password)

    def get_id(self):
        return (self.id)

    @login_manager.user_loader
    def load_user(id):         
        return User.query.get(int(id))

class Role(db.Model):
    __tablename__="roles"
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    def __repr__(self):
        return f'<Role {self.id} {self.role_name}>'