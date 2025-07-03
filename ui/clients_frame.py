import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

class ClientsFrame(ctk.CTkFrame):
    """
    Frame que contém a interface e a lógica para o gerenciamento de clientes.
    """
    def __init__(self, parent, db, app_ref):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.app = app_ref
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Frame do Formulário ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.form_frame.grid_columnconfigure((1, 3), weight=1)

        # --- Widgets do Formulário ---
        # Linha 1: Informações Pessoais
        ctk.CTkLabel(self.form_frame, text="Nome Completo:").grid(row=0, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_nome = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do cliente")
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Telefone:").grid(row=0, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_telefone = ctk.CTkEntry(self.form_frame, placeholder_text="(00) 90000-0000")
        self.entry_telefone.grid(row=0, column=3, padx=(5,10), pady=5, sticky="ew")

        # Linha 2: Informações de Contato
        ctk.CTkLabel(self.form_frame, text="Email:").grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(self.form_frame, placeholder_text="email@exemplo.com")
        self.entry_email.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Próximo Contato:").grid(row=1, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_prox_contato = ctk.CTkEntry(self.form_frame, placeholder_text="DD/MM/AAAA")
        self.entry_prox_contato.grid(row=1, column=3, padx=(5,10), pady=5, sticky="ew")

        # --- Seção "Perfil de Busca" ---
        profile_label = ctk.CTkLabel(self.form_frame, text="Perfil de Busca do Cliente", font=ctk.CTkFont(size=12, weight="bold"))
        profile_label.grid(row=2, column=0, columnspan=4, padx=10, pady=(10,0), sticky="w")

        # Linha 3: Perfil de Busca
        ctk.CTkLabel(self.form_frame, text="Tipo de Imóvel:").grid(row=3, column=0, padx=(10,5), pady=5, sticky="w")
        self.combo_tipo_interesse = ctk.CTkComboBox(self.form_frame, values=["", "Apartamento", "Casa", "Terreno", "Comercial"])
        self.combo_tipo_interesse.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Quartos (mín.):").grid(row=3, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_quartos_min = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: 3")
        self.entry_quartos_min.grid(row=3, column=3, padx=(5,10), pady=5, sticky="ew")
        
        # Linha 4: Perfil de Busca
        ctk.CTkLabel(self.form_frame, text="Preço (máx.) R$:").grid(row=4, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_preco_max = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: 500000.00")
        self.entry_preco_max.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Status:").grid(row=4, column=2, padx=(10,5), pady=5, sticky="w")
        self.combo_status = ctk.CTkComboBox(self.form_frame, values=["Prospect", "Contatado", "Visitando", "Em Negociação", "Comprador", "Inativo"])
        self.combo_status.grid(row=4, column=3, padx=(5,10), pady=5, sticky="ew")

        # --- Frame de Botões ---
        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.btn_add = ctk.CTkButton(self.button_frame, text="Adicionar Cliente", command=self.add_client)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_update = ctk.CTkButton(self.button_frame, text="Atualizar Selecionado", command=self.update_client)
        self.btn_update.grid(row=0, column=1, padx=5, pady=5)

        self.btn_delete = ctk.CTkButton(self.button_frame, text="Deletar Selecionado", command=self.delete_client, fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)

        self.btn_clear = ctk.CTkButton(self.button_frame, text="Limpar Campos", command=self.clear_fields, fg_color="gray50", hover_color="gray30")
        self.btn_clear.grid(row=0, column=3, padx=5, pady=5)

        # --- Tabela (Treeview) ---
        self.setup_treeview()
        self.populate_treeview()
        self.update_button_states()

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

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Telefone", "Status", "Próximo Contato"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Próximo Contato", text="Próximo Contato")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=300)
        self.tree.column("Telefone", width=150)
        self.tree.column("Status", width=120, anchor="center")
        self.tree.column("Próximo Contato", width=150, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nswe")
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        
        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def populate_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        query = "SELECT id, nome_completo, telefone, status, proximo_contato FROM clientes ORDER BY nome_completo"
        for row in self.db.fetch_query(query):
            self.tree.insert("", "end", values=row)

    def on_item_select(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        
        client_id = self.tree.item(selected_item, 'values')[0]
        query = "SELECT * FROM clientes WHERE id = ?"
        client_data = self.db.fetch_query(query, (client_id,))
        if client_data:
            data = client_data[0]
            self.clear_fields(clear_selection=False)
            self.entry_nome.insert(0, data[2])
            self.combo_status.set(data[3] or "")
            self.entry_telefone.insert(0, data[5] or "")
            self.entry_email.insert(0, data[6] or "")
            self.entry_prox_contato.insert(0, data[12] or "")
            # Preenche os novos campos de perfil de busca
            self.combo_tipo_interesse.set(data[14] or "")
            self.entry_quartos_min.insert(0, str(data[15] or ""))
            self.entry_preco_max.insert(0, str(data[16] or ""))

    def add_client(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showerror("Erro de Validação", "O campo 'Nome Completo' é obrigatório.")
            return

        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            quartos_min = int(self.entry_quartos_min.get()) if self.entry_quartos_min.get() else None
            preco_max = float(self.entry_preco_max.get()) if self.entry_preco_max.get() else None
        except ValueError:
            messagebox.showerror("Erro de Validação", "Os campos 'Quartos' e 'Preço' devem ser números válidos.")
            return

        query = """INSERT INTO clientes (data_cadastro, nome_completo, status, telefone, email, proximo_contato, 
                                        tipo_imovel_interesse, quartos_min_interesse, preco_max_interesse) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        params = (data_cadastro, nome, self.combo_status.get(), self.entry_telefone.get(), self.entry_email.get(), 
                  self.entry_prox_contato.get(), self.combo_tipo_interesse.get(), quartos_min, preco_max)
        
        try:
            self.db.execute_query(query, params)
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
            self.populate_treeview()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível adicionar o cliente:\n{e}")

    def update_client(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Seleção Necessária", "Por favor, selecione um cliente para atualizar.")
            return
            
        client_id = self.tree.item(selected_item, 'values')[0]
        
        try:
            quartos_min = int(self.entry_quartos_min.get()) if self.entry_quartos_min.get() else None
            preco_max = float(self.entry_preco_max.get()) if self.entry_preco_max.get() else None
        except ValueError:
            messagebox.showerror("Erro de Validação", "Os campos 'Quartos' e 'Preço' devem ser números válidos.")
            return

        query = """UPDATE clientes SET nome_completo=?, status=?, telefone=?, email=?, proximo_contato=?,
                                     tipo_imovel_interesse=?, quartos_min_interesse=?, preco_max_interesse=?
                   WHERE id=?"""
        params = (self.entry_nome.get(), self.combo_status.get(), self.entry_telefone.get(), self.entry_email.get(), 
                  self.entry_prox_contato.get(), self.combo_tipo_interesse.get(), quartos_min, preco_max, client_id)
        
        try:
            self.db.execute_query(query, params)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            self.populate_treeview()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível atualizar o cliente:\n{e}")

    def clear_fields(self, clear_selection=True):
        self.entry_nome.delete(0, 'end')
        self.entry_telefone.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.combo_status.set("")
        self.entry_prox_contato.delete(0, 'end')
        # Limpa os novos campos
        self.combo_tipo_interesse.set("")
        self.entry_quartos_min.delete(0, 'end')
        self.entry_preco_max.delete(0, 'end')
        if clear_selection and self.tree.focus():
            self.tree.selection_remove(self.tree.focus())

    def update_button_states(self):
        """Ativa ou desativa os botões baseando-se no status da licença."""
        if self.app.is_activated:
            self.btn_add.configure(state="normal", text="Adicionar Cliente")
            self.btn_update.configure(state="normal")
            self.btn_delete.configure(state="normal")
        else:
            self.btn_add.configure(state="disabled", text="Adicionar (Requer Ativação)")
            self.btn_update.configure(state="disabled")
            self.btn_delete.configure(state="disabled")
    
    def delete_client(self):
        """Deleta um cliente selecionado."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Seleção Necessária", "Por favor, selecione um cliente na tabela para deletar.")
            return
        
        if messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja deletar este cliente? Todas as interações relacionadas também serão excluídas permanentemente."):
            client_id = self.tree.item(selected_item, 'values')[0]
            try:
                self.db.execute_query("DELETE FROM clientes WHERE id=?", (client_id,))
                messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!")
                self.populate_treeview()
                self.clear_fields()
            except Exception as e:
                messagebox.showerror("Erro de Banco de Dados", f"Não foi possível deletar o cliente:\n{e}")

    def get_all_clients_for_combobox(self):
        """
        Busca todos os clientes no banco de dados e os formata para uso
        no ComboBox da tela de interações.
        
        :return: Uma lista de strings, cada uma no formato "ID: Nome Completo".
        """
        query = "SELECT id, nome_completo FROM clientes ORDER BY nome_completo"
        clients = self.db.fetch_query(query)
        return [f"{client[0]}: {client[1]}" for client in clients] if clients else []

    def select_client_by_id(self, client_id_to_select):
        """
        Busca por um cliente na tabela pelo seu ID e o seleciona programaticamente.
        """
        self.populate_treeview()
        for item_id in self.tree.get_children():
            item_values = self.tree.item(item_id, 'values')
            if item_values and int(item_values[0]) == client_id_to_select:
                self.tree.selection_set(())
                self.tree.selection_set(item_id)
                self.tree.focus(item_id)
                self.tree.see(item_id)
                self.on_item_select(None)
                return
