from flask import Flask, request
from flask_login import current_user, login_required
from flask_login.utils import login_user, logout_user

from config import db, ma, login_manager
from models import Role, User
from schema import userschema, userschemas, roleschema, roleschemas


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db.init_app(app)
ma.init_app(app)
login_manager.init_app(app)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Login"""
    if request.method == "POST":
        payload = request.get_json()
        username = payload['username']
        # password_hash = payload['password_hash']
        user = User.query.filter_by(username=username).first()
        print("user ",user)
        try:
            login_user(user=user, remember=False)
            print(" logged in user ",current_user)
            return 'Logged in successfully.....!'
        except:
            print("Login with appropriate username and password....!")
            return "Login with appropriate username and password....!"
    else:
        return "Login with username and password"


@app.route('/add-user', methods=['POST'])
def add_user():
    payload = request.get_json()
    user = userschema.load(payload)
    db.session.add(user)
    db.session.commit()
    return {'Message': 'User Created'}, 201

@app.route('/add-role', methods=['POST'])
def add_role():
    payload = request.get_json()
    print(payload)
    role_name = payload.get('role_name')
    exist_role = Role.query.filter(Role.role_name==role_name).scalar()
    if exist_role is not None:
        return {'Message': 'Role Already exist'}, 409
    role = roleschema.load(payload)  # => JSON to OBJ (Sereliazation)
    db.session.add(role)
    db.session.commit()
    return {'Message': 'Role Created'}, 201

@app.route('/get', methods=["GET"])
@login_required
def get_users():
    res = User.query.all()
    user_result = userschemas.dump(res)
    role = Role.query.all()
    role_result = roleschemas.dump(role)
    return {'Message': 'Success', 'Users': user_result, 'Roles': role_result}, 200


@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return 'You have successfully been logged out.'



if __name__ == '__main__':
    with app.app_context():
        # Create the db tables & if it is created it will not create new one
        db.create_all()
    app.run(debug=True)     # Make application up with the debug mode
