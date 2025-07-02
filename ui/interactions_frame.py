import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

class InteractionsFrame(ctk.CTkFrame):
    """
    Frame que contém a interface para registrar e visualizar as interações com os clientes.
    """
    def __init__(self, parent, db, clients_frame_ref):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.clients_frame_ref = clients_frame_ref
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Frame do Formulário ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.form_frame.grid_columnconfigure(1, weight=1)

        # --- Widgets do Formulário ---
        ctk.CTkLabel(self.form_frame, text="Cliente:").grid(row=0, column=0, padx=(10,5), pady=10, sticky="w")
        # Este ComboBox será preenchido com os clientes do banco de dados
        self.combo_cliente = ctk.CTkComboBox(self.form_frame, values=["Nenhum cliente cadastrado"], state="readonly")
        self.combo_cliente.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Tipo de Interação:").grid(row=1, column=0, padx=(10,5), pady=10, sticky="w")
        self.combo_tipo = ctk.CTkComboBox(self.form_frame, values=["Ligação", "Email", "WhatsApp", "Visita ao Imóvel", "Reunião"], state="readonly")
        self.combo_tipo.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Resumo:").grid(row=2, column=0, padx=(10,5), pady=10, sticky="w")
        self.entry_resumo = ctk.CTkEntry(self.form_frame, placeholder_text="Descreva o contato com o cliente...")
        self.entry_resumo.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        self.btn_add = ctk.CTkButton(self.form_frame, text="Registrar Interação", command=self.add_interaction)
        self.btn_add.grid(row=3, column=1, padx=5, pady=10, sticky="e")
        
        # --- Tabela (Treeview) ---
        self.setup_treeview()
        self.populate_treeview()

    def setup_treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=('Calibri', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=1, column=0, sticky="nswe", padx=10, pady=(0,10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Cliente", "Data", "Tipo", "Resumo"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Resumo", text="Resumo")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Cliente", width=250)
        self.tree.column("Data", width=150, anchor="center")
        self.tree.column("Tipo", width=150)
        self.tree.column("Resumo", width=400)

        self.tree.grid(row=0, column=0, sticky="nswe")
        
        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def populate_treeview(self):
        """Busca e exibe o histórico de interações, ordenado pela mais recente."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Usamos um JOIN para buscar o nome do cliente na tabela 'clientes'
        query = """
        SELECT i.id, c.nome_completo, i.data, i.tipo_interacao, i.resumo
        FROM interacoes i
        JOIN clientes c ON i.cliente_id = c.id
        ORDER BY i.data DESC
        """
        for row in self.db.fetch_query(query):
            # Formata a data para um formato mais legível
            data_formatada = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
            values = (row[0], row[1], data_formatada, row[3], row[4])
            self.tree.insert("", "end", values=values)

    def update_client_list(self):
        """
        Busca a lista de clientes atualizada e preenche o ComboBox.
        Este método é chamado pela janela principal (App) sempre que esta tela é exibida.
        """
        clients = self.clients_frame_ref.get_all_clients_for_combobox()
        if clients:
            self.combo_cliente.configure(values=clients)
            self.combo_cliente.set(clients[0])
        else:
            self.combo_cliente.configure(values=["Nenhum cliente cadastrado"])
            self.combo_cliente.set("Nenhum cliente cadastrado")

    def add_interaction(self):
        """Adiciona um novo registro de interação ao banco de dados."""
        cliente_selecionado = self.combo_cliente.get()
        if not cliente_selecionado or cliente_selecionado == "Nenhum cliente cadastrado":
            messagebox.showerror("Erro de Validação", "É necessário selecionar um cliente.")
            return

        resumo = self.entry_resumo.get().strip()
        if not resumo:
            messagebox.showerror("Erro de Validação", "O campo 'Resumo' é obrigatório.")
            return
            
        try:
            # Extrai o ID do cliente do texto "ID: Nome"
            cliente_id = int(cliente_selecionado.split(":")[0])
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Formato de cliente inválido na lista.")
            return

        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tipo = self.combo_tipo.get()

        query = "INSERT INTO interacoes (cliente_id, data, tipo_interacao, resumo) VALUES (?, ?, ?, ?)"
        params = (cliente_id, data, tipo, resumo)
        
        try:
            self.db.execute_query(query, params)
            messagebox.showinfo("Sucesso", "Interação registrada com sucesso!")
            self.populate_treeview()
            self.entry_resumo.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível registrar a interação:\n{e}")

