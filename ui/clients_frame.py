import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

class ClientsFrame(ctk.CTkFrame):
    """
    Frame que contém a interface e a lógica para o gerenciamento de clientes.
    """
    def __init__(self, parent, db):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Frame do Formulário ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(self.form_frame, text="Nome Completo:").grid(row=0, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_nome = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do cliente")
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(self.form_frame, text="Telefone:").grid(row=0, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_telefone = ctk.CTkEntry(self.form_frame, placeholder_text="(00) 90000-0000")
        self.entry_telefone.grid(row=0, column=3, padx=(5,10), pady=5, sticky="ew")
        ctk.CTkLabel(self.form_frame, text="Email:").grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(self.form_frame, placeholder_text="email@exemplo.com")
        self.entry_email.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(self.form_frame, text="Status:").grid(row=1, column=2, padx=(10,5), pady=5, sticky="w")
        self.combo_status = ctk.CTkComboBox(self.form_frame, values=["Prospect", "Contatado", "Visitando", "Em Negociação", "Comprador", "Inativo"])
        self.combo_status.grid(row=1, column=3, padx=(5,10), pady=5, sticky="ew")

        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.btn_add = ctk.CTkButton(self.button_frame, text="Adicionar Cliente", command=self.add_client)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)
        self.btn_update = ctk.CTkButton(self.button_frame, text="Atualizar Selecionado", command=self.update_client)
        self.btn_update.grid(row=0, column=1, padx=5, pady=5)
        self.btn_delete = ctk.CTkButton(self.button_frame, text="Deletar Selecionado", command=self.delete_client, fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)
        self.btn_clear = ctk.CTkButton(self.button_frame, text="Limpar Campos", command=self.clear_fields, fg_color="gray50", hover_color="gray30")
        self.btn_clear.grid(row=0, column=3, padx=5, pady=5)

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
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Telefone", "Email", "Status"), show='headings')
        self.tree.heading("ID", text="ID"); self.tree.heading("Nome", text="Nome"); self.tree.heading("Telefone", text="Telefone"); self.tree.heading("Email", text="Email"); self.tree.heading("Status", text="Status")
        self.tree.column("ID", width=50, anchor="center"); self.tree.column("Nome", width=300); self.tree.column("Telefone", width=150); self.tree.column("Email", width=250); self.tree.column("Status", width=120, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nswe")
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def populate_treeview(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        query = "SELECT id, nome_completo, telefone, email, status FROM clientes ORDER BY nome_completo"
        for row in self.db.fetch_query(query): self.tree.insert("", "end", values=row)

    def on_item_select(self, event):
        selected_item = self.tree.focus()
        if not selected_item: return
        client_id = self.tree.item(selected_item, 'values')[0]
        query = "SELECT * FROM clientes WHERE id = ?"
        client_data = self.db.fetch_query(query, (client_id,))
        if client_data:
            data = client_data[0]
            self.clear_fields(clear_selection=False)
            self.entry_nome.insert(0, data[2]); self.combo_status.set(data[3] or ""); self.entry_telefone.insert(0, data[5] or ""); self.entry_email.insert(0, data[6] or "")

    def add_client(self):
        nome = self.entry_nome.get().strip()
        if not nome: messagebox.showerror("Erro de Validação", "O campo 'Nome Completo' é obrigatório."); return
        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO clientes (data_cadastro, nome_completo, status, telefone, email) VALUES (?, ?, ?, ?, ?)"
        params = (data_cadastro, nome, self.combo_status.get(), self.entry_telefone.get(), self.entry_email.get())
        try:
            self.db.execute_query(query, params); messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!"); self.populate_treeview(); self.clear_fields()
        except Exception as e: messagebox.showerror("Erro de Banco de Dados", f"Não foi possível adicionar o cliente:\n{e}")

    def update_client(self):
        selected_item = self.tree.focus()
        if not selected_item: messagebox.showwarning("Seleção Necessária", "Por favor, selecione um cliente na tabela para atualizar."); return
        client_id = self.tree.item(selected_item, 'values')[0]
        query = "UPDATE clientes SET nome_completo=?, status=?, telefone=?, email=? WHERE id=?"
        params = (self.entry_nome.get(), self.combo_status.get(), self.entry_telefone.get(), self.entry_email.get(), client_id)
        try:
            self.db.execute_query(query, params); messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!"); self.populate_treeview(); self.clear_fields()
        except Exception as e: messagebox.showerror("Erro de Banco de Dados", f"Não foi possível atualizar o cliente:\n{e}")

    def delete_client(self):
        selected_item = self.tree.focus()
        if not selected_item: messagebox.showwarning("Seleção Necessária", "Por favor, selecione um cliente na tabela para deletar."); return
        if messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja deletar este cliente? Todas as interações relacionadas também serão excluídas permanentemente."):
            client_id = self.tree.item(selected_item, 'values')[0]
            try:
                self.db.execute_query("DELETE FROM clientes WHERE id=?", (client_id,)); messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!"); self.populate_treeview(); self.clear_fields()
            except Exception as e: messagebox.showerror("Erro de Banco de Dados", f"Não foi possível deletar o cliente:\n{e}")

    def clear_fields(self, clear_selection=True):
        self.entry_nome.delete(0, 'end'); self.entry_telefone.delete(0, 'end'); self.entry_email.delete(0, 'end'); self.combo_status.set("")
        if clear_selection and self.tree.focus(): self.tree.selection_remove(self.tree.focus())

    def get_all_clients_for_combobox(self):
        """
        Busca todos os clientes no banco de dados e os formata para uso
        no ComboBox da tela de interações.
        
        :return: Uma lista de strings, cada uma no formato "ID: Nome Completo".
        """
        query = "SELECT id, nome_completo FROM clientes ORDER BY nome_completo"
        clients = self.db.fetch_query(query)
        return [f"{client[0]}: {client[1]}" for client in clients] if clients else []

