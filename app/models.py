# app/models.py
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy import Index, text, event, DDL
from app.extensions import db  # assumes db is initialized in __init__.py
from sqlalchemy.ext.compiler import compiles

class Diagnosis(db.Model):
    __tablename__ = 'snomed'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    effectiveTime = db.Column(db.String(8), nullable=False)         # e.g. '20020131'
    active = db.Column(db.Boolean, nullable=False)                  # True or False
    moduleId = db.Column(db.BigInteger, nullable=False)
    conceptId = db.Column(db.BigInteger, nullable=False)
    languageCode = db.Column(db.String(5), nullable=False)
    typeId = db.Column(db.BigInteger, nullable=False)
    term = db.Column(db.String, nullable=False)
    caseSignificanceId = db.Column(db.BigInteger, nullable=False)
    search_vector = db.Column(TSVECTOR)

    __table_args__ = (
        Index('ix_search_vector', 'search_vector', postgresql_using='gin'),
    )

    def __repr__(self):
        return f"<Diagnosis {self.term}>"
    
# Attach raw SQL to create trigram and fuzzy extensions
@event.listens_for(Diagnosis.__table__, 'after_create')
def create_extensions(target, connection, **kw):
    connection.execute(DDL("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
    connection.execute(DDL("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch"))

# Trigram index via raw DDL
@event.listens_for(Diagnosis.__table__, 'after_create')
def create_trigram_index(target, connection, **kw):
    connection.execute(DDL(
        "CREATE INDEX IF NOT EXISTS ix_snomed_trgm ON snomed USING GIN (term gin_trgm_ops)"
    ))
