import customtkinter as ctk
from tkinter import ttk

class MatchResultsWindow(ctk.CTkToplevel):
    """
    Uma janela Toplevel (pop-up) para exibir os resultados de uma busca
    de matchmaking, como uma lista de imóveis compatíveis.
    """
    def __init__(self, master, title, results, columns):
        super().__init__(master)
        
        self.title(title)
        self.geometry("800x400")
        
        # Faz com que esta janela fique em foco e bloqueie a de trás
        self.transient(master)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        if not results:
            label = ctk.CTkLabel(self, text="Nenhum resultado compatível encontrado.", font=ctk.CTkFont(size=16))
            label.pack(pady=50)
            return

        # --- Tabela (Treeview) para exibir os resultados ---
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Configura o estilo da tabela
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=('Calibri', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        # Cria a tabela com as colunas fornecidas
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Define os cabeçalhos e o tamanho das colunas
        for col_name, width in columns.items():
            self.tree.heading(col_name, text=col_name)
            self.tree.column(col_name, width=width, anchor="w")

        self.tree.grid(row=0, column=0, sticky="nswe")
        
        # Adiciona os resultados na tabela
        for row in results:
            self.tree.insert("", "end", values=row)
            
        # Adiciona a barra de rolagem
        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)
