# Hermes Plugin — Genial Care

Plugin Hermes que configura o setup da Genial Care na sua máquina com um
comando: `hermes genial-setup`.

## O que o plugin faz

| Item | Descrição |
|---|---|
| Provider LLM | `anthropic/claude-sonnet-5` via OpenRouter (modelo principal, auxiliares e delegação) |
| Chave OpenRouter | Obrigatória — o comando pede na primeira execução e grava em `~/.hermes/.env` |
| MCPs corporativos | Atlassian, Granola, Slack e Metabase via `mcp.json` centralizado no GCS (merge aditivo) |
| gcloud | Instala e autentica com sua conta `@genialcare.com.br` (fase 2 do plano) |
| Browser | Chrome com depuração remota (CDP) na porta 9222, perfil isolado |
| gws | Orientação de autenticação (client_secret baixado do GCS) |

## Instalação (após ter o Hermes instalado)

```shell
hermes plugins install GenialCare/hermes-plugin-genial --enable
hermes genial-setup
```

## Desenvolvimento

```shell
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest -v
```

Validação oficial do Hermes (mesmo gate da catalog CI):

```shell
hermes plugins validate . --json
```

## Plano

O plano de implementação completo vive em `.hermes/plans/` da máquina do
autor — as fases: esqueleto → gcloud → GCS (mcp.json + client_secret
centralizados) → integração → documentação e transição dos scripts antigos.
