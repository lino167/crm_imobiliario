import unittest
import os
import json

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import license_manager

class TestLicenseManager(unittest.TestCase):
    """
    Suíte de testes para o módulo license_manager.
    """

    def setUp(self):
        """Executado ANTES de cada teste."""
        self.test_license_file = '.test_license.dat'
        license_manager.LICENSE_FILE = self.test_license_file
        
        self.valid_key = "CRM-TESTUSER-0E7F-19AD-32B1-93DA"
        self.invalid_key = "CRM-FAKEUSER-1111-2222-3333-4444"

    def tearDown(self):
        """Executado DEPOIS de cada teste."""
        if os.path.exists(self.test_license_file):
            os.remove(self.test_license_file)

    def test_validate_key_valid(self):
        """Testa se uma chave gerada corretamente é considerada válida."""
        self.assertTrue(license_manager.validate_key(self.valid_key))

    def test_validate_key_invalid(self):
        """Testa se uma chave incorreta é considerada inválida."""
        self.assertFalse(license_manager.validate_key(self.invalid_key))
        
    def test_validate_key_malformed(self):
        """Testa se chaves com formato errado são inválidas."""
        self.assertFalse(license_manager.validate_key("chave-errada"))
        self.assertFalse(license_manager.validate_key(""))

    def test_activation_cycle(self):
        """Testa o ciclo completo: checar, ativar e checar novamente."""
        self.assertFalse(license_manager.check_license())
        self.assertFalse(license_manager.activate_license(self.invalid_key))
        self.assertTrue(license_manager.activate_license(self.valid_key))
        self.assertTrue(os.path.exists(self.test_license_file))
        self.assertTrue(license_manager.check_license())

    def test_check_license_tampered_file(self):
        """Testa se a checagem falha se o arquivo de licença for adulterado."""
        fake_data = {'key': self.invalid_key, 'status': 'ACTIVE'}
        with open(self.test_license_file, 'w') as f:
            json.dump(fake_data, f)
        self.assertFalse(license_manager.check_license())


if __name__ == '__main__':
    unittest.main()
