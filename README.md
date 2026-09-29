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
| **PyJWT + pwdlib**  | Autenticação com JWT e hash de senha (Argon2)    |
| **pytest**          | Testes automatizados                             |
| **Ruff**            | Lint e formatação do código                      |

---

## 📁 Estrutura do Projeto

```
.
├── .github/workflows/       # CI: lint e testes a cada push
├── alembic/                 # Migrações do banco de dados
│   ├── env.py
│   └── versions/
├── app/
│   ├── api/
│   │   ├── dependencies.py  # Autenticação e permissões por nível
│   │   ├── main.py          # Instância do FastAPI (app.api.main:app)
│   │   └── routes/          # Rotas da API
│   ├── core/
│   │   ├── configs.py       # Leitura das variáveis de ambiente (.env)
│   │   ├── database.py      # Engine, sessão e Base do SQLAlchemy
│   │   ├── security.py      # Hash de senha e tokens JWT
│   │   └── models/          # Models do SQLAlchemy
│   ├── repositories/        # Acesso ao banco de dados
│   ├── schemas/             # Schemas Pydantic (entrada e saída)
│   ├── scripts/             # Scripts de linha de comando (ex.: criar ADMIN)
│   ├── services/            # Regras de negócio
│   └── utils/
├── tests/                   # Testes com pytest
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
        pip install pytest ruff     # opcional: ferramentas de desenvolvimento
        ```

3. Configure as variáveis de ambiente

    Copie o arquivo de exemplo e ajuste os valores:

    ```bash
    cp .env.example .env      # Linux/macOS
    copy .env.example .env    # Windows
    ```

    | Variável | Descrição |
    |---|---|
    | `DATABASE_URL` | URL do banco. Por padrão, SQLite (`sqlite:///./database.db`) |
    | `SECRET_KEY` | Chave que assina os tokens JWT. Gere uma com `python -c "import secrets; print(secrets.token_hex(32))"` |
    | `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do token, em minutos (padrão: 30) |

    Sem a `DATABASE_URL` ou a `SECRET_KEY`, a aplicação não inicia.

4. Crie as tabelas do banco com o Alembic

    ```bash
    alembic upgrade head
    ```

    O schema do banco é gerenciado apenas pelo Alembic. Ao alterar um model, gere e aplique uma nova migration:

    ```bash
    alembic revision --autogenerate -m "descricao da mudanca"
    alembic upgrade head
    ```

5. Crie o primeiro funcionário ADMIN

    Todas as rotas exigem login, então o primeiro ADMIN é criado pelo terminal (a senha é pedida sem aparecer na tela):

    ```bash
    python -m app.scripts.create_admin --name "Seu Nome" --email voce@empresa.com --cpf 12345678901
    ```

6. Rode a aplicação

    ```bash
    uvicorn app.api.main:app --reload
    ```

7. Acesse a documentação em:

    ```
    http://localhost:8000/docs
    ```

## 📃 Documentação da API

A documentação automática gerada pelo **FastAPI** pode ser acessada via **Swagger UI**, onde é possível testar todos os endpoints, consultar schemas e ver exemplos de requisição e resposta.

No Swagger, clique em **Authorize** e informe o e-mail (no campo `username`) e a senha para fazer login.

## 🔐 Autenticação e permissões

O login é feito em `POST /auth/token`, com e-mail e senha, e retorna um token JWT. Envie o token no header `Authorization: Bearer <token>` em todas as outras rotas.

| Ação                          | JUNIOR | PLENO | SENIOR | ADMIN |
|-------------------------------|:------:|:-----:|:------:|:-----:|
| Consultar funcionários e clientes | ✅ | ✅ | ✅ | ✅ |
| Criar clientes                | ❌ | ✅ | ✅ | ✅ |
| Vincular/desvincular clientes | ❌ | ✅ | ✅ | ✅ |
| Criar funcionários            | ❌ | ❌ | ❌ | ✅ |
| Ver CPF e e-mail sem máscara  | ❌ | ❌ | ❌ | ✅ |

Funcionários **JUNIOR** podem atender no máximo 5 clientes.

## 🧪 Testes e qualidade de código

```bash
pytest                   # roda os testes (banco SQLite em memória)
ruff check .             # lint
ruff format .            # formata o código
```

O workflow em `.github/workflows/ci.yml` roda o lint, a verificação de formatação e os testes a cada push e pull request.