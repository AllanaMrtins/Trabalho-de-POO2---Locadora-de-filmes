from PySide6.QtWidgets import (
    QMainWindow,QWidget,QVBoxLayout,
    QListWidget,QLabel,QMessageBox
)

from PySide6.QtGui import QAction

from modelos import Filme
from dialogo_filme import DialogoFilme


class JanelaPrincipal(QMainWindow):
    def __init__(self, filmes):
        super().__init__()

        self._filmes = filmes

        self.setWindowTitle("Locadora de Filmes")

        self.criar_catalogo()
        self.criar_menu()
        self.criar_toolbar()

    def criar_catalogo(self):
        widget = QWidget()
        layout = QVBoxLayout()

        titulo = QLabel("Catálogo de Filmes")

        self.lista_filmes = QListWidget()

        layout.addWidget(titulo)
        layout.addWidget(self.lista_filmes)

        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.carregar_catalogo()

    def carregar_catalogo(self):
        self.lista_filmes.clear()

        for filme in self._filmes:

            if filme.esta_disponivel():
                status = "Disponível"
            else:
                status = "Alugado"

            texto = (
                f"{filme.get_titulo()} - "
                f"{filme.get_genero()} - "
                f"{filme.get_ano()} - "
                f"{status}"
            )

            self.lista_filmes.addItem(texto)

    def atualizar_catalogo(self):
        self.carregar_catalogo()

        QMessageBox.information(
            self,
            "Catálogo",
            "Catálogo atualizado com sucesso!"
        )

    def criar_menu(self):
        menu_filmes = self.menuBar().addMenu("Filmes")

        acao_cadastrar = QAction("Cadastrar filme",self)
        acao_editar = QAction("Editar filme",self)
        acao_atualizar = QAction("Atualizar catálogo", self)

        acao_sair = QAction("Sair",self)

        acao_cadastrar.triggered.connect(self.cadastrar_filme)
        acao_editar.triggered.connect(self.editar_filme)
        acao_atualizar.triggered.connect(self.atualizar_catalogo)

        acao_sair.triggered.connect(self.close)

        menu_filmes.addAction(acao_cadastrar)
        menu_filmes.addAction(acao_editar)
        menu_filmes.addAction(acao_atualizar)
        menu_filmes.addSeparator()
        menu_filmes.addAction(acao_sair)

    def criar_toolbar(self):
        toolbar = self.addToolBar("Ferramentas")

        acao_cadastrar = QAction(
            "Cadastrar",self)

        acao_editar = QAction(
            "Editar",self)

        acao_atualizar = QAction(
            "Atualizar",self)

        acao_cadastrar.triggered.connect(self.cadastrar_filme )
        acao_editar.triggered.connect(self.editar_filme)
        acao_atualizar.triggered.connect(self.atualizar_catalogo)

        toolbar.addAction(acao_cadastrar)
        toolbar.addAction(acao_editar)
        toolbar.addAction(acao_atualizar)

    def cadastrar_filme(self):
        dialogo = DialogoFilme(parent=self)

        if dialogo.exec():

            dados = dialogo.get_dados_filme()

            filme = Filme(
                dados["codigo"],
                dados["titulo"],
                dados["genero"],
                dados["ano"] )

            self._filmes.append(filme)

            self.carregar_catalogo()

            QMessageBox.information(
                self,
                "Filme",
                "Filme cadastrado com sucesso!"
            )

    def editar_filme(self):
        indice = self.lista_filmes.currentRow()

        if indice < 0:
            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione um filme."
            )
            return

        filme = self._filmes[indice]

        dialogo = DialogoFilme(
            filme=filme,
            parent=self
        )

        if dialogo.exec():

            dados = dialogo.get_dados_filme()
            filme.set_titulo(dados["titulo"])
            filme.set_genero(dados["genero"])
            filme.set_ano(dados["ano"])
            self.carregar_catalogo()

            QMessageBox.information(
                self,
                "Filme",
                "Filme editado com sucesso!"
            )