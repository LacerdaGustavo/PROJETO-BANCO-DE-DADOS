from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey
)

from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Pessoa(Base):
    __tablename__ = "pessoa"

    id_pessoa = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    telefone = Column(String)
    data_nascimento = Column(Date)
    is_flamengo = Column(Boolean)

    paciente = relationship(
        "Paciente",
        back_populates="pessoa",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Paciente(Base):
    __tablename__ = "paciente"

    id_pessoa = Column(
        Integer,
        ForeignKey("pessoa.id_pessoa"),
        primary_key=True
    )

    num_convenio = Column(String)
    grupo_sanguineo = Column(String)
    alergias = Column(String)
    endereco = Column(String)

    pessoa = relationship(
        "Pessoa",
        back_populates="paciente"
    )