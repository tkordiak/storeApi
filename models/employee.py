from db import db


class EmployeeModel(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    role = db.Column(db.String(80))
    email = db.Column(db.String(80))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')

    def __init__(self, name, role, email, store_id):
        self.name = name
        self.role = role
        self.email = email
        self.store_id = store_id

    def json(self):
        return {'id': self.id, 'name': self.name,
                'role': self.role, 'email': self.email, 'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
