import customtkinter as ctk
import license_manager
from ui import DashboardFrame, ClientsFrame, PropertiesFrame, InteractionsFrame, LicenseFrame

class App(ctk.CTk):
    """
    Classe principal da aplicação. Herda de ctk.CTk para criar a janela.
    Responsável por montar a estrutura da UI e gerenciar a navegação.
    """
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.is_activated = license_manager.check_license()

        self.title("CRM Imobiliário Pro")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Frame de Navegação ---
        self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nswe")
        self.nav_frame.grid_rowconfigure(5, weight=1) 

        self.logo_label = ctk.CTkLabel(self.nav_frame, text="CRM Pro", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_dashboard = ctk.CTkButton(self.nav_frame, text="Dashboard", command=self.show_dashboard_frame)
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_clientes = ctk.CTkButton(self.nav_frame, text="Clientes", command=self.show_clients_frame)
        self.btn_clientes.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_imoveis = ctk.CTkButton(self.nav_frame, text="Imóveis", command=self.show_properties_frame)
        self.btn_imoveis.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_interacoes = ctk.CTkButton(self.nav_frame, text="Interações", command=self.show_interactions_frame)
        self.btn_interacoes.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.btn_license = ctk.CTkButton(self.nav_frame, text="Licença e Ativação", command=self.show_license_frame)
        self.btn_license.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        # --- Frame de Conteúdo ---
        self.content_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#2B2B2B")
        self.content_frame.grid(row=0, column=1, sticky="nswe", padx=(10, 20), pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # --- Inicialização dos Frames ---
        self.dashboard_frame = DashboardFrame(self.content_frame, self.db, self)
        self.clients_frame = ClientsFrame(self.content_frame, self.db, self)
        self.properties_frame = PropertiesFrame(self.content_frame, self.db, self)
        self.interactions_frame = InteractionsFrame(self.content_frame, self.db, self.clients_frame)
        self.license_frame = LicenseFrame(self.content_frame, on_activation_success=self.on_activation_success)

        self.show_dashboard_frame()

    def on_activation_success(self):
        """
        Callback chamado pela tela de licença após uma ativação bem-sucedida.
        """
        self.is_activated = True
        self.clients_frame.update_button_states()
        self.properties_frame.update_button_states()

    def show_frame(self, frame_to_show):
        """
        Esconde todos os frames e mostra apenas o selecionado.
        """
        for frame in (self.dashboard_frame, self.clients_frame, self.properties_frame, self.interactions_frame, self.license_frame):
            frame.grid_forget()
        frame_to_show.grid(row=0, column=0, sticky="nswe")

    def show_dashboard_frame(self):
        self.dashboard_frame.update_stats()
        self.show_frame(self.dashboard_frame)

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

    def show_license_frame(self):
        self.license_frame.check_and_display_status()
        self.show_frame(self.license_frame)

    def navigate_to_client(self, client_id):
        """
        Navega para a tela de clientes e seleciona um cliente específico.
        Chamado pelo botão 'Ver Ficha' do dashboard.
        """
        print(f"Navegando para o cliente com ID: {client_id}")
        # Primeiro, muda para a tela de clientes
        self.show_frame(self.clients_frame)
        # Depois, chama a função para selecionar o cliente na tabela
        self.clients_frame.select_client_by_id(client_id)
