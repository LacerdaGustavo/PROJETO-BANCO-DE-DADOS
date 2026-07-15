import customtkinter as ctk
from tkinter import ttk

from database import (
    listar_atendimentos_combo,
    listar_procedimentos_atendimento,
    excluir_procedimento_realizado,
    buscar_id_procedimento
)


def criar_tela(parent):

    
    # Pesquisa
    

    def pesquisar():

        atendimento = combo_atendimento.get()

        if atendimento == "":
            return

        id_atendimento = int(
            atendimento.split(" - ")[0]
        )

        procedimentos = listar_procedimentos_atendimento(
            id_atendimento
        )

        # Limpa a tabela
        for item in tabela.get_children():
            tabela.delete(item)

        # Insere os resultados
        for procedimento in procedimentos:
            tabela.insert(
                "",
                "end",
                values=procedimento
            )


    def excluir():

        selecionado = tabela.selection()

        if not selecionado:
            print("Selecione um procedimento.")
            return

        valores = tabela.item(selecionado[0])["values"]

        nome_procedimento = valores[0]

        atendimento = combo_atendimento.get()

        id_atendimento = int(
            atendimento.split(" - ")[0]
        )

        # Procura o id do procedimento pelo nome
        id_procedimento = buscar_id_procedimento(nome_procedimento)

        sucesso = excluir_procedimento_realizado(
            id_atendimento,
            id_procedimento
        )

        if sucesso:
            print("Procedimento excluído com sucesso!")
            pesquisar()
        else:
            print("Este procedimento já foi faturado.")

        
    # Título
    

    titulo = ctk.CTkLabel(
        parent,
        text="Procedimentos Realizados",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=20)

    
    # Busca os atendimentos
    

    atendimentos = listar_atendimentos_combo()

    nomes_atendimentos = []

    for atendimento in atendimentos:

        nomes_atendimentos.append(
            f"{atendimento[0]} - {atendimento[1]}"
        )

   
    # Área de pesquisa
    

    pesquisa = ctk.CTkFrame(parent)
    pesquisa.pack(fill="x", padx=20)

    combo_atendimento = ctk.CTkComboBox(
        pesquisa,
        values=nomes_atendimentos,
        width=350
    )

    combo_atendimento.pack(
        side="left",
        padx=10,
        pady=10
    )

    ctk.CTkButton(
        pesquisa,
        text="Pesquisar",
        command=pesquisar
    ).pack(
        side="left",
        padx=10
    )


    ctk.CTkButton(
        pesquisa,
        text="Excluir Procedimento",
        command=excluir
    ).pack(
        side="left",
        padx=10
    )
    
    # Tabela
    

    tabela = ttk.Treeview(
        parent,
        columns=(
            "Procedimento",
            "Quantidade",
            "Tempo"
        ),
        show="headings",
        height=14
    )

    tabela.heading(
        "Procedimento",
        text="Procedimento"
    )

    tabela.heading(
        "Quantidade",
        text="Quantidade"
    )

    tabela.heading(
        "Tempo",
        text="Tempo Real (min)"
    )

    tabela.column(
        "Procedimento",
        width=400
    )

    tabela.column(
        "Quantidade",
        width=120,
        anchor="center"
    )

    tabela.column(
        "Tempo",
        width=150,
        anchor="center"
    )

    tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    