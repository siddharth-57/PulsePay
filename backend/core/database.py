# This Database Connection File Creates:
#     PostgreSQL engine
#     DB session factory
#     SQLAlchemy base class
    
# All DB operations will use this file. 
# This is a central file that manages all communication between your backend application and the PostgreSQL database.
# When building a backend (especially with FastAPI + SQLAlchemy), you should not manually connect to the database everywhere in your code.
# Instead, you create one reusable database configuration file and every other file imports it.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy is a Python library used to work with databases like PostgreSQL, MySQL, SQLite, etc.
# It acts as a bridge between: your Python code and your database, you can write code in python and this library will convert it into SQL behind the scenes

from backend.core.config import settings


engine = create_engine(settings.DATABASE_URL)   # The engine is the actual connection bridge between your app and PostgreSQL.

SessionLocal = sessionmaker(    #A session is like a temporary conversation with the database.
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()   #This is the foundation for all your database tables/models.