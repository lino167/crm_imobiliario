import unittest
import os
import json

# Ajusta o path para encontrar os módulos do projeto
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import license_manager

class TestLicenseManager(unittest.TestCase):
    """
    Suíte de testes para o módulo license_manager.
    """

    def setUp(self):
        """Executado ANTES de cada teste."""
        # Define um arquivo de licença de TESTE para não interferir com o real
        self.test_license_file = '.test_license.dat'
        license_manager.LICENSE_FILE = self.test_license_file
        
        # Chave válida para os testes, gerada com o identificador "TESTUSER"
        # Isso garante que a validação não dependa do seu gerador pessoal.
        self.valid_key = "CRM-TESTUSER-D6D7-96B1-3729-1F0A"
        self.invalid_key = "CRM-FAKEUSER-1111-2222-3333-4444"

    def tearDown(self):
        """Executado DEPOIS de cada teste."""
        # Deleta o arquivo de licença de teste se ele existir
        if os.path.exists(self.test_license_file):
            os.remove(self.test_license_file)

    def test_validate_key_valid(self):
        """Testa se uma chave gerada corretamente é considerada válida."""
        print("Executando: test_validate_key_valid")
        self.assertTrue(license_manager.validate_key(self.valid_key))

    def test_validate_key_invalid(self):
        """Testa se uma chave incorreta é considerada inválida."""
        print("Executando: test_validate_key_invalid")
        self.assertFalse(license_manager.validate_key(self.invalid_key))
        
    def test_validate_key_malformed(self):
        """Testa se chaves com formato errado são inválidas."""
        print("Executando: test_validate_key_malformed")
        self.assertFalse(license_manager.validate_key("chave-errada"))
        self.assertFalse(license_manager.validate_key(""))

    def test_activation_cycle(self):
        """Testa o ciclo completo: checar, ativar e checar novamente."""
        print("Executando: test_activation_cycle")
        # 1. Antes de ativar, a licença deve ser inválida
        self.assertFalse(license_manager.check_license())
        
        # 2. Tenta ativar com uma chave inválida, deve falhar
        self.assertFalse(license_manager.activate_license(self.invalid_key))
        
        # 3. Ativa com uma chave válida, deve ter sucesso
        self.assertTrue(license_manager.activate_license(self.valid_key))
        
        # 4. Verifica se o arquivo de licença foi criado
        self.assertTrue(os.path.exists(self.test_license_file))
        
        # 5. Após ativar, a checagem de licença deve retornar True
        self.assertTrue(license_manager.check_license())

    def test_check_license_tampered_file(self):
        """Testa se a checagem falha se o arquivo de licença for adulterado."""
        print("Executando: test_check_license_tampered_file")
        # Cria um arquivo de licença falso
        fake_data = {'key': self.invalid_key, 'status': 'ACTIVE'}
        with open(self.test_license_file, 'w') as f:
            json.dump(fake_data, f)
            
        # A checagem deve revalidar a chave e falhar
        self.assertFalse(license_manager.check_license())
