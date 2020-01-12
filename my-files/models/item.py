from typing import List

from database import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name) -> 'ItemModel':
        # SELECT * FROM __tablename__ WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List['ItemModel']:
        # SELECT * FROM __tablename__
        return cls.query.all()

    def save_to_db(self):
        # INSERT INTO __tablename__ VALUES (NULL, ?, ?)
        # UPDATE __tablename__ SET price=? WHERE name=?
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        # DELETE FROM items WHERE name=?
        db.session.delete(self)
        db.session.commit()
