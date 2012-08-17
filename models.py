from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Jogador(Base):
    __tablename__ = 'jogadores'
    id = Column(Integer, primary_key=True)
    nome = Column(Text, unique=True)

    def __init__(self, nome):
        self.nome = nome

