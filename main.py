import customtkinter as ctk
from app import App
from database import Database

def main():
    """
    Função principal para configurar e executar a aplicação CRM Imobiliário.

    Orquestra a inicialização do banco de dados, a configuração da UI
    e o ciclo de vida da aplicação.
    """
    db_manager = None
    try:
        # 1. Configura a aparência global da aplicação (antes de criar a janela)
        ctk.set_appearance_mode("System")  # Opções: "Light", "Dark", "System"
        ctk.set_default_color_theme("blue")

        # 2. Inicializa o gerenciador do banco de dados
        print("Inicializando o banco de dados...")
        db_manager = Database()

        # 3. Cria e executa a aplicação principal, passando a instância do banco
        print("Iniciando a aplicação...")
        main_app = App(db=db_manager)
        main_app.mainloop() # Inicia o loop de eventos da interface gráfica

    except ImportError as e:
        print(f"\nERRO: Falha ao importar um módulo necessário: {e}")
        print("Verifique se todos os arquivos (como app.py e os frames da UI) foram criados.")
    except Exception as e:
        print(f"\nOcorreu um erro fatal na aplicação: {e}")
        # Em uma aplicação de produção, poderíamos logar este erro em um arquivo.
    finally:
        # 4. Garante que a conexão com o banco de dados seja fechada ao sair
        if db_manager:
            db_manager.close()

if __name__ == "__main__":
    main()
