from sqlalchemy import select, func
from sqlalchemy import extract

from backend.database import SessionLocal

from datetime import datetime
from sqlalchemy.exc import IntegrityError


from sqlalchemy.orm import aliased

from backend.models import (
    Pessoa,
    Paciente,
    Profissional,
    Residente,
    Preceptor,
    Atendimento,
    Procedimento,
    ProcedimentoRealizado,
    Unidade,
    Escala
)


def listar_pacientes():

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(
                Pessoa.id_pessoa,
                Pessoa.nome,
                Pessoa.cpf,
                Pessoa.telefone,
                Pessoa.data_nascimento,
                Pessoa.is_flamengo,
                Paciente.num_convenio,
                Paciente.grupo_sanguineo,
                Paciente.alergias,
                Paciente.endereco

            ).join(
                Paciente,
                Pessoa.id_pessoa == Paciente.id_pessoa

            ).order_by(
                Pessoa.nome
            )

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()



def buscar_paciente(id_pessoa):

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(
                Pessoa.id_pessoa,
                Pessoa.nome,
                Pessoa.cpf,
                Pessoa.telefone,
                Pessoa.data_nascimento,
                Pessoa.is_flamengo,
                Paciente.num_convenio,
                Paciente.grupo_sanguineo,
                Paciente.alergias,
                Paciente.endereco

            ).join(

                Paciente,
                Pessoa.id_pessoa == Paciente.id_pessoa

            ).where(

                Pessoa.id_pessoa == id_pessoa

            )

        )

        return resultado.first()

    finally:

        session.close()



def cadastrar_paciente(
    nome,
    cpf,
    telefone,
    data_nascimento,
    is_flamengo,
    convenio,
    grupo_sanguineo,
    alergias,
    endereco
):

    session = SessionLocal()

    try:

        data_nascimento = datetime.strptime(
            data_nascimento,
            "%d/%m/%Y"
        ).date()

        pessoa = Pessoa(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            data_nascimento=data_nascimento,
            is_flamengo=is_flamengo
        )

        paciente = Paciente(
            num_convenio=convenio,
            grupo_sanguineo=grupo_sanguineo,
            alergias=alergias,
            endereco=endereco
        )

        pessoa.paciente = paciente

        session.add(pessoa)

        session.commit()

        print("Paciente cadastrado com sucesso!")

    except Exception:

        session.rollback()
        raise

    finally:
        session.close()





def atualizar_paciente(
    id_pessoa,
    nome,
    cpf,
    telefone,
    data_nascimento,
    is_flamengo,
    convenio,
    grupo_sanguineo,
    alergias,
    endereco
):

    session = SessionLocal()

    try:

        pessoa = session.get(Pessoa, id_pessoa)

        if pessoa is None:
            return

        data_nascimento = datetime.strptime(
            data_nascimento.strip(),
            "%d/%m/%Y"
        ).date()

        pessoa.nome = nome
        pessoa.cpf = cpf
        pessoa.telefone = telefone
        pessoa.data_nascimento = data_nascimento
        pessoa.is_flamengo = is_flamengo

        pessoa.paciente.num_convenio = convenio
        pessoa.paciente.grupo_sanguineo = grupo_sanguineo
        pessoa.paciente.alergias = alergias
        pessoa.paciente.endereco = endereco

        session.commit()

        print("Paciente atualizado com sucesso!")

    except Exception:

        session.rollback()
        raise

    finally:

        session.close()




def excluir_paciente(id_pessoa):

    session = SessionLocal()

    try:

        pessoa = session.get(Pessoa, id_pessoa)

        if pessoa is not None:

            session.delete(pessoa)

            session.commit()

        return True

    except IntegrityError:
        session.rollback()
        print("Não é possível excluir o paciente porque existem atendimentos vinculados.")
        return False

    except Exception:
        session.rollback()
        raise

    finally:

        session.close()




def listar_atendimentos():

    session = SessionLocal()

    try:

        paciente_pessoa = aliased(Pessoa)
        residente_pessoa = aliased(Pessoa)
        preceptor_pessoa = aliased(Pessoa)

        residente_prof = aliased(Profissional)
        preceptor_prof = aliased(Profissional)

        resultado = session.execute(

            select(

                Atendimento.id_atendimento,

                paciente_pessoa.nome,

                residente_pessoa.nome,

                preceptor_pessoa.nome,

                Atendimento.data_hora,

                Atendimento.duracao_minutos

            )

            .join(
                Paciente,
                Atendimento.id_paciente == Paciente.id_pessoa
            )

            .join(
                paciente_pessoa,
                Paciente.id_pessoa == paciente_pessoa.id_pessoa
            )

            .join(
                Residente,
                Atendimento.id_residente == Residente.id_profissional
            )

            .join(
                residente_prof,
                Residente.id_profissional == residente_prof.id_pessoa
            )

            .join(
                residente_pessoa,
                residente_prof.id_pessoa == residente_pessoa.id_pessoa
            )

            .join(
                Preceptor,
                Atendimento.id_preceptor == Preceptor.id_profissional
            )

            .join(
                preceptor_prof,
                Preceptor.id_profissional == preceptor_prof.id_pessoa
            )

            .join(
                preceptor_pessoa,
                preceptor_prof.id_pessoa == preceptor_pessoa.id_pessoa
            )

            .order_by(
                Atendimento.data_hora.desc()
            )

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()




def listar_pacientes_combo():

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(
                Pessoa.id_pessoa,
                Pessoa.nome
            )

            .join(
                Paciente,
                Pessoa.id_pessoa == Paciente.id_pessoa
            )

            .order_by(Pessoa.nome)

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()






def listar_residentes_combo():

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(
                Residente.id_profissional,
                Pessoa.nome
            )

            .join(
                Profissional,
                Residente.id_profissional == Profissional.id_pessoa
            )

            .join(
                Pessoa,
                Profissional.id_pessoa == Pessoa.id_pessoa
            )

            .order_by(Pessoa.nome)

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()






def listar_preceptores_combo():

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(
                Preceptor.id_profissional,
                Pessoa.nome
            )

            .join(
                Profissional,
                Preceptor.id_profissional == Profissional.id_pessoa
            )

            .join(
                Pessoa,
                Profissional.id_pessoa == Pessoa.id_pessoa
            )

            .order_by(Pessoa.nome)

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()




def cadastrar_atendimento(
    id_paciente,
    id_residente,
    id_preceptor,
    data_hora,
    duracao
):

    session = SessionLocal()

    try:

        data_hora = datetime.strptime(
            data_hora.strip(),
            "%d/%m/%Y %H:%M"
        )

        atendimento = Atendimento(

            data_hora=data_hora,

            duracao_minutos=duracao,

            id_paciente=id_paciente,

            id_residente=id_residente,

            id_preceptor=id_preceptor

        )

        session.add(atendimento)

        session.commit()

    except Exception:

        session.rollback()

        raise

    finally:

        session.close()




def listar_atendimentos_paciente(id_paciente):

    session = SessionLocal()

    try:

        paciente_pessoa = aliased(Pessoa)
        residente_pessoa = aliased(Pessoa)
        preceptor_pessoa = aliased(Pessoa)

        residente_prof = aliased(Profissional)
        preceptor_prof = aliased(Profissional)

        resultado = session.execute(

            select(

                Atendimento.id_atendimento,

                paciente_pessoa.nome,

                residente_pessoa.nome,

                preceptor_pessoa.nome,

                Atendimento.data_hora,

                Atendimento.duracao_minutos

            )

            .join(
                Paciente,
                Atendimento.id_paciente == Paciente.id_pessoa
            )

            .join(
                paciente_pessoa,
                Paciente.id_pessoa == paciente_pessoa.id_pessoa
            )

            .join(
                Residente,
                Atendimento.id_residente == Residente.id_profissional
            )

            .join(
                residente_prof,
                Residente.id_profissional == residente_prof.id_pessoa
            )

            .join(
                residente_pessoa,
                residente_prof.id_pessoa == residente_pessoa.id_pessoa
            )

            .join(
                Preceptor,
                Atendimento.id_preceptor == Preceptor.id_profissional
            )

            .join(
                preceptor_prof,
                Preceptor.id_profissional == preceptor_prof.id_pessoa
            )

            .join(
                preceptor_pessoa,
                preceptor_prof.id_pessoa == preceptor_pessoa.id_pessoa
            )

            .where(
                Atendimento.id_paciente == id_paciente
            )

            .order_by(
                Atendimento.data_hora
            )

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()





def listar_atendimentos_combo():

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(
                Atendimento.id_atendimento,
                Pessoa.nome
            )

            .join(
                Paciente,
                Atendimento.id_paciente == Paciente.id_pessoa
            )

            .join(
                Pessoa,
                Paciente.id_pessoa == Pessoa.id_pessoa
            )

            .order_by(
                Atendimento.id_atendimento
            )

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()



def listar_procedimentos_atendimento(id_atendimento):

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(

                Procedimento.nome,

                ProcedimentoRealizado.quantidade,

                ProcedimentoRealizado.tempo_real_minutos

            )

            .join(
                Procedimento,
                ProcedimentoRealizado.id_procedimento ==
                Procedimento.id_procedimento
            )

            .where(
                ProcedimentoRealizado.id_atendimento == id_atendimento
            )

            .order_by(
                Procedimento.nome
            )

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()







def buscar_id_procedimento(nome):

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(Procedimento.id_procedimento)

            .where(
                Procedimento.nome == nome
            )

        ).scalar_one_or_none()

        return resultado

    finally:

        session.close()






def excluir_procedimento_realizado(
    id_atendimento,
    id_procedimento
):

    session = SessionLocal()

    try:

        procedimento = session.get(

            ProcedimentoRealizado,

            (id_atendimento, id_procedimento)

        )

        if procedimento is None:
            return False

        if procedimento.faturado:
            return False

        session.delete(procedimento)

        session.commit()

        return True

    except Exception:

        session.rollback()

        raise

    finally:

        session.close()





def calcular_tempo_medio_residente():

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(

                Pessoa.nome,

                func.round(
                    func.avg(Atendimento.duracao_minutos),
                    2
                )

            )

            .join(
                Profissional,
                Atendimento.id_residente == Profissional.id_pessoa
            )

            .join(
                Pessoa,
                Profissional.id_pessoa == Pessoa.id_pessoa
            )

            .group_by(Pessoa.nome)

            .order_by(Pessoa.nome)

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()





def ranking_residentes():

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(

                Pessoa.nome,

                func.count()

            )

            .select_from(Atendimento)

            .join(
                Profissional,
                Atendimento.id_residente == Profissional.id_pessoa
            )

            .join(
                Pessoa,
                Profissional.id_pessoa == Pessoa.id_pessoa
            )

            .group_by(Pessoa.nome)

            .order_by(
                func.count().desc()
            )

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()




def preceptores_mes(mes, ano):

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(

                Pessoa.nome,

                func.count()

            )

            .select_from(Atendimento)

            .join(
                Profissional,
                Atendimento.id_preceptor == Profissional.id_pessoa
            )

            .join(
                Pessoa,
                Profissional.id_pessoa == Pessoa.id_pessoa
            )

            .where(
                extract("month", Atendimento.data_hora) == mes,
                extract("year", Atendimento.data_hora) == ano
            )

            .group_by(Pessoa.nome)

            .having(
                func.count() > 5
            )

            .order_by(
                func.count().desc()
            )

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()



def pacientes_sem_risco_alto():

    session = SessionLocal()

    try:

        subconsulta = (

            select(Atendimento.id_paciente)

            .join(
                ProcedimentoRealizado,
                Atendimento.id_atendimento ==
                ProcedimentoRealizado.id_atendimento
            )

            .join(
                Procedimento,
                ProcedimentoRealizado.id_procedimento ==
                Procedimento.id_procedimento
            )

            .where(
                Procedimento.nivel_risco == "ALTO"
            )

            .distinct()

        )

        resultado = session.execute(

            select(Pessoa.nome)

            .join(
                Paciente,
                Pessoa.id_pessoa == Paciente.id_pessoa
            )

            .where(
                ~Paciente.id_pessoa.in_(subconsulta)
            )

            .order_by(Pessoa.nome)

        )

        return [tuple(linha) for linha in resultado]

    finally:

        session.close()


def plantoes_residente():

    session = SessionLocal()

    try:

        resultado = session.execute(

            select(
                Unidade.nome,
                Pessoa.nome,
                func.count()
            )

            .select_from(Escala)

            .join(
                Unidade,
                Escala.id_unidade == Unidade.id_unidade
            )

            .join(
                Profissional,
                Escala.id_residente == Profissional.id_pessoa
            )

            .join(
                Pessoa,
                Profissional.id_pessoa == Pessoa.id_pessoa
            )

            .group_by(
                Unidade.nome,
                Pessoa.nome
            )

            .order_by(
                Unidade.nome,
                Pessoa.nome
            )

        )

        return [tuple(linha) for linha in resultado]

    finally:
        session.close()