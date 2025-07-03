import sqlite3
import os

class Database:
    """
    Classe responsável por gerenciar todas as operações com o banco de dados SQLite.
    """
    def __init__(self, db_name="crm_imobiliario.db"):
        self.db_name = db_name
        self.conn = None
        try:
            self.connect()
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Erro CRÍTICO na inicialização do banco de dados: {e}")

    def connect(self):
        """
        Estabelece a conexão com o arquivo do banco de dados SQLite.
        """
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        print("Conexão com o banco de dados estabelecida com sucesso.")

    def create_tables(self):
        """
        Cria as tabelas do sistema se elas ainda não existirem.
        """
        try:
            # --- MUDANÇA AQUI: Adicionados novos campos para o perfil de busca ---
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_cadastro TEXT NOT NULL,
                nome_completo TEXT NOT NULL,
                status TEXT,
                fonte TEXT,
                telefone TEXT,
                email TEXT,
                perfil_imovel TEXT,
                bairros_interesse TEXT,
                tipo_imovel TEXT,
                quartos_min INTEGER,
                preco_max REAL,
                proximo_contato TEXT,
                observacoes TEXT,
                
                -- Campos para Matchmaking --
                tipo_imovel_interesse TEXT,
                quartos_min_interesse INTEGER,
                preco_max_interesse REAL
            )
            """)

            # Tabela de Imóveis (sem alterações)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS imoveis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_ref TEXT UNIQUE NOT NULL,
                endereco TEXT,
                bairro TEXT,
                tipo TEXT,
                quartos INTEGER,
                suites INTEGER,
                vagas INTEGER,
                area REAL,
                preco_venda REAL,
                status TEXT,
                link_anuncio TEXT
            )
            """)

            # Tabela de Interações (sem alterações)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS interacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                data TEXT NOT NULL,
                tipo_interacao TEXT,
                resumo TEXT,
                imoveis_apresentados TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
            )
            """)
            self.conn.commit()
            print("Tabelas verificadas/criadas com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar as tabelas: {e}")

    def execute_query(self, query, params=()):
        """Executa uma query de modificação de dados (INSERT, UPDATE, DELETE)."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")
            raise e

    def fetch_query(self, query, params=()):
        """Executa uma query de busca de dados (SELECT)."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar dados: {e}")
            return []

    def close(self):
        """Fecha a conexão com o banco de dados de forma segura."""
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")
