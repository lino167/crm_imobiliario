import customtkinter as ctk
from datetime import datetime, timedelta

class DashboardFrame(ctk.CTkFrame):
    """
    Frame que exibe um dashboard com os principais indicadores de desempenho (KPIs).
    """
    def __init__(self, parent, db):
        super().__init__(parent, fg_color="transparent")
        self.db = db

        # Configura o grid para que os cartões se expandam igualmente
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # --- Criação dos Cartões de KPI ---
        self.card_total_clientes = self.create_kpi_card("Total de Clientes", "0")
        self.card_total_clientes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.card_negociacao = self.create_kpi_card("Clientes em Negociação", "0")
        self.card_negociacao.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.card_imoveis = self.create_kpi_card("Imóveis Disponíveis", "0")
        self.card_imoveis.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.card_novos_clientes = self.create_kpi_card("Novos Clientes (30d)", "0")
        self.card_novos_clientes.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.card_interacoes = self.create_kpi_card("Total de Interações", "0")
        self.card_interacoes.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Armazena as labels de valor para poder atualizá-las depois
        self.total_clientes_value = self.card_total_clientes.winfo_children()[1]
        self.negociacao_value = self.card_negociacao.winfo_children()[1]
        self.imoveis_value = self.card_imoveis.winfo_children()[1]
        self.novos_clientes_value = self.card_novos_clientes.winfo_children()[1]
        self.interacoes_value = self.card_interacoes.winfo_children()[1]

    def create_kpi_card(self, title, value):
        """
        Função auxiliar para criar um cartão de KPI padronizado.
        
        :param title: O título do indicador.
        :param value: O valor inicial do indicador.
        :return: O frame do cartão criado.
        """
        card_frame = ctk.CTkFrame(self, corner_radius=10)
        card_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(card_frame, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        value_label = ctk.CTkLabel(card_frame, text=value, font=ctk.CTkFont(size=36, weight="bold"), text_color="#3484F0")
        value_label.grid(row=1, column=0, padx=20, pady=(10, 20))

        return card_frame

    def update_stats(self):
        """
        Busca os dados mais recentes do banco de dados e atualiza os valores nos cartões.
        Este método deve ser chamado sempre que a tela do dashboard for exibida.
        """
        try:
            # 1. Total de Clientes
            total_clientes = self.db.fetch_query("SELECT COUNT(*) FROM clientes")[0][0]
            self.total_clientes_value.configure(text=str(total_clientes))

            # 2. Clientes em Negociação
            negociacao = self.db.fetch_query("SELECT COUNT(*) FROM clientes WHERE status = 'Em Negociação'")[0][0]
            self.negociacao_value.configure(text=str(negociacao))

            # 3. Imóveis Disponíveis (Adicionaremos o status 'Disponível' ao cadastrar)
            imoveis = self.db.fetch_query("SELECT COUNT(*) FROM imoveis WHERE status = 'Disponível'")[0][0]
            self.imoveis_value.configure(text=str(imoveis))

            # 4. Novos Clientes nos últimos 30 dias
            date_30_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
            novos_clientes = self.db.fetch_query("SELECT COUNT(*) FROM clientes WHERE data_cadastro >= ?", (date_30_days_ago,))[0][0]
            self.novos_clientes_value.configure(text=str(novos_clientes))

            # 5. Total de Interações
            interacoes = self.db.fetch_query("SELECT COUNT(*) FROM interacoes")[0][0]
            self.interacoes_value.configure(text=str(interacoes))

        except Exception as e:
            print(f"Erro ao atualizar as estatísticas do dashboard: {e}")
            # Você pode querer exibir uma mensagem de erro na UI aqui.
