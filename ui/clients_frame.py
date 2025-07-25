import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
from .match_results_window import MatchResultsWindow

class ClientsFrame(ctk.CTkFrame):
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

        # --- Seção: Informações Pessoais ---
        ctk.CTkLabel(self.form_frame, text="Informações Pessoais", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, columnspan=4, padx=10, pady=(10,0), sticky="w")
        
        ctk.CTkLabel(self.form_frame, text="Nome Completo:").grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_nome = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do cliente")
        self.entry_nome.grid(row=1, column=1, columnspan=3, padx=(0,10), pady=5, sticky="ew")
        
        # --- Seção: Perfil de Busca (Dinâmico) ---
        ctk.CTkLabel(self.form_frame, text="Perfil de Busca do Imóvel", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, columnspan=4, padx=10, pady=(10,0), sticky="w")
        
        ctk.CTkLabel(self.form_frame, text="Interesse Principal:").grid(row=3, column=0, padx=(10,5), pady=5, sticky="w")
        self.combo_negocio_interesse = ctk.CTkComboBox(self.form_frame, values=["Comprar", "Alugar"], command=self.toggle_profile_fields)
        self.combo_negocio_interesse.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.combo_negocio_interesse.set("Comprar")

        # --- Sub-Frame para campos de Perfil ---
        # Este frame conterá os campos que mudam
        self.profile_fields_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.profile_fields_frame.grid(row=4, column=0, columnspan=4, sticky="ew")
        self.profile_fields_frame.grid_columnconfigure((1, 3), weight=1)

        # Widgets que estarão dentro do frame de perfil
        ctk.CTkLabel(self.profile_fields_frame, text="Tipo de Imóvel:").grid(row=0, column=0, padx=(10,5), pady=5, sticky="w")
        self.combo_tipo_interesse = ctk.CTkComboBox(self.profile_fields_frame, values=["", "Apartamento", "Casa", "Sobrado", "Terreno", "Comercial"])
        self.combo_tipo_interesse.grid(row=0, column=1, padx=0, pady=5, sticky="ew")
        
        self.label_finalidade = ctk.CTkLabel(self.profile_fields_frame, text="Finalidade:")
        self.label_finalidade.grid(row=0, column=2, padx=(10,5), pady=5, sticky="w")
        self.combo_finalidade = ctk.CTkComboBox(self.profile_fields_frame, values=["", "Moradia", "Investimento"])
        self.combo_finalidade.grid(row=0, column=3, padx=(0,10), pady=5, sticky="ew")

        self.label_preco_min = ctk.CTkLabel(self.profile_fields_frame, text="Preço Mín. (R$):")
        self.label_preco_min.grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_preco_min = ctk.CTkEntry(self.profile_fields_frame, placeholder_text="Ex: 300000")
        self.entry_preco_min.grid(row=1, column=1, padx=0, pady=5, sticky="ew")
        
        self.label_preco_max = ctk.CTkLabel(self.profile_fields_frame, text="Preço Máx. (R$):")
        self.label_preco_max.grid(row=1, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_preco_max = ctk.CTkEntry(self.profile_fields_frame, placeholder_text="Ex: 500000")
        self.entry_preco_max.grid(row=1, column=3, padx=(0,10), pady=5, sticky="ew")

        ctk.CTkLabel(self.profile_fields_frame, text="Quartos (mín.):").grid(row=2, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_quartos_min = ctk.CTkEntry(self.profile_fields_frame, placeholder_text="Ex: 3")
        self.entry_quartos_min.grid(row=2, column=1, padx=0, pady=5, sticky="ew")

        ctk.CTkLabel(self.profile_fields_frame, text="Banheiros (mín.):").grid(row=2, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_banheiros_min = ctk.CTkEntry(self.profile_fields_frame, placeholder_text="Ex: 2")
        self.entry_banheiros_min.grid(row=2, column=3, padx=(0,10), pady=5, sticky="ew")

        ctk.CTkLabel(self.profile_fields_frame, text="Vagas (mín.):").grid(row=3, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_vagas_min = ctk.CTkEntry(self.profile_fields_frame, placeholder_text="Ex: 1")
        self.entry_vagas_min.grid(row=3, column=1, padx=0, pady=5, sticky="ew")

        ctk.CTkLabel(self.profile_fields_frame, text="Bairros de Interesse:").grid(row=3, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_bairros_interesse = ctk.CTkEntry(self.profile_fields_frame, placeholder_text="Ex: Vila Nova, Velha")
        self.entry_bairros_interesse.grid(row=3, column=3, padx=(0,10), pady=5, sticky="ew")
        
        # --- Seção: Status e Follow-up ---
        ctk.CTkLabel(self.form_frame, text="Status e Acompanhamento", font=ctk.CTkFont(size=12, weight="bold")).grid(row=5, column=0, columnspan=4, padx=10, pady=(10,0), sticky="w")
        
        ctk.CTkLabel(self.form_frame, text="Status do Cliente:").grid(row=6, column=0, padx=(10,5), pady=5, sticky="w")
        self.combo_status = ctk.CTkComboBox(self.form_frame, values=["Prospect", "Contatado", "Visitando", "Em Negociação", "Comprador", "Inativo"])
        self.combo_status.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Próximo Contato:").grid(row=6, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_prox_contato = ctk.CTkEntry(self.form_frame, placeholder_text="DD/MM/AAAA")
        self.entry_prox_contato.grid(row=6, column=3, padx=(5,10), pady=5, sticky="ew")

        # --- Frame de Botões ---
        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.btn_add = ctk.CTkButton(self.button_frame, text="Adicionar Cliente", command=self.add_client)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)
        self.btn_update = ctk.CTkButton(self.button_frame, text="Atualizar Selecionado", command=self.update_client)
        self.btn_update.grid(row=0, column=1, padx=5, pady=5)
        self.btn_delete = ctk.CTkButton(self.button_frame, text="Deletar Selecionado", command=self.delete_client, fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)
        self.btn_clear = ctk.CTkButton(self.button_frame, text="Limpar Campos", command=self.clear_fields, fg_color="gray50", hover_color="gray30")
        self.btn_clear.grid(row=0, column=3, padx=5, pady=5)
        self.btn_match = ctk.CTkButton(self.button_frame, text="Buscar Imóveis Compatíveis", command=self.find_matching_properties, fg_color="#1F6AA5")
        self.btn_match.grid(row=0, column=4, padx=5, pady=5)

        # --- Tabela (Treeview) ---
        self.setup_treeview()
        self.populate_treeview()
        self.update_button_states()
        self.toggle_profile_fields(None)

    def toggle_profile_fields(self, choice):
        """Mostra ou esconde os campos de perfil com base no interesse do cliente."""
        interesse = self.combo_negocio_interesse.get()
        if interesse == "Comprar":
            self.label_preco_min.configure(text="Preço Mín. (R$):")
            self.label_preco_max.configure(text="Preço Máx. (R$):")
            self.label_finalidade.grid()
            self.combo_finalidade.grid()
            self.entry_preco_min.grid()
        elif interesse == "Alugar":
            self.label_preco_min.configure(text="Aluguel Mín. (R$):")
            self.label_preco_max.configure(text="Aluguel Máx. (R$):")
            self.label_finalidade.grid_remove()
            self.combo_finalidade.grid_remove()
            self.entry_preco_min.grid_remove()

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
        self.tree.heading("ID", text="ID"); self.tree.heading("Nome", text="Nome"); self.tree.heading("Telefone", text="Telefone"); self.tree.heading("Status", text="Status"); self.tree.heading("Próximo Contato", text="Próximo Contato")
        self.tree.column("ID", width=50, anchor="center"); self.tree.column("Nome", width=300); self.tree.column("Telefone", width=150); self.tree.column("Status", width=120, anchor="center"); self.tree.column("Próximo Contato", width=150, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nswe")
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        
        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def populate_treeview(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        query = "SELECT id, nome_completo, telefone, status, proximo_contato FROM clientes ORDER BY nome_completo"
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
            
            negocio_interesse = data[9] or "Comprar"
            self.combo_negocio_interesse.set(negocio_interesse)
            self.toggle_profile_fields(None)

            self.entry_nome.insert(0, data[2]); self.entry_telefone.insert(0, data[5]); self.entry_email.insert(0, data[6]); self.combo_status.set(data[3] or ""); self.entry_prox_contato.insert(0, data[7] or "")
            self.combo_tipo_interesse.set(data[10] or ""); self.entry_preco_min.insert(0, str(data[11] or "")); self.entry_preco_max.insert(0, str(data[12] or "")); self.entry_quartos_min.insert(0, str(data[13] or "")); self.entry_banheiros_min.insert(0, str(data[14] or "")); self.entry_vagas_min.insert(0, str(data[15] or "")); self.entry_bairros_interesse.insert(0, data[16] or ""); self.combo_finalidade.set(data[17] or "")

    def add_client(self):
        nome = self.entry_nome.get().strip()
        if not nome: messagebox.showerror("Erro de Validação", "O campo 'Nome Completo' é obrigatório."); return
        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            preco_min = float(self.entry_preco_min.get()) if self.entry_preco_min.get() else None
            preco_max = float(self.entry_preco_max.get()) if self.entry_preco_max.get() else None
            quartos_min = int(self.entry_quartos_min.get()) if self.entry_quartos_min.get() else None
            banheiros_min = int(self.entry_banheiros_min.get()) if self.entry_banheiros_min.get() else None
            vagas_min = int(self.entry_vagas_min.get()) if self.entry_vagas_min.get() else None
        except ValueError: messagebox.showerror("Erro de Validação", "Os campos de preço e características devem ser números válidos."); return

        query = """INSERT INTO clientes (data_cadastro, nome_completo, status, telefone, email, proximo_contato, tipo_negocio_interesse, tipo_imovel_interesse, preco_min_interesse, preco_max_interesse, quartos_min_interesse, banheiros_min_interesse, vagas_min_interesse, bairros_interesse, finalidade) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        params = (data_cadastro, nome, self.combo_status.get(), self.entry_telefone.get(), self.entry_email.get(), self.entry_prox_contato.get(), self.combo_negocio_interesse.get(), self.combo_tipo_interesse.get(), preco_min, preco_max, quartos_min, banheiros_min, vagas_min, self.entry_bairros_interesse.get(), self.combo_finalidade.get())
        try:
            self.db.execute_query(query, params); messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!"); self.populate_treeview(); self.clear_fields()
        except Exception as e: messagebox.showerror("Erro de Banco de Dados", f"Não foi possível adicionar o cliente:\n{e}")

    def update_client(self):
        selected_item = self.tree.focus()
        if not selected_item: messagebox.showwarning("Seleção Necessária", "Por favor, selecione um cliente para atualizar."); return
        client_id = self.tree.item(selected_item, 'values')[0]
        try:
            preco_min = float(self.entry_preco_min.get()) if self.entry_preco_min.get() else None
            preco_max = float(self.entry_preco_max.get()) if self.entry_preco_max.get() else None
            quartos_min = int(self.entry_quartos_min.get()) if self.entry_quartos_min.get() else None
            banheiros_min = int(self.entry_banheiros_min.get()) if self.entry_banheiros_min.get() else None
            vagas_min = int(self.entry_vagas_min.get()) if self.entry_vagas_min.get() else None
        except ValueError: messagebox.showerror("Erro de Validação", "Os campos de preço e características devem ser números válidos."); return
        query = """UPDATE clientes SET nome_completo=?, status=?, telefone=?, email=?, proximo_contato=?, tipo_negocio_interesse=?, tipo_imovel_interesse=?, preco_min_interesse=?, preco_max_interesse=?, quartos_min_interesse=?, banheiros_min_interesse=?, vagas_min_interesse=?, bairros_interesse=?, finalidade=? WHERE id=?"""
        params = (self.entry_nome.get(), self.combo_status.get(), self.entry_telefone.get(), self.entry_email.get(), self.entry_prox_contato.get(), self.combo_negocio_interesse.get(), self.combo_tipo_interesse.get(), preco_min, preco_max, quartos_min, banheiros_min, vagas_min, self.entry_bairros_interesse.get(), self.combo_finalidade.get(), client_id)
        try:
            self.db.execute_query(query, params); messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!"); self.populate_treeview(); self.clear_fields()
        except Exception as e: messagebox.showerror("Erro de Banco de Dados", f"Não foi possível atualizar o cliente:\n{e}")

    def clear_fields(self, clear_selection=True):
        self.entry_nome.delete(0, 'end'); self.entry_telefone.delete(0, 'end'); self.entry_email.delete(0, 'end'); self.combo_status.set(""); self.entry_prox_contato.delete(0, 'end'); self.combo_tipo_interesse.set(""); self.entry_preco_min.delete(0, 'end'); self.entry_preco_max.delete(0, 'end'); self.entry_quartos_min.delete(0, 'end'); self.entry_banheiros_min.delete(0, 'end'); self.entry_vagas_min.delete(0, 'end'); self.entry_bairros_interesse.delete(0, 'end'); self.combo_finalidade.set(""); self.combo_negocio_interesse.set("Comprar")
        if clear_selection and self.tree.focus(): self.tree.selection_remove(self.tree.focus())

    def update_button_states(self):
        if self.app.is_activated:
            self.btn_add.configure(state="normal", text="Adicionar Cliente"); self.btn_update.configure(state="normal"); self.btn_delete.configure(state="normal"); self.btn_match.configure(state="normal")
        else:
            self.btn_add.configure(state="disabled", text="Adicionar (Requer Ativação)"); self.btn_update.configure(state="disabled"); self.btn_delete.configure(state="disabled"); self.btn_match.configure(state="disabled")
    
    def delete_client(self):
        selected_item = self.tree.focus()
        if not selected_item: messagebox.showwarning("Seleção Necessária", "Por favor, selecione um cliente na tabela para deletar."); return
        if messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja deletar este cliente? Todas as interações relacionadas também serão excluídas permanentemente."):
            client_id = self.tree.item(selected_item, 'values')[0]
            try:
                self.db.execute_query("DELETE FROM clientes WHERE id=?", (client_id,)); messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!"); self.populate_treeview(); self.clear_fields()
            except Exception as e: messagebox.showerror("Erro de Banco de Dados", f"Não foi possível deletar o cliente:\n{e}")

    def get_all_clients_for_combobox(self):
        query = "SELECT id, nome_completo FROM clientes ORDER BY nome_completo"
        clients = self.db.fetch_query(query)
        return [f"{client[0]}: {client[1]}" for client in clients] if clients else []

    def select_client_by_id(self, client_id_to_select):
        self.populate_treeview()
        for item_id in self.tree.get_children():
            item_values = self.tree.item(item_id, 'values')
            if item_values and int(item_values[0]) == client_id_to_select:
                self.tree.selection_set(()); self.tree.selection_set(item_id); self.tree.focus(item_id); self.tree.see(item_id); self.on_item_select(None); return

    def find_matching_properties(self):
        selected_item = self.tree.focus()
        if not selected_item: messagebox.showwarning("Seleção Necessária", "Por favor, selecione um cliente na tabela para buscar imóveis."); return
        client_id = self.tree.item(selected_item, 'values')[0]
        query_client_profile = """SELECT tipo_negocio_interesse, tipo_imovel_interesse, preco_min_interesse, preco_max_interesse, quartos_min_interesse, banheiros_min_interesse, vagas_min_interesse FROM clientes WHERE id = ?"""
        profile = self.db.fetch_query(query_client_profile, (client_id,))
        if not profile: messagebox.showerror("Erro", "Não foi possível encontrar o perfil do cliente selecionado."); return
        
        p_negocio, p_tipo, p_preco_min, p_preco_max, p_quartos, p_banheiros, p_vagas = profile[0]

        if not p_negocio: messagebox.showwarning("Perfil Incompleto", "Defina o 'Interesse Principal' (Comprar ou Alugar) para este cliente antes de buscar."); return

        # Busca Ampla
        query = "SELECT codigo_ref, tipo, bairro, quartos, banheiros, vagas, preco_venda, preco_aluguel FROM imoveis WHERE status = 'Disponível'"
        params = []
        
        if p_negocio == "Comprar":
            query += " AND (tipo_negocio = 'Venda' OR tipo_negocio = 'Venda e Aluguel')"
            if p_preco_min is not None: query += " AND preco_venda >= ?"; params.append(p_preco_min)
            if p_preco_max is not None: query += " AND preco_venda <= ?"; params.append(p_preco_max)
        elif p_negocio == "Alugar":
            query += " AND (tipo_negocio = 'Aluguel' OR tipo_negocio = 'Venda e Aluguel')"
            if p_preco_max is not None: query += " AND preco_aluguel <= ?"; params.append(p_preco_max)

        candidate_properties = self.db.fetch_query(query, tuple(params))
        
        # Pontuação e Ranking
        scored_results = []
        for prop in candidate_properties:
            codigo, tipo, bairro, quartos, banheiros, vagas, p_venda, p_aluguel = prop
            score = 0
            # Pontuação por tipo de imóvel
            if p_tipo and tipo == p_tipo: score += 50
            # Pontuação por quartos
            if p_quartos and quartos is not None and quartos >= p_quartos: score += 25
            # Pontuação por banheiros
            if p_banheiros and banheiros is not None and banheiros >= p_banheiros: score += 15
            # Pontuação por vagas
            if p_vagas and vagas is not None and vagas >= p_vagas: score += 10
            
            valor_display = p_venda if p_negocio == "Comprar" else p_aluguel
            formatted_price = f"{valor_display:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if valor_display is not None else "N/A"
            
            scored_results.append([codigo, tipo, bairro, quartos, banheiros, vagas, formatted_price, f"{score}%"])

        scored_results.sort(key=lambda x: int(x[7].strip('%')), reverse=True)

        # Exibe os resultados
        columns = {"Código Ref.": 100, "Tipo": 100, "Bairro": 150, "Quartos": 60, "Banheiros": 70, "Vagas": 60, "Preço (R$)": 110, "Compatibilidade": 100}
        MatchResultsWindow(master=self.app, title=f"Matchmaking para: {self.entry_nome.get()}", results=scored_results, columns=columns)
