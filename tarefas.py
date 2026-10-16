
import json
from queue import Queue

from PySide6.QtCore import QThread, Signal


class GerenciadorArquivos(QThread):
    resultado = Signal(str, object, str)

    def __init__(self):
        super().__init__()
        self.fila = Queue()

    def carregar(self, caminho):
        self.fila.put(("carregar", caminho, None))

    def salvar(self, caminho, dados):
        self.fila.put(("salvar", caminho, dados))

    def encerrar(self):
        self.fila.put(("encerrar", None, None))

    def run(self):
        while True:
            operacao, caminho, dados = self.fila.get()

            if operacao == "encerrar":
                break

            try:
                if operacao == "carregar":
                    try:
                        with open(caminho, "r", encoding="utf-8") as arquivo:
                            dados = json.load(arquivo)

                    except FileNotFoundError:
                        dados = None

                    self.resultado.emit("carregar", dados, "")

                elif operacao == "salvar":
                    with open(caminho, "w", encoding="utf-8") as arquivo:
                        json.dump(
                            dados,
                            arquivo,
                            ensure_ascii=False,
                            indent=4
                        )

                    self.resultado.emit("salvar", None, "")

            except Exception as erro:
                self.resultado.emit(operacao, None, str(erro))

