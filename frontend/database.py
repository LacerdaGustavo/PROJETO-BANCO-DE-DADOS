import psycopg2
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

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            pe.id_pessoa,
            pe.nome,
            pe.cpf,
            pe.telefone,
            pe.data_nascimento,
            pe.is_flamengo,
            pa.num_convenio,
            pa.grupo_sanguineo,
            pa.alergias,
            pa.endereco
        FROM paciente pa
        JOIN pessoa pe
            ON pa.id_pessoa = pe.id_pessoa
        ORDER BY pe.nome;
    """)

    pacientes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return pacientes



def cadastrar_paciente(nome,cpf,telefone,data_nascimento,is_flamengo,convenio,grupo_sanguineo,alergias,endereco
):
    print("Entrou em cadastrar_paciente")
    conexao = conectar()

    cursor = conexao.cursor()

    data_nascimento = datetime.strptime(
        data_nascimento,
        "%d/%m/%Y"
    ).date()

    # Insere na tabela pessoa
    cursor.execute("""
        INSERT INTO pessoa
        (nome, cpf, data_nascimento, is_flamengo, telefone)

        VALUES (%s, %s, %s , %s , %s)

        RETURNING id_pessoa
    """, (nome, cpf, data_nascimento, is_flamengo, telefone))

    id_pessoa = cursor.fetchone()[0]
    print("ID:", id_pessoa)

    # Insere na tabela paciente
    cursor.execute("""
        INSERT INTO paciente
        (id_pessoa, num_convenio, alergias, grupo_sanguineo,endereco)

        VALUES (%s, %s, %s, %s, %s)
    """, (id_pessoa, convenio, alergias, grupo_sanguineo,endereco))

    conexao.commit()
    print("Paciente cadastrado com sucesso!")
    cursor.close()
    conexao.close()



def buscar_paciente(id_pessoa):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            pe.id_pessoa,
            pe.nome,
            pe.cpf,
            pe.telefone,
            pe.data_nascimento,
            pe.is_flamengo,
            pa.num_convenio,
            pa.grupo_sanguineo,
            pa.alergias,
            pa.endereco
        FROM pessoa pe
        JOIN paciente pa
            ON pe.id_pessoa = pa.id_pessoa
        WHERE pe.id_pessoa = %s
    """, (id_pessoa,))

    paciente = cursor.fetchone()

    cursor.close()
    conexao.close()

    return paciente



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

    conexao = conectar()

    cursor = conexao.cursor()

    # Primeiro remove da tabela paciente
    cursor.execute("""
        DELETE FROM paciente
        WHERE id_pessoa = %s
    """, (id_pessoa,))

    # Depois remove da tabela pessoa
    cursor.execute("""
        DELETE FROM pessoa
        WHERE id_pessoa = %s
    """, (id_pessoa,))

    conexao.commit()

    cursor.close()
    conexao.close()  


 
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


def listar_residentes_combo():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            r.id_profissional,
            pe.nome
        FROM residente r
        JOIN profissional pr
            ON r.id_profissional = pr.id_pessoa
        JOIN pessoa pe
            ON pr.id_pessoa = pe.id_pessoa
        ORDER BY pe.nome
    """)

    residentes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return residentes


def listar_preceptores_combo():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            p.id_profissional,
            pe.nome
        FROM preceptor p
        JOIN profissional pr
            ON p.id_profissional = pr.id_pessoa
        JOIN pessoa pe
            ON pr.id_pessoa = pe.id_pessoa
        ORDER BY pe.nome
    """)

    preceptores = cursor.fetchall()

    cursor.close()
    conexao.close()

    return preceptores



def listar_atendimentos():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT

            a.id_atendimento,

            pac.nome,

            res.nome,

            pre.nome,

            a.data_hora,

            a.duracao_minutos

        FROM atendimento a

        JOIN pessoa pac
            ON a.id_paciente = pac.id_pessoa

        JOIN profissional pr_res
            ON a.id_residente = pr_res.id_pessoa

        JOIN pessoa res
            ON pr_res.id_pessoa = res.id_pessoa

        JOIN profissional pr_pre
            ON a.id_preceptor = pr_pre.id_pessoa

        JOIN pessoa pre
            ON pr_pre.id_pessoa = pre.id_pessoa

        ORDER BY a.data_hora DESC
    """)

    atendimentos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return atendimentos


def cadastrar_atendimento(
    id_paciente,
    id_residente,
    id_preceptor,
    data_hora,
    duracao
):

    conexao = conectar()

    cursor = conexao.cursor()

    data_hora = datetime.strptime(
        data_hora.strip(),
        "%d/%m/%Y %H:%M"
    )

    cursor.execute("""
        INSERT INTO atendimento
        (
            data_hora,
            duracao_minutos,
            id_paciente,
            id_residente,
            id_preceptor
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """, (
        data_hora,
        duracao,
        id_paciente,
        id_residente,
        id_preceptor
    ))

    conexao.commit()

    cursor.close()

    conexao.close()



def listar_atendimentos_paciente(id_paciente):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            a.id_atendimento,
            pac.nome,
            res.nome,
            pre.nome,
            a.data_hora,
            a.duracao_minutos

        FROM atendimento a

        JOIN pessoa pac
            ON a.id_paciente = pac.id_pessoa

        JOIN profissional pr_res
            ON a.id_residente = pr_res.id_pessoa

        JOIN pessoa res
            ON pr_res.id_pessoa = res.id_pessoa

        JOIN profissional pr_pre
            ON a.id_preceptor = pr_pre.id_pessoa

        JOIN pessoa pre
            ON pr_pre.id_pessoa = pre.id_pessoa

        WHERE a.id_paciente = %s

        ORDER BY a.data_hora;
    """, (id_paciente,))

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados


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


