# Sistema de Gestão de Funcionários e Clientes

[![CI](https://github.com/francisco-duo/Sistema-de-gest-o-de-funcion-rios-e-clientes/actions/workflows/ci.yml/badge.svg)](https://github.com/francisco-duo/Sistema-de-gest-o-de-funcion-rios-e-clientes/actions/workflows/ci.yml)

## 🚀 Visão Geral

API backend construída com **FastAPI** e **SQLAlchemy** para gerenciar funcionários, clientes e o vínculo entre eles, com autenticação JWT, permissões por nível de acesso e log de auditoria.

O sistema permite:

- Cadastro e consulta de funcionários e clientes
- Vínculo Many-to-Many entre funcionários e clientes
- Login com JWT e controle de acesso pelo nível do funcionário (JUNIOR, PLENO, SENIOR, ADMIN)
- Máscara de dados sensíveis (CPF e e-mail) nas respostas, exceto para ADMIN
- Regras de negócio, como o limite de clientes para funcionários JUNIOR
- Log de auditoria das ações que alteram dados, com o autor de cada ação
- Filtros e paginação nas listagens
- Schemas de entrada e saída separados com Pydantic

---

## 💡 Funcionalidades Principais

| Funcionalidade                     | Descrição                                                                 |
|------------------------------------|---------------------------------------------------------------------------|
| Gerenciamento de Funcionários      | Criação (só ADMIN), consulta e listagem com filtros por nome, nível e categoria |
| Gerenciamento de Clientes          | Criação, consulta e listagem com filtro por nome e paginação              |
| Vínculo Funcionário-Cliente        | Funcionários atendem vários clientes (e vice-versa); vincular e desvincular |
| Autenticação                       | Login com e-mail e senha, token JWT e senha salva com hash Argon2          |
| Controle de Permissões             | Cada ação exige um nível mínimo de acesso                                 |
| Máscara de Dados                   | CPF e e-mail mascarados para quem não é ADMIN                              |
| Validação de Documentos            | CPF e CNPJ aceitos com ou sem máscara e salvos só com dígitos             |
| Regras de Negócio                  | Limite de 5 clientes para JUNIOR, sem duplicidade de e-mail, CPF ou CNPJ  |
| Logs de Auditoria                  | Registro automático de criações e vínculos, na mesma transação da ação    |
| Documentação Automática            | Swagger UI e ReDoc gerados pelo FastAPI                                   |

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia          | Finalidade                                       |
|---------------------|--------------------------------------------------|
| **FastAPI**         | Framework web para APIs REST                     |
| **SQLAlchemy 2.0**  | Mapeamento objeto-relacional (ORM)               |
| **SQLite**          | Banco de dados leve para desenvolvimento         |
| **Pydantic**        | Validação e serialização de dados                |
| **Alembic**         | Migrações do banco de dados                      |
| **Uvicorn**         | Servidor ASGI para rodar a aplicação             |
| **PyJWT + pwdlib**  | Tokens JWT e hash de senha (Argon2)              |
| **pytest**          | Testes automatizados                             |
| **Ruff**            | Lint e formatação do código                      |
| **uv**              | Gerenciamento do ambiente e das dependências     |

---

## 📁 Estrutura do Projeto

```
.
├── .github/workflows/       # CI: lint, formatação e testes a cada push
├── alembic/                 # Migrações do banco de dados
│   ├── env.py
│   └── versions/
├── app/
│   ├── api/
│   │   ├── dependencies.py  # Autenticação e permissões por nível
│   │   ├── main.py          # Instância do FastAPI (app.api.main:app)
│   │   └── routes/          # Rotas: auth, employees e clients
│   ├── core/
│   │   ├── configs.py       # Leitura das variáveis de ambiente (.env)
│   │   ├── database.py      # Engine, sessão (get_db) e Base do SQLAlchemy
│   │   ├── security.py      # Hash de senha e tokens JWT
│   │   └── models/          # Models do SQLAlchemy
│   ├── repositories/        # Acesso ao banco de dados
│   ├── schemas/             # Schemas Pydantic (entrada e saída)
│   ├── scripts/             # Scripts de linha de comando (criar ADMIN)
│   ├── services/            # Regras de negócio e auditoria
│   └── utils/               # Máscaras e validação de CPF/CNPJ
├── tests/                   # Testes com pytest
├── .env.example             # Modelo do arquivo .env
├── alembic.ini
├── pyproject.toml           # Dependências e configuração do pytest e do ruff
├── requirements.txt         # Dependências para pip, gerado a partir do uv.lock
└── uv.lock
```

A requisição passa pelas camadas nesta ordem: **routes** (HTTP e permissões) → **services** (regras de negócio e auditoria) → **repositories** (consultas ao banco) → **models**.

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

        O `uv sync` cria o `.venv` e instala as versões exatas do `uv.lock`, incluindo as ferramentas de desenvolvimento. Com `uv`, rode os comandos dos próximos passos com o prefixo `uv run` (ex.: `uv run alembic upgrade head`).

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

    | Variável | Obrigatória | Descrição |
    |---|:---:|---|
    | `DATABASE_URL` | ✅ | URL do banco. Por padrão, SQLite (`sqlite:///./database.db`) |
    | `SECRET_KEY` | ✅ | Chave que assina os tokens JWT. Gere uma com `python -c "import secrets; print(secrets.token_hex(32))"` |
    | `ACCESS_TOKEN_EXPIRE_MINUTES` | ❌ | Validade do token, em minutos (padrão: 30) |

    Sem a `DATABASE_URL` ou a `SECRET_KEY`, a aplicação não inicia e mostra uma mensagem explicando o que falta.

4. Crie as tabelas do banco com o Alembic

    ```bash
    alembic upgrade head
    ```

5. Crie o primeiro funcionário ADMIN

    Todas as rotas exigem login, então o primeiro ADMIN é criado pelo terminal. A senha (mínimo de 8 caracteres) é pedida sem aparecer na tela:

    ```bash
    python -m app.scripts.create_admin --name "Seu Nome" --email voce@empresa.com --cpf 12345678901
    ```

6. Rode a aplicação

    ```bash
    uvicorn app.api.main:app --reload
    ```

7. Acesse a documentação em `http://localhost:8000/docs` (Swagger UI) ou `http://localhost:8000/redoc` (ReDoc).

    No Swagger, clique em **Authorize** e informe o e-mail (no campo `username`) e a senha.

---

## 🔌 Endpoints

| Método | Rota | Descrição | Nível mínimo |
|---|---|---|---|
| `POST` | `/auth/token` | Login com e-mail e senha; retorna o token JWT | — |
| `GET` | `/auth/me` | Dados do funcionário autenticado | Qualquer |
| `GET` | `/employees` | Lista funcionários (filtros: `name`, `level`, `category_id`) | Qualquer |
| `POST` | `/employees` | Cria um funcionário | ADMIN |
| `GET` | `/employees/{id}` | Busca um funcionário | Qualquer |
| `GET` | `/employees/{id}/clients` | Lista os clientes do funcionário | Qualquer |
| `POST` | `/employees/{id}/clients` | Vincula um cliente (`{"client_id": 1}`) | PLENO |
| `DELETE` | `/employees/{id}/clients/{client_id}` | Desvincula um cliente | PLENO |
| `GET` | `/clients` | Lista clientes (filtro: `name`) | Qualquer |
| `POST` | `/clients` | Cria um cliente | PLENO |
| `GET` | `/clients/{id}` | Busca um cliente | Qualquer |

**Paginação:** as listagens aceitam `skip` (padrão 0) e `limit` (padrão 20, máximo 100) e respondem neste formato:

```json
{
  "items": [
    { "id": 1, "name": "ACME Ltda", "email": "c*****o@acme.com", "cnpj": "12.345.678/0001-90" }
  ],
  "total": 1,
  "skip": 0,
  "limit": 20
}
```

**Exemplo:** criar um funcionário (como ADMIN):

```bash
curl -X POST http://localhost:8000/employees \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ana Souza", "email": "ana@empresa.com", "cpf": "123.456.789-01", "password": "senha-segura-123", "level": "PLENO"}'
```

**Códigos de erro:**

| Código | Quando acontece |
|---|---|
| `401` | Sem token, token inválido ou expirado, ou login com e-mail/senha errados |
| `403` | O nível do funcionário não permite a operação |
| `404` | Funcionário, cliente ou categoria não encontrado, ou vínculo inexistente |
| `409` | E-mail, CPF ou CNPJ já cadastrado, ou cliente já vinculado |
| `422` | Dados inválidos (e-mail, CPF/CNPJ, senha curta, nível inexistente) ou limite de clientes do JUNIOR atingido |

---

## 🔐 Autenticação e permissões

O login é feito em `POST /auth/token`, com e-mail e senha, e retorna um token JWT. Envie o token no header `Authorization: Bearer <token>` em todas as outras rotas.

| Ação                              | JUNIOR | PLENO | SENIOR | ADMIN |
|-----------------------------------|:------:|:-----:|:------:|:-----:|
| Consultar funcionários e clientes | ✅ | ✅ | ✅ | ✅ |
| Criar clientes                    | ❌ | ✅ | ✅ | ✅ |
| Vincular/desvincular clientes     | ❌ | ✅ | ✅ | ✅ |
| Criar funcionários                | ❌ | ❌ | ❌ | ✅ |
| Ver CPF e e-mail sem máscara      | ❌ | ❌ | ❌ | ✅ |

Para quem não é ADMIN, o CPF aparece como `***.456.789-**` e o e-mail como `a*******a@empresa.com`. O CNPJ, por ser um dado público de empresa, aparece sempre completo e formatado.

---

## 📋 Regras de negócio

- Um funcionário **JUNIOR** pode atender no máximo **5 clientes**. PLENO, SENIOR e ADMIN não têm limite.
- E-mail e CPF são únicos entre funcionários; e-mail e CNPJ são únicos entre clientes.
- CPF e CNPJ são aceitos com ou sem máscara (`123.456.789-01` ou `12345678901`) e salvos só com dígitos.
- Novos funcionários são **JUNIOR** quando o nível não é informado.
- A senha precisa ter pelo menos 8 caracteres e é salva com hash Argon2; ela nunca aparece nas respostas.

---

## 📝 Auditoria

As ações que alteram dados geram um registro na tabela `logs`, gravado na mesma transação da ação (se a ação falhar, o log também não é gravado):

| Ação | Quando |
|---|---|
| `CREATE_EMPLOYEE` | Criação de funcionário |
| `CREATE_CLIENT` | Criação de cliente |
| `LINK_CLIENT` | Vínculo de cliente a funcionário |
| `UNLINK_CLIENT` | Remoção de vínculo |

Cada registro guarda o autor (`employee:<id>`, ou `system` para ações feitas por script) e a data/hora, que no SQLite é gravada em UTC. Os logs não guardam CPF, CNPJ, e-mail nem senha.

---

## 🗃️ Migrações do banco

O schema do banco é gerenciado apenas pelo Alembic. Ao alterar um model, gere e aplique uma nova migration:

```bash
alembic revision --autogenerate -m "descricao da mudanca"
alembic upgrade head
```

Revise sempre o arquivo gerado: o autogenerate não detecta mudanças de tamanho de `String`, `CHECK` constraints nem `server_default`. O teste `tests/test_migrations.py` avisa quando os models e as migrations estão diferentes.

---

## 🧪 Testes e qualidade de código

```bash
pytest                   # roda os testes (banco SQLite em memória, novo a cada teste)
ruff check .             # lint
ruff format .            # formata o código
```

Os testes cobrem models, autenticação, permissões, regras de negócio, máscaras e migrations.

O workflow em `.github/workflows/ci.yml` roda o lint, a verificação de formatação e os testes a cada push e pull request, usando as versões do `uv.lock`.
