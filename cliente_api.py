import os

import requests


class ErroAPI(Exception):
    """Erro ao falar com a API (rede fora do ar ou resposta de erro)."""


def ler_url_api(caminho=".env"):
    """Lê API_URL do ambiente ou do arquivo .env (padrão: localhost:8000)."""
    if "API_URL" not in os.environ and os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()

                if linha.startswith("API_URL="):
                    os.environ["API_URL"] = linha.split("=", 1)[1].strip()

    return os.environ.get("API_URL", "http://localhost:8000").rstrip("/")


class ClienteAPI:
    """Faz as requisições HTTP à API. É a única classe que conhece a rede."""

    def __init__(self, url_base=None, timeout=5):
        self.url_base = url_base or ler_url_api()
        self.timeout = timeout
        self.sessao = requests.Session()

    def _requisitar(self, metodo, caminho, **argumentos):
        try:
            resposta = self.sessao.request(
                metodo,
                self.url_base + caminho,
                timeout=self.timeout,
                **argumentos
            )
        except requests.ConnectionError:
            raise ErroAPI(
                f"Não foi possível conectar à API em {self.url_base}."
            )
        except requests.Timeout:
            raise ErroAPI("A API demorou demais para responder.")

        if resposta.status_code >= 400:
            raise ErroAPI(self._mensagem_de_erro(resposta))

        if resposta.status_code == 204:
            return None

        return resposta.json()

    @staticmethod
    def _mensagem_de_erro(resposta):
        try:
            detalhe = resposta.json()["detail"]
        except (ValueError, KeyError):
            return f"Erro {resposta.status_code} na API."

        if isinstance(detalhe, list):
            # erro de validação (422): junta as mensagens dos campos
            return "; ".join(item.get("msg", "") for item in detalhe)

        return str(detalhe)

    def listar(self):
        return self._requisitar("GET", "/filmes")

    def inserir(self, dados):
        return self._requisitar("POST", "/filmes", json=dados)

    def alugar(self, id_filme, cliente, dias):
        return self._requisitar(
            "PUT",
            f"/filmes/{id_filme}/alugar",
            json={"cliente": cliente, "dias": dias}
        )

    def devolver(self, id_filme):
        return self._requisitar("PUT", f"/filmes/{id_filme}/devolver")

    def remover(self, id_filme):
        return self._requisitar("DELETE", f"/filmes/{id_filme}")

    def fechar(self):
        self.sessao.close()
