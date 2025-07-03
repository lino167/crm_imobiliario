import os

# Garante que estamos usando o mesmo caminho do arquivo de licença
LICENSE_FILE = os.path.join(os.path.expanduser('~'), '.crm_pro_license.dat')

def reset():
    """
    Verifica se o arquivo de licença existe e o remove para simular
    uma nova instalação.
    """
    print(f"Procurando pelo arquivo de licença em: {LICENSE_FILE}")
    
    if os.path.exists(LICENSE_FILE):
        try:
            os.remove(LICENSE_FILE)
            print("✅ Sucesso! Arquivo de licença removido.")
            print("O programa agora iniciará como se fosse a primeira vez.")
        except Exception as e:
            print(f"❌ Erro! Não foi possível remover o arquivo: {e}")
    else:
        print("ℹ️ Nenhuma licença para remover. O programa já está no estado 'não ativado'.")

if __name__ == "__main__":
    reset()

