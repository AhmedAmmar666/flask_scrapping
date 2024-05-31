from sqlalchemy import create_engine, Column, Integer, String, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase



engine = create_engine('sqlite:///test.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
  pass

class Book(Base):
  __tablename__ = 'books'

  id = Column(Integer, primary_key=True)
  title = Column(String(100), unique=True)
  price = Column(String(50))
  description = Column(String(500))
  page = Column(Integer)

Base.metadata.create_all(engine)
