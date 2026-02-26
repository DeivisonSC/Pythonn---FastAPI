from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Conexão com o MySQL do Laragon usando pymysql
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/api_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()