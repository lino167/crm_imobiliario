import customtkinter as ctk
from tkinter import messagebox
import license_manager

class LicenseFrame(ctk.CTkFrame):
    """
    Frame que exibe o status da licença e permite a ativação do produto.
    """
    # MUDANÇA 1: O __init__ agora aceita o callback
    def __init__(self, parent, on_activation_success_callback):
        super().__init__(parent, fg_color="transparent")
        # Armazena a função de callback para ser chamada depois
        self.on_activation_success = on_activation_success_callback
        
        self.grid_columnconfigure(0, weight=1)

        # --- Frame Principal para Centralizar Conteúdo ---
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0, padx=20, pady=20)
        
        # --- Status da Licença ---
        self.status_title_label = ctk.CTkLabel(center_frame, text="Status da Licença:", font=ctk.CTkFont(size=16, weight="bold"))
        self.status_title_label.pack(pady=(20, 5))
        
        self.status_value_label = ctk.CTkLabel(center_frame, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.status_value_label.pack(pady=(0, 20))
        
        # --- Seção de Ativação ---
        self.key_entry_label = ctk.CTkLabel(center_frame, text="Insira a chave de licença para ativar todas as funcionalidades:")
        self.key_entry_label.pack(pady=(20, 5))
        
        self.entry_key = ctk.CTkEntry(center_frame, placeholder_text="CRM-NOME-XXXX-XXXX-XXXX-XXXX", width=360)
        self.entry_key.pack(pady=10)
        
        self.btn_activate = ctk.CTkButton(center_frame, text="Ativar Produto", command=self.activate)
        self.btn_activate.pack(pady=10)
        
        # --- Contato para Licença ---
        self.contact_label = ctk.CTkLabel(center_frame, text="\nPara adquirir uma licença ou obter suporte, entre em contato:\nteamzatha@gmail.com",
                                          font=ctk.CTkFont(size=12))
        self.contact_label.pack(pady=(30, 20))

        self.check_and_display_status()

    def check_and_display_status(self):
        """Verifica a licença e atualiza a interface de acordo."""
        if license_manager.check_license():
            self.status_value_label.configure(text="ATIVADO", text_color="green")
            self.entry_key.configure(state="disabled", placeholder_text="Produto já ativado.")
            self.btn_activate.configure(state="disabled")
        else:
            self.status_value_label.configure(text="NÃO ATIVADO (Modo de Visualização)", text_color="red")
            self.entry_key.configure(state="normal")
            self.btn_activate.configure(state="normal")
            
    def activate(self):
        key = self.entry_key.get().strip()
        if license_manager.activate_license(key):
            messagebox.showinfo("Sucesso", "Produto ativado com sucesso! Todas as funcionalidades foram liberadas.")
            self.check_and_display_status() # Atualiza o status na tela
            self.on_activation_success() # Avisa o app principal que a ativação ocorreu
        else:
            messagebox.showerror("Erro", "Chave de licença inválida.")
