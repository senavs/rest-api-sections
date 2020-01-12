from typing import List

from database import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name) -> 'StoreModel':
        # SELECT * FROM __tablename__ WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List['StoreModel']:
        # SELECT * FROM __tablename__
        return cls.query.all()

    def save_to_db(self):
        # INSERT INTO __tablename__ VALUES (NULL, ?, ?)
        # UPDATE __tablename__ SET price=? WHERE name=?
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        # DELETE FROM __tablename__ WHERE name=?
        db.session.delete(self)
        db.session.commit()
