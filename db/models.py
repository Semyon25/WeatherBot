from sqlalchemy import Column, BigInteger, String, Index, func, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

class Location(Base):
    __tablename__ = 'locations'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    
    __table_args__ = (
        Index(
            'uq_user_location_lower',
            'user_id',
            func.lower(name),
            unique=True
        ),
    )

class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        UniqueConstraint("user_id", "time", "mode", name="uq_user_time_mode"),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    time = Column(String, nullable=False)
    mode = Column(String, nullable=False)