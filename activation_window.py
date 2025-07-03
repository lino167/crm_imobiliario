import customtkinter as ctk
from tkinter import messagebox
import license_manager

class ActivationWindow(ctk.CTk):
    def __init__(self, on_success_callback):
        super().__init__()
        self.on_success_callback = on_success_callback
        self.title("Ativação do Produto - CRM Imobiliário Pro")
        self.geometry("400x200")
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Por favor, insira sua chave de licença:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.entry_key = ctk.CTkEntry(self, placeholder_text="CRM-NOME-XXXX-XXXX-XXXX-XXXX", width=360)
        self.entry_key.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_activate = ctk.CTkButton(self, text="Ativar", command=self.activate)
        self.btn_activate.grid(row=2, column=0, padx=20, pady=(10, 20))

    def activate(self):
        key = self.entry_key.get().strip()
        if license_manager.activate_license(key):
            messagebox.showinfo("Sucesso", "Produto ativado com sucesso! O programa será iniciado.")
            self.destroy() # Fecha a janela de ativação
            self.on_success_callback() # Chama a função para iniciar o app principal
        else:
            messagebox.showerror("Erro", "Chave de licença inválida. Verifique a chave e tente novamente.")