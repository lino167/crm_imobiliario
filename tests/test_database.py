import unittest
import os
from datetime import datetime

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import Database

class TestDatabase(unittest.TestCase):
    """
    Suíte de testes para a classe Database.
    Usa um banco de dados em memória para garantir o isolamento dos testes.
    """

    def setUp(self):
        """
        Método executado ANTES de cada teste.
        Cria uma nova instância do banco de dados em memória.
        """
       
        self.db = Database(db_name=':memory:')

    def tearDown(self):
        """
        Método executado DEPOIS de cada teste.
        Fecha a conexão com o banco de dados.
        """
        self.db.close()

    def test_table_creation(self):
        """
        Testa se as tabelas 'clientes', 'imoveis' e 'interacoes' foram criadas.
        """
        print("Executando: test_table_creation")
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = self.db.fetch_query(query)
        
        table_names = [table[0] for table in tables]
        
        self.assertIn('clientes', table_names)
        self.assertIn('imoveis', table_names)
        self.assertIn('interacoes', table_names)

    def test_add_and_fetch_client(self):
        """
        Testa a inserção e a busca de um novo cliente.
        """
        print("Executando: test_add_and_fetch_client")
        data_cadastro = datetime.now().strftime("%Y-%m-%d")
        
       
        client_data = (
            data_cadastro, 'João da Silva', 'Prospect', 'Indicação', 
            '(47) 99999-8888', 'joao.silva@email.com', 'Apto 2Q', 'Centro', 
            'Apartamento', 2, 500000.00, '', 'Cliente com urgência.'
        )
        
       
        insert_query = """
        INSERT INTO clientes (data_cadastro, nome_completo, status, fonte, telefone, email, 
                              perfil_imovel, bairros_interesse, tipo_imovel, quartos_min, 
                              preco_max, proximo_contato, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
      
        client_id = self.db.execute_query(insert_query, client_data)
        self.assertIsNotNone(client_id) # Verifica se um ID foi retornado

     
        fetch_query = "SELECT nome_completo, email FROM clientes WHERE id = ?"
        result = self.db.fetch_query(fetch_query, (client_id,))
        
        self.assertEqual(len(result), 1) # Deve encontrar exatamente um cliente
        self.assertEqual(result[0][0], 'João da Silva') # Verifica o nome
        self.assertEqual(result[0][1], 'joao.silva@email.com') # Verifica o email

    def test_delete_client(self):
        """
        Testa a exclusão de um cliente.
        """
        print("Executando: test_delete_client")
        add_query = "INSERT INTO clientes (data_cadastro, nome_completo) VALUES (?, ?)"
        client_id = self.db.execute_query(add_query, (datetime.now().strftime("%Y-%m-%d"), 'Cliente a ser Deletado'))
        
      
        delete_query = "DELETE FROM clientes WHERE id = ?"
        self.db.execute_query(delete_query, (client_id,))
        
        
        fetch_query = "SELECT * FROM clientes WHERE id = ?"
        result = self.db.fetch_query(fetch_query, (client_id,))
        
        self.assertEqual(len(result), 0) # Não deve encontrar nenhum resultado

    def test_foreign_key_cascade_delete(self):
        """
        Testa a funcionalidade ON DELETE CASCADE da chave estrangeira.
        Ao deletar um cliente, suas interações devem ser deletadas automaticamente.
        """
        print("Executando: test_foreign_key_cascade_delete")
       
        add_client_query = "INSERT INTO clientes (data_cadastro, nome_completo) VALUES (?, ?)"
        client_id = self.db.execute_query(add_client_query, (datetime.now().strftime("%Y-%m-%d"), 'Cliente com Interação'))
        self.assertIsNotNone(client_id)

        
        add_interaction_query = "INSERT INTO interacoes (cliente_id, data, resumo) VALUES (?, ?, ?)"
        interaction_id = self.db.execute_query(add_interaction_query, (client_id, datetime.now().strftime("%Y-%m-%d"), "Teste de interação"))
        self.assertIsNotNone(interaction_id)

        interaction_result = self.db.fetch_query("SELECT * FROM interacoes WHERE id = ?", (interaction_id,))
        self.assertEqual(len(interaction_result), 1)

        self.db.execute_query("DELETE FROM clientes WHERE id = ?", (client_id,))

        interaction_result_after_delete = self.db.fetch_query("SELECT * FROM interacoes WHERE id = ?", (interaction_id,))
        self.assertEqual(len(interaction_result_after_delete), 0, "A interação deveria ter sido deletada em cascata.")


if __name__ == '__main__':
    unittest.main()
