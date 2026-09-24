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

O projeto foi feito para praticar **Programação Orientada a Objetos**: cada parte do sistema (o filme, a tela principal e cada janela de formulário) é uma classe separada, em seu próprio arquivo.

---

##  Funcionalidades

-  **Adicionar filme:** informando título, gênero e ano.
-  **Alugar filme:** informando o nome do cliente e os dias de aluguel (de 1 a 30). Também dá para alugar com duplo clique no filme.
-  **Devolver filme:** deixa o filme disponível de novo.
-  **Remover filme:** tira o filme da lista.
-  **Buscar filme:** a lista é filtrada enquanto você digita o título.
-  **Status:** cada filme aparece como *Disponível* ou *Alugado*.
-  **Avisos e confirmações:** o sistema avisa quando nenhum filme foi selecionado e pede confirmação antes de devolver, remover ou sair.

O sistema já começa com 4 filmes de exemplo: *Interestelar*, *Toy Story*, *O Poderoso Chefão* e *Homem-Aranha*.

---

## 🗂️ Estrutura do projeto

| Arquivo | O que faz |
| --- | --- |
| `main.py` | Inicia o programa e abre a janela principal. |
| `modelos.py` | Classe `Filme`, que guarda título, gênero, ano, se está disponível, o cliente e os dias de aluguel. |
| `janela_principal.py` | Classe `JanelaPrincipal`: a tela principal, com a lista, os botões, os menus e a lógica de adicionar, alugar, devolver, remover e buscar. |
| `dialogo_filme.py` | Classe `DialogoFilme`: janelinha para cadastrar um filme. |
| `dialogo_aluguel.py` | Classe `DialogoAluguel`: janelinha para registrar o cliente e os dias do aluguel. |
| `sobre.py` | Classe `JanelaSobre`: janela com informações sobre o sistema. |

---

## 🧠 Como funciona

1. **`Filme`** é o objeto que representa cada filme. Quando ele é criado, começa como *disponível*. Ao ser alugado, guarda o nome do cliente e os dias; ao ser devolvido, esses dados são limpos.
2. **`JanelaPrincipal`** guarda uma lista com todos os filmes. Cada botão e item de menu está ligado a um método (por exemplo, o botão *Alugar* chama `alugar_filme()`).
3. **Os diálogos** abrem quando é preciso digitar informações. Se o campo obrigatório (título ou cliente) estiver vazio, a janela não fecha.

### Conceitos de POO usados

- **Classes e objetos:** `Filme`, `JanelaPrincipal` e os diálogos.
- **Herança:** a tela principal herda de `QMainWindow` e os diálogos herdam de `QDialog`.
- **Encapsulamento e organização:** cada classe cuida de uma tarefa e fica em um arquivo próprio.
- **Sobrescrita de métodos:** `__str__` na classe `Filme` e `closeEvent` na tela principal.

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

---

## 🔧 Melhorias futuras

- Salvar os dados em arquivo ou banco de dados (hoje eles se perdem ao fechar o programa).
- Mostrar o cliente e os dias de aluguel na lista.
- Cadastro de clientes e histórico de aluguéis.

---

## 👥 Equipe

- **Allana**
- **Gabriel**
- **Janiele**

---

 
<div align="center">
Feito pelo grupo para a disciplina de POO2 · Trabalho para fins acadêmicos
</div>