import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import secrets
import os

class PasswordDialog:
    def __init__(self, parent):
        self.parent = parent
        self.password = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Enter Password")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("300x100")
        x = parent.winfo_x() + (parent.winfo_width() - 300) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 100) // 2
        self.dialog.geometry(f"+{x}+{y}")
        
        # Password entry
        tk.Label(self.dialog, text="Enter password:").pack(pady=5)
        self.password_entry = tk.Entry(self.dialog, show="*")
        self.password_entry.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=5)
        
        ok_button = tk.Button(button_frame, text="OK", command=self.on_ok)
        ok_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def on_ok(self):
        self.password = self.password_entry.get()
        self.dialog.destroy()
    
    def on_cancel(self):
        self.password = None
        self.dialog.destroy()
    
    def get_password(self):
        return self.password

class SecureEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure File Editor")
        self.root.geometry("800x600")
        
        self.current_file = None
        self.salt = None
        self.fernet = None
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=5)
        
        self.new_button = ttk.Button(toolbar, text="New", command=self.new_file)
        self.new_button.pack(side=tk.LEFT, padx=5)
        
        self.open_button = ttk.Button(toolbar, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(toolbar, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.save_as_button = ttk.Button(toolbar, text="Save As", command=self.save_file_as)
        self.save_as_button.pack(side=tk.LEFT, padx=5)
        
        # Create text editor
        self.text_editor = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD)
        self.text_editor.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def generate_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)
    
    def new_file(self):
        self.text_editor.delete(1.0, tk.END)
        self.current_file = None
        self.salt = secrets.token_bytes(16)
        
        dialog = PasswordDialog(self.root)
        password = dialog.get_password()
        if password:
            self.fernet = self.generate_key(password, self.salt)
        else:
            messagebox.showwarning("Error", "Password cannot be empty")
    
    def open_file(self):
        file_name = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Secure Files", "*.lcv")]
        )
        
        if file_name:
            try:
                with open(file_name, 'rb') as file:
                    self.salt = file.read(16)
                    encrypted_data = file.read()
                
                dialog = PasswordDialog(self.root)
                password = dialog.get_password()
                if password:
                    self.fernet = self.generate_key(password, self.salt)
                    decrypted_data = self.fernet.decrypt(encrypted_data)
                    self.text_editor.delete(1.0, tk.END)
                    self.text_editor.insert(tk.END, decrypted_data.decode())
                    self.current_file = file_name
                else:
                    messagebox.showwarning("Error", "Password cannot be empty")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    def save_file(self):
        if not self.fernet:
            messagebox.showwarning("Error", "Please create a new file or open an existing one first")
            return
            
        if not self.current_file:
            self.save_file_as()
            return
            
        try:
            data = self.text_editor.get(1.0, tk.END).encode()
            encrypted_data = self.fernet.encrypt(data)
            
            with open(self.current_file, 'wb') as file:
                file.write(self.salt)
                file.write(encrypted_data)
                
            messagebox.showinfo("Success", "File saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def save_file_as(self):
        if not self.fernet:
            messagebox.showwarning("Error", "Please create a new file or open an existing one first")
            return
            
        file_name = filedialog.asksaveasfilename(
            title="Save File",
            defaultextension=".lcv",
            filetypes=[("Secure Files", "*.lcv")]
        )
        
        if file_name:
            if not file_name.endswith('.lcv'):
                file_name += '.lcv'
                
            self.current_file = file_name
            self.save_file()
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = SecureEditor()
    app.run() 