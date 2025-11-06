from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from .bulk_data_schema import candidate_fields, spreadsheet_fields, zip_fields
from .api_data_schema import congress_fields, financial_summary_fields, geographic_contribution_fields

db = SQLAlchemy()

data_type_map = {
    'shortString': db.String(15),
    'string': db.String(45),
    'longString': db.String(120),
    'extraLongString': db.String(200),
    'integer': db.Integer,
    'dateTime': db.DateTime
}

@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

def create_model_class(class_name, fields, primary_key, include_update):
    class_attrs = {'__tablename__': class_name.lower()}

    for field in fields:
        key = field['key']
        data_type = data_type_map[field['data_type']]

        if key == primary_key:
            class_attrs[key] = db.Column(data_type, primary_key=True)
        else:
            class_attrs[key] = db.Column(data_type)

        if include_update:
            class_attrs['lastUpdated'] = db.Column(db.DateTime, default=datetime.now())

    return type(class_name, (Base,), class_attrs)

custom_fields = []

politician_fields = candidate_fields + congress_fields + spreadsheet_fields + custom_fields

class Politician(Base):
    __tablename__ = 'politician'

    # Add existing fields dynamically
    for field in politician_fields:
        key = field['key']
        data_type = data_type_map[field['data_type']]
        if key == 'fecId1':
            locals()[key] = db.Column(data_type, primary_key=True)
        else:
            locals()[key] = db.Column(data_type)

    lastUpdated = db.Column(db.DateTime, default=datetime.now())

    # Relationships
    financial_summaries = relationship("FinancialSummary", back_populates="politician")
    geographic_contributions = relationship("GeographicContribution", back_populates="politician")

class FinancialSummary(Base):
    __tablename__ = 'financial_summary'

    id = db.Column(db.Integer, primary_key=True)
    politician_id = db.Column(db.String(15), ForeignKey('politician.fecId1'))
    election_year = db.Column(db.Integer)
    
    # Add financial fields dynamically
    for field in financial_summary_fields:
        key = field['key']
        data_type = data_type_map[field['data_type']]
        locals()[key] = db.Column(data_type)

    lastUpdated = db.Column(db.DateTime, default=datetime.now())
    
    # Relationship
    politician = relationship("Politician", back_populates="financial_summaries")

class GeographicContribution(Base):
    __tablename__ = 'geographic_contribution'

    id = db.Column(db.Integer, primary_key=True)
    politician_id = db.Column(db.String(15), ForeignKey('politician.fecId1'))
    
    # Add geographic fields dynamically
    for field in geographic_contribution_fields:
        key = field['key']
        data_type = data_type_map[field['data_type']]
        locals()[key] = db.Column(data_type)

    lastUpdated = db.Column(db.DateTime, default=datetime.now())
    
    # Relationship
    politician = relationship("Politician", back_populates="geographic_contributions")

class Zip(Base):
    __tablename__ = 'zip'
    
    # Add zip fields dynamically
    for field in zip_fields:
        key = field['key']
        data_type = data_type_map[field['data_type']]
        if key == 'fullZip':
            locals()[key] = db.Column(data_type, primary_key=True)
        else:
            locals()[key] = db.Column(data_type)