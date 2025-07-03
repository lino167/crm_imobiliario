import hashlib
import os
import json
import re

# ESTE SEGREDO DEVE SER EXATAMENTE O MESMO DO SEU GERADOR DE CHAVES.
SECRET_SALT = "M3u_S3gr3d0_SuP3r_C0mpl3x0_2025"
LICENSE_FILE = os.path.join(os.path.expanduser('~'), '.crm_pro_license.dat')

def validate_key(key: str) -> bool:
    """
    Valida se uma chave de licença é matematicamente correta.
    """
    try:
        parts = key.strip().upper().split('-')
        if len(parts) < 6 or parts[0] != 'CRM':
            return False

        client_identifier_from_key = "-".join(parts[1:-4])
        key_part = "".join(parts[-4:])
        sanitized_identifier = re.sub(r'[^A-Z0-9]', '', client_identifier_from_key)

        salted_identifier = sanitized_identifier + SECRET_SALT
        full_hash = hashlib.sha256(salted_identifier.encode()).hexdigest()
        
        return key_part == full_hash[:16].upper()
    except Exception as e:
        print(f"Erro ao validar a chave: {e}")
        return False

def activate_license(key: str) -> bool:
    """
    Valida a chave e, se for válida, cria o arquivo de licença.
    """
    if validate_key(key):
        try:
            license_data = {
                'key': key,
                'status': 'ACTIVE'
            }
            with open(LICENSE_FILE, 'w') as f:
                json.dump(license_data, f)
            return True
        except:
            return False
    return False

def check_license() -> bool:
    """
    Verifica se o arquivo de licença existe e se a chave dentro dele é válida.
    ESTA É A FUNÇÃO QUE ESTAVA FALTANDO.
    """
    if not os.path.exists(LICENSE_FILE):
        return False
    
    try:
        with open(LICENSE_FILE, 'r') as f:
            license_data = json.load(f)
        
        if license_data.get('status') == 'ACTIVE' and validate_key(license_data.get('key', '')):
            return True
        return False
    except:
        return False
