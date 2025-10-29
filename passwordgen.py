import customtkinter as ctk
from tkinter import messagebox
import random
import string
import pyperclip
from datetime import datetime
import os

# Set CustomTkinter theme and color
ctk.set_appearance_mode("System")  # Options: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")

class ModernPasswordGenerator(ctk.CTk):
    """
    Password Generator using CustomTkinter for a modern, attractive GUI.
    """
    def __init__(self):
        super().__init__()
        self.title("Secure Password Generator 🔐")
        self.geometry("500x550")
        
        # --- Variables ---
        self.len_var = ctk.IntVar(value=14) 
        self.upper_var = ctk.BooleanVar(value=True)
        self.lower_var = ctk.BooleanVar(value=True)
        self.digit_var = ctk.BooleanVar(value=True)
        self.symbol_var = ctk.BooleanVar(value=True)
        self.exclude_ambiguous_var = ctk.BooleanVar(value=True) 
        self.password_output = ctk.StringVar()
        self.strength_var = ctk.StringVar(value="—") 
        self.history_file = "password_history.txt"

        self._create_widgets()

    def _create_widgets(self):
        """Sets up all GUI elements with CustomTkinter style."""
        
        # --- 1. Main Title ---
        title_label = ctk.CTkLabel(self, text="Password Configuration", 
                                   font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(pady=(20, 10))

        # --- 2. Length Input ---
        len_frame = ctk.CTkFrame(self)
        len_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(len_frame, text="Password Length (8-32):", width=150).pack(side="left", padx=(15, 5))
        
        self.length_entry = ctk.CTkEntry(len_frame, textvariable=self.len_var, width=60)
        self.length_entry.pack(side="right", padx=15)

        # --- 3. Character Selection Checkboxes ---
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(padx=20, pady=10, fill="x")

        # Checkboxes are much cleaner in CustomTkinter
        ctk.CTkCheckBox(options_frame, text="Uppercase (A-Z)", variable=self.upper_var).grid(row=0, column=0, sticky="w", padx=15, pady=5)
        ctk.CTkCheckBox(options_frame, text="Lowercase (a-z)", variable=self.lower_var).grid(row=1, column=0, sticky="w", padx=15, pady=5)
        ctk.CTkCheckBox(options_frame, text="Numbers (0-9)", variable=self.digit_var).grid(row=0, column=1, sticky="w", padx=15, pady=5)
        ctk.CTkCheckBox(options_frame, text="Symbols (!@#...)", variable=self.symbol_var).grid(row=1, column=1, sticky="w", padx=15, pady=5)
        
        # --- 4. Exclusion Option ---
        exclude_frame = ctk.CTkFrame(self)
        exclude_frame.pack(padx=20, pady=5, fill="x")

        ctk.CTkCheckBox(exclude_frame, text="Exclude Ambiguous (l, 1, I, O, 0)", 
                        variable=self.exclude_ambiguous_var, text_color="orange").pack(anchor="w", padx=15)


        # --- 5. Generate Button ---
        generate_button = ctk.CTkButton(self, text="GENERATE PASSWORD", command=self.generate_and_display, 
                                        font=ctk.CTkFont(size=16, weight="bold"), 
                                        height=40, corner_radius=10)
        generate_button.pack(pady=15, padx=20, fill="x")
        
        # --- 6. Output Display and Copy Button ---
        output_frame = ctk.CTkFrame(self)
        output_frame.pack(pady=10, padx=20, fill="x")
        
        # Styled Password Output Field
        self.output_entry = ctk.CTkEntry(output_frame, textvariable=self.password_output, state='readonly', 
                                         font=ctk.CTkFont(family="Courier", size=14, weight="bold"), 
                                         justify='center', width=300, corner_radius=8)
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), ipady=5)
        
        copy_button = ctk.CTkButton(output_frame, text="Copy", command=self.copy_password, 
                                    width=80, fg_color="gray", hover_color="darkgray")
        copy_button.pack(side="right", padx=10)
        
        # --- 7. Strength Indicator Label ---
        strength_label_frame = ctk.CTkFrame(self, fg_color="transparent")
        strength_label_frame.pack(pady=(10, 20))
        
        ctk.CTkLabel(strength_label_frame, text="Strength:", 
                     font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)
        
        # DYNAMIC STRENGTH DISPLAY
        self.strength_display = ctk.CTkLabel(strength_label_frame, textvariable=self.strength_var, 
                                             font=ctk.CTkFont(size=14, weight="bold"), 
                                             padx=10, corner_radius=5)
        self.strength_display.pack(side="left")

    # --- Core Logic Methods ---

    def _get_strength_rating(self, password):
        """Rates the password strength."""
        rating = 0
        
        if len(password) >= 16: rating += 3
        elif len(password) >= 12: rating += 2
        elif len(password) >= 8: rating += 1

        if any(c.isupper() for c in password): rating += 1
        if any(c.islower() for c in password): rating += 1
        if any(c.isdigit() for c in password): rating += 1
        if any(c in string.punctuation for c in password): rating += 1

        # CustomTkinter uses string names for colors
        if rating >= 6:
            return "Excellent", "green"
        elif rating >= 4:
            return "Strong", "blue"
        elif rating >= 2:
            return "Medium", "yellow"
        else:
            return "Weak", "red"

    def _generate_password(self):
        # ... (This logic remains the same as before to preserve functionality)
        p_length = self.len_var.get()
        char_pool = ""
        required_chars = []
        
        if self.upper_var.get():
            char_pool += string.ascii_uppercase
            required_chars.append(random.choice(string.ascii_uppercase))

        if self.lower_var.get():
            char_pool += string.ascii_lowercase
            required_chars.append(random.choice(string.ascii_lowercase))

        if self.digit_var.get():
            char_pool += string.digits
            required_chars.append(random.choice(string.digits))

        if self.symbol_var.get():
            safe_symbols = "!@#$%^&*-=_+" 
            char_pool += safe_symbols
            required_chars.append(random.choice(safe_symbols))

        if not char_pool:
            messagebox.showerror("Configuration Error", "Please select at least one character type.")
            return None
        
        if self.exclude_ambiguous_var.get():
            ambiguous_chars = 'l1IO0'
            char_pool = "".join(c for c in char_pool if c not in ambiguous_chars)
            required_chars = [random.choice(char_pool) for _ in required_chars] 

        if p_length < len(required_chars):
            messagebox.showerror("Length Error", f"Password length must be at least {len(required_chars)} to include all selected types.")
            return None
        
        fill_length = p_length - len(required_chars) 
        random_fill = [random.choice(char_pool) for _ in range(fill_length)]
        final_password_list = required_chars + random_fill
        random.shuffle(final_password_list)

        return "".join(final_password_list)

    def _log_history(self, password, strength):
        """Logs the generated password and its strength."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Strength: {strength} | Password: {password}\n"
        try:
            with open(self.history_file, "a") as f:
                f.write(log_entry)
        except IOError:
            print(f"Warning: Could not write to history file: {self.history_file}")

    def generate_and_display(self):
        """Runs logic, updates display, and logs."""
        new_password = self._generate_password()
        
        if new_password:
            self.password_output.set(new_password)
            
            # --- STRENGTH DYNAMIC COLOR CHANGE (CustomTkinter) ---
            strength_text, strength_color = self._get_strength_rating(new_password)
            self.strength_var.set(strength_text)
            self.strength_display.configure(fg_color=strength_color) # Use fg_color for background tint
            
            self._log_history(new_password, strength_text)
            messagebox.showinfo("Success", f"Password generated and logged. Strength: {strength_text}")

    def copy_password(self):
        """Copies the generated password to the system clipboard."""
        current_password = self.password_output.get()
        if current_password:
            try:
                pyperclip.copy(current_password)
                messagebox.showinfo("Copied!", "Password copied to clipboard.")
            except Exception:
                messagebox.showerror("Copy Error", "Could not copy to clipboard. Please copy manually.")
        else:
            messagebox.showwarning("Copy Warning", "No password has been generated yet.")

# Run the application
if __name__ == "__main__":
    app = ModernPasswordGenerator()
    app.mainloop()