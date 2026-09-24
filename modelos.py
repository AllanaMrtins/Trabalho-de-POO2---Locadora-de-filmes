class Filme:
    def __init__(self, titulo, genero, ano):
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.disponivel = True
        self.cliente = ""
        self.dias = 0

    def __str__(self):
        if self.disponivel:
            status = "Disponível"
        else:
            status = "Alugado"

        return f"{self.titulo} | {self.genero} | {self.ano} | {status}"