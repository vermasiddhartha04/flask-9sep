from app import db
import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    roles = db.relationship('Role', secondary='role_mapping', back_populates='users')

    def __init__(self, name, email, password, roles):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.roles = roles

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', secondary='role_mapping', back_populates='roles')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class RoleMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('role_mappings', cascade='all, delete-orphan'))
    role = db.relationship('Role', backref=db.backref('role_mappings', cascade='all, delete-orphan'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

def initialize_roles():
    roles = ['admin', 'user', 'guest']
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            new_role = Role(name=role_name)
            db.session.add(new_role)
    db.session.commit()
