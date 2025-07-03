import os

# O caminho para o arquivo de licença.
# É crucial que seja exatamente o mesmo definido no seu arquivo license_manager.py
LICENSE_FILE = os.path.join(os.path.expanduser('~'), '.crm_pro_license.dat')

def reset_activation():
    """
    Verifica se o arquivo de licença existe no computador e o remove.
    Isso simula uma nova instalação para fins de teste.
    """
    print("--- Script de Reset de Ativação ---")
    print(f"Procurando pelo arquivo de licença em: {LICENSE_FILE}")
    
    # Verifica se o arquivo realmente existe no caminho especificado
    if os.path.exists(LICENSE_FILE):
        try:
            # Tenta remover o arquivo
            os.remove(LICENSE_FILE)
            print("\n✅ Sucesso! Arquivo de licença removido.")
            print("O programa agora iniciará como se fosse a primeira vez.")
        except Exception as e:
            # Informa se ocorrer algum erro de permissão ou outro problema
            print(f"\n❌ Erro! Não foi possível remover o arquivo: {e}")
    else:
        # Informa se o arquivo já não existia
        print("\nℹ️ Nenhuma licença para remover. O programa já está no estado 'não ativado'.")

if __name__ == "__main__":
    # Este bloco garante que a função só seja executada quando o script é rodado diretamente
    reset_activation()

