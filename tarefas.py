from queue import Queue

from PySide6.QtCore import QThread, Signal

from cliente_api import ClienteAPI, ErroAPI


class GerenciadorAPI(QThread):
    """Thread que faz as requisições à API, uma de cada vez, em ordem.

    A janela envia pedidos pela fila e recebe o resultado pelo sinal
    `resultado(operacao, dados, erro)`. Assim a interface não trava
    enquanto espera a resposta da rede.
    """

    resultado = Signal(str, object, str)

    def __init__(self):
        super().__init__()
        self.fila = Queue()

    def carregar(self):
        self.fila.put(("carregar", None))

    def inserir(self, dados):
        self.fila.put(("inserir", dados))

    def alugar(self, id_filme, cliente, dias):
        self.fila.put(("alugar", (id_filme, cliente, dias)))

    def devolver(self, id_filme):
        self.fila.put(("devolver", id_filme))

    def remover(self, id_filme):
        self.fila.put(("remover", id_filme))

    def encerrar(self):
        self.fila.put(("encerrar", None))

    def run(self):
        cliente = ClienteAPI()

        while True:
            operacao, dados = self.fila.get()

            if operacao == "encerrar":
                break

            try:
                if operacao == "carregar":
                    saida = cliente.listar()

                elif operacao == "inserir":
                    saida = cliente.inserir(dados)

                elif operacao == "alugar":
                    saida = cliente.alugar(*dados)

                elif operacao == "devolver":
                    saida = cliente.devolver(dados)

                elif operacao == "remover":
                    saida = cliente.remover(dados)

                self.resultado.emit(operacao, saida, "")

            except ErroAPI as erro:
                self.resultado.emit(operacao, None, str(erro))

            except Exception as erro:
                self.resultado.emit(operacao, None, f"Erro inesperado: {erro}")

        cliente.fechar()
