from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:miftah@localhost:5432/TodosAppDatabase'
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:andesca21@localhost:3306/TodosAppDatabase'

# SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./todosapp.db'
# engine = create_async_engine('sqlite+aiosqlite:///./todosapp.db', echo=True)
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
