# CONTEXTO FOCADO - ALVO 1: CONFIGURAÇÃO INICIAL

**Alvo 1:** Configuração Inicial: Estrutura do Monorepo, Docker, CI/CD (.github/workflows), linters (.pre-commit-config.yaml) e dependências (pyproject.toml, package.json).

## Seções Relevantes do Blueprint:

### 1. Organização do Código-Fonte (Monorepo)
- Adotaremos um **monorepo**, contendo tanto o código do backend (`backend/`) quanto do frontend (`frontend/`) no mesmo repositório Git
- Esta abordagem simplifica o gerenciamento de dependências, facilita a consistência entre a API e o cliente, e agiliza o pipeline de CI/CD

### 2. Stack Tecnológica Definida
- **Backend:** Python 3.10+, Django 4.2+, Django REST Framework, PostgreSQL, Redis, Celery, Poetry
- **Frontend:** React 18+, TypeScript, Vite, TanStack Query, Zustand, Tailwind CSS, npm

### 3. Estrutura de Diretórios Proposta
```
iabank/
├── .github/workflows/
├── backend/
│   ├── src/iabank/
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .gitignore
└── .pre-commit-config.yaml
```

## Modelos e Dependências:

Os arquivos já existem no projeto com as seguintes configurações:

- **pyproject.toml**: Dependências Python completas (Django 4.2+, DRF, PostgreSQL, Redis, Celery, etc.)
- **package.json**: Dependências Frontend (React 18+, TypeScript, Vite, TanStack Query, etc.)
- **docker-compose.yml**: Serviços PostgreSQL, Redis, Backend Django, Celery Worker
- **.pre-commit-config.yaml**: Hooks para Black, Ruff, MyPy, ESLint, Prettier, segurança
- **.github/workflows/ci.yml**: Pipeline completo de CI/CD com testes backend/frontend

## Contratos de Interface:

- **Docker**: Containerização completa com health checks
- **CI/CD**: Pipeline automatizado com quality gates
- **Linting**: Configuração padronizada para Python (Black, Ruff) e TypeScript (ESLint, Prettier)
- **Ambiente**: Estratégia com django-environ e arquivos .env

## Resumo de Redução:

- Contexto original: 1088 linhas
- Contexto focado: 184 linhas  
- Redução: 83%

---

**Contexto extraído do Blueprint Arquitetural para implementação do Alvo 1**