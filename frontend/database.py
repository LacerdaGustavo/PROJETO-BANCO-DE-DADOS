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


def listar_procedimentos_atendimento(id_atendimento):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT

            p.nome,
            pr.quantidade,
            pr.tempo_real_minutos

        FROM procedimento_realizado pr

        JOIN procedimento p
            ON pr.id_procedimento = p.id_procedimento

        WHERE pr.id_atendimento = %s

        ORDER BY p.nome
    """, (id_atendimento,))

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados


def listar_atendimentos_combo():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            a.id_atendimento,
            p.nome
        FROM atendimento a
        JOIN pessoa p
            ON a.id_paciente = p.id_pessoa
        ORDER BY a.id_atendimento;
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados



def excluir_procedimento_realizado(
    id_atendimento,
    id_procedimento
):

    conexao = conectar()

    cursor = conexao.cursor()

    # Verifica se já foi faturado
    cursor.execute("""
        SELECT faturado
        FROM procedimento_realizado
        WHERE
            id_atendimento = %s
        AND
            id_procedimento = %s
    """, (
        id_atendimento,
        id_procedimento
    ))

    resultado = cursor.fetchone()

    if resultado is None:

        cursor.close()
        conexao.close()
        return False

    faturado = resultado[0]

    if faturado:

        cursor.close()
        conexao.close()
        return False

    cursor.execute("""
        DELETE
        FROM procedimento_realizado
        WHERE
            id_atendimento=%s
        AND
            id_procedimento=%s
    """, (
        id_atendimento,
        id_procedimento
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    return True



def buscar_id_procedimento(nome):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_procedimento
        FROM procedimento
        WHERE nome = %s
    """, (nome,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado:
        return resultado[0]

    return None


def calcular_tempo_medio_residente():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            pe.nome,
            ROUND(AVG(a.duracao_minutos), 2) AS tempo_medio
        FROM atendimento a
        JOIN profissional pr
            ON a.id_residente = pr.id_pessoa
        JOIN pessoa pe
            ON pr.id_pessoa = pe.id_pessoa
        GROUP BY pe.nome
        ORDER BY pe.nome;
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados



def ranking_residentes():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT

            pe.nome,
            COUNT(*) AS total_atendimentos

        FROM atendimento a

        JOIN profissional pr
            ON a.id_residente = pr.id_pessoa

        JOIN pessoa pe
            ON pr.id_pessoa = pe.id_pessoa

        GROUP BY pe.nome

        ORDER BY total_atendimentos DESC;
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados




def preceptores_mes(mes, ano):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT

            pe.nome,
            COUNT(*) AS total

        FROM atendimento a

        JOIN profissional pr
            ON a.id_preceptor = pr.id_pessoa

        JOIN pessoa pe
            ON pr.id_pessoa = pe.id_pessoa

        WHERE
            EXTRACT(MONTH FROM a.data_hora) = %s
        AND
            EXTRACT(YEAR FROM a.data_hora) = %s

        GROUP BY pe.nome

        HAVING COUNT(*) > 5

        ORDER BY total DESC;
    """,(mes,ano))

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados




def plantoes_residente():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT

            u.nome,
            pe.nome,
            COUNT(*) AS quantidade

        FROM escala e

        JOIN unidade u
            ON e.id_unidade = u.id_unidade

        JOIN profissional pr
            ON e.id_residente = pr.id_pessoa

        JOIN pessoa pe
            ON pr.id_pessoa = pe.id_pessoa

        WHERE

            EXTRACT(MONTH FROM e.data_plantao)=EXTRACT(MONTH FROM CURRENT_DATE)

        AND

            EXTRACT(YEAR FROM e.data_plantao)=EXTRACT(YEAR FROM CURRENT_DATE)

        GROUP BY

            u.nome,
            pe.nome

        ORDER BY

            u.nome,
            pe.nome;
    """)

    dados=cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados






def pacientes_sem_risco_alto():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT

            pe.nome

        FROM paciente pa

        JOIN pessoa pe
            ON pa.id_pessoa = pe.id_pessoa

        WHERE pa.id_pessoa NOT IN(

            SELECT DISTINCT
                a.id_paciente

            FROM atendimento a

            JOIN procedimento_realizado pr
                ON a.id_atendimento = pr.id_atendimento

            JOIN procedimento p
                ON pr.id_procedimento = p.id_procedimento

            WHERE p.nivel_risco='ALTO'

        )

        ORDER BY pe.nome;
    """)

    dados=cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados


