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





class Procedimento(Base):
    __tablename__ = "procedimento"

    id_procedimento = Column(Integer, primary_key=True)

    codigo = Column(String)

    nome = Column(String)

    tempo_medio_minutos = Column(Integer)

    nivel_risco = Column(String)

    media_tempo_procedimento = Column(String)




class ProcedimentoRealizado(Base):
    __tablename__ = "procedimento_realizado"

    id_atendimento = Column(
        Integer,
        ForeignKey("atendimento.id_atendimento"),
        primary_key=True
    )

    id_procedimento = Column(
        Integer,
        ForeignKey("procedimento.id_procedimento"),
        primary_key=True
    )

    quantidade = Column(Integer)

    tempo_real_minutos = Column(Integer)

    observacao = Column(String)

    faturado = Column(Boolean)

    hora_inicio = Column(DateTime)

    atendimento = relationship("Atendimento")

    procedimento = relationship("Procedimento")



class Unidade(Base):
    __tablename__ = "unidade"

    id_unidade = Column(Integer, primary_key=True)

    nome = Column(String)

    tipo = Column(String)

    capacidade_leitos = Column(Integer)





class Escala(Base):
    __tablename__ = "escala"

    id_escala = Column(Integer, primary_key=True)

    id_unidade = Column(
        Integer,
        ForeignKey("unidade.id_unidade")
    )

    dia_semana = Column(String)

    turno = Column(String)

    id_residente = Column(
        Integer,
        ForeignKey("residente.id_profissional")
    )

    id_preceptor = Column(
        Integer,
        ForeignKey("preceptor.id_profissional")
    )

    data_plantao = Column(Date)

    unidade = relationship("Unidade")

    residente = relationship("Residente")

    preceptor = relationship("Preceptor")

