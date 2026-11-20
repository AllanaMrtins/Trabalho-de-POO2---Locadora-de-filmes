from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
import psycopg

from repositorio import RepositorioFilmes

app = FastAPI(
    title="API da Locadora de Filmes",
    description="Intermediária entre a aplicação desktop e o banco PostgreSQL.",
    version="3.1.0",
)


# ---------- modelos de entrada e saída (validação automática) ----------

class FilmeEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    genero: str = Field(min_length=1, max_length=50)
    ano: int = Field(ge=1900, le=2100)


class AluguelEntrada(BaseModel):
    cliente: str = Field(min_length=1, max_length=200)
    dias: int = Field(ge=1, le=30)


class FilmeSaida(BaseModel):
    id: int
    titulo: str
    genero: str
    ano: int
    disponivel: bool
    cliente: str
    dias: int


# ---------- conexão com o banco (uma por requisição) ----------

def obter_repositorio():
    repositorio = RepositorioFilmes()

    try:
        repositorio.conectar()
    except psycopg.OperationalError:
        raise HTTPException(
            status_code=503,
            detail="Banco de dados indisponível."
        )

    try:
        yield repositorio
    except psycopg.Error:
        repositorio.conexao.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao acessar o banco de dados."
        )
    finally:
        repositorio.fechar()


def exigir_filme(repositorio, id_filme):
    filme = repositorio.obter(id_filme)

    if filme is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado.")

    return filme


# ---------- rotas ----------

@app.get("/saude")
def saude(repositorio: RepositorioFilmes = Depends(obter_repositorio)):
    """Confirma que a API está no ar e consegue falar com o banco."""
    return {"api": "ok", "banco": "ok"}


@app.get("/filmes", response_model=list[FilmeSaida])
def listar_filmes(repositorio: RepositorioFilmes = Depends(obter_repositorio)):
    return repositorio.listar()


@app.get("/filmes/{id_filme}", response_model=FilmeSaida)
def buscar_filme(
    id_filme: int,
    repositorio: RepositorioFilmes = Depends(obter_repositorio)
):
    return exigir_filme(repositorio, id_filme)


@app.post("/filmes", response_model=FilmeSaida, status_code=201)
def cadastrar_filme(
    filme: FilmeEntrada,
    repositorio: RepositorioFilmes = Depends(obter_repositorio)
):
    return repositorio.inserir(filme.titulo, filme.genero, filme.ano)


@app.put("/filmes/{id_filme}/alugar", response_model=FilmeSaida)
def alugar_filme(
    id_filme: int,
    aluguel: AluguelEntrada,
    repositorio: RepositorioFilmes = Depends(obter_repositorio)
):
    exigir_filme(repositorio, id_filme)

    if repositorio.alugar(id_filme, aluguel.cliente, aluguel.dias) == 0:
        raise HTTPException(
            status_code=409, detail="Este filme já está alugado."
        )

    return repositorio.obter(id_filme)


@app.put("/filmes/{id_filme}/devolver", response_model=FilmeSaida)
def devolver_filme(
    id_filme: int,
    repositorio: RepositorioFilmes = Depends(obter_repositorio)
):
    exigir_filme(repositorio, id_filme)

    if repositorio.devolver(id_filme) == 0:
        raise HTTPException(
            status_code=409, detail="Este filme não está alugado."
        )

    return repositorio.obter(id_filme)


@app.delete("/filmes/{id_filme}", status_code=204)
def remover_filme(
    id_filme: int,
    repositorio: RepositorioFilmes = Depends(obter_repositorio)
):
    exigir_filme(repositorio, id_filme)
    repositorio.remover(id_filme)

    return Response(status_code=204)
