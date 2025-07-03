import customtkinter as ctk
from datetime import datetime, timedelta

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, db, app_ref):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        self.app = app_ref # Referência à janela principal para navegação

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Linha da agenda vai expandir

        # --- Frame para os Cartões de KPI ---
        kpi_frame = ctk.CTkFrame(self)
        kpi_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        kpi_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.card_total_clientes = self.create_kpi_card(kpi_frame, "Total de Clientes", "0")
        self.card_total_clientes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.card_negociacao = self.create_kpi_card(kpi_frame, "Clientes em Negociação", "0")
        self.card_negociacao.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.card_imoveis = self.create_kpi_card(kpi_frame, "Imóveis Disponíveis", "0")
        self.card_imoveis.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.total_clientes_value = self.card_total_clientes.winfo_children()[1]
        self.negociacao_value = self.card_negociacao.winfo_children()[1]
        self.imoveis_value = self.card_imoveis.winfo_children()[1]

        # --- Frame para a Agenda de Follow-up ---
        agenda_frame = ctk.CTkFrame(self)
        agenda_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        agenda_frame.grid_rowconfigure(1, weight=1)
        agenda_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(agenda_frame, text="Agenda de Hoje (Follow-ups)", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, padx=20, pady=(10,5), sticky="w")
        
        self.agenda_scrollable_frame = ctk.CTkScrollableFrame(agenda_frame, label_text="")
        self.agenda_scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.agenda_scrollable_frame.grid_columnconfigure(0, weight=1)

    def create_kpi_card(self, parent, title, value):
        """
        Função auxiliar para criar um cartão de KPI padronizado.
        
        :param parent: O frame pai onde o cartão será colocado.
        :param title: O título do indicador.
        :param value: O valor inicial do indicador.
        :return: O frame do cartão criado.
        """
        card_frame = ctk.CTkFrame(parent, corner_radius=10)
        card_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(card_frame, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        value_label = ctk.CTkLabel(card_frame, text=value, font=ctk.CTkFont(size=36, weight="bold"), text_color="#3484F0")
        value_label.grid(row=1, column=0, padx=20, pady=(10, 20))

        return card_frame

    def update_stats(self):
        """Atualiza os KPIs e a lista de follow-ups."""
        try:
            total_clientes = self.db.fetch_query("SELECT COUNT(*) FROM clientes")[0][0]
            self.total_clientes_value.configure(text=str(total_clientes))
            negociacao = self.db.fetch_query("SELECT COUNT(*) FROM clientes WHERE status = 'Em Negociação'")[0][0]
            self.negociacao_value.configure(text=str(negociacao))
            imoveis = self.db.fetch_query("SELECT COUNT(*) FROM imoveis WHERE status = 'Disponível'")[0][0]
            self.imoveis_value.configure(text=str(imoveis))
        except Exception as e:
            print(f"Erro ao atualizar KPIs: {e}")

        # Atualiza a agenda de follow-up
        # Limpa a lista antiga
        for widget in self.agenda_scrollable_frame.winfo_children():
            widget.destroy()

        try:
            # Busca clientes com contato para hoje ou atrasado
            hoje_str = datetime.now().strftime("%d/%m/%Y")
            query = "SELECT id, nome_completo, proximo_contato FROM clientes WHERE proximo_contato != '' AND proximo_contato <= ? ORDER BY proximo_contato"
            
            tasks = self.db.fetch_query(query, (hoje_str,))

            if not tasks:
                ctk.CTkLabel(self.agenda_scrollable_frame, text="Nenhum follow-up para hoje. Bom trabalho!").pack(pady=10)
                return

            for i, task in enumerate(tasks):
                client_id, nome, data_contato = task
                
                task_frame = ctk.CTkFrame(self.agenda_scrollable_frame, fg_color=("gray85", "gray20"))
                task_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
                task_frame.grid_columnconfigure(1, weight=1)
                
                label_text = f"Falar com: {nome} (Agendado para: {data_contato})"
                ctk.CTkLabel(task_frame, text=label_text).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
                
                # Botão que chama a navegação
                view_button = ctk.CTkButton(task_frame, text="Ver Ficha", width=100,
                                            command=lambda c_id=client_id: self.app.navigate_to_client(c_id))
                view_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        except Exception as e:
            print(f"Erro ao atualizar agenda: {e}")
            ctk.CTkLabel(self.agenda_scrollable_frame, text="Erro ao carregar a agenda.").pack(pady=10)

