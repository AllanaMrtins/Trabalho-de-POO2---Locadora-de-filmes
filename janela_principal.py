from PySide6.QtWidgets import(
    QMainWindow, QWidget, QVBoxLayout, QListWidget, 
    QLabel, QMessageBox
)

from PySide6.QtGui import QAction

class JanelaPrincipal(QMainWindow):
    def __init__(self, filmes):
        super().__init__()
        self._filmes = filmes
        self.setWindowTitle("Locadora de Filmes")
        self.setMinimumSize(700, 500)

        self.criar_catalogo()
        self.criar_menu()
        self.criar_toolbar()

    def criar_catalogo(self):
        widget = QWidget()
        layout = QVBoxLayout()

        titulo = QLabel("Catálogo de Filmes")
        self.lista_filmes = QListWidget()

        for filme in self._filmes:
            status = "Disponível" if filme.esta_disponivel() else "Alugado"
            texto = (
                f"{filme.get_titulo()} - "
                f"{filme.get_genero()} - "
                f"{filme.get_ano()} - "
                f"{status}"
            )
            self.lista_filmes.addItem(texto)

        layout.addWidget(titulo)
        layout.addWidget(self.lista_filmes)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def criar_menu(self):
        menu_filmes = self.menuBar().addMenu("Filmes")
        acao_atualizar = QAction("Atualizar catálogo", self)
        acao_sair = QAction("Sair", self)

        acao_atualizar.triggered.connect(self.atualizar_catalogo)
        acao_sair.triggered.connect(self.close)

        menu_filmes.addAction(acao_atualizar)
        menu_filmes.addSeparator()
        menu_filmes.addAction(acao_sair)

    def criar_toolbar(self):
        toolbar = self.addToolBar("Ferramentas")
        acao_atualizar = QAction("Atualizar", self)
        acao_atualizar.triggered.connect(self.atualizar_catalogo)
        toolbar.addAction(acao_atualizar)

    def atualizar_catalogo(self):
        self.lista_filmes.clear()

        for filme in self._filmes:
            status = "Disponivel" if filme.esta_disponivel() else "Alugado"

            texto = (
                f"{filmes.get_titulo()} - "
                f"{filmes.get_genero()} - "
                f"{filmes.get_ano()} - "
                f"{status}"
            )
            self.lista_filmes.addItem(texto)