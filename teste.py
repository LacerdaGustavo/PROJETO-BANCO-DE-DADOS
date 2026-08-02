from frontend.backend.crud import listar_atendimentos

for atendimento in listar_atendimentos():
    print(atendimento)