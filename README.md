# ProjetoFinanceiro

Sistema de importação de despesas com **frontend** em HTML/CSS/JavaScript, **backend** em Flask, armazenamento em **Google Sheets** e **categorização automática** com a API **Gemini** (Google GenAI).

## Estrutura do repositório

```
ProjetoFinal/
├── frontend/                 # Interface para enviar Excel e categorizar
├── backend/
│   ├── main.py               # Entrada recomendada do servidor
│   ├── app.py                # Compatibilidade: reexporta o app (python app.py)
│   ├── requirements.txt
│   ├── .env.example          # Modelo de variáveis de ambiente
│   └── src/                  # Código da API (módulos importados via sys.path)
│       ├── config.py
│       ├── routes/           # Apenas endpoints HTTP
│       ├── services/         # Regras de negócio e orquestração
│       ├── agent/            # Integração Gemini + prompts/
│       │   ├── gemini_agent.py
│       │   ├── streaming.py  # Contrato para streaming (futuro)
│       │   └── prompts/
│       ├── integrations/     # Excel e Google Sheets
│       ├── validators/       # Validação de entrada
│       ├── models/           # Estruturas de dados (ex.: despesas)
│       └── utils/            # Funções auxiliares
└── README.md
```

## Requisitos do Excel

O arquivo deve conter exatamente as colunas:

- `Data`
- `Descrição` (ou `Descricao`, normalizado internamente)
- `Valor`

Cada linha importada vira uma linha na planilha com: **ID**, **Data**, **Descrição**, **Valor**, **Categoria** (vazia até a categorização).

## Pré-requisitos

- Python **3.10+**
- Planilha Google compartilhada com a **conta de serviço** (permissão de editor)
- Chave **Gemini** ([Google AI Studio](https://aistudio.google.com/apikey)) — apenas para categorização automática

## Instalação do backend

Abra o terminal na pasta do projeto e entre em `backend`:

```cmd
cd backend
```

### 1) Ambiente virtual (recomendado)

**Windows (cmd):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear scripts, ajuste a política de execução apenas para a sessão atual ou use o **cmd** com `activate.bat`.

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Dependências

```bash
pip install -r requirements.txt
```

O projeto usa o pacote **`google-genai`**. Se ainda tiver o SDK antigo, remova com `pip uninstall google-generativeai`.

### 3) Arquivo `.env`

Na pasta `backend`, copie o exemplo e edite:

**Windows (cmd):**

```cmd
copy .env.example .env
```

**PowerShell:**

```powershell
Copy-Item .env.example .env
```

Conteúdo esperado (ajuste os valores):

```env
PORT=3333
GOOGLE_SHEETS_ID=SEU_ID_DA_PLANILHA
GOOGLE_SHEETS_WORKSHEET=Despesas
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json
GEMINI_API_KEY=SUA_CHAVE_GEMINI
GEMINI_MODEL=gemini-2.0-flash
```

| Variável | Uso |
|----------|-----|
| `PORT` | Porta HTTP do Flask |
| `GOOGLE_SHEETS_ID` | ID da planilha (trecho entre `/d/` e `/edit` na URL) |
| `GOOGLE_SHEETS_WORKSHEET` | Nome da aba das despesas |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Caminho do JSON da conta de serviço |
| `GEMINI_API_KEY` | Chave da API Gemini — necessária para `POST /categorizar` e categorização via `POST /processar` |
| `GEMINI_MODEL` | Modelo (ex.: `gemini-2.0-flash`) |

A importação de Excel **não** exige Gemini; a categorização **exige** `GEMINI_API_KEY`.

### 4) Credenciais Google (Sheets)

1. Salve o JSON da conta de serviço (por exemplo `credentials.json`) na pasta `backend`, ou em outro caminho indicado em `GOOGLE_SERVICE_ACCOUNT_FILE`.
2. Compartilhe a planilha com o e-mail da conta de serviço (`…@….iam.gserviceaccount.com`) como **editor**.
3. Na primeira linha da aba, use cabeçalhos compatíveis: **ID**, **Data**, **Descrição**, **Valor**, **Categoria**.

## Executar o servidor

Na pasta `backend`, com o ambiente virtual ativado:

```bash
python main.py
```

Alternativa (compatível com versões anteriores):

```bash
python app.py
```

O servidor fica em `http://localhost:3333` (ou na porta definida em `PORT`).

## Rotas da API

| Método | Caminho | Descrição |
|--------|---------|-----------|
| GET | `/teste` | Verifica se o servidor está no ar |
| GET | `/dashboard` | Página HTML do dashboard financeiro (gráfico de pizza) |
| GET | `/dados_dashboard` | Dados agregados de despesas por categoria (JSON) |
| POST | `/import/expenses` | Importa Excel (`multipart/form-data`, campo `file`) |
| POST | `/categorizar` | Categoriza linhas sem categoria (corpo JSON vazio, `{}` ou `{"limit": n}`) |
| POST | `/processar` | **Rota unificada**: ver abaixo |

### POST `/processar`

- **Importação:** envie `multipart/form-data` com o campo **`file`** (mesmo comportamento de `/import/expenses`).
- **Categorização:** envie JSON com `"acao": "categorizar"` e, opcionalmente, `"limit"`:

```json
{ "acao": "categorizar", "limit": 10 }
```

## Exemplos com `curl` (servidor em `localhost:3333`)

Health check:

```bash
curl http://localhost:3333/teste
```

Dados do dashboard (JSON):

```bash
curl http://localhost:3333/dados_dashboard
```

Categorizar (corpo vazio ou `{}`):

```bash
curl -X POST http://localhost:3333/categorizar -H "Content-Type: application/json" -d "{}"
```

Categorizar com limite:

```bash
curl -X POST http://localhost:3333/categorizar -H "Content-Type: application/json" -d "{\"limit\": 10}"
```

Categorizar via rota unificada:

```bash
curl -X POST http://localhost:3333/processar -H "Content-Type: application/json" -d "{\"acao\": \"categorizar\"}"
```

Importar Excel (ajuste o caminho do arquivo):

```bash
curl -X POST http://localhost:3333/import/expenses -F "file=@C:\caminho\para\despesas.xlsx"
```

Ou pela rota unificada:

```bash
curl -X POST http://localhost:3333/processar -F "file=@C:\caminho\para\despesas.xlsx"
```

## Dashboard Financeiro (MVP)

Abra no navegador:

- `http://localhost:3333/dashboard`

Preview do dashboard (adicione sua imagem em `docs/dashboard-preview.png`):

![Preview do Dashboard](docs/dashboard-preview.png)

O dashboard usa:

- **Chart.js** para renderizar o gráfico de pizza
- `GET /dados_dashboard` para buscar os dados agregados
- `backend/templates/dashboard.html` como página
- `backend/static/js/script_dashboard.js` para buscar dados e montar o gráfico

Formato retornado por `GET /dados_dashboard`:

```json
{
  "despesas_por_categoria": {
    "Alimentação": 1200.5,
    "Transporte": 430.0,
    "Moradia": 2500.0,
    "Lazer": 320.75,
    "Outros": 180.2
  }
}
```

Regras da agregação no backend:

- Lê os dados da planilha Google Sheets
- Considera apenas **despesas** (valores negativos)
- Agrupa por categoria
- Soma os valores por categoria (em módulo/valor absoluto para visualização)
- Categorias não mapeadas ou vazias são consolidadas em `Outros`

## Frontend

Abra `frontend/index.html` no navegador (ou use uma extensão tipo Live Server). O JavaScript chama `http://localhost:3333` — o backend precisa estar rodando.

## Fluxo da API (resumo)

**Importação:** rota → validador → serviço → leitura Excel → gravação na planilha.

**Categorização:** rota → validador → serviço → leitura da planilha → prompt → Gemini → atualização da coluna **Categoria**.

Para detalhes da organização em camadas (`routes`, `services`, `agent`, `integrations`, etc.), veja a árvore em **Estrutura do repositório** acima.
