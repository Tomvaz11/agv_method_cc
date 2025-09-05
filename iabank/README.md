# IABANK

[![Status](https://img.shields.io/badge/status-foundation_dna_implemented-green)](https://github.com/your-org/iabank)
[![CI/CD](https://github.com/your-org/iabank/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/iabank/actions)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://djangoproject.com)
[![React](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org)

Sistema de gestão de empréstimos moderno e eficiente desenvolvido seguindo o **Método AGV v5.0**.

## 🏗️ Foundation DNA - Alvo 0 Implementado

Este projeto implementa a **Foundation DNA** completa do sistema IABANK, estabelecendo todos os padrões arquiteturais e estruturas base que serão replicados por todos os alvos futuros.

### ✅ DNA Arquitetural Implementado

- **🔧 Classes Base Funcionais**: `BaseTenantModel`, `BaseSerializer`, `BaseViewSet`, etc.
- **🏢 Multi-Tenancy Nativo**: Isolamento completo de dados desde a fundação
- **👥 Sistema de Usuários Completo**: Modelo customizado com JWT integrado
- **🎯 Exemplo Funcional**: App `customers` implementado como template
- **🧪 Testes Foundation**: Estrutura completa de testes com factories
- **🔄 CI/CD Pipeline**: GitHub Actions com qualidade gates
- **📦 Docker Ready**: Ambiente completo containerizado

## 🚀 Stack Tecnológica

### Backend
- **Python 3.10+** - Linguagem principal
- **Django 4.2+** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Banco de dados principal  
- **Redis** - Cache e filas
- **Celery** - Processamento assíncrono
- **Poetry** - Gerenciamento de dependências

### Frontend
- **React 18+** - Interface do usuário
- **TypeScript** - Tipagem estática
- **Vite** - Build tool e dev server
- **TanStack Query** - Gerenciamento de estado servidor
- **Zustand** - Estado global cliente
- **Tailwind CSS** - Estilização

### DevOps & Qualidade
- **Docker & Docker Compose** - Containerização
- **GitHub Actions** - CI/CD
- **Pre-commit hooks** - Qualidade de código
- **Black, Ruff, ESLint** - Linters e formatters
- **pytest, Vitest** - Frameworks de teste

## 🏁 Como Começar

### Pré-requisitos

- **Docker** e **Docker Compose** instalados
- **Git** para versionamento
- **Python 3.10+** e **Poetry** (para desenvolvimento local)
- **Node.js 18+** e **npm** (para frontend)

### 🐳 Execução com Docker (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/your-org/iabank.git
cd iabank

# 2. Configure as variáveis de ambiente
cp backend/.env.example backend/.env

# 3. Suba os serviços
docker-compose up -d --build

# 4. Execute as migrações
docker-compose exec backend poetry run python src/manage.py migrate

# 5. Crie um superusuário
docker-compose exec backend poetry run python src/manage.py createsuperuser

# 6. Acesse a aplicação
# - Backend API: http://localhost:8000/api/v1/
# - Admin: http://localhost:8000/admin/
# - Health Check: http://localhost:8000/health/
```

### 💻 Execução Local (Desenvolvimento)

```bash
# Backend
cd backend
cp .env.example .env
poetry install
poetry run python src/manage.py migrate
poetry run python src/manage.py runserver

# Frontend (em outro terminal)
cd frontend
npm install
npm run dev
```

## 🧪 Executar Testes

### Backend
```bash
# Todos os testes
docker-compose exec backend poetry run pytest

# Com coverage
docker-compose exec backend poetry run pytest --cov=src

# Testes específicos
docker-compose exec backend poetry run pytest src/iabank/core/tests/
```

### Frontend
```bash
# Todos os testes
cd frontend && npm run test

# Com UI
npm run test:ui

# Coverage
npm run test:coverage
```

## 📊 Validação da Foundation DNA

A Foundation DNA pode ser validada através dos seguintes comandos:

```bash
# 1. Verificar se os serviços sobem corretamente
docker-compose up -d --build

# 2. Validar health checks
curl http://localhost:8000/health/

# 3. Executar testes da foundation
docker-compose exec backend poetry run pytest src/iabank/core/tests/
docker-compose exec backend poetry run pytest src/iabank/users/tests/  
docker-compose exec backend poetry run pytest src/iabank/customers/tests/

# 4. Verificar migrações
docker-compose exec backend poetry run python src/manage.py showmigrations

# 5. Validar linting e formatting
docker-compose exec backend poetry run ruff check src/
docker-compose exec backend poetry run black --check src/

# 6. Testar criação de tenant e usuário via shell
docker-compose exec backend poetry run python src/manage.py shell
```

## 🏗️ Estrutura do Projeto

```
iabank/
├── 📁 .github/workflows/     # CI/CD pipelines
├── 📁 backend/              # Django backend
│   ├── 📁 src/iabank/       # Código fonte principal
│   │   ├── 📁 core/         # ✅ App base (Tenant, BaseModels)
│   │   ├── 📁 users/        # ✅ Sistema de usuários
│   │   ├── 📁 customers/    # ✅ Exemplo funcional completo
│   │   ├── 📁 operations/   # 🚧 Empréstimos (futura implementação)
│   │   └── 📁 finance/      # 🚧 Financeiro (futura implementação)
│   ├── 📄 pyproject.toml    # Dependências Python
│   └── 📄 Dockerfile        # Container backend
├── 📁 frontend/             # React frontend
│   ├── 📁 src/              # Estrutura feature-based
│   │   ├── 📁 shared/       # ✅ Configurações e utilitários
│   │   ├── 📁 features/     # 🚧 Funcionalidades (futura implementação)
│   │   └── 📁 entities/     # 🚧 Entidades de negócio
│   ├── 📄 package.json      # Dependências Node
│   └── 📄 Dockerfile        # Container frontend
├── 📄 docker-compose.yml    # Orquestração completa
└── 📄 README.md            # Este arquivo
```

## 🎯 Próximos Alvos (Implementação Futura)

Seguindo o **Método AGV v5.0**, os próximos alvos serão implementados utilizando esta Foundation DNA como base:

1. **Alvo 1-7**: Sistema de Autenticação JWT completo
2. **Alvo 8-13**: CRUD de Clientes com isolamento de tenant
3. **Alvo 14-17**: Sistema de Consultores
4. **Alvo 18-23**: Sistema de Empréstimos e Parcelas
5. **Alvo 24-29**: Interface React completa

## 🔧 Padrões Estabelecidos para Replicação

### Models
- Sempre herdar de `BaseTenantModel` para isolamento de dados
- Usar `BaseManager` para queries otimizadas
- Implementar métodos `can_be_deleted()` e `to_dict()`
- Seguir convenções de nomenclatura consistentes

### Serializers
- Herdar de `BaseTenantSerializer` para isolamento automático
- Implementar validações de tenant consistency
- Usar computed fields para dados formatados
- Seguir padrão Create/List/Update separados

### ViewSets
- Herdar de `BaseTenantViewSet` para filtering automático
- Implementar actions customizadas padronizadas (activate, deactivate, stats)
- Usar permissions classes consistentes
- Implementar paginação e filtros

### Tests
- Usar factories do `factory-boy` para dados de teste
- Implementar testes de isolamento de tenant obrigatórios
- Seguir padrão AAA (Arrange, Act, Assert)
- Validar tanto funcionalidade quanto performance

## 📝 Contribuição

1. Siga o [Blueprint Arquitetural](BLUEPRINT_ARQUITETURAL.md)
2. Utilize o **Método AGV v5.0** para implementações
3. Todos os PRs devem passar pelos quality gates de CI/CD
4. Mantenha cobertura de testes > 80%
5. Documente mudanças no CHANGELOG.md

## 📜 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**🤖 Foundation DNA implementada com [Método AGV v5.0](https://github.com/agv-method)**

*Este README documenta a Foundation DNA completa. Para implementações futuras, consulte o Blueprint Arquitetural e siga os padrões estabelecidos.*