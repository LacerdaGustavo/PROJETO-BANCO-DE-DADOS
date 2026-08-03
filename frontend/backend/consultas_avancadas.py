from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, case
from backend.models import (
    Pessoa, Paciente, Residente, Preceptor, 
    Atendimento, Procedimento, ProcedimentoRealizado
)

def preceptores_pacientes_flamenguistas(session: Session):
    # cria 'apelidos' para a tabela Pessoa, pois usa 2x na mesma consulta
    PessoaPreceptor = aliased(Pessoa)
    PessoaPaciente = aliased(Pessoa)

    resultados = session.query(PessoaPreceptor.nome.label("nome_preceptor")).\
        join(Preceptor, Preceptor.id_profissional == PessoaPreceptor.id_pessoa).\
        join(Atendimento, Atendimento.id_preceptor == Preceptor.id_profissional).\
        join(Paciente, Paciente.id_pessoa == Atendimento.id_paciente).\
        join(PessoaPaciente, PessoaPaciente.id_pessoa == Paciente.id_pessoa).\
        filter(PessoaPaciente.is_flamengo == True).\
        distinct().all()
        
    return resultados

def ultimo_atendimento_pacientes(session: Session):
    #subconsulta para encontrar a data mais recente de cada paciente
    subquery = session.query(
        Atendimento.id_paciente, 
        func.max(Atendimento.data_hora).label("ultima_data")
    ).group_by(Atendimento.id_paciente).subquery()

    #apelidos para a tabela Pessoa
    PessoaPaciente = aliased(Pessoa)
    PessoaResidente = aliased(Pessoa)
    PessoaPreceptor = aliased(Pessoa)

    resultados = session.query(
        PessoaPaciente.nome.label('nome_paciente'),
        Atendimento.data_hora,
        PessoaResidente.nome.label('nome_residente'),
        PessoaPreceptor.nome.label('nome_preceptor'),
        func.string_agg(Procedimento.nome, ', ').label('procedimentos')
    ).\
    join(subquery, (Atendimento.id_paciente == subquery.c.id_paciente) & (Atendimento.data_hora == subquery.c.ultima_data)).\
    join(Paciente, Paciente.id_pessoa == Atendimento.id_paciente).\
    join(PessoaPaciente, PessoaPaciente.id_pessoa == Paciente.id_pessoa).\
    join(Residente, Residente.id_profissional == Atendimento.id_residente).\
    join(PessoaResidente, PessoaResidente.id_pessoa == Residente.id_profissional).\
    join(Preceptor, Preceptor.id_profissional == Atendimento.id_preceptor).\
    join(PessoaPreceptor, PessoaPreceptor.id_pessoa == Preceptor.id_profissional).\
    outerjoin(ProcedimentoRealizado, ProcedimentoRealizado.id_atendimento == Atendimento.id_atendimento).\
    outerjoin(Procedimento, Procedimento.id_procedimento == ProcedimentoRealizado.id_procedimento).\
    group_by(
        PessoaPaciente.nome,
        Atendimento.data_hora,
        PessoaResidente.nome,
        PessoaPreceptor.nome
    ).all()

    return resultados

def percentual_risco_alto_residentes(session: Session):
    PessoaResidente = aliased(Pessoa)

    resultados = session.query(
        PessoaResidente.nome,
        func.count(ProcedimentoRealizado.id_procedimento).label('total_procedimentos'),
        func.sum(case((Procedimento.nivel_risco == 'ALTO', 1), else_=0)).label('total_alto_risco')
    ).\
    join(Residente, Residente.id_profissional == PessoaResidente.id_pessoa).\
    join(Atendimento, Atendimento.id_residente == Residente.id_profissional).\
    join(ProcedimentoRealizado, ProcedimentoRealizado.id_atendimento == Atendimento.id_atendimento).\
    join(Procedimento, Procedimento.id_procedimento == ProcedimentoRealizado.id_procedimento).\
    group_by(PessoaResidente.nome).all()

    retorno = []
    for res in resultados: 
        percentual = (res.total_alto_risco / res.total_procedimentos * 100) if res.total_procedimentos > 0 else 0
        retorno.append({
            "residente": res.nome,
            "total_procedimentos": res.total_procedimentos,
            "total_alto_risco": res.total_alto_risco,
            "percentual": round(percentual,2)
        })

    return retorno

