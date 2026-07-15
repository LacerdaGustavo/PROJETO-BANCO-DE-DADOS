import customtkinter as ctk
from tkinter import ttk

from database import (
    listar_atendimentos,
    listar_pacientes_combo,
    listar_residentes_combo,
    listar_preceptores_combo,
    cadastrar_atendimento,
    listar_atendimentos_paciente
)

def criar_tela(parent):

    
    # Atualiza a tabela
    

    def carregar_atendimentos():

        # Limpa a tabela
        for item in tabela.get_children():
            tabela.delete(item)

        # Busca os dados no banco
        atendimentos = listar_atendimentos()

        # Insere na Treeview
        for atendimento in atendimentos:
            tabela.insert("", "end", values=atendimento)

    
    
    def abrir_cadastro():

        # Cria a janela
        janela = ctk.CTkToplevel(parent)
        janela.title("Novo Atendimento")
        janela.geometry("500x500")
        janela.grab_set()

        # Título
        ctk.CTkLabel(
            janela,
            text="Novo Atendimento",
            font=("Arial", 22, "bold")
        ).pack(pady=20)
        ##pacientes
        pacientes = listar_pacientes_combo()

        nomes_pacientes = []

        for paciente in pacientes:
            nomes_pacientes.append(paciente[1])

        ctk.CTkLabel(
            janela,
            text="Paciente"
        ).pack()

        combo_paciente = ctk.CTkComboBox(
            janela,
            values=nomes_pacientes,
            width=350
        )

        combo_paciente.pack(pady=10)

    
        # Residentes
        residentes = listar_residentes_combo()

        nomes_residentes = []

        for residente in residentes:
            nomes_residentes.append(residente[1])

        ctk.CTkLabel(
            janela,
            text="Residente"
        ).pack()

        combo_residente = ctk.CTkComboBox(
            janela,
            values=nomes_residentes,
            width=350
        )
        combo_residente.pack(pady=10)

        # Preceptores
        preceptores = listar_preceptores_combo()

        nomes_preceptores = []

        for preceptor in preceptores:
            nomes_preceptores.append(preceptor[1])

        ctk.CTkLabel(
        janela,
        text="Preceptor"
        ).pack()

        combo_preceptor = ctk.CTkComboBox(
        janela,
        values=nomes_preceptores,
        width=350
        )

        combo_preceptor.pack(pady=10)

        # Data
        ctk.CTkLabel(
            janela,
            text="Data e Hora"
        ).pack()

        entrada_data = ctk.CTkEntry(
            janela,
            width=350,
            placeholder_text="dd/mm/aaaa hh:mm"
        )
        entrada_data.pack(pady=10)

        # Duração
        ctk.CTkLabel(
            janela,
            text="Duração (minutos)"
        ).pack()

        entrada_duracao = ctk.CTkEntry(
            janela,
            width=350
    )
        entrada_duracao.pack(pady=10)

        # Salvar
        def salvar():

            # Nome selecionado
            nome_paciente = combo_paciente.get()
            nome_residente = combo_residente.get()
            nome_preceptor = combo_preceptor.get()

            # Procura o ID do paciente
            for paciente in pacientes:
                if paciente[1] == nome_paciente:
                    id_paciente = paciente[0]
                    break

            # Procura o ID do residente
            for residente in residentes:
                if residente[1] == nome_residente:
                    id_residente = residente[0]
                    break

            # Procura o ID do preceptor
            for preceptor in preceptores:
                if preceptor[1] == nome_preceptor:
                    id_preceptor = preceptor[0]
                    break

            data_hora = entrada_data.get()

            duracao = int(entrada_duracao.get())

            cadastrar_atendimento(
                id_paciente,
                id_residente,
                id_preceptor,
                data_hora,
                duracao
            )

            carregar_atendimentos()

            janela.destroy()

        ctk.CTkButton(
            janela,
            text="Salvar",
            width=180,
            command=salvar
        ).pack(pady=20)


        # Título
        
    titulo = ctk.CTkLabel(
         parent,
         text="Atendimentos",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=20)



    pacientes = listar_pacientes_combo()

    nomes_pacientes = []

    for paciente in pacientes:
        nomes_pacientes.append(paciente[1])

    pesquisa = ctk.CTkFrame(parent)
    pesquisa.pack(fill="x", padx=20)

    combo_paciente = ctk.CTkComboBox(
        pesquisa,
        values=nomes_pacientes,
        width=300
    )

    combo_paciente.pack(side="left", padx=10, pady=10)
    
    def pesquisar():

        nome = combo_paciente.get()

        print("Paciente escolhido:", nome)

        id_paciente = None

        for paciente in pacientes:

            print(paciente)

            if paciente[1] == nome:

                id_paciente = paciente[0]
                break

        if id_paciente is None:
            print("Paciente não encontrado!")
            return

        print("ID encontrado:", id_paciente)

        dados = listar_atendimentos_paciente(id_paciente)

        print("Dados retornados:", dados)

        tabela.delete(*tabela.get_children())

        for linha in dados:
            tabela.insert("", "end", values=linha)

    # Tabela
    
    tabela = ttk.Treeview(
        parent,
        columns=(
            "ID",
            "Paciente",
            "Residente",
            "Preceptor",
            "Data/Hora",
            "Duração"
        ),
        show="headings",
        height=14
    )

    tabela.heading("ID", text="ID")
    tabela.heading("Paciente", text="Paciente")
    tabela.heading("Residente", text="Residente")
    tabela.heading("Preceptor", text="Preceptor")
    tabela.heading("Data/Hora", text="Data/Hora")
    tabela.heading("Duração", text="Duração (min)")

    tabela.column("ID", width=60, anchor="center")
    tabela.column("Paciente", width=180)
    tabela.column("Residente", width=180)
    tabela.column("Preceptor", width=180)
    tabela.column("Data/Hora", width=170)
    tabela.column("Duração", width=100, anchor="center")

    tabela.pack(fill="both", expand=True, padx=20, pady=20)

    # Carrega os dados
    carregar_atendimentos()

    
    # Botão
    

    botoes = ctk.CTkFrame(parent)
    botoes.pack(pady=15)

    ctk.CTkButton(
        botoes,
        text="Novo Atendimento",
        width=180,
        command=abrir_cadastro
    ).pack()



    ctk.CTkButton(
        pesquisa,
        text="Pesquisar",
        command=pesquisar
).pack(side="left", padx=10)