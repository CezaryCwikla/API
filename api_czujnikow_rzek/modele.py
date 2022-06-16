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


class DanePowietrza(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'meteo_data'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    measurement_time = db.Column(db.Date)
    wind_speed = db.Column(db.Float(precision=2))
    wind_direct = db.Column(db.Float(precision=2))
    temperature = db.Column(db.Float(precision=2))
    pressure = db.Column(db.Float(precision=2))
    humidity = db.Column(db.Float(precision=2))
    rain = db.Column(db.Integer)
    location_id = db.Column(db.Integer)


    def __repr__(self):
        return f'<{self.__class__.__name__}>:   {self.id} '

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value

class DanePMPowietrza(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'fardata_pm_raw_data'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    measurement_time = db.Column(db.Date)
    pm1 = db.Column(db.Float(precision=2))
    pm25 = db.Column(db.Float(precision=2))
    pm10 = db.Column(db.Float(precision=2))


    def __repr__(self):
        return f'<{self.__class__.__name__}>:   {self.id} '

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value


class DaneHalasu(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'fardata_noise_level'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    measurement_time = db.Column(db.Date)
    leq = db.Column(db.Float(precision=2))


    def __repr__(self):
        return f'<{self.__class__.__name__}>:   {self.id} '

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value


class DaneZanieczyszczeniaPowietrza(db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'fardata_atmo_data'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    measurement_time = db.Column(db.Date)
    NO2 = db.Column(db.Float(precision=2))
    NO = db.Column(db.Float(precision=2))
    CO = db.Column(db.Float(precision=2))
    CO2_NDIR = db.Column(db.Float(precision=2))

    def __repr__(self):
        return f'<{self.__class__.__name__}>:   {self.id} '

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value



class StacjePowietrza(db.Model):
    __bind_key__ = 'three'
    __tablename__ = 'STACJE_METEO'
    ID = db.Column(db.Integer, primary_key=True)
    ADRES = db.Column(db.String(20))
    ID_ADRES = db.Column(db.String(20))
    DL_G = db.Column(db.String(20))
    SZ_G = db.Column(db.String(20))


    def __repr__(self):
        return f'<{self.__class__.__name__}>:   {self.ID} '

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value



class DanePowietrzaSchema(Schema):
    id = fields.Integer(dump_only=True)
    device_id = fields.Integer()
    measurement_time = fields.DateTime()
    wind_speed = fields.Float()
    wind_direct = fields.Float()
    temperature = fields.Float()
    pressure = fields.Float()
    humidity = fields.Float()
    rain = fields.Integer()



class DanePMPowietrzaSchema(Schema):
    id = fields.Integer(dump_only=True)
    device_id = fields.Integer()
    measurement_time = fields.DateTime()
    pm1 = fields.Float()
    pm25 = fields.Float()
    pm10 = fields.Float()

class DaneHalasuSchema(Schema):
    id = fields.Integer(dump_only=True)
    device_id = fields.Integer()
    measurement_time = fields.DateTime()
    leq = fields.Float()


class DaneZanieczyszczeniaPowietrzaSchema(Schema):
    id = fields.Integer(dump_only=True)
    device_id = fields.Integer()
    measurement_time = fields.DateTime()
    NO2 = fields.Float()
    NO = fields.Float()
    CO = fields.Float()
    CO2_NDIR = fields.Float()



class StacjePowietrzaSchema(Schema):
    ID = fields.Integer(dump_only=True)
    ADRES = fields.String()
    DL_G = fields.String()
    SZ_G = fields.String()


class CzujnikSchema(Schema):
    id = fields.Integer(dump_only=True)
    place = fields.String()
    river = fields.String()
    lat = fields.Float()
    lng = fields.Float()
    warning = fields.Integer()
    alarm = fields.Integer()
    status_id = fields.String()
    type = fields.String()
    #data = fields.List(fields.Nested(lambda: SampleDataSchema()))

class SampleDataSchema(Schema):
    DateTime = fields.DateTime()
    LoggerID = fields.Integer()
    Value = fields.Integer()



czujnik_schema = CzujnikSchema()
sample_schema = SampleDataSchema()
danepowietrza_schema = DanePowietrzaSchema()
stacjepowietrza_schema = StacjePowietrzaSchema()
danepmpowietrza_schema = DanePMPowietrzaSchema()
danehalasu_schema = DaneHalasuSchema()
danezanieczyszczenia_schemna = DaneZanieczyszczeniaPowietrzaSchema()