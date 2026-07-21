import hashlib
import sqlite3
import random
from cryptography.fernet import Fernet

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

# ----------------- Database & Helper Logic ----------------- #
class DatabaseHandler:
    def __init__(self):
        self.con = sqlite3.connect("Password.db")
        self.sq = self.con.cursor()
        self.init_db()

    def save_db(self):
        self.con.commit()

    def init_db(self):
        self.sq.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username PRIMARY KEY,
            password TEXT
        )
        """)
        self.sq.execute("""
        CREATE TABLE IF NOT EXISTS websites(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            name_websites TEXT,
            key_name_websites TEXT,
            username_websites TEXT,
            key_username_websites TEXT,
            password_websites TEXT,
            key_password_websites TEXT
        )
        """)
        self.save_db()

    def encrypt_data(self, key, text_bytes):
        cipher = Fernet(key)
        return cipher.encrypt(text_bytes)

    def decrypt_data(self, key, encrypted_bytes):
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_bytes)

    def hash_text(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

db = DatabaseHandler()

# ----------------- Utility Popup ----------------- #
def show_popup(title, text):
    content = BoxLayout(orientation='vertical', padding=10, spacing=10)
    content.add_widget(Label(text=text, halign='center'))
    close_btn = Button(text="OK", size_hint=(1, 0.3))
    content.add_widget(close_btn)
    
    popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
    close_btn.bind(on_release=popup.dismiss)
    popup.open()

# ----------------- Kivy Screens ----------------- #
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text="Password Manager Login", font_size=20))
        
        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False)
        
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        
        btn = Button(text="Login or Create Account", background_color=(0, 1, 0, 1))
        btn.bind(on_release=self.check_login_or_create)
        layout.add_widget(btn)
        
        self.add_widget(layout)

    def check_login_or_create(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            show_popup("Error", "Please fill in all fields.")
            return

        hash1 = db.hash_text(username)
        hash2 = db.hash_text(password)

        db.sq.execute("SELECT username, password FROM users WHERE username = ?", (hash1,))
        db_user = db.sq.fetchone()

        if not db_user:
            db.sq.execute("INSERT INTO users (username, password) VALUES (?, ?)", (hash1, hash2))
            db.save_db()
            show_popup("Success", "Added new admin user successfully!")
        elif hash1 == db_user[0] and hash2 == db_user[1]:
            app = App.get_running_app()
            app.current_user = hash1
            show_popup("Signed In", "Welcome back!")
            self.username_input.text = ""
            self.password_input.text = ""
            self.manager.current = "main_menu"
        else:
            show_popup("Error", "Incorrect username or password.")


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=2, padding=20, spacing=15)

        btn_add = Button(text="Add New Account", background_color=(1, 1, 0, 1))
        btn_add.bind(on_release=lambda x: setattr(self.manager, 'current', 'add_account'))

        btn_add_rd = Button(text="Add Account (Random Pass)", background_color=(0, 1, 0, 1))
        btn_add_rd.bind(on_release=lambda x: setattr(self.manager, 'current', 'add_account_rd'))

        btn_delete = Button(text="Delete Account", background_color=(1, 0.4, 0, 1))
        btn_delete.bind(on_release=lambda x: setattr(self.manager, 'current', 'delete_account'))

        btn_delete_all = Button(text="Delete ALL Accounts", background_color=(1, 0.4, 1, 1))
        btn_delete_all.bind(on_release=self.delete_all_accounts)

        btn_show_all = Button(text="Show All Accounts", background_color=(1, 0, 0, 1))
        btn_show_all.bind(on_release=self.go_to_show_accounts)

        btn_exit = Button(text="Log Out", background_color=(0, 1, 1, 1))
        btn_exit.bind(on_release=self.logout)

        layout.add_widget(btn_add)
        layout.add_widget(btn_add_rd)
        layout.add_widget(btn_delete)
        layout.add_widget(btn_delete_all)
        layout.add_widget(btn_show_all)
        layout.add_widget(btn_exit)

        self.add_widget(layout)

    def delete_all_accounts(self, instance):
        app = App.get_running_app()
        db.sq.execute("SELECT id FROM websites WHERE username = ?", (app.current_user,))
        if not db.sq.fetchall():
            show_popup("Error", "No accounts found to delete.")
        else:
            db.sq.execute("DELETE FROM websites WHERE username = ?", (app.current_user,))
            db.save_db()
            show_popup("Success", "All accounts deleted successfully.")

    def go_to_show_accounts(self, instance):
        show_screen = self.manager.get_screen('show_accounts')
        show_screen.load_accounts()
        self.manager.current = 'show_accounts'

    def logout(self, instance):
        App.get_running_app().current_user = None
        self.manager.current = 'login'


class AddAccountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Enter Website Name"))
        self.website_input = TextInput(multiline=False)
        layout.add_widget(self.website_input)

        layout.add_widget(Label(text="Enter Username"))
        self.username_input = TextInput(multiline=False)
        layout.add_widget(self.username_input)

        layout.add_widget(Label(text="Enter Password"))
        self.password_input = TextInput(multiline=False)
        layout.add_widget(self.password_input)

        btn_save = Button(text="Save Account", background_color=(0, 1, 0, 1))
        btn_save.bind(on_release=self.save_account)
        layout.add_widget(btn_save)

        btn_back = Button(text="Back Home", background_color=(1, 0, 0, 1))
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main_menu'))
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def save_account(self, instance):
        app = App.get_running_app()
        name = self.website_input.text.encode()
        user = self.username_input.text.encode()
        pwd = self.password_input.text.encode()

        key1, key2, key3 = Fernet.generate_key(), Fernet.generate_key(), Fernet.generate_key()
        enc1 = db.encrypt_data(key1, name)
        enc2 = db.encrypt_data(key2, user)
        enc3 = db.encrypt_data(key3, pwd)

        db.sq.execute("""
        INSERT INTO websites(
            username, name_websites, key_name_websites, 
            username_websites, key_username_websites, 
            password_websites, key_password_websites
        ) VALUES (?, ?, ?, ?, ?, ?, ?)""", 
        (app.current_user, enc1, key1, enc2, key2, enc3, key3))
        
        db.save_db()
        show_popup("Success", "Account saved successfully!")
        self.website_input.text = ""
        self.username_input.text = ""
        self.password_input.text = ""
        self.manager.current = 'main_menu'


class AddAccountRandomScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Enter Website Name"))
        self.website_input = TextInput(multiline=False)
        layout.add_widget(self.website_input)

        layout.add_widget(Label(text="Enter Username"))
        self.username_input = TextInput(multiline=False)
        layout.add_widget(self.username_input)

        layout.add_widget(Label(text="Enter Password Length (Integer)"))
        self.length_input = TextInput(multiline=False)
        layout.add_widget(self.length_input)

        btn_save = Button(text="Generate & Save", background_color=(0, 1, 0, 1))
        btn_save.bind(on_release=self.save_account_rd)
        layout.add_widget(btn_save)

        btn_back = Button(text="Back Home", background_color=(1, 0, 0, 1))
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main_menu'))
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def save_account_rd(self, instance):
        try:
            length = int(self.length_input.text)
            chars = "abcdefghijklmnopqrstuvwxyz1234567890~!@#$%^&*_:?"
            generated_pwd = "".join(random.choice(chars) for _ in range(length))

            app = App.get_running_app()
            name = self.website_input.text.encode()
            user = self.username_input.text.encode()
            pwd = generated_pwd.encode()

            key1, key2, key3 = Fernet.generate_key(), Fernet.generate_key(), Fernet.generate_key()
            enc1 = db.encrypt_data(key1, name)
            enc2 = db.encrypt_data(key2, user)
            enc3 = db.encrypt_data(key3, pwd)

            db.sq.execute("""
            INSERT INTO websites(
                username, name_websites, key_name_websites, 
                username_websites, key_username_websites, 
                password_websites, key_password_websites
            ) VALUES (?, ?, ?, ?, ?, ?, ?)""", 
            (app.current_user, enc1, key1, enc2, key2, enc3, key3))
            
            db.save_db()
            show_popup("Success", f"Account created!\nGenerated Password: {generated_pwd}")
            self.website_input.text = ""
            self.username_input.text = ""
            self.length_input.text = ""
            self.manager.current = 'main_menu'
        except ValueError:
            show_popup("Value Error", "Password length must be a valid integer.")


class ShowAccountsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.scroll = ScrollView()
        self.accounts_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.accounts_container.bind(minimum_height=self.accounts_container.setter('height'))
        
        self.scroll.add_widget(self.accounts_container)
        self.main_layout.add_widget(self.scroll)

        btn_back = Button(text="Back to Home", size_hint_y=None, height=40, background_color=(1, 0, 0, 1))
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main_menu'))
        self.main_layout.add_widget(btn_back)

        self.add_widget(self.main_layout)

    def load_accounts(self):
        self.accounts_container.clear_widgets()
        app = App.get_running_app()

        db.sq.execute("SELECT * FROM websites WHERE username = ?", (app.current_user,))
        all_websites = db.sq.fetchall()

        if not all_websites:
            show_popup("Error", "No websites found.")
            return

        for site in all_websites:
            site_id = site[0]
            name = db.decrypt_data(site[3], site[2]).decode()
            user = db.decrypt_data(site[5], site[4]).decode()
            pwd = db.decrypt_data(site[7], site[6]).decode()

            info_text = f"ID: {site_id} | Site: {name} | User: {user} | Pass: {pwd}"
            lbl = Label(text=info_text, size_hint_y=None, height=30)
            self.accounts_container.add_widget(lbl)


class DeleteAccountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="Enter ID to Delete"))
        self.id_input = TextInput(multiline=False)
        layout.add_widget(self.id_input)

        btn_delete = Button(text="Delete This Account", background_color=(0, 1, 0, 1))
        btn_delete.bind(on_release=self.delete_by_id)
        layout.add_widget(btn_delete)

        btn_back = Button(text="Back Home", background_color=(1, 0, 0, 1))
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main_menu'))
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def delete_by_id(self, instance):
        app = App.get_running_app()
        try:
            target_id = int(self.id_input.text)
            db.sq.execute("SELECT id FROM websites WHERE id = ? AND username = ?", (target_id, app.current_user))
            item = db.sq.fetchone()

            if item:
                db.sq.execute("DELETE FROM websites WHERE id = ?", (target_id,))
                db.save_db()
                show_popup("Done", "Account deleted successfully.")
                self.id_input.text = ""
                self.manager.current = 'main_menu'
            else:
                show_popup("Error", "Account ID not found for current user.")
        except ValueError:
            show_popup("Error", "Please enter a valid numeric ID.")


# ----------------- Main App Class ----------------- #
class PasswordManagerApp(App):
    def build(self):
        self.current_user = None
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(AddAccountScreen(name='add_account'))
        sm.add_widget(AddAccountRandomScreen(name='add_account_rd'))
        sm.add_widget(ShowAccountsScreen(name='show_accounts'))
        sm.add_widget(DeleteAccountScreen(name='delete_account'))
        
        return sm

if __name__ == "__main__":
    PasswordManagerApp().run()