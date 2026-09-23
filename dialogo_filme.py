from PySide6.QtWidgets import (
    QDialog,QVBoxLayout,QFormLayout,QLineEdit,QSpinBox,
    QComboBox,QPushButton,QMessageBox
)


class DialogoFilme(QDialog):
    def __init__(self, filme=None, parent=None):
        super().__init__(parent)

        self._filme = filme
        self._dados_filme = None

        self.setWindowTitle("Cadastro de Filme")

        layout = QVBoxLayout()
        formulario = QFormLayout()

        self.campo_codigo = QLineEdit()
        self.campo_titulo = QLineEdit()

        self.campo_genero = QComboBox()

        self.campo_genero.addItems([
            "Ação",
            "Comédia",
            "Drama",
            "Terror",
            "Romance",
            "Ficção",
            "Animação"
        ])

        self.campo_ano = QSpinBox()
        self.campo_ano.setMinimum(1900)
        self.campo_ano.setMaximum(2100)
        self.campo_ano.setValue(2026)

        formulario.addRow("Código:", self.campo_codigo)
        formulario.addRow("Título:", self.campo_titulo)
        formulario.addRow("Gênero:", self.campo_genero)
        formulario.addRow("Ano:", self.campo_ano)

        layout.addLayout(formulario)

        self.botao_salvar = QPushButton("Salvar")
        self.botao_cancelar = QPushButton("Cancelar")

        layout.addWidget(self.botao_salvar)
        layout.addWidget(self.botao_cancelar)

        self.setLayout(layout)

        self.botao_salvar.clicked.connect(self.salvar)
        self.botao_cancelar.clicked.connect(self.reject)

        if self._filme is not None:
            self.carregar_filme()

    def carregar_filme(self):
        self.campo_codigo.setText(
            str(self._filme.get_codigo())
        )

        self.campo_titulo.setText(
            self._filme.get_titulo()
        )

        indice = self.campo_genero.findText(
            self._filme.get_genero()
        )

        if indice >= 0:
            self.campo_genero.setCurrentIndex(indice)

        self.campo_ano.setValue(
            self._filme.get_ano()
        )

    def salvar(self):
        codigo = self.campo_codigo.text().strip()
        titulo = self.campo_titulo.text().strip()
        genero = self.campo_genero.currentText()
        ano = self.campo_ano.value()

        if codigo == "" or titulo == "":
            QMessageBox.warning(
                self,
                "Atenção",
                "Preencha todos os campos."
            )
            return

        self._dados_filme = {
            "codigo": codigo,
            "titulo": titulo,
            "genero": genero,
            "ano": ano
        }

        self.accept()

    def get_dados_filme(self):
        return self._dados_filme