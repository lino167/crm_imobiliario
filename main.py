import customtkinter as ctk
from app import App
from database import Database

def main():
    db_manager = None
    try:
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        db_manager = Database()
        app = App(db=db_manager) 
        app.mainloop()
    except Exception as e:
        print(f"Ocorreu um erro fatal: {e}")
    finally:
        if db_manager:
            db_manager.close()

if __name__ == "__main__":
    main()