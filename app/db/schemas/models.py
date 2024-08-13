from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from .bulk_data_schema import candidate_fields, spreadsheet_fields
from .api_data_schema import congress_fields

db = SQLAlchemy()

data_type_map = {
    'shortString': db.String(15),
    'string': db.String(45),
    'longString': db.String(120),
    'integer': db.Integer,
    'dateTime': db.DateTime
}

@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

def create_model_class(class_name, fields, primary_key):
    class_attrs = {'__tablename__': class_name.lower()}

    for field in fields:
        key = field['key']
        data_type = data_type_map[field['data_type']]

        if key == primary_key:
            class_attrs[key] = db.Column(data_type, primary_key=True)
        else:
            class_attrs[key] = db.Column(data_type)

        class_attrs['lastUpdated'] = db.Column(db.DateTime, default=datetime.now())

    return type(class_name, (Base,), class_attrs)

custom_fields =[]

politician_fields = candidate_fields + congress_fields + spreadsheet_fields + custom_fields

Politician = create_model_class(
    'Politician',
    politician_fields,
    'candidateId1'
)
