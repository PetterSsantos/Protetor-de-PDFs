import sys
import os
import subprocess
import fitz  
import qdarktheme
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFileDialog,
    QStatusBar,
    QTabWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

class PDFProtectorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Configuração da Janela Principal ---
        self.setWindowTitle("Protetor de PDFs")
        self.setFixedSize(500, 400) # Aumentei um pouco a altura para acomodar o status bar melhor

        # --- Configuração do Ícone SVG ---
        # Constrói o caminho para o ícone de forma robusta
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, 'assets', 'icons', 'app.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # --- Abas para Proteger e Desproteger ---
        self.tabs = QTabWidget()
        self.protect_tab = QWidget()
        self.unprotect_tab = QWidget()

        self.tabs.addTab(self.protect_tab, "🔒 Proteger PDF")
        self.tabs.addTab(self.unprotect_tab, "🔓 Desproteger PDF")

        self.setup_protect_ui()
        self.setup_unprotect_ui()

        self.setCentralWidget(self.tabs)

        # --- Barra de Status Aprimorada ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Pronto para proteger seus arquivos.")
        self.status_bar.addWidget(self.status_label, 1) # O '1' faz o label se expandir

        # Botão que será mostrado/ocultado
        self.view_file_button = QPushButton("📂 Abrir Local")
        self.view_file_button.hide()
        self.status_bar.addPermanentWidget(self.view_file_button)

    def create_file_selection_group(self, label_text, button_text, on_click):
        """Cria um grupo de widgets para seleção de arquivo."""
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        label = QLabel(label_text)
        file_path_label = QLineEdit("Nenhum arquivo selecionado")
        file_path_label.setReadOnly(True)
        browse_button = QPushButton(button_text)
        browse_button.clicked.connect(lambda: on_click(file_path_label))
        
        file_layout = QHBoxLayout()
        file_layout.addWidget(file_path_label)
        file_layout.addWidget(browse_button)
        
        group_layout.addWidget(label)
        group_layout.addLayout(file_layout)
        
        return group_layout, file_path_label

    def create_password_group(self, label_text):
        """Cria um grupo de widgets para entrada de senha."""
        group_layout = QVBoxLayout()
        group_layout.setSpacing(10)
        label = QLabel(label_text)
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        group_layout.addWidget(label)
        group_layout.addWidget(password_input)

        return group_layout, password_input

    def setup_ui_tab(self, tab, file_label_text, password_label_text, button_text, on_action_click):
        """Função genérica para configurar as abas."""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        file_group, file_label = self.create_file_selection_group(
            file_label_text, "Procurar...", self.select_file
        )
        password_group, password_input = self.create_password_group(password_label_text)
        
        action_button = QPushButton(button_text)
        action_button.setFixedHeight(40)
        action_button.clicked.connect(on_action_click)
        
        layout.addLayout(file_group)
        layout.addLayout(password_group)
        layout.addWidget(action_button)
        layout.addStretch()

        return file_label, password_input

    def setup_protect_ui(self):
        """Configura a interface da aba 'Proteger'."""
        self.protect_file_label, self.protect_password_input = self.setup_ui_tab(
            self.protect_tab,
            "1. Selecione o arquivo PDF para proteger:",
            "2. Defina uma senha de proteção:",
            "🔒 Proteger Arquivo",
            self.protect_pdf
        )

    def setup_unprotect_ui(self):
        """Configura a interface da aba 'Desproteger'."""
        self.unprotect_file_label, self.unprotect_password_input = self.setup_ui_tab(
            self.unprotect_tab,
            "1. Selecione o arquivo PDF protegido:",
            "2. Digite a senha do arquivo:",
            "🔓 Desproteger Arquivo",
            self.unprotect_pdf
        )

    def select_file(self, label_to_update):
        """Abre o diálogo para selecionar um arquivo PDF."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar PDF", "", "Arquivos PDF (*.pdf)")
        if file_path:
            label_to_update.setText(file_path)
            self.show_status_message("Arquivo selecionado. Pronto para a próxima ação.")

    def show_status_message(self, message, message_type='info', file_path=None):
        """Exibe uma mensagem na barra de status e o botão 'Abrir Local' se aplicável."""
        # Define a cor da mensagem com base no tipo
        if message_type == 'success':
            self.status_label.setStyleSheet("color: #4CAF50;") # Verde
        elif message_type == 'error':
            self.status_label.setStyleSheet("color: #F44336;") # Vermelho
        else: # info
            self.status_label.setStyleSheet("") # Cor padrão do tema

        self.status_label.setText(message)

        # Lógica para o botão "Abrir Local"
        if file_path:
            self.view_file_button.show()
            # Desconecta sinais antigos para evitar múltiplas chamadas
            try: self.view_file_button.clicked.disconnect() 
            except TypeError: pass # Ignora erro se não houver conexão
            # Conecta o sinal com o novo caminho do arquivo
            self.view_file_button.clicked.connect(lambda: self.open_file_location(file_path))
        else:
            self.view_file_button.hide()

    def open_file_location(self, path):
        """Abre a pasta contendo o arquivo especificado no gerenciador de arquivos do sistema."""
        if sys.platform == 'win32':
            subprocess.run(['explorer', '/select,', os.path.normpath(path)])
        elif sys.platform == 'darwin': # macOS
            subprocess.run(['open', '-R', path])
        else: # linux
            folder = os.path.dirname(path)
            subprocess.run(['xdg-open', folder])

    def protect_pdf(self):
        """Lógica para proteger o PDF."""
        file_path = self.protect_file_label.text()
        password = self.protect_password_input.text()

        if "Nenhum arquivo" in file_path or not file_path:
            self.show_status_message("Erro: Por favor, selecione um arquivo primeiro.", 'error')
            return
        if not password:
            self.show_status_message("Erro: Por favor, digite uma senha.", 'error')
            return

        try:
            self.show_status_message("Processando...", 'info')
            QApplication.processEvents()

            doc = fitz.open(file_path)
            if doc.is_encrypted:
                self.show_status_message("Erro: O arquivo já está protegido.", 'error')
                doc.close()
                return

            output_path = file_path.replace(".pdf", "_protegido.pdf")
            doc.save(
                output_path,
                encryption=fitz.PDF_ENCRYPT_AES_256,
                owner_pw=password,
                user_pw=password,
                permissions=-1,
            )
            doc.close()
            
            self.show_status_message(f"Sucesso! Salvo como '{os.path.basename(output_path)}'", 'success', file_path=output_path)
            self.protect_file_label.setText("Nenhum arquivo selecionado")
            self.protect_password_input.clear()

        except Exception as e:
            self.show_status_message(f"Erro ao processar o arquivo: {e}", 'error')

    def unprotect_pdf(self):
        """Lógica para desproteger o PDF."""
        file_path = self.unprotect_file_label.text()
        password = self.unprotect_password_input.text()

        if "Nenhum arquivo" in file_path or not file_path:
            self.show_status_message("Erro: Por favor, selecione um arquivo primeiro.", 'error')
            return
        if not password:
            self.show_status_message("Erro: Por favor, digite a senha.", 'error')
            return

        try:
            self.show_status_message("Processando...", 'info')
            QApplication.processEvents()

            doc = fitz.open(file_path)
            if not doc.is_encrypted:
                self.show_status_message("Aviso: Este arquivo não está protegido.", 'info')
                doc.close()
                return

            if doc.authenticate(password):
                output_path = file_path.replace(".pdf", "_desprotegido.pdf")
                doc.save(output_path)
                doc.close()

                self.show_status_message(f"Sucesso! Salvo como '{os.path.basename(output_path)}'", 'success', file_path=output_path)
                self.unprotect_file_label.setText("Nenhum arquivo selecionado")
                self.unprotect_password_input.clear()
            else:
                self.show_status_message("Erro: Senha incorreta.", 'error')
                doc.close()

        except Exception as e:
            self.show_status_message(f"Erro ao processar o arquivo: {e}", 'error')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    #qdarktheme.setup_theme()
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = PDFProtectorApp()
    window.show()
    sys.exit(app.exec())