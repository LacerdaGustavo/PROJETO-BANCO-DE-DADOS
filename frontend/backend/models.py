from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
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



class Profissional(Base):
    __tablename__ = "profissional"

    id_pessoa = Column(
        Integer,
        ForeignKey("pessoa.id_pessoa"),
        primary_key=True
    )

    crm = Column(String)

    data_admissao = Column(Date)

    especialidade = Column(String)

    pessoa = relationship("Pessoa")




class Atendimento(Base):
    __tablename__ = "atendimento"

    id_atendimento = Column(Integer, primary_key=True)

    data_hora = Column(DateTime)

    duracao_minutos = Column(Integer)

    id_paciente = Column(
        Integer,
        ForeignKey("paciente.id_pessoa")
    )

    id_residente = Column(
        Integer,
        ForeignKey("residente.id_profissional")
    )

    id_preceptor = Column(
        Integer,
        ForeignKey("preceptor.id_profissional")
    )

    paciente = relationship(
        "Paciente",
        foreign_keys=[id_paciente]
    )

    residente = relationship(
        "Residente",
        foreign_keys=[id_residente]
    )

    preceptor = relationship(
        "Preceptor",
        foreign_keys=[id_preceptor]
    )

class Residente(Base):
    __tablename__ = "residente"

    id_profissional = Column(
        Integer,
        ForeignKey("profissional.id_pessoa"),
        primary_key=True
    )

    ano_residencia = Column(String)

    profissional = relationship("Profissional")





class Preceptor(Base):
    __tablename__ = "preceptor"

    id_profissional = Column(
        Integer,
        ForeignKey("profissional.id_pessoa"),
        primary_key=True
    )

    titulacao = Column(String)

    profissional = relationship("Profissional")