import psycopg2
from backend import crud as orm

from datetime import datetime


def conectar():

    conexao = psycopg2.connect(
        host="localhost",
        database="hospital",
        user="postgres",
        password="Senha123"
    )

    return conexao


def listar_pacientes():
    return orm.listar_pacientes()



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
    return orm.cadastrar_paciente(
        nome,
        cpf,
        telefone,
        data_nascimento,
        is_flamengo,
        convenio,
        grupo_sanguineo,
        alergias,
        endereco
    )



def buscar_paciente(id_pessoa):
    return orm.buscar_paciente(id_pessoa)


##ATUALIZA PACIENTE##

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

    conexao = conectar()

    cursor = conexao.cursor()

    # Converte a data para o formato aceito pelo PostgreSQL
    data_nascimento = datetime.strptime(
        data_nascimento.strip(),
        "%d/%m/%Y"
    ).date()

    # Atualiza a tabela PESSOA
    cursor.execute("""
        UPDATE pessoa
        SET
            nome = %s,
            cpf = %s,
            telefone = %s,
            data_nascimento = %s,
            is_flamengo = %s
        WHERE id_pessoa = %s
    """, (
        nome,
        cpf,
        telefone,
        data_nascimento,
        is_flamengo,
        id_pessoa
    ))

    # Atualiza a tabela PACIENTE
    cursor.execute("""
        UPDATE paciente
        SET
            num_convenio = %s,
            grupo_sanguineo = %s,
            alergias = %s,
            endereco = %s
        WHERE id_pessoa = %s
    """, (
        convenio,
        grupo_sanguineo,
        alergias,
        endereco,
        id_pessoa
    ))

    conexao.commit()

    print("Paciente atualizado com sucesso!")

    cursor.close()
    conexao.close()



def excluir_paciente(id_pessoa):
    return orm.excluir_paciente(id_pessoa)

 
def listar_pacientes_combo():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            pe.id_pessoa,
            pe.nome
        FROM pessoa pe
        JOIN paciente pa
            ON pe.id_pessoa = pa.id_pessoa
        ORDER BY pe.nome
    """)

    pacientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return pacientes 


def listar_pacientes_combo():
    return orm.listar_pacientes_combo()


def listar_residentes_combo():
    return orm.listar_residentes_combo()


def listar_preceptores_combo():
    return orm.listar_preceptores_combo()

def listar_atendimentos():
    return orm.listar_atendimentos()

    


def cadastrar_atendimento(
    id_paciente,
    id_residente,
    id_preceptor,
    data_hora,
    duracao
):

    return orm.cadastrar_atendimento(
        id_paciente,
        id_residente,
        id_preceptor,
        data_hora,
        duracao
    )



def listar_atendimentos_paciente(id_paciente):

    return orm.listar_atendimentos_paciente(id_paciente)


def listar_atendimentos_combo():
    return orm.listar_atendimentos_combo()

def listar_procedimentos_atendimento(id_atendimento):
    return orm.listar_procedimentos_atendimento(id_atendimento)

def buscar_id_procedimento(nome):
    return orm.buscar_id_procedimento(nome)

def excluir_procedimento_realizado(id_atendimento, id_procedimento):
    return orm.excluir_procedimento_realizado(
        id_atendimento,
        id_procedimento
    )



def calcular_tempo_medio_residente():
    return orm.calcular_tempo_medio_residente()

def ranking_residentes():
    return orm.ranking_residentes()

def preceptores_mes(mes, ano):
    return orm.preceptores_mes(mes, ano)

def plantoes_residente():
    return orm.plantoes_residente()

def pacientes_sem_risco_alto():
    return orm.pacientes_sem_risco_alto()
