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


