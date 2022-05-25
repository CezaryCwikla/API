from api_czujnikow_rzek import db

from datetime import datetime,date
from marshmallow import Schema, fields, validate, validates, ValidationError


class Czujnik(db.Model):
    __tablename__ = 'Logger'
    id = db.Column(db.Integer, primary_key=True)
    PhoneNumberID = db.Column(db.Integer)
    Logger_id = db.Column(db.String(12))
    place = db.Column(db.String(100))
    river = db.Column(db.String(100))
    lat = db.Column(db.Numeric(11,6))
    lng = db.Column(db.Numeric(11,6))
    warning = db.Column(db.Integer)
    alarm = db.Column(db.Integer)
    status_id = db.Column(db.String(25))
    visible = db.Column(db.Integer)
    type = db.Column(db.String(20))
    list_sort_order = db.Column(db.Integer)
    created_user_id = db.Column(db.Integer)
    updated_user_id = db.Column(db.Integer)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)
    data = db.relationship('SampleData', back_populates='logger')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.place}   {self.id}  {self.data}'

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value


class SampleData(db.Model):
    __tablename__ = 'Sample'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    LoggerID = db.Column(db.Integer, db.ForeignKey('Logger.id'), nullable=False)
    logger = db.relationship('Czujnik', back_populates='data')
    Channel = db.Column(db.Integer)
    DateTime = db.Column(db.Date, nullable=False)
    Value = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f'<{self.DateTime} - {self.id}  {self.Value}'

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value


class CzujnikSchema(Schema):
    id = fields.Integer(dump_only=True)
    PhoneNumberID = fields.Integer()
    Logger_id = fields.String()
    place = fields.String()
    river = fields.String()
    lat = fields.Float()
    lng = fields.Float()
    warning = fields.Integer()
    alarm = fields.Integer()
    status_id = fields.String()
    visible = fields.Integer()
    type = fields.String()
    list_sort_order = fields.Integer()
    created_user_id = fields.Integer()
    updated_user_id = fields.Integer()
    created_at = fields.Date()
    updated_at = fields.Date()
    data = fields.List(fields.Nested(lambda: SampleDataSchema()))

class SampleDataSchema(Schema):
    id = fields.Integer(dump_only=True)
    LoggerID = fields.Integer()
    Channel = fields.Integer()
    DateTime = fields.Date()
    Value = fields.Integer()



czujnik_schema = CzujnikSchema()
sample_schema = SampleDataSchema()

