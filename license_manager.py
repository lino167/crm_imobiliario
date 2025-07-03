import hashlib
import os
import json
import wmi # Biblioteca para acessar informações de hardware do Windows

# ESTE SEGREDO DEVE SER EXATAMENTE O MESMO DO SEU GERADOR DE CHAVES.
SECRET_SALT = "M3u_S3gr3d0_SuP3r_C0mpl3x0_2025"
LICENSE_FILE = os.path.join(os.path.expanduser('~'), '.crm_pro_license.dat')

def get_machine_id():
    """
    Gera um ID único para a máquina baseado no número de série do primeiro disco rígido.
    Este é um identificador bastante estável.
    """
    try:
        c = wmi.WMI()
        # Pega o primeiro disco físico
        for disk in c.Win32_DiskDrive():
            # Retorna o número de série do disco, que é um bom identificador único
            return disk.SerialNumber.strip()
    except Exception as e:
        print(f"Erro ao obter o ID da máquina: {e}")
        # Como fallback, podemos usar um identificador menos seguro, como o nome do computador
        return os.environ.get('COMPUTERNAME', 'UNKNOWN_PC')

def validate_key(key: str, machine_id: str) -> bool:
    """
    Valida se uma chave de licença é matematicamente correta PARA UMA MÁQUINA ESPECÍFICA.
    """
    try:
        parts = key.strip().upper().split('-')
        if len(parts) != 6 or parts[0] != 'CRM':
            return False

        client_identifier = parts[1]
        key_part = "".join(parts[2:])
        
        # O hash agora é gerado com o nome do cliente E o ID da máquina
        salted_string = client_identifier + machine_id + SECRET_SALT
        full_hash = hashlib.sha256(salted_string.encode()).hexdigest()
        
        return key_part == full_hash[:16].upper()
    except:
        return False

def activate_license(key: str) -> bool:
    """
    Valida a chave contra o ID da máquina atual e cria o arquivo de licença.
    """
    current_machine_id = get_machine_id()
    if validate_key(key, current_machine_id):
        try:
            license_data = {
                'key': key,
                'machine_id': current_machine_id, # Salva o ID da máquina no arquivo
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
    Verifica se o arquivo de licença existe e se a chave é válida para a máquina atual.
    """
    if not os.path.exists(LICENSE_FILE):
        return False
    
    try:
        with open(LICENSE_FILE, 'r') as f:
            license_data = json.load(f)
        
        key_from_file = license_data.get('key', '')
        # Revalida a chave contra o ID da máquina ATUAL
        current_machine_id = get_machine_id()
        
        if license_data.get('status') == 'ACTIVE' and validate_key(key_from_file, current_machine_id):
            return True
        return False
    except:
        return False
