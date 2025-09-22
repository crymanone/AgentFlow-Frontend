from kivy.lang import Builder
from kivy.clock import mainthread, Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import firebase_helper

Window.size = (400, 700)

class LoginScreen(MDScreen): pass
class RegisterScreen(MDScreen): pass
class DashboardScreen(MDScreen): pass

class AgentFlowApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.firebase_api_key = "DISABLED"
        self.firebase = None
        
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('agentflow.kv')

    def on_start(self):
        self.firebase = firebase_helper.FirebaseHelper(self.firebase_api_key)
        self.firebase.bind_callbacks(on_success=self.on_auth_success, on_error=self.on_auth_error)
        self.go_to_login_screen()

    @mainthread
    def on_auth_success(self, event_type):
        if event_type == 'sign_out':
            self.go_to_login_screen(); toast("Sesión cerrada (Simulado)"); return
        self.root.ids.screen_manager.current = 'dashboard'
        self.root.ids.top_app_bar.title = "Dashboard"

    @mainthread
    def on_auth_error(self, error):
        toast(f"Función desactivada: {error}")

    def sign_in(self):
        screen = self.root.ids.screen_manager.get_screen('login')
        email, pw = screen.ids.email.text.strip(), screen.ids.password.text.strip()
        if email and pw:
            # Simulación de éxito para probar navegación
            toast("Simulando login exitoso...")
            self.on_auth_success('sign_in')
        else:
            toast("Rellena todos los campos.")

    def sign_up(self):
        toast("Función de registro desactivada temporalmente.")

    def go_to_login_screen(self):
        sm = self.root.ids.screen_manager; sm.current = 'login'; top_bar = self.root.ids.top_app_bar
        top_bar.title = "Iniciar Sesión"; top_bar.right_action_items = []; top_bar.left_action_items = []

    def go_to_register_screen(self):
        sm = self.root.ids.screen_manager; sm.current = 'register'; top_bar = self.root.ids.top_app_bar
        top_bar.title = "Registro"; top_bar.left_action_items = [["arrow-left", lambda x: self.go_to_login_screen()]]

if __name__ == '__main__':
    AgentFlowApp().run()