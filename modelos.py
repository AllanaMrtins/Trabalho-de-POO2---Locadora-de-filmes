class Filme:
    def __init__(self, codigo, titulo, genero, ano):
        self._codigo = codigo
        self._titulo = titulo
        self._genero = genero
        self._ano = ano
        self._disponivel = True

    def get_codigo(self):
        return self._codigo

    def get_titulo(self):
        return self._titulo

    def get_genero(self):
        return self._genero

    def get_ano(self):
        return self._ano

    def esta_disponivel(self):
        return self._disponivel

    def alugar(self):
        if self._disponivel:
            self._disponivel = False
            return True
        return False

    def devolver(self):
        self._disponivel = True


class Cliente:
    def __init__(self, codigo, nome, telefone):
        self._codigo = codigo
        self._nome = nome
        self._telefone = telefone

    def get_codigo(self):
        return self._codigo

    def get_nome(self):
        return self._nome

    def get_telefone(self):
        return self._telefone


class Aluguel:
    def __init__(self, cliente, filme, data):
        self._cliente = cliente
        self._filme = filme
        self._data = data
        self._ativo = True

    def get_cliente(self):
        return self._cliente

    def get_filme(self):
        return self._filme

    def get_data(self):
        return self._data

    def esta_ativo(self):
        return self._ativo

    def finalizar(self):
        if self._ativo:
            self._ativo = False
            self._filme.devolver()