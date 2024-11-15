from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://waldo:133843@localhost:3306/trabajofinalFBD"

engine = create_engine(DATABASE_URL, echo=True)
meta = MetaData()
conn = engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
