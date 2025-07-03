import sqlite3
import os

class Database:
    def __init__(self, db_name="crm_imobiliario.db"):
        self.db_name = db_name
        self.conn = None
        try:
            self.connect()
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Erro CRÍTICO na inicialização do banco de dados: {e}")

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        print("Conexão com o banco de dados estabelecida com sucesso.")

    def create_tables(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_cadastro TEXT NOT NULL,
                nome_completo TEXT NOT NULL,
                status TEXT,
                fonte TEXT,
                telefone TEXT,
                email TEXT,
                proximo_contato TEXT,
                observacoes TEXT,
                
                -- Perfil de Busca Detalhado --
                tipo_negocio_interesse TEXT, -- 'Comprar' ou 'Alugar'
                tipo_imovel_interesse TEXT,
                preco_min_interesse REAL,
                preco_max_interesse REAL,
                quartos_min_interesse INTEGER,
                banheiros_min_interesse INTEGER,
                vagas_min_interesse INTEGER,
                bairros_interesse TEXT,
                finalidade TEXT, 
                urgencia TEXT, 
                caracteristicas_desejadas TEXT
            )
            """)

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS imoveis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_ref TEXT UNIQUE NOT NULL,
                rua TEXT, numero TEXT, bairro TEXT, cidade TEXT,
                tipo TEXT, quartos INTEGER, suites INTEGER, banheiros INTEGER,
                vagas INTEGER, area REAL, 
                
                -- Novos campos de negócio --
                tipo_negocio TEXT, -- 'Venda', 'Aluguel', 'Venda e Aluguel'
                preco_venda REAL,
                preco_aluguel REAL,

                status TEXT, -- Status do imóvel (Disponível, Alugado, Vendido)
                link_anuncio TEXT
            )
            """)

            # Tabela de Interações
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS interacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER, data TEXT NOT NULL, tipo_interacao TEXT,
                resumo TEXT, imoveis_apresentados TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
            )
            """)
            self.conn.commit()
            print("Tabelas verificadas/criadas com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar as tabelas: {e}")

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")
            raise e

    def fetch_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar dados: {e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")
