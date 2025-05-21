# Sistema de Gestão de Funcionários e Clientes

## 🚀 Visão Geral

Este projeto é uma API backend construída com **FastAPI** e **SQLAlchemy** que gerencia funcionários, clientes e seus relacionamentos, implementando regras de negócio avançadas e boas práticas modernas.

O sistema permite:

- Cadastro e consulta de funcionários e clientes
- Relacionamento Many-to-Many entre funcionários e clientes
- Controle de acesso baseado no nível de permissão do funcionário
- Máscara de dados sensíveis (CPF, e-mail) nas respostas da API
- Validação de regras de negócio, como limite de clientes para funcionários júnior
- Registro de logs de auditoria para ações críticas
- Filtros, paginação e ordenação nas listagens
- Separação clara entre schemas de entrada e saída com Pydantic

---

## 💡 Funcionalidades Principais

| Funcionalidade                        | Descrição                                                               |
|-------------------------------------|-------------------------------------------------------------------------|
| Gerenciamento de Funcionários        | Criação, atualização, consulta com dados mascarados                      |
| Gerenciamento de Clientes            | Criação, consulta com filtros e paginação                               |
| Relacionamento Funcionário-Cliente   | Funcionários podem atender múltiplos clientes (e vice-versa)           |
| Controle de Permissões               | Acesso a dados sensíveis restrito por nível de acesso                    |
| Máscara de Dados                    | CPF e e-mail exibidos com máscara para proteger privacidade              |
| Regras de Negócio                   | Limite de clientes por funcionário e restrição por nível hierárquico    |
| Logs de Auditoria                   | Registro automático de ações para rastreamento e segurança              |
| API RESTful com FastAPI              | Documentação automática via Swagger UI                                  |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia          | Finalidade                                      |
|---------------------|------------------------------------------------|
| **FastAPI**         | Framework web rápido e moderno para APIs REST   |
| **SQLAlchemy ORM**  | Mapeamento objeto-relacional para banco de dados |
| **SQLite**          | Banco de dados leve para desenvolvimento         |
| **Pydantic**        | Validação e serialização de dados                 |
| **Alembic** (opcional) | Migrações de banco de dados                       |
| **Uvicorn**         | Servidor ASGI para rodar a aplicação FastAPI     |

---

## 📁 Estrutura do Projeto

## ⚙️ Como executar o projeto

1. Clone o repositório

    ```bash
    git clone https://github.com/francisco-duo/Sistema-de-gest-o-de-funcion-rios-e-clientes.git
    cd 
    ```

2. Crie um ambiente virtual, ative e instale

    - Caso esteja utilizando `pip`

        ```
        python -m venv venv

        source venv/bin/activate  # Linux/macOS
        venv\Scripts\activate     # Windows

        pip install -r requirements.txt
        ```
    - Caso esteja utilizando `uv`

        ```
        uv venv create
        uv pip install  # pyproject.toml
        ```

3. Rode a aplicação

    ```
    uvicorn app.main:app --reload
    ```

4. Acesse a documentação em:

    ```
    http://localhost:8000/docs
    ```

## 📃 Documentação da API

A documentação automática gerada pelo **FastAPI** pode ser acessada via **Swagger UI**, onde é possível testar todos os endpoints, consultar schemas e ver exemplos de requisição e resposta.