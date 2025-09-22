import threading
from kivy.clock import mainthread, Clock
import requests
from kivy.storage.jsonstore import JsonStore

TOKEN_FILE = "session.json"

class FirebaseHelper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.id_token = None
        self.refresh_token = None
        self.store = JsonStore(TOKEN_FILE)
        self.on_success_callback = lambda event: print(f"Evento '{event}' exitoso.")
        self.on_error_callback = lambda error: print(f"Error: {error}")
        self.load_tokens()

    def bind_callbacks(self, on_success, on_error):
        self.on_success_callback = on_success
        self.on_error_callback = on_error

    def is_logged_in(self):
        return self.id_token is not None

    def get_token(self):
        return self.id_token

    def save_tokens(self):
        self.store.put("firebase_session", idToken=self.id_token, refreshToken=self.refresh_token)

    def load_tokens(self):
        if self.store.exists("firebase_session"):
            tokens = self.store.get("firebase_session")
            self.id_token = tokens.get("idToken")
            self.refresh_token = tokens.get("refreshToken")

    def clear_tokens(self):
        if self.store.exists("firebase_session"):
            self.store.delete("firebase_session")
        self.id_token = None
        self.refresh_token = None

    def sign_in(self, email, password):
        threading.Thread(target=self._worker, args=(email, password, "signInWithPassword"), daemon=True).start()
    
    def sign_up(self, email, password):
        threading.Thread(target=self._worker, args=(email, password, "signUp"), daemon=True).start()
    
    def _worker(self, email, password, method):
        endpoint = f"https://identitytoolkit.googleapis.com/v1/accounts:{method}?key={self.api_key}"
        try:
            resp = requests.post(endpoint, json={"email": email, "password": password, "returnSecureToken": True})
            resp.raise_for_status()
            data = resp.json()
            self.id_token, self.refresh_token = data.get('idToken'), data.get('refreshToken')
            self.save_tokens()
            Clock.schedule_once(lambda dt: self.on_success_callback('sign_in' if method == "signInWithPassword" else 'sign_up'))
        except requests.exceptions.HTTPError as e:
            err = e.response.json().get('error', {})
            Clock.schedule_once(lambda dt: self.on_error_callback(err.get('message', 'Error desconocido')))
        except Exception as e:
            print(f"Firebase worker error: {e}")
            Clock.schedule_once(lambda dt: self.on_error_callback("NETWORK_ERROR"))

    def sign_out(self):
        self.clear_tokens()
        self.on_success_callback('sign_out')