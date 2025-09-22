# --- firebase_helper.py ---
# --- LÓGICA DE FIREBASE TEMPORALMENTE DESACTIVADA PARA COMPILAR ---

class FirebaseHelper:
    def __init__(self, api_key):
        print("ADVERTENCIA: FirebaseHelper está en modo desactivado.")
        self.api_key = api_key
        
    def bind_callbacks(self, on_success, on_error):
        self.on_success = on_success
        self.on_error = on_error

    def is_logged_in(self):
        return False

    def sign_in(self, email, password):
        print("Firebase sign_in llamado, pero está desactivado.")
        self.on_error("LOGIN_DISABLED")
        
    def sign_up(self, email, password):
        print("Firebase sign_up llamado, pero está desactivado.")
        self.on_error("SIGNUP_DISABLED")

    def sign_out(self):
        print("Firebase sign_out llamado, pero está desactivado.")
        self.on_success('sign_out')