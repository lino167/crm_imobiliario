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

        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.form_frame.grid_columnconfigure((1, 3), weight=1)
        ctk.CTkLabel(self.form_frame, text="Código Ref.:").grid(row=0, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_codigo = ctk.CTkEntry(self.form_frame, placeholder_text="Ex: APTO-123")
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(self.form_frame, text="Tipo:").grid(row=0, column=2, padx=(10,5), pady=5, sticky="w")
        self.combo_tipo = ctk.CTkComboBox(self.form_frame, values=["Apartamento", "Casa", "Terreno", "Comercial"])
        self.combo_tipo.grid(row=0, column=3, padx=(5,10), pady=5, sticky="ew")
        ctk.CTkLabel(self.form_frame, text="Endereço:").grid(row=1, column=0, padx=(10,5), pady=5, sticky="w")
        self.entry_endereco = ctk.CTkEntry(self.form_frame, placeholder_text="Rua, Número, Bairro")
        self.entry_endereco.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(self.form_frame, text="Preço (R$):").grid(row=1, column=2, padx=(10,5), pady=5, sticky="w")
        self.entry_preco = ctk.CTkEntry(self.form_frame, placeholder_text="500000.00")
        self.entry_preco.grid(row=1, column=3, padx=(5,10), pady=5, sticky="ew")

        self.button_frame = ctk.CTkFrame(self.form_frame)
        self.button_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.btn_add = ctk.CTkButton(self.button_frame, text="Adicionar Imóvel", command=self.add_property)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5)
        self.btn_update = ctk.CTkButton(self.button_frame, text="Atualizar Selecionado", command=self.update_property)
        self.btn_update.grid(row=0, column=1, padx=5, pady=5)
        self.btn_delete = ctk.CTkButton(self.button_frame, text="Deletar Selecionado", command=self.delete_property, fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)
        self.btn_clear = ctk.CTkButton(self.button_frame, text="Limpar Campos", command=self.clear_fields, fg_color="gray50", hover_color="gray30")
        self.btn_clear.grid(row=0, column=3, padx=5, pady=5)

        self.setup_treeview()
        self.populate_treeview()
        
        self.update_button_states()

    def update_button_states(self):
        """Ativa ou desativa os botões baseando-se no status da licença."""
        if self.app.is_activated:
            self.btn_add.configure(state="normal", text="Adicionar Imóvel")
            self.btn_update.configure(state="normal")
            self.btn_delete.configure(state="normal")
        else:
            self.btn_add.configure(state="disabled", text="Adicionar (Requer Ativação)")
            self.btn_update.configure(state="disabled")
            self.btn_delete.configure(state="disabled")

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
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Código", "Tipo", "Endereço", "Preço"), show='headings')
        self.tree.heading("ID", text="ID"); self.tree.heading("Código", text="Código Ref."); self.tree.heading("Tipo", text="Tipo"); self.tree.heading("Endereço", text="Endereço"); self.tree.heading("Preço", text="Preço (R$)")
        self.tree.column("ID", width=50, anchor="center"); self.tree.column("Código", width=150); self.tree.column("Tipo", width=150); self.tree.column("Endereço", width=350); self.tree.column("Preço", width=150, anchor="e")
        self.tree.grid(row=0, column=0, sticky="nswe")
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def populate_treeview(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        query = "SELECT id, codigo_ref, tipo, endereco, preco_venda FROM imoveis ORDER BY codigo_ref"
        for row in self.db.fetch_query(query):
            preco_formatado = f"{row[4]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if row[4] else "0,00"
            values = row[:4] + (preco_formatado,)
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
            self.entry_codigo.insert(0, data[1]); self.entry_endereco.insert(0, data[2]); self.combo_tipo.set(data[4] or ""); self.entry_preco.insert(0, str(data[9] or ""))

    def add_property(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo: messagebox.showerror("Erro de Validação", "O campo 'Código Ref.' é obrigatório."); return
        try:
            preco = float(self.entry_preco.get()) if self.entry_preco.get() else 0.0
        except ValueError: messagebox.showerror("Erro de Validação", "O campo 'Preço' deve ser um número válido."); return
        query = "INSERT INTO imoveis (codigo_ref, endereco, tipo, preco_venda, status) VALUES (?, ?, ?, ?, ?)"
        params = (codigo, self.entry_endereco.get(), self.combo_tipo.get(), preco, "Disponível")
        try:
            self.db.execute_query(query, params); messagebox.showinfo("Sucesso", "Imóvel adicionado com sucesso!"); self.populate_treeview(); self.clear_fields()
        except sqlite3.IntegrityError: messagebox.showerror("Erro de Duplicidade", f"O Código de Referência '{codigo}' já existe no banco de dados.")
        except Exception as e: messagebox.showerror("Erro de Banco de Dados", f"Não foi possível adicionar o imóvel:\n{e}")

    def update_property(self):
        selected_item = self.tree.focus()
        if not selected_item: messagebox.showwarning("Seleção Necessária", "Selecione um imóvel na tabela para atualizar."); return
        try:
            preco = float(self.entry_preco.get()) if self.entry_preco.get() else 0.0
        except ValueError: messagebox.showerror("Erro de Validação", "O campo 'Preço' deve ser um número válido."); return
        property_id = self.tree.item(selected_item, 'values')[0]
        query = "UPDATE imoveis SET codigo_ref=?, endereco=?, tipo=?, preco_venda=? WHERE id=?"
        params = (self.entry_codigo.get(), self.entry_endereco.get(), self.combo_tipo.get(), preco, property_id)
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
        self.entry_codigo.delete(0, 'end'); self.entry_endereco.delete(0, 'end'); self.entry_preco.delete(0, 'end'); self.combo_tipo.set("")
        if clear_selection and self.tree.focus(): self.tree.selection_remove(self.tree.focus())

