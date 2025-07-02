import customtkinter as ctk
from ui import ClientsFrame, PropertiesFrame, InteractionsFrame

#vamos mantê-la caso queira adicionar novas telas no futuro.
class PlaceholderFrame(ctk.CTkFrame):
        def __init__(self, parent, title):
            super().__init__(parent, fg_color="transparent")
            label = ctk.CTkLabel(self, text=f"Área de {title}", font=ctk.CTkFont(size=24, weight="bold"))
            label.pack(pady=100)

# --- Classe Principal da Aplicação ---
class App(ctk.CTk):
        def __init__(self, db):
            super().__init__()
            self.db = db
            self.title("CRM Imobiliário Pro")
            self.geometry("1200x700")
            self.minsize(1000, 600)

            # ... (Navegação e Grid - NENHUMA MUDANÇA AQUI) ...
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
            self.nav_frame.grid(row=0, column=0, sticky="nswe")
            self.nav_frame.grid_rowconfigure(4, weight=1)
            self.logo_label = ctk.CTkLabel(self.nav_frame, text="CRM Pro", font=ctk.CTkFont(size=20, weight="bold"))
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            self.btn_clientes = ctk.CTkButton(self.nav_frame, text="Clientes", command=self.show_clients_frame)
            self.btn_clientes.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
            self.btn_imoveis = ctk.CTkButton(self.nav_frame, text="Imóveis", command=self.show_properties_frame)
            self.btn_imoveis.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
            self.btn_interacoes = ctk.CTkButton(self.nav_frame, text="Interações", command=self.show_interactions_frame)
            self.btn_interacoes.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
            self.content_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#2B2B2B")
            self.content_frame.grid(row=0, column=1, sticky="nswe", padx=(10, 20), pady=20)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure(0, weight=1)

            # --- Inicialização dos Frames de Conteúdo (AQUI ESTÁ A MUDANÇA) ---
            self.clients_frame = ClientsFrame(self.content_frame, self.db)
            self.properties_frame = PropertiesFrame(self.content_frame, self.db)
            # Passamos a referência de clients_frame para interactions_frame
            self.interactions_frame = InteractionsFrame(self.content_frame, self.db, self.clients_frame)

            # Exibir o frame inicial
            self.show_clients_frame()

        def show_frame(self, frame_to_show):
            for frame in (self.clients_frame, self.properties_frame, self.interactions_frame):
                frame.grid_forget()
            frame_to_show.grid(row=0, column=0, sticky="nswe")

        def show_clients_frame(self):
            self.clients_frame.populate_treeview()
            self.show_frame(self.clients_frame)

        def show_properties_frame(self):
            self.properties_frame.populate_treeview()
            self.show_frame(self.properties_frame)
            
        def show_interactions_frame(self):
            self.interactions_frame.update_client_list()
            self.interactions_frame.populate_treeview()
            self.show_frame(self.interactions_frame)
    