from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Usando directamente la URL de conexión de Railway
DATABASE_URL = "mysql+pymysql://root:TmyoKsSywRvSqIHWOEPSpOJoJLUudwpz@junction.proxy.rlwy.net:27665/railway"

engine = create_engine(DATABASE_URL, echo=True)
meta = MetaData()
conn = engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
