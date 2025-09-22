from kivy.lang import Builder
from kivy.clock import mainthread, Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivy.core.window import Window
import firebase_helper

Window.size = (400, 700)

class LoginScreen(MDScreen): pass
class RegisterScreen(MDScreen): pass
class DashboardScreen(MDScreen): pass

class AgentFlowApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # IMPORTANTE: Reemplaza con tu API Key Web de Firebase
        self.firebase_api_key = "AIzaSyArnRR7t8X5HDHj0kT4mHSNK04MMswySVo"
        self.firebase = None
        
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('agentflow.kv')

    def on_start(self):
        self.firebase = firebase_helper.FirebaseHelper(self.firebase_api_key)
        self.firebase.bind_callbacks(on_success=self.on_auth_success, on_error=self.on_auth_error)
        
        if self.firebase.is_logged_in():
            self.on_auth_success("session_restored")
        else:
            self.go_to_login_screen()

    @mainthread
    def on_auth_success(self, event_type):
        sm = self.root.ids.screen_manager
        if event_type == 'sign_out':
            self.go_to_login_screen()
            toast("Sesión cerrada")
            return
        
        sm.current = 'dashboard'
        top_bar = self.root.ids.top_app_bar
        top_bar.title = "Dashboard"
        top_bar.right_action_items = [["logout", lambda x: self.firebase.sign_out()]]
        
        if event_type in ['sign_in', 'sign_up']: toast("Acceso concedido")
        elif event_type == 'session_restored': toast("Sesión restaurada")

    @mainthread
    def on_auth_error(self, error):
        error_map = { "INVALID_LOGIN_CREDENTIALS": "Credenciales inválidas.", "EMAIL_EXISTS": "El correo ya está en uso.", "WEAK_PASSWORD": "La contraseña debe tener al menos 6 caracteres.", "NETWORK_ERROR": "Error de red." }
        current_screen = self.root.ids.screen_manager.current
        if current_screen == 'login':
            self.root.ids.screen_manager.get_screen('login').ids.error_label.text = error_map.get(error, "Error desconocido.")
        else:
            toast(error_map.get(error, "Error desconocido."))

    def sign_in(self):
        screen = self.root.ids.screen_manager.get_screen('login')
        email, pw = screen.ids.email.text.strip(), screen.ids.password.text.strip()
        if email and pw: self.firebase.sign_in(email, pw)
        else: toast("Rellena todos los campos.")

    def sign_up(self):
        screen = self.root.ids.screen_manager.get_screen('register')
        email, pw = screen.ids.register_email.text.strip(), screen.ids.register_password.text.strip()
        if email and len(pw) >= 6: self.firebase.sign_up(email, pw)
        else: toast("Email inválido o contraseña demasiado corta.")

    def go_to_login_screen(self):
        sm = self.root.ids.screen_manager; sm.current = 'login'; top_bar = self.root.ids.top_app_bar
        top_bar.title = "Iniciar Sesión"; top_bar.right_action_items = []; top_bar.left_action_items = []

    def go_to_register_screen(self):
        sm = self.root.ids.screen_manager; sm.current = 'register'; top_bar = self.root.ids.top_app_bar
        top_bar.title = "Registro"; top_bar.left_action_items = [["arrow-left", lambda x: self.go_to_login_screen()]]

if __name__ == '__main__':
    AgentFlowApp().run()