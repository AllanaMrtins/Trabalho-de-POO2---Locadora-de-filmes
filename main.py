import sys

from PySide6.QtWidgets import QApplication

from modelos import Filme, Cliente
from janela_principal import JanelaPrincipal


def main():
    app = QApplication(sys.argv)

    filmes = [
        Filme(1, "Interestelar", "Ficção", 2014),
        Filme(2, "Vingadores", "Ação", 2019),
        Filme(3, "Toy Story", "Animação", 1995)
    ]

    clientes = [
        Cliente(1, "Allana", "99999-1111"),
        Cliente(2, "Ana", "99999-2222"),
        Cliente(3, "Maria", "99999-3333")
    ]

    janela = JanelaPrincipal(filmes)

    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()