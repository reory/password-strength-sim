import customtkinter as ctk
import numpy as np
import re
import logging
from datetime import datetime

# Logging configuration
logging.basicConfig(
    filename = "Password_log.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

def analyse_single_password(password: str):
    """Logic for a single password input"""

    if not password:
        return 0, "Empty"
    
    # Password length
    length_score = np.clip(len(password), 0, 12)

    # Complexitiy checks
    has_digit = 2 if re.search(r'\d', password) else 0
    has_special = 3 if re.search(r'[!@#%£$^&*(),.?":{}|<>]', password) else 0
    has_upper = 2 if re.search(r'[A-Z]', password) else 0

    total_score = length_score + has_digit + has_special + has_upper

    # Categorise
    if total_score <= 5: label = "Very Weak 😱"
    elif total_score <= 10: label = "Weak 😟"
    elif total_score <= 15: label = "Moderate 😁"
    else: label = "Strong 💪🏼"

    return total_score, label

# GUI setup

class PasswordApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Strength Sim")
        self.geometry("400x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # GUI Elements
        self.label = ctk.CTkLabel(
            self, text="Enter Password to Test:", font=("Arial", 16))
        self.label.pack(pady=20)
        
        self.entry = ctk.CTkEntry(
            self, 
            placeholder_text="Type here....", 
            # Added * so when user types password it remains hidden.
            width=250, show="*"
        )
        self.entry.pack(pady=10)

        self.btn = ctk.CTkButton(
            self, text="Check Strength", command=self.update_result)
        self.btn.pack(pady=20)

        self.result_score = ctk.CTkLabel(
            self, text="Score: -", font=("Arial", 14))
        self.result_score.pack(pady=5)

        self.result_label = ctk.CTkLabel(
            self, text="Strength: -", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=5)

    def update_result(self):
        """Update result once password has been entered and processed."""

        password = self.entry.get()
        score, strength = analyse_single_password(password)
        
        # Update the GUI
        self.result_score.configure(text=f"Score: {score}")
        self.result_label.configure(text=f"Result: {strength}")

        # Change text colour based on strength of password
        if "Strong" in strength:
            self.result_label.configure(text_color="#2ECC71")
        elif "Weak" in strength:
            self.result_label.configure(text_color="#E74C3C")
        else:
            self.result_label.configure(text_color="#F1C40F")

        # The logging action
        logging.info(
            f"Logging Audit Performed | Score: {score} | Strength: {strength}")
        print(f"Log updated for score {score}")

if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()