import threading
import time
import sys
import os

# (tava com problema nessa parte) garante que o Python reconheça a pasta atual para os imports, independente de onde o terminal for aberto.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal
from backend.models import Atendimento

def escalar_residente(nome_transacao, id_residente, id_atendimento_vaga):
    """
    Simula a tentativa de alocar um residente em uma vaga (atendimento).
    Utiliza Lock Pessimista (FOR UPDATE) para evitar condição de corrida.
    """
    session = SessionLocal()
    try:
        print(f"[{nome_transacao}] Iniciando tentativa de escala para o Residente {id_residente}...")
        
        # lock pessimista: seleciona a vaga e bloqueia a linha no banco (FOR UPDATE)
        vaga = session.query(Atendimento).filter(
            Atendimento.id_atendimento == id_atendimento_vaga
        ).with_for_update().first()

        if not vaga:
            print(f"[{nome_transacao}] ERRO: Vaga de atendimento não encontrada.")
            return

        time.sleep(2)

        # verifica se alguém já pegou a vaga nesse meio tempo
        if vaga.id_residente is not None:
            print(f"[{nome_transacao}] FALHA: A vaga já foi preenchida por outro residente (Residente {vaga.id_residente}). Operação abortada.")
        else:
            # Vaga está livre, realiza a escala
            vaga.id_residente = id_residente
            session.commit()
            print(f"[{nome_transacao}] SUCESSO: Residente {id_residente} escalado com sucesso na vaga!")

    except Exception as e:
        session.rollback()
        print(f"[{nome_transacao}] Erro durante a transação (Rollback executado): {e}")
    finally:
        session.close()

def simular_concorrencia():
    print("-INICIANDO SIMULAÇÃO DE CONCORRÊNCIA (LOCK PESSIMISTA)-\n")
    
    id_vaga_alvo = 1  
    id_residente_a = 101  
    id_residente_b = 102  

    #duas "threads" (simulando dois usuários diferentes ao mesmo tempo)
    thread_1 = threading.Thread(target=escalar_residente, args=("Transação A (Coordenação)", id_residente_a, id_vaga_alvo))
    thread_2 = threading.Thread(target=escalar_residente, args=("Transação B (Secretaria)", id_residente_b, id_vaga_alvo))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()
    
    print("\n-FIM DA SIMULAÇÃO-")

if __name__ == "__main__":
    simular_concorrencia()