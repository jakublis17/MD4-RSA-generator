import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMainWindow, QStackedWidget, QFileDialog

from tymon import Keys, Dane, Public_key, isprime, NWD
class Aplikacja(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikacja")
        self.keys = None
        self.stacked_widget=QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.signature = None
        self.message = ""
        self.message2 = ""
        self.pubkey = None


        widget1 = QWidget()
        layout1 = QVBoxLayout()
        label1 = QLabel("Stwórz parę kluczy")
        layout1.addWidget(label1)
        p_label = QLabel("p:")
        layout1.addWidget(p_label)
        self.p_lineedit = QLineEdit()
        layout1.addWidget(self.p_lineedit)
        q_label = QLabel("q:")
        layout1.addWidget(q_label)
        self.q_lineedit = QLineEdit()
        layout1.addWidget(self.q_lineedit)
        e_label = QLabel("e:")
        layout1.addWidget(e_label)
        self.e_lineedit = QLineEdit()
        layout1.addWidget(self.e_lineedit)
        createkeys_button = QPushButton("Stwórz klucze")
        createkeys_button.clicked.connect(self.create_keys)
        layout1.addWidget(createkeys_button)
        self.private_key_button = QPushButton("Zapisz wygenerowany klucz prywatny")
        self.private_key_button.clicked.connect(self.save_private_key)
        layout1.addWidget(self.private_key_button)
        self.public_key_button = QPushButton("Zapisz wygenerowany klucz publiczny")
        self.public_key_button.clicked.connect(self.save_public_key)
        layout1.addWidget(self.public_key_button)
        next_button1 = QPushButton("Przejdź dalej")
        next_button1.clicked.connect(self.nastepny_widget)
        layout1.addWidget(next_button1)
        widget1.setLayout(layout1)
        self.stacked_widget.addWidget(widget1)


        widget2 = QWidget()
        layout2 = QVBoxLayout()
        label2 = QLabel("Podpisywanie dokumentów tekstowych")
        layout2.addWidget(label2)
        self.text_input = QLineEdit()
        layout2.addWidget(self.text_input)
        input_text_button = QPushButton("Wprowadź tekst")
        input_text_button.clicked.connect(self.signatureapp)
        layout2.addWidget(input_text_button)
        uploaddane_button = QPushButton("Wybierz plik")
        uploaddane_button.clicked.connect(self.signatureapp)
        layout2.addWidget(uploaddane_button)
        next_button2 = QPushButton("Przejdź dalej")
        next_button2.clicked.connect(self.nastepny_widget)
        layout2.addWidget(next_button2)
        widget2.setLayout(layout2)
        self.stacked_widget.addWidget(widget2)

        widget3 = QWidget()
        layout3 = QVBoxLayout()
        label3 = QLabel("Weryfikacja podpisu")
        upload_public_key_button = QPushButton("Załącz klucz publiczny")
        upload_public_key_button.clicked.connect(self.load_public_key)
        layout3.addWidget(upload_public_key_button)
        upload_message_button = QPushButton("Załącz wiadomość")
        upload_message_button.clicked.connect(self.load_message)
        layout3.addWidget(upload_message_button)
        signature_label = QLabel("Podpis:")
        layout3.addWidget(signature_label)
        self.signature_input = QLineEdit()
        layout3.addWidget(self.signature_input)
        layout3.addWidget(label3)
        check_button = QPushButton("Sprawdź podpis")
        check_button.clicked.connect(self.verify_signature)
        layout3.addWidget(check_button)
        next_button3 = QPushButton("Przejdź dalej")
        next_button3.clicked.connect(self.nastepny_widget)
        layout3.addWidget(next_button3)
        widget3.setLayout(layout3)
        self.stacked_widget.addWidget(widget3)

        self.widget_count = self.stacked_widget.count()
        self.current_widget_index = 0
    def nastepny_widget(self):
        self.current_widget_index += 1
        if self.current_widget_index >= self.stacked_widget.count():
            self.current_widget_index = 0
        self.stacked_widget.setCurrentIndex(self.current_widget_index)

    def create_keys(self):
        p = int(self.p_lineedit.text())
        q = int(self.q_lineedit.text())
        e_text = self.e_lineedit.text()
        e = int(e_text) if e_text else 1
        try:
            self.keys = Keys(p, q, e)
            key_label = QLabel(f"Klucz publiczny: {self.keys.public_key}, Klucz prywatny: {self.keys.get_private_key()}")
            layout = self.stacked_widget.currentWidget().layout()
            layout.addWidget(key_label)

        except ValueError as e:
            error_label = QLabel(str(e))
            layout = self.stacked_widget.currentWidget().layout()
            layout.addWidget(error_label)

    def save_private_key(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Zapisz klucz publiczny", "", "Text Files (*.txt)")
        self.keys.private_key_to_file(file_path)

    def save_public_key(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Zapisz klucz prywatny", "", "Text Files (*.txt)")
        self.keys.public_key_to_file(file_path)

    def signatureapp(self):
        key = self.keys
        if key and self.text_input.text():
            self.message = self.text_input.text()
            self.signature = key.signature(Dane.from_string(self.message))
            signature_label = QLabel(f"Signature: {self.signature}")
            layout = self.stacked_widget.currentWidget().layout()
            layout.addWidget(signature_label)
        else:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, "Wybierz plik")
            if file_path:
                key = self.keys
                self.message = str(file_path)
                self.signature = key.signature(Dane.from_file(file_path))
                signature_label = QLabel(f"Podpis: {self.signature}")
                layout = self.stacked_widget.currentWidget().layout()
                layout.addWidget(signature_label)

    def verify_signature(self):
        signature = int(self.signature_input.text())
        public_key = self.pubkey
        message = self.message2

        if public_key and message and signature:
            dane = Dane.from_string(message)
            pub_key = public_key
            if pub_key.check_signature(dane, signature):
                result_label = QLabel("Podpis jest prawidłowy.")
            else:
                result_label = QLabel("Podpis jest nieprawidłowy.")
            layout = self.stacked_widget.currentWidget().layout()
            layout.addWidget(result_label)

    def load_public_key(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Załącz klucz publiczny", "", "Text Files (*.txt)")
        if file_path:
            self.pubkey = Public_key.from_file(file_path)
            return self.pubkey
        return None

    def load_message(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Załącz tekst", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r') as file:
                self.message2 = file.read()
                return self.message2
        return None


def main():
    app =QApplication(sys.argv)
    aplikacja = Aplikacja()
    aplikacja.show()
    app.exec()

if __name__ == "__main__":
    main()
