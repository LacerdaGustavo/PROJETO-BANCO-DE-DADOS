from sqlalchemy import select

from backend.database import SessionLocal
from backend.models import Pessoa, Paciente
from datetime import datetime
from sqlalchemy.exc import IntegrityError


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