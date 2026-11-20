
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

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from modelos import Filme
from dialogo_filme import DialogoFilme
from dialogo_aluguel import DialogoAluguel
from sobre import JanelaSobre
from tarefas import GerenciadorAPI


class JanelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.filmes = []
        self.carregamento_concluido = False

        self.setWindowTitle("Locadora de Filmes")
        self.setMinimumSize(850, 550)

        self.criar_interface()
        self.criar_menu()
        self.criar_barra_ferramentas()

        self.tarefas_api = GerenciadorAPI()
        self.tarefas_api.resultado.connect(
            self.tratar_resultado_api
        )
        self.tarefas_api.start()

        self.recarregar_filmes()

    def criar_interface(self):
        widget_central = QWidget()
        layout_principal = QVBoxLayout()

        titulo = QLabel("Locadora de Filmes")
        titulo.setStyleSheet("font-size: 26px; font-weight: bold;")

        subtitulo = QLabel("Gerencie os filmes disponíveis na locadora.")

        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText(
            "Buscar filme pelo título..."
        )

        self.lista_filmes = QListWidget()
        self.lista_filmes.itemDoubleClicked.connect(
            self.alugar_filme
        )

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
        acao_recarregar = QAction("Recarregar da API", self)
        acao_sair = QAction("Sair", self)

        acao_adicionar.triggered.connect(self.adicionar_filme)
        acao_recarregar.triggered.connect(self.recarregar_filmes)
        acao_sair.triggered.connect(self.close)

        menu_arquivo.addAction(acao_adicionar)
        menu_arquivo.addAction(acao_recarregar)
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
        self.addToolBar("Barra de ferramentas")

    def recarregar_filmes(self):
        self.statusBar().showMessage("Carregando filmes da API...")
        self.tarefas_api.carregar()

    def carregar_filmes(self, registros):
        self.filmes = [Filme.de_dicionario(r) for r in registros]

        self.carregamento_concluido = True
        self.atualizar_lista()

    def tratar_resultado_api(self, operacao, dados, erro):
        if erro:
            self.statusBar().showMessage("Erro ao falar com a API.")

            QMessageBox.warning(
                self,
                "Erro de comunicação",
                "Não foi possível concluir a operação.\n"
                "Verifique se a API e o banco estão em execução "
                "(docker compose up -d).\n\n" + erro
            )

            # após um erro, sincroniza a lista com o que está no servidor
            if self.carregamento_concluido and operacao != "carregar":
                self.tarefas_api.carregar()

            return

        if operacao == "carregar":
            self.carregar_filmes(dados)
            return

        mensagens = {
            "inserir": ("Sucesso", "Filme adicionado com sucesso."),
            "devolver": ("Devolução", "Filme devolvido com sucesso."),
            "remover": ("Remoção", "Filme removido com sucesso."),
        }

        if operacao == "alugar":
            QMessageBox.information(
                self,
                "Aluguel realizado",
                f"Filme: {dados['titulo']}\n"
                f"Cliente: {dados['cliente']}\n"
                f"Dias: {dados['dias']}\n\n"
                "Aluguel realizado com sucesso."
            )
        else:
            titulo, texto = mensagens[operacao]
            QMessageBox.information(self, titulo, texto)

        # recarrega para refletir o estado real do servidor
        self.tarefas_api.carregar()

    def atualizar_lista(self):
        self.mostrar_filmes(self.campo_busca.text())

        self.statusBar().showMessage(
            f"{len(self.filmes)} filme(s) cadastrado(s)."
        )

    def mostrar_filmes(self, texto=""):
        texto = texto.lower()

        self.lista_filmes.clear()

        for filme in self.filmes:
            if texto in filme.titulo.lower():
                self.lista_filmes.addItem(str(filme))
                item = self.lista_filmes.item(self.lista_filmes.count() - 1)
                item.setData(Qt.UserRole, filme.id)

    def adicionar_filme(self):
        if not self.carregamento_concluido:
            return

        dialogo = DialogoFilme(self)

        if dialogo.exec():
            titulo, genero, ano = dialogo.obter_dados()

            self.tarefas_api.inserir(
                {"titulo": titulo, "genero": genero, "ano": ano}
            )

    def obter_filme_selecionado(self):
        item = self.lista_filmes.currentItem()

        if item is None:
            return None

        id_filme = item.data(Qt.UserRole)

        for filme in self.filmes:
            if filme.id == id_filme:
                return filme

        return None

    def alugar_filme(self):
        if not self.carregamento_concluido:
            return

        filme = self.obter_filme_selecionado()

        if filme is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Selecione um filme."
            )
            return

        if not filme.disponivel:
            QMessageBox.warning(
                self,
                "Aviso",
                "Este filme já está alugado."
            )
            return

        dialogo = DialogoAluguel(filme, self)

        if dialogo.exec():
            cliente, dias = dialogo.obter_dados()

            self.tarefas_api.alugar(filme.id, cliente, dias)

    def devolver_filme(self):
        if not self.carregamento_concluido:
            return

        filme = self.obter_filme_selecionado()

        if filme is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Selecione um filme."
            )
            return

        if filme.disponivel:
            QMessageBox.information(
                self,
                "Aviso",
                "Este filme já está disponível."
            )
            return

        resposta = QMessageBox.question(
            self,
            "Devolver filme",
            f"Deseja devolver '{filme.titulo}'?"
        )

        if resposta == QMessageBox.Yes:
            self.tarefas_api.devolver(filme.id)

    def remover_filme(self):
        if not self.carregamento_concluido:
            return

        filme = self.obter_filme_selecionado()

        if filme is None:
            QMessageBox.warning(
                self,
                "Aviso",
                "Selecione um filme."
            )
            return

        resposta = QMessageBox.question(
            self,
            "Remover filme",
            f"Deseja remover '{filme.titulo}'?"
        )

        if resposta == QMessageBox.Yes:
            self.tarefas_api.remover(filme.id)

    def buscar_filme(self, texto):
        self.mostrar_filmes(texto)

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
            self.tarefas_api.encerrar()
            self.tarefas_api.wait()
            evento.accept()
        else:
            evento.ignore()
