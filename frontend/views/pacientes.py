import customtkinter as ctk
from tkinter import ttk

from database import( listar_pacientes, cadastrar_paciente, buscar_paciente, atualizar_paciente, excluir_paciente)


def criar_tela(parent):

    
    # Função para abrir a janela de cadastro
   
    def abrir_cadastro(paciente=None):

        janela = ctk.CTkToplevel(parent)
        janela.title("Cadastrar Paciente")
        janela.geometry("600x1000")
        janela.grab_set()

       
        # Título

        ctk.CTkLabel(
            janela,
            text="Cadastrar Paciente",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

       

        # DADOS DA PESSOA
        
        frame_pessoa = ctk.CTkFrame(janela)
        frame_pessoa.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            frame_pessoa,
            text="Dados da Pessoa",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Nome
        ctk.CTkLabel(frame_pessoa, text="Nome").pack(anchor="w", padx=20)

        entrada_nome = ctk.CTkEntry(frame_pessoa, width=450)
        entrada_nome.pack(pady=5)

        # CPF
        ctk.CTkLabel(frame_pessoa, text="CPF").pack(anchor="w", padx=20)

        entrada_cpf = ctk.CTkEntry(frame_pessoa, width=450)
        entrada_cpf.pack(pady=5)

        # Telefone
        ctk.CTkLabel(frame_pessoa, text="Telefone").pack(anchor="w", padx=20)

        entrada_telefone = ctk.CTkEntry(frame_pessoa, width=450)
        entrada_telefone.pack(pady=5)

        # Data de nascimento
        ctk.CTkLabel(frame_pessoa, text="Data de nascimento").pack(anchor="w", padx=20)

        entrada_data = ctk.CTkEntry(
            frame_pessoa,
            width=450,
            placeholder_text="dd/mm/aaaa"
        )
        entrada_data.pack(pady=5)

        # Flamenguista
        check_flamengo = ctk.CTkCheckBox(
            frame_pessoa,
            text="Flamenguista"
        )
        check_flamengo.pack(anchor="w", padx=20, pady=10)

        # Endereço
        ctk.CTkLabel(frame_pessoa,text="Endereço").pack(anchor="w", padx=20)

        entrada_endereco = ctk.CTkEntry(frame_pessoa,width=450)
        entrada_endereco.pack(pady=5)

        ##DADOS DO PACIENTE#
        
        frame_paciente = ctk.CTkFrame(janela)
        frame_paciente.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            frame_paciente,
            text="Dados do Paciente",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Convênio
        ctk.CTkLabel(frame_paciente, text="Convênio").pack(anchor="w", padx=20)

        entrada_convenio = ctk.CTkEntry(frame_paciente, width=450)
        entrada_convenio.pack(pady=5)

        # Grupo sanguíneo
        ctk.CTkLabel(frame_paciente, text="Grupo sanguíneo").pack(anchor="w", padx=20)

        combo_grupo = ctk.CTkComboBox(
            frame_paciente,
            values=[
                "A+",
                "A-",
                "B+",
                "B-",
                "AB+",
                "AB-",
                "O+",
                "O-"
            ],
            width=450
        )

        combo_grupo.pack(pady=5)
        combo_grupo.set("Selecione")

        # Alergias
        ctk.CTkLabel(frame_paciente, text="Alergias").pack(anchor="w", padx=20)

        texto_alergias = ctk.CTkTextbox(
            frame_paciente,
            width=450,
            height=90
        )

        texto_alergias.pack(pady=5)

        
# Preenche os campos se estiver editando

        if paciente is not None:

            entrada_nome.insert(0, paciente[1])

            entrada_cpf.insert(0, paciente[2])

            entrada_telefone.insert(0, paciente[3])

            entrada_data.insert(
                0,
                paciente[4].strftime("%d/%m/%Y")
            )

            if paciente[5]:
                check_flamengo.select()

            entrada_convenio.insert(0, paciente[6])

            combo_grupo.set(paciente[7])

            texto_alergias.insert(
                "1.0",
                paciente[8]
            )
            print(paciente)
            print(len(paciente))
            
            entrada_endereco.insert(
                0,
                str(paciente[9]) if paciente[9] is not None else ""
            )
        # SALVAR
       
        def salvar():
            print("Botão Salvar foi clicado")

            nome = entrada_nome.get()
            cpf = entrada_cpf.get()
            telefone = entrada_telefone.get()
            data = entrada_data.get()

            flamengo = check_flamengo.get()
            flamengo = bool(flamengo)

            convenio = entrada_convenio.get()
            grupo = combo_grupo.get()
            alergias = texto_alergias.get("1.0", "end").strip()
            endereco = entrada_endereco.get()

            print(nome)
            print(cpf)
            print(telefone)
            print(data)
            print(flamengo)
            print(convenio)
            print(grupo)
            print(alergias)
            print(endereco)

            if paciente is None:
                cadastrar_paciente(
                    nome,
                    cpf,
                    telefone,
                    data,
                    flamengo,
                    convenio,
                    grupo,
                    alergias,
                    endereco
                )
                carregar_pacientes()
            else:
                atualizar_paciente(
                    paciente[0],
                    nome,
                    cpf,
                    telefone,
                    data,
                    flamengo,
                    convenio,
                    grupo,
                    alergias,
                    endereco
                )
                carregar_pacientes()
                # Depois chamaremos o database.py

            janela.destroy()

        ctk.CTkButton(
            janela,
            text="Salvar",
            width=200,
            command=salvar
        ).pack(pady=20)
        
    ##EDITAR##
    def editar_paciente():

        # Verifica se existe uma linha selecionada
        selecionado = tabela.selection()

        if not selecionado:
            print("Selecione um paciente.")
            return

        # Obtém os dados da linha selecionada
        dados = tabela.item(selecionado[0])

        valores = dados["values"]

        # O primeiro valor é o id_pessoa
        id_pessoa = valores[0]

        # Busca o paciente no banco
        paciente = buscar_paciente(id_pessoa)

        # Abre a janela já preenchida
        abrir_cadastro(paciente)

    ##EXCLUIR
    def excluir():

        selecionado = tabela.selection()

        if not selecionado:
            print("Selecione um paciente.")
            return

        dados = tabela.item(selecionado[0])

        valores = dados["values"]

        id_pessoa = valores[0]

        excluir_paciente(id_pessoa)

        print("Paciente excluído.")

    #Carregar
    def carregar_pacientes():

        for item in tabela.get_children():
            tabela.delete(item)

        pacientes = listar_pacientes()

        for paciente in pacientes:
            tabela.insert("", "end", values=paciente)



    # Título

    titulo = ctk.CTkLabel(
        parent,
        text="Pacientes",
        font=("Arial", 28, "bold")
    )

    titulo.pack(pady=20)

    
    # Pesquisa
    
    pesquisa = ctk.CTkFrame(parent)
    pesquisa.pack(fill="x", padx=20)

    entrada = ctk.CTkEntry(
        pesquisa,
        width=400,
        placeholder_text="Pesquisar paciente..."
    )

    entrada.pack(side="left", padx=10, pady=10)

    ctk.CTkButton(
        pesquisa,
        text="Pesquisar"
    ).pack(side="left", padx=10)

   
    # Tabela
  
    tabela = ttk.Treeview(
        parent,
        columns=(
            "ID",
            "Nome",
            "CPF",
            "Telefone",
            "Nascimento",
            "Flamengo",
            "Convênio",
            "Grupo",
            "Alergias",
            "Endereço"
        ),
        show="headings",
        height=12
    )

    tabela.heading("ID", text="ID")
    tabela.heading("Nome", text="Nome")
    tabela.heading("CPF", text="CPF")
    tabela.heading("Telefone", text="Telefone")
    tabela.heading("Nascimento", text="Nascimento")
    tabela.heading("Flamengo", text="Flamengo")
    tabela.heading("Convênio", text="Convênio")
    tabela.heading("Grupo", text="Grupo")
    tabela.heading("Alergias", text="Alergias")
    tabela.heading("Endereço", text="Endereço")

    tabela.column("ID", width=40, anchor="center")
    tabela.column("Nome", width=140)
    tabela.column("CPF", width=110)
    tabela.column("Telefone", width=100)
    tabela.column("Nascimento", width=90, anchor="center")
    tabela.column("Flamengo", width=70, anchor="center")
    tabela.column("Convênio", width=100)
    tabela.column("Grupo", width=55, anchor="center")
    tabela.column("Alergias", width=170)
    tabela.column("Endereço", width=200)

    pacientes = listar_pacientes()

    carregar_pacientes()

    tabela.pack(fill="both", expand=True, padx=20, pady=20)

    
    # Botões
    
    botoes = ctk.CTkFrame(parent)
    botoes.pack(pady=15)

    ctk.CTkButton(
        botoes,
        text="Cadastrar",
        width=120,
        command=abrir_cadastro
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        botoes,
        text="Editar",
        width=120,
        command=editar_paciente
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        botoes,
        text="Excluir",
        width=120,
        command=excluir
    ).pack(side="left", padx=10)