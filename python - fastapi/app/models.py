from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Perfil(Base):
    __tablename__ = "perfis"

    id = Column(Integer, primary_key=True, index=True)
    perfil_nome = Column(String(255), nullable=False) # Adicionado o tamanho 255
    
    usuario = relationship("Usuario", back_populates="perfil", uselist=False)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)        # Adicionado o tamanho 255
    email = Column(String(255), unique=True, index=True, nullable=False) # Tamanho 255
    senha = Column(String(255), nullable=False)       # Adicionado o tamanho 255
    
    id_perfil = Column(Integer, ForeignKey("perfis.id"), unique=True)
    perfil = relationship("Perfil", back_populates="usuario")