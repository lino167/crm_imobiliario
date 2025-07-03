# -*- coding: utf-8 -*-
import customtkinter as ctk
from tkinter import messagebox
import license_manager

class LicenseFrame(ctk.CTkFrame):
    """
    Frame que exibe o status da licença e permite a ativação do produto.
    """
    def __init__(self, parent, on_activation_success):
        super().__init__(parent, fg_color="transparent")
        self.on_activation_success = on_activation_success
        
        self.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0, padx=20, pady=20)
        
        # --- Seção de ID da Máquina ---
        ctk.CTkLabel(center_frame, text="Seu ID de Máquina (para ativação):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 5))
        
        self.machine_id_var = ctk.StringVar(value="Gerando...")
        machine_id_entry = ctk.CTkEntry(center_frame, textvariable=self.machine_id_var, state="readonly", width=360, justify='center')
        machine_id_entry.pack(pady=5)
        
        # --- Seção de Ativação ---
        ctk.CTkLabel(center_frame, text="Insira a chave de licença recebida:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        
        self.entry_key = ctk.CTkEntry(center_frame, placeholder_text="CRM-NOME-XXXX-XXXX-XXXX-XXXX", width=360)
        self.entry_key.pack(pady=10)
        
        self.btn_activate = ctk.CTkButton(center_frame, text="Ativar Produto", command=self.activate)
        self.btn_activate.pack(pady=10)
        
        # --- Contato para Licença ---
        self.contact_label = ctk.CTkLabel(center_frame, text="\nPara adquirir uma licença, envie seu 'ID de Máquina' para:\nteamzatha@gmail.com", font=ctk.CTkFont(size=12))
        self.contact_label.pack(pady=(30, 20))

        self.check_and_display_status()

    def check_and_display_status(self):
        """Verifica a licença e atualiza a interface de acordo."""
        machine_id = license_manager.get_machine_id()
        self.machine_id_var.set(machine_id)
        
        if license_manager.check_license():
            self.entry_key.configure(state="disabled", placeholder_text="Produto ativado nesta máquina.")
            self.btn_activate.configure(state="disabled")
        else:
            self.entry_key.configure(state="normal")
            self.btn_activate.configure(state="normal")
            
    def activate(self):
        """Tenta ativar o produto com a chave inserida."""
        key = self.entry_key.get().strip()
        if not key:
            messagebox.showwarning("Campo Vazio", "Por favor, insira a chave de licença.")
            return
            
        if license_manager.activate_license(key):
            messagebox.showinfo("Sucesso", "Produto ativado com sucesso! Todas as funcionalidades foram liberadas.")
            self.check_and_display_status()
            self.on_activation_success()
        else:
            messagebox.showerror("Erro", "Chave de licença inválida ou para outra máquina.")
