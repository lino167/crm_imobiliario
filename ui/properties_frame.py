import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3

class PropertiesFrame(ctk.CTkFrame):
    """
    Frame que contém a interface e a lógica para o gerenciamento de imóveis.
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
        # Linha 1: Dados Principais
        ctk.CTkLabel(self.form_frame, text="Código Ref.:").grid(row=0, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_codigo = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: APTO-123")
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Preço (R$):").grid(row=0, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_preco = ctk.CTkEntry(self.form_frame, placeholder_text="500000.00")
        self.entry_preco.grid(row=0, column=3, padx=(5,10), pady=5, sticky="ew")

        # Linha 2: Endereço
        ctk.CTkLabel(self.form_frame, text="Rua:").grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_rua = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: Rua das Palmeiras")
        self.entry_rua.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Número:").grid(row=1, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_numero = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: 123")
        self.entry_numero.grid(row=1, column=3, padx=(5,10), pady=5, sticky="ew")

        # Linha 3: Endereço
        ctk.CTkLabel(self.form_frame, text="Bairro:").grid(row=2, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_bairro = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: Vila Nova")
        self.entry_bairro.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Cidade:").grid(row=2, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_cidade = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: Blumenau")
        self.entry_cidade.grid(row=2, column=3, padx=(5,10), pady=5, sticky="ew")

        # Linha 4: Características
        ctk.CTkLabel(self.form_frame, text="Tipo:").grid(row=3, column=0, padx=(10,5), pady=5, sticky="w")
        self.combo_tipo = ctk.CTkComboBox(self.form_frame, values=["Apartamento", "Casa", "Sobrado", "Terreno", "Comercial"])
        self.combo_tipo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Quartos:").grid(row=3, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_quartos = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: 3")
        self.entry_quartos.grid(row=3, column=3, padx=(5,10), pady=5, sticky="ew")

        # Linha 5: Características
        ctk.CTkLabel(self.form_frame, text="Banheiros:").grid(row=4, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_banheiros = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: 2")
        self.entry_banheiros.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        # --- MUDANÇA AQUI: Adicionado o campo de Vagas de Garagem ---
        ctk.CTkLabel(self.form_frame, text="Vagas Garagem:").grid(row=4, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_vagas = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: 2")
        self.entry_vagas.grid(row=4, column=3, padx=(5,10), pady=5, sticky="ew")

        # --- Frame de Botões ---
        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.btn_add = ctk.CTkButton(self.button_frame, text="Adicionar Imóvel", command=self.add_property)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_update = ctk.CTkButton(self.button_frame, text="Atualizar Selecionado", command=self.update_property)
        self.btn_update.grid(row=0, column=1, padx=5, pady=5)

        self.btn_delete = ctk.CTkButton(self.button_frame, text="Deletar Selecionado", command=self.delete_property, fg_color="#D32F2F", hover_color="#B71C1C")
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

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Código", "Tipo", "Bairro", "Quartos", "Preço"), show='headings')
        self.tree.heading("ID", text="ID"); self.tree.heading("Código", text="Código Ref."); self.tree.heading("Tipo", text="Tipo"); self.tree.heading("Bairro", text="Bairro"); self.tree.heading("Quartos", text="Quartos"); self.tree.heading("Preço", text="Preço (R$)")
        self.tree.column("ID", width=50, anchor="center"); self.tree.column("Código", width=120); self.tree.column("Tipo", width=120); self.tree.column("Bairro", width=200); self.tree.column("Quartos", width=80, anchor="center"); self.tree.column("Preço", width=120, anchor="e")

        self.tree.grid(row=0, column=0, sticky="nswe")
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        
        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def populate_treeview(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        query = "SELECT id, codigo_ref, tipo, bairro, quartos, preco_venda FROM imoveis ORDER BY codigo_ref"
        for row in self.db.fetch_query(query):
            preco_formatado = f"{row[5]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if row[5] is not None else "0,00"
            values = row[:5] + (preco_formatado,)
            self.tree.insert("", "end", values=values)

    def on_item_select(self, event):
        selected_item = self.tree.focus()
        if not selected_item: return
        property_id = self.tree.item(selected_item, 'values')[0]
        query = "SELECT * FROM imoveis WHERE id = ?"
        property_data = self.db.fetch_query(query, (property_id,))
        if property_data:
            data = property_data[0]
            self.clear_fields(clear_selection=False)
            self.entry_codigo.insert(0, data[1]); self.entry_rua.insert(0, data[2] or ""); self.entry_numero.insert(0, data[3] or ""); self.entry_bairro.insert(0, data[4] or ""); self.entry_cidade.insert(0, data[5] or ""); self.combo_tipo.set(data[6] or ""); self.entry_quartos.insert(0, str(data[7] or "")); self.entry_banheiros.insert(0, str(data[9] or "")); self.entry_vagas.insert(0, str(data[10] or "")); self.entry_preco.insert(0, str(data[12] or ""))

    def add_property(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo: messagebox.showerror("Erro de Validação", "O campo 'Código Ref.' é obrigatório."); return
        try:
            quartos = int(self.entry_quartos.get()) if self.entry_quartos.get() else None
            banheiros = int(self.entry_banheiros.get()) if self.entry_banheiros.get() else None
            vagas = int(self.entry_vagas.get()) if self.entry_vagas.get() else None
            preco = float(self.entry_preco.get()) if self.entry_preco.get() else 0.0
        except ValueError: messagebox.showerror("Erro de Validação", "Os campos de preço, quartos, banheiros e vagas devem ser números válidos."); return
        query = "INSERT INTO imoveis (codigo_ref, rua, numero, bairro, cidade, tipo, quartos, banheiros, vagas, preco_venda, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        params = (codigo, self.entry_rua.get(), self.entry_numero.get(), self.entry_bairro.get(), self.entry_cidade.get(), self.combo_tipo.get(), quartos, banheiros, vagas, preco, "Disponível")
        try:
            self.db.execute_query(query, params); messagebox.showinfo("Sucesso", "Imóvel adicionado com sucesso!"); self.populate_treeview(); self.clear_fields()
        except sqlite3.IntegrityError: messagebox.showerror("Erro de Duplicidade", f"O Código de Referência '{codigo}' já existe no banco de dados.")
        except Exception as e: messagebox.showerror("Erro de Banco de Dados", f"Não foi possível adicionar o imóvel:\n{e}")

    def update_property(self):
        selected_item = self.tree.focus()
        if not selected_item: messagebox.showwarning("Seleção Necessária", "Selecione um imóvel na tabela para atualizar."); return
        try:
            quartos = int(self.entry_quartos.get()) if self.entry_quartos.get() else None
            banheiros = int(self.entry_banheiros.get()) if self.entry_banheiros.get() else None
            vagas = int(self.entry_vagas.get()) if self.entry_vagas.get() else None
            preco = float(self.entry_preco.get()) if self.entry_preco.get() else 0.0
        except ValueError: messagebox.showerror("Erro de Validação", "Os campos de preço, quartos, banheiros e vagas devem ser números válidos."); return
        property_id = self.tree.item(selected_item, 'values')[0]
        query = "UPDATE imoveis SET codigo_ref=?, rua=?, numero=?, bairro=?, cidade=?, tipo=?, quartos=?, banheiros=?, vagas=?, preco_venda=? WHERE id=?"
        params = (self.entry_codigo.get(), self.entry_rua.get(), self.entry_numero.get(), self.entry_bairro.get(), self.entry_cidade.get(), self.combo_tipo.get(), quartos, banheiros, vagas, preco, property_id)
        try:
            self.db.execute_query(query, params); messagebox.showinfo("Sucesso", "Imóvel atualizado com sucesso!"); self.populate_treeview(); self.clear_fields()
        except sqlite3.IntegrityError: messagebox.showerror("Erro de Duplicidade", "O Código de Referência inserido já pertence a outro imóvel.")
        except Exception as e: messagebox.showerror("Erro de Banco de Dados", f"Não foi possível atualizar o imóvel:\n{e}")

    def delete_property(self):
        selected_item = self.tree.focus()
        if not selected_item: messagebox.showwarning("Seleção Necessária", "Selecione um imóvel para deletar."); return
        if messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja deletar este imóvel?"):
            property_id = self.tree.item(selected_item, 'values')[0]
            try:
                self.db.execute_query("DELETE FROM imoveis WHERE id=?", (property_id,)); messagebox.showinfo("Sucesso", "Imóvel deletado com sucesso!"); self.populate_treeview(); self.clear_fields()
            except Exception as e: messagebox.showerror("Erro", f"Não foi possível deletar o imóvel:\n{e}")

    def clear_fields(self, clear_selection=True):
        self.entry_codigo.delete(0, 'end'); self.entry_rua.delete(0, 'end'); self.entry_numero.delete(0, 'end'); self.entry_bairro.delete(0, 'end'); self.entry_cidade.delete(0, 'end'); self.entry_preco.delete(0, 'end'); self.combo_tipo.set(""); self.entry_quartos.delete(0, 'end'); self.entry_banheiros.delete(0, 'end'); self.entry_vagas.delete(0, 'end')
        if clear_selection and self.tree.focus(): self.tree.selection_remove(self.tree.focus())

    def update_button_states(self):
        if self.app.is_activated:
            self.btn_add.configure(state="normal", text="Adicionar Imóvel"); self.btn_update.configure(state="normal"); self.btn_delete.configure(state="normal")
        else:
            self.btn_add.configure(state="disabled", text="Adicionar (Requer Ativação)"); self.btn_update.configure(state="disabled"); self.btn_delete.configure(state="disabled")
