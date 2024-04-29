from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QComboBox
import sys
from backend import Chatbot
import threading


class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chatbot = Chatbot()

        self.setMinimumSize(760, 500)

        # Add chat area widget
        self.chat_area = QTextEdit(self)
        self.chat_area.setGeometry(10, 10, 480, 320)
        self.chat_area.setReadOnly(True)

        # Add the input field widget
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(10, 340, 480, 40)
        self.input_field.setPlaceholderText("Enter prompt here...")
        self.input_field.returnPressed.connect(self.send_message)

        # Add the system role input field widget
        self.system_input_field = QTextEdit(self)
        self.system_input_field.setGeometry(500, 50, 250, 75)
        self.system_input_field.setPlaceholderText("Enter System Role Message Here...")

        # Add the button
        self.button = QPushButton("Send", self)
        self.button.setGeometry(500, 340, 100, 40)
        self.button.clicked.connect(self.send_message)

        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(500, 10, 120, 30)
        self.combo_box.addItems(["Llama3-8b-8192", "Llama3-70b-8192", "mixtral-8x7b-32768"])
        self.combo_box.currentIndexChanged.connect(self.change_model)

        self.show()

    def send_message(self):
        user_input = self.input_field.text().strip()
        system_role = self.system_input_field.toPlainText().strip()
        self.chat_area.append(f"<p style='color:#1E90FF'>Me: {user_input}</p>")
        self.input_field.clear()

        thread = threading.Thread(target=self.get_bot_response, args=(user_input, system_role))
        thread.start()

        # self.get_bot_response(user_input)

    def get_bot_response(self, user_input, system_role):
        response = self.chatbot.get_response(user_input, system_role)
        if user_input.lower() == "reset":
            self.chat_area.append("<<<<<<<<<< CONVERSATION RESETED HERE >>>>>>>>>>>> ")
            self.chatbot.reset_conversation()
            return
        self.chat_area.append(f"Bot: {response}")

    def change_model(self):
        self.chatbot.change_model(self.combo_box.currentText())


app = QApplication(sys.argv)
main_window = ChatbotWindow()
sys.exit(app.exec())
