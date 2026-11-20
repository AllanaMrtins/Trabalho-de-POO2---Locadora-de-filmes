-- Executado automaticamente pelo contêiner na primeira inicialização
-- (quando o volume de dados ainda está vazio).

CREATE TABLE IF NOT EXISTS filmes (
    id          SERIAL PRIMARY KEY,
    titulo      VARCHAR(200) NOT NULL,
    genero      VARCHAR(50)  NOT NULL,
    ano         INTEGER      NOT NULL CHECK (ano BETWEEN 1900 AND 2100),
    disponivel  BOOLEAN      NOT NULL DEFAULT TRUE,
    cliente     VARCHAR(200) NOT NULL DEFAULT '',
    dias        INTEGER      NOT NULL DEFAULT 0 CHECK (dias BETWEEN 0 AND 30),
    CONSTRAINT aluguel_coerente CHECK (
        (disponivel AND cliente = '' AND dias = 0)
        OR (NOT disponivel AND cliente <> '' AND dias > 0)
    )
);

INSERT INTO filmes (titulo, genero, ano) VALUES
    ('Interestelar',      'Ficção',   2014),
    ('Toy Story',         'Animação', 1995),
    ('O Poderoso Chefão', 'Drama',    1972),
    ('Homem-Aranha',      'Ação',     2002);
