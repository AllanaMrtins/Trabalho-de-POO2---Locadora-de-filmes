<div align="center">

# 🎬 Locadora de Filmes

Sistema para gerenciar os filmes e os aluguéis de uma locadora.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)

*Trabalho da disciplina de Programação Orientada a Objetos II (POO2)*

</div>

---

## 📖 Sobre o projeto

A **Locadora de Filmes** é um programa com interface gráfica feito em **Python** com a biblioteca **PySide6**. Com ele, o atendente consegue cadastrar filmes, alugar para um cliente, registrar a devolução, remover filmes e buscar pelo título.

O projeto foi feito para praticar **Programação Orientada a Objetos**: cada parte do sistema (o filme, a tela principal, as janelas de formulário e o gerenciador de arquivos) é uma classe separada, em seu próprio arquivo.

Na versão atual (2.1.0), os dados ficam salvos no arquivo `filmes.json`, e a leitura e a gravação desse arquivo acontecem em uma **thread** separada, para a tela não travar.

---

##  Funcionalidades

-  **Adicionar filme:** informando título, gênero e ano.
-  **Alugar filme:** informando o nome do cliente e os dias de aluguel (de 1 a 30). Também dá para alugar com duplo clique no filme.
-  **Devolver filme:** deixa o filme disponível de novo.
-  **Remover filme:** tira o filme da lista.
-  **Buscar filme:** a lista é filtrada enquanto você digita o título.
-  **Status:** cada filme aparece como *Disponível* ou *Alugado*.
-  **Dados salvos:** os filmes ficam gravados em `filmes.json` e continuam lá quando o programa é fechado e aberto de novo.
-  **Arquivo em segundo plano:** ler e gravar o arquivo é feito por uma thread, sem travar a tela.
-  **Avisos e confirmações:** o sistema avisa quando nenhum filme foi selecionado e pede confirmação antes de devolver, remover ou sair.

Se o arquivo `filmes.json` não existir, ele é criado automaticamente com 4 filmes de exemplo: *Interestelar*, *Toy Story*, *O Poderoso Chefão* e *Homem-Aranha*.

---

## 🗂️ Estrutura do projeto

| Arquivo | O que faz |
| --- | --- |
| `main.py` | Inicia o programa e abre a janela principal. |
| `modelos.py` | Classe `Filme`, que guarda título, gênero, ano, se está disponível, o cliente e os dias de aluguel. Tem os métodos `para_dicionario` e `de_dicionario`, usados para gravar e ler o JSON. |
| `janela_principal.py` | Classe `JanelaPrincipal`: a tela principal, com a lista, os botões, os menus e a lógica de adicionar, alugar, devolver, remover e buscar. |
| `tarefas.py` | Classe `GerenciadorArquivos`: thread que lê e grava o `filmes.json`. |
| `dialogo_filme.py` | Classe `DialogoFilme`: janelinha para cadastrar um filme. |
| `dialogo_aluguel.py` | Classe `DialogoAluguel`: janelinha para registrar o cliente e os dias do aluguel. |
| `sobre.py` | Classe `JanelaSobre`: janela com informações sobre o sistema. |
| `filmes.json` | Arquivo com os filmes cadastrados. É criado automaticamente na primeira execução. |

---

## 🧠 Como funciona

1. **`Filme`** é o objeto que representa cada filme. Quando ele é criado, começa como *disponível*. Ao ser alugado, guarda o nome do cliente e os dias; ao ser devolvido, esses dados são limpos. Ele também sabe se converter para dicionário e voltar de um dicionário, o que permite gravar no JSON.
2. **`JanelaPrincipal`** guarda uma lista com todos os filmes. Cada botão e item de menu está ligado a um método (por exemplo, o botão *Alugar* chama `alugar_filme()`).
3. **`GerenciadorArquivos`** roda em uma thread própria. A janela não lê nem grava o arquivo: ela coloca um pedido (carregar, salvar ou encerrar) em uma fila, e a thread atende os pedidos um de cada vez, na ordem. Quando termina, a thread avisa a janela por um sinal (`Signal`).
4. **Os diálogos** abrem quando é preciso digitar informações. Se o campo obrigatório (título ou cliente) estiver vazio, a janela não fecha.

### Fluxo do arquivo

1. Ao abrir o programa, a janela pede à thread para carregar o `filmes.json`. Enquanto isso, as operações da lista ficam bloqueadas (`carregamento_concluido`).
2. Quando a leitura termina, a lista é montada e as operações são liberadas.
3. A cada adicionar, alugar, devolver ou remover, a janela pede à thread para salvar.
4. Ao fechar, a janela manda a thread encerrar e espera ela terminar, para não perder nenhuma gravação pendente.

### Conceitos de POO usados

- **Classes e objetos:** `Filme`, `JanelaPrincipal`, `GerenciadorArquivos` e os diálogos.
- **Herança:** a tela principal herda de `QMainWindow`, os diálogos herdam de `QDialog` e o gerenciador de arquivos herda de `QThread`.
- **Encapsulamento e organização:** cada classe cuida de uma tarefa e fica em um arquivo próprio.
- **Sobrescrita de métodos:** `__str__` na classe `Filme`, `closeEvent` na tela principal e `run` no gerenciador de arquivos.
- **Threads e sinais:** a leitura e a gravação rodam em paralelo com a interface, e a comunicação de volta é feita por `Signal`.

---

## 🚀 Como executar

Você precisa ter o [Python 3.10 ou superior](https://www.python.org/downloads/) instalado.

```bash
# 1. Baixe o projeto
git clone https://github.com/AllanaMrtins/Trabalho-de-POO2---Locadora-de-filmes.git
cd Trabalho-de-POO2---Locadora-de-filmes

# 2. Instale a biblioteca da interface
pip install PySide6

# 3. Execute
python main.py
```

---

## 📘 Como usar

- **Adicionar:** clique em *Adicionar Filme*, preencha os dados e confirme.
- **Alugar:** selecione um filme, clique em *Alugar* (ou dê duplo clique), informe o cliente e os dias.
- **Devolver:** selecione um filme alugado, clique em *Devolver* e confirme.
- **Remover:** selecione o filme, clique em *Remover* e confirme.
- **Buscar:** digite o título no campo de busca, no topo da tela.

Tudo o que você fizer é salvo automaticamente em `filmes.json`.

---

## 📝 Histórico de versões

- **2.1.0 (16/10/2026):** leitura e gravação do arquivo em uma thread (`tarefas.py`), com fila de operações, sinais e encerramento seguro ao fechar o programa.
- **2.0.0 (09/10/2026):** dados salvos em `filmes.json`, com `para_dicionario` e `de_dicionario` na classe `Filme`.
- **1.0.0:** interface gráfica, cadastro, busca, aluguel, devolução e remoção, com dados só na memória.

---

## 🔧 Melhorias futuras

- Mostrar o cliente e os dias de aluguel na lista.
- Cadastro de clientes e histórico de aluguéis.
- Trocar o arquivo JSON por um banco de dados.

---

## 👥 Equipe

- **Allana Camily de Sousa Martins**
- **Gabriel dos Santos Silva**
- **Janiele de Jesus Barbosa**

---

 
<div align="center">
Feito pelo grupo para a disciplina de POO2 · Trabalho para fins acadêmicos
</div>
