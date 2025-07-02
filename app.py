import customtkinter as ctk


class PlaceholderFrame(ctk.CTkFrame):
    """Um frame genérico para marcar o lugar das futuras telas."""
    def __init__(self, parent, title):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        label = ctk.CTkLabel(self, text=f"Área de {title}",
                               font=ctk.CTkFont(size=24, weight="bold"))
        label.grid(row=0, column=0, padx=20, pady=20)

# --- Classe Principal da Aplicação ---

class App(ctk.CTk):
    """
    Classe principal da aplicação. Herda de ctk.CTk para criar a janela.
    Responsável por montar a estrutura da UI: menu lateral e área de conteúdo.
    """
    def __init__(self, db):
        super().__init__()
        self.db = db # Armazena a instância do banco de dados

        # --- Configuração da Janela Principal ---
        self.title("CRM Imobiliário Pro")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # --- Layout Principal com Grid (1 linha, 2 colunas) ---
        # A coluna 0 (menu) tem largura fixa, a coluna 1 (conteúdo) se expande.
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Frame de Navegação (Menu Lateral) ---
        self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nswe")
        self.nav_frame.grid_rowconfigure(4, weight=1) # Espaçador para empurrar o botão de tema para baixo

        self.logo_label = ctk.CTkLabel(self.nav_frame, text="CRM Pro",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botões de navegação
        self.btn_clientes = ctk.CTkButton(self.nav_frame, text="Clientes", command=self.show_clients_frame)
        self.btn_clientes.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_imoveis = ctk.CTkButton(self.nav_frame, text="Imóveis", command=self.show_properties_frame)
        self.btn_imoveis.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_interacoes = ctk.CTkButton(self.nav_frame, text="Interações", command=self.show_interactions_frame)
        self.btn_interacoes.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # --- Frame de Conteúdo Principal ---
        self.content_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#2B2B2B")
        self.content_frame.grid(row=0, column=1, sticky="nswe", padx=(10, 20), pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # --- Inicialização dos Frames de Conteúdo ---
        self.clients_frame = PlaceholderFrame(self.content_frame, "Gerenciamento de Clientes")
        self.properties_frame = PlaceholderFrame(self.content_frame, "Gerenciamento de Imóveis")
        self.interactions_frame = PlaceholderFrame(self.content_frame, "Registro de Interações")

        # --- Exibir o frame inicial ---
        self.show_clients_frame()

    def show_frame(self, frame_to_show):
        """Esconde todos os frames e mostra apenas o selecionado."""
        self.clients_frame.grid_forget()
        self.properties_frame.grid_forget()
        self.interactions_frame.grid_forget()
        frame_to_show.grid(row=0, column=0, sticky="nswe")

    def show_clients_frame(self):
        """Callback para o botão 'Clientes'."""
        self.show_frame(self.clients_frame)

    def show_properties_frame(self):
        """Callback para o botão 'Imóveis'."""
        self.show_frame(self.properties_frame)
        
    def show_interactions_frame(self):
        """Callback para o botão 'Interações'."""
        self.show_frame(self.interactions_frame)

