import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.consultas_avancadas import (
    preceptores_pacientes_flamenguistas,
    ultimo_atendimento_pacientes,
    percentual_risco_alto_residentes
)

# Conecta diretamente no banco 'hospital' do seu Mac
DATABASE_URL = "postgresql://isabellasousa@localhost:5432/hospital"

def testar_tudo():
    print("Conectando ao banco de dados...")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("\n--- 1. Testando Preceptores de Pacientes Flamenguistas ---")
        res_flamengo = preceptores_pacientes_flamenguistas(session)
        for row in res_flamengo:
            print(f"Preceptor(a): {row.nome_preceptor}")
            
        print("\n--- 2. Testando Último Atendimento de Cada Paciente ---")
        res_ultimos = ultimo_atendimento_pacientes(session)
        for row in res_ultimos:
            print(f"Paciente: {row.nome_paciente} | Data: {row.data_hora} | Residente: {row.nome_residente} | Preceptor: {row.nome_preceptor} | Procedimentos: {row.procedimentos}")
            
        print("\n--- 3. Testando Percentual de Alto Risco por Residente ---")
        res_risco = percentual_risco_alto_residentes(session)
        for row in res_risco:
            print(f"Residente: {row['residente']} | Total: {row['total_procedimentos']} | Alto Risco: {row['alto_risco']} | Percentual: {row['percentual']}%")
            
    except Exception as e:
        print(f"Ocorreu um erro durante o teste: {e}")
    finally:
        session.close()
        print("\nSessão encerrada.")

if __name__ == "__main__":
    testar_tudo()