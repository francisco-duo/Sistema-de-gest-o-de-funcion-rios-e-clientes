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
| **Alembic**         | Migrações de banco de dados                      |
| **Uvicorn**         | Servidor ASGI para rodar a aplicação FastAPI     |

---

## 📁 Estrutura do Projeto

```
.
├── alembic/                 # Migrações do banco de dados
│   ├── env.py
│   └── versions/
├── app/
│   ├── api/
│   │   ├── main.py          # Instância do FastAPI (app.api.main:app)
│   │   └── routes/          # Rotas da API
│   ├── core/
│   │   ├── configs.py       # Leitura das variáveis de ambiente (.env)
│   │   ├── database.py      # Engine, sessão e Base do SQLAlchemy
│   │   └── models/          # Models do SQLAlchemy
│   ├── repositories/        # Acesso ao banco de dados
│   ├── schemas/             # Schemas Pydantic (entrada e saída)
│   ├── services/            # Regras de negócio
│   └── utils/
├── .env.example             # Modelo do arquivo .env
├── alembic.ini
├── pyproject.toml           # Dependências (uv)
├── requirements.txt         # Dependências (pip), gerado a partir do uv.lock
└── uv.lock
```

---

## ⚙️ Como executar o projeto

1. Clone o repositório

    ```bash
    git clone https://github.com/francisco-duo/Sistema-de-gest-o-de-funcion-rios-e-clientes.git
    cd Sistema-de-gest-o-de-funcion-rios-e-clientes
    ```

2. Crie o ambiente virtual e instale as dependências

    - Com `uv` (recomendado)

        ```bash
        uv sync
        ```

        O `uv sync` cria o `.venv` e instala as versões exatas do `uv.lock`. Com `uv`, rode os comandos dos próximos passos com o prefixo `uv run` (ex.: `uv run alembic upgrade head`).

    - Com `pip`

        ```bash
        python -m venv .venv

        source .venv/bin/activate   # Linux/macOS
        .venv\Scripts\activate      # Windows

        pip install -r requirements.txt
        ```

3. Configure as variáveis de ambiente

    Copie o arquivo de exemplo e ajuste a `DATABASE_URL` se necessário:

    ```bash
    cp .env.example .env      # Linux/macOS
    copy .env.example .env    # Windows
    ```

    Por padrão, o projeto usa SQLite (`DATABASE_URL=sqlite:///./database.db`). Sem a `DATABASE_URL`, a aplicação não inicia.

4. Crie as tabelas do banco com o Alembic

    ```bash
    alembic upgrade head
    ```

    O schema do banco é gerenciado apenas pelo Alembic. Ao alterar um model, gere e aplique uma nova migration:

    ```bash
    alembic revision --autogenerate -m "descricao da mudanca"
    alembic upgrade head
    ```

5. Rode a aplicação

    ```bash
    uvicorn app.api.main:app --reload
    ```

6. Acesse a documentação em:

    ```
    http://localhost:8000/docs
    ```

## 📃 Documentação da API

A documentação automática gerada pelo **FastAPI** pode ser acessada via **Swagger UI**, onde é possível testar todos os endpoints, consultar schemas e ver exemplos de requisição e resposta.