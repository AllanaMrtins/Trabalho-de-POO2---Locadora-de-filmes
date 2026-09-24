from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLabel,
    QPushButton,
    QMessageBox,
    QLineEdit
)

from PySide6.QtGui import QAction

from modelos import Filme
from dialogo_filme import DialogoFilme
from dialogo_aluguel import DialogoAluguel
from sobre import JanelaSobre


class JanelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.filmes = []

        self.setWindowTitle("Locadora de Filmes")
        self.setMinimumSize(850, 550)

        self.criar_interface()
        self.criar_menu()
        self.criar_barra_ferramentas()
        self.carregar_filmes()

    def criar_interface(self):
        widget_central = QWidget()
        layout_principal = QVBoxLayout()

        titulo = QLabel("Locadora de Filmes")
        titulo.setStyleSheet("font-size: 26px; font-weight: bold;")

        subtitulo = QLabel("Gerencie os filmes disponíveis na locadora.")

        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar filme pelo título...")

        self.lista_filmes = QListWidget()

        self.lista_filmes.itemDoubleClicked.connect(self.alugar_filme)

        botoes = QHBoxLayout()

        botao_adicionar = QPushButton("Adicionar Filme")
        botao_alugar = QPushButton("Alugar")
        botao_devolver = QPushButton("Devolver")
        botao_remover = QPushButton("Remover")

        botao_adicionar.clicked.connect(self.adicionar_filme)
        botao_alugar.clicked.connect(self.alugar_filme)
        botao_devolver.clicked.connect(self.devolver_filme)
        botao_remover.clicked.connect(self.remover_filme)

        self.campo_busca.textChanged.connect(self.buscar_filme)

        botoes.addWidget(botao_adicionar)
        botoes.addWidget(botao_alugar)
        botoes.addWidget(botao_devolver)
        botoes.addWidget(botao_remover)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)
        layout_principal.addWidget(self.campo_busca)
        layout_principal.addWidget(self.lista_filmes)
        layout_principal.addLayout(botoes)

        widget_central.setLayout(layout_principal)

        self.setCentralWidget(widget_central)

        self.statusBar().showMessage("Sistema pronto.")

    def criar_menu(self):
        menu_arquivo = self.menuBar().addMenu("Arquivo")

        acao_adicionar = QAction("Adicionar filme", self)
        acao_sair = QAction("Sair", self)

        acao_adicionar.triggered.connect(self.adicionar_filme)
        acao_sair.triggered.connect(self.close)

        menu_arquivo.addAction(acao_adicionar)
        menu_arquivo.addSeparator()
        menu_arquivo.addAction(acao_sair)

        menu_filmes = self.menuBar().addMenu("Filmes")

        acao_alugar = QAction("Alugar filme", self)
        acao_devolver = QAction("Devolver filme", self)
        acao_remover = QAction("Remover filme", self)

        acao_alugar.triggered.connect(self.alugar_filme)
        acao_devolver.triggered.connect(self.devolver_filme)
        acao_remover.triggered.connect(self.remover_filme)

        menu_filmes.addAction(acao_alugar)
        menu_filmes.addAction(acao_devolver)
        menu_filmes.addAction(acao_remover)

        menu_ajuda = self.menuBar().addMenu("Ajuda")

        acao_sobre = QAction("Sobre", self)
        acao_sobre.triggered.connect(self.mostrar_sobre)

        menu_ajuda.addAction(acao_sobre)

    def criar_barra_ferramentas(self):
        barra = self.addToolBar("Barra de ferramentas")

    def carregar_filmes(self):
        self.filmes.append(Filme("Interestelar", "Ficção", 2014))
        self.filmes.append(Filme("Toy Story", "Animação", 1995))
        self.filmes.append(Filme("O Poderoso Chefão", "Drama", 1972))
        self.filmes.append(Filme("Homem-Aranha", "Ação", 2002))

        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista_filmes.clear()

        for filme in self.filmes:
            self.lista_filmes.addItem(str(filme))

        self.statusBar().showMessage(f"{len(self.filmes)} filme(s) cadastrado(s).")

    def adicionar_filme(self):
        dialogo = DialogoFilme(self)

        if dialogo.exec():
            titulo, genero, ano = dialogo.obter_dados()

            filme = Filme(titulo, genero, ano)

            self.filmes.append(filme)

            self.atualizar_lista()

            QMessageBox.information(self, "Sucesso", "Filme adicionado com sucesso.")

    def obter_filme_selecionado(self):
        indice = self.lista_filmes.currentRow()

        if indice < 0:
            return None

        texto = self.lista_filmes.item(indice).text()

        for filme in self.filmes:
            if str(filme) == texto:
                return filme

        return None

    def alugar_filme(self):
        filme = self.obter_filme_selecionado()

        if filme is None:
            QMessageBox.warning(self, "Aviso", "Selecione um filme.")
            return

        if not filme.disponivel:
            QMessageBox.warning(self, "Aviso", "Este filme já está alugado.")
            return

        dialogo = DialogoAluguel(filme, self)

        if dialogo.exec():
            cliente, dias = dialogo.obter_dados()

            filme.disponivel = False
            filme.cliente = cliente
            filme.dias = dias

            self.atualizar_lista()

            QMessageBox.information(
                self,
                "Aluguel realizado",
                f"Filme: {filme.titulo}\n"
                f"Cliente: {cliente}\n"
                f"Dias: {dias}\n\n"
                "Aluguel realizado com sucesso."
            )

    def devolver_filme(self):
        filme = self.obter_filme_selecionado()

        if filme is None:
            QMessageBox.warning(self, "Aviso", "Selecione um filme.")
            return

        if filme.disponivel:
            QMessageBox.information(self, "Aviso", "Este filme já está disponível.")
            return

        resposta = QMessageBox.question(
            self,
            "Devolver filme",
            f"Deseja devolver '{filme.titulo}'?"
        )

        if resposta == QMessageBox.Yes:
            filme.disponivel = True
            filme.cliente = ""
            filme.dias = 0

            self.atualizar_lista()

            QMessageBox.information(
                self,
                "Devolução",
                "Filme devolvido com sucesso."
            )

    def remover_filme(self):
        filme = self.obter_filme_selecionado()

        if filme is None:
            QMessageBox.warning(self, "Aviso", "Selecione um filme.")
            return

        resposta = QMessageBox.question(
            self,
            "Remover filme",
            f"Deseja remover '{filme.titulo}'?"
        )

        if resposta == QMessageBox.Yes:
            self.filmes.remove(filme)
            self.atualizar_lista()

            QMessageBox.information(
                self,
                "Remoção",
                "Filme removido com sucesso."
            )

    def buscar_filme(self, texto):
        texto = texto.lower()

        self.lista_filmes.clear()

        for filme in self.filmes:
            if texto in filme.titulo.lower():
                self.lista_filmes.addItem(str(filme))

    def mostrar_sobre(self):
        janela = JanelaSobre(self)
        janela.exec()

    def closeEvent(self, evento):
        resposta = QMessageBox.question(
            self,
            "Sair",
            "Deseja realmente sair?"
        )

        if resposta == QMessageBox.Yes:
            evento.accept()
        else:
            evento.ignore()