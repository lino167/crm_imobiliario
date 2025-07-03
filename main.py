import customtkinter as ctk
from app import App
from database import Database
import license_manager
from activation_window import ActivationWindow

def run_main_app():
    """
    Função que inicializa e executa a aplicação principal do CRM.
    """
    db_manager = None
    try:
        db_manager = Database()
        main_app = App(db=db_manager)
        main_app.mainloop()
    except Exception as e:
        print(f"Ocorreu um erro na aplicação principal: {e}")
    finally:
        if db_manager:
            db_manager.close()

def main():
    """
    Ponto de entrada principal. Verifica a licença antes de decidir o que fazer.
    """
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    if license_manager.check_license():
        # Se a licença é válida, roda o app principal
        print("Licença válida encontrada. Iniciando aplicação...")
        run_main_app()
    else:
        # Se não, mostra a janela de ativação
        print("Nenhuma licença válida encontrada. Solicitando ativação...")
        # A janela de ativação vai chamar 'run_main_app' se a chave for correta
        activation_app = ActivationWindow(on_success_callback=run_main_app)
        activation_app.mainloop()

if __name__ == "__main__":
    main()