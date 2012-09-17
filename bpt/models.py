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

class BdJogador(Base):
    __tablename__ = 'jogadores'
    id = Column(Integer, primary_key=True)
    nome = Column(Text, unique=True, nullable=False)
    senha = Column(Text, nullable=False)
    email = Column(Text)

    #id = Column(mysql.BIGINT(20, unsigned=True), primary_key=True, autoincrement=True)

    #def __init__(self, nome, senha):
    #    self.nome = nome
    #    self.senha = senha

