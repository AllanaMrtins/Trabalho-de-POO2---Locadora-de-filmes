import os

import psycopg
from psycopg.rows import dict_row


def ler_configuracao():
    """Lê os dados de conexão das variáveis de ambiente.

    No contêiner da API, essas variáveis vêm do docker-compose.yml.
    """
    return {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": int(os.environ.get("POSTGRES_PORT", "5432")),
        "dbname": os.environ.get("POSTGRES_DB", "locadora"),
        "user": os.environ.get("POSTGRES_USER", "locadora"),
        "password": os.environ.get("POSTGRES_PASSWORD", "locadora123"),
    }


class RepositorioFilmes:
    """Camada de acesso ao banco: é a única classe que conhece SQL."""

    COLUNAS = "id, titulo, genero, ano, disponivel, cliente, dias"

    def __init__(self, configuracao=None):
        self.configuracao = configuracao or ler_configuracao()
        self.conexao = None

    def conectar(self):
        self.conexao = psycopg.connect(
            **self.configuracao,
            row_factory=dict_row,
            connect_timeout=5
        )

    def fechar(self):
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None

    def listar(self):
        with self.conexao.cursor() as cursor:
            cursor.execute(
                f"SELECT {self.COLUNAS} FROM filmes ORDER BY id"
            )
            return cursor.fetchall()

    def obter(self, id_filme):
        with self.conexao.cursor() as cursor:
            cursor.execute(
                f"SELECT {self.COLUNAS} FROM filmes WHERE id = %s",
                (id_filme,)
            )
            return cursor.fetchone()

    def inserir(self, titulo, genero, ano):
        with self.conexao.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO filmes (titulo, genero, ano) "
                f"VALUES (%s, %s, %s) RETURNING {self.COLUNAS}",
                (titulo, genero, ano)
            )
            filme = cursor.fetchone()

        self.conexao.commit()
        return filme

    def alugar(self, id_filme, cliente, dias):
        """Aluga só se o filme estiver disponível. Retorna linhas alteradas."""
        with self.conexao.cursor() as cursor:
            cursor.execute(
                "UPDATE filmes SET disponivel = FALSE, cliente = %s, dias = %s "
                "WHERE id = %s AND disponivel = TRUE",
                (cliente, dias, id_filme)
            )
            alteradas = cursor.rowcount

        self.conexao.commit()
        return alteradas

    def devolver(self, id_filme):
        """Devolve só se o filme estiver alugado. Retorna linhas alteradas."""
        with self.conexao.cursor() as cursor:
            cursor.execute(
                "UPDATE filmes SET disponivel = TRUE, cliente = '', dias = 0 "
                "WHERE id = %s AND disponivel = FALSE",
                (id_filme,)
            )
            alteradas = cursor.rowcount

        self.conexao.commit()
        return alteradas

    def remover(self, id_filme):
        with self.conexao.cursor() as cursor:
            cursor.execute("DELETE FROM filmes WHERE id = %s", (id_filme,))
            removidas = cursor.rowcount

        self.conexao.commit()
        return removidas
