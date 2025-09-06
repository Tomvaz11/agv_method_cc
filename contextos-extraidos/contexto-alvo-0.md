# CONTEXTO FOCADO - ALVO 0: FOUNDATION DNA

## Visão Geral da Arquitetura Base

- **Arquitetura:** Camadas (Layered Architecture) aplicada a uma aplicação Monolítica Modular
- **Backend:** Django estruturado seguindo princípios da Arquitetura Limpa
- **Camadas:** Apresentação, Aplicação, Domínio, Infraestrutura
- **Frontend:** SPA desacoplado comunicando via API RESTful
- **Organização:** Monorepo (backend/ e frontend/)

## Estratégia de Multi-tenancy (Fundação Crítica)

```python
# iabank/core/models.py (Modelos base)
from django.db import models
from django.contrib.auth.models import AbstractUser

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    # ... outros detalhes do tenant

class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users")
    # ... outros campos de usuário

class BaseTenantModel(models.Model):
    """Modelo abstrato para garantir que todos os dados sejam vinculados a um tenant."""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```

## Estrutura de Diretórios Core

```
iabank/
├── backend/
│   ├── src/
│   │   └── iabank/
│   │       ├── __init__.py
│   │       ├── settings.py
│   │       ├── urls.py
│   │       ├── wsgi.py
│   │       ├── asgi.py
│   │       ├── core/            # App com modelos base, middlewares, etc.
│   │       └── users/           # App de Usuários e Permissões
│   ├── manage.py
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
├── docker-compose.yml
├── .gitignore
└── .pre-commit-config.yaml
```

## Modelos e Dependências

### Modelos de Base (Core Foundation)
- **Tenant:** Entidade fundamental para isolamento multi-tenant
- **User(AbstractUser):** Usuário customizado com vínculo obrigatório ao tenant
- **BaseTenantModel:** Classe abstrata que garante herança de tenant para todos os modelos

### Dependências Críticas de Configuração
- Django 4.2+ como framework base
- Django REST Framework para APIs
- PostgreSQL como banco principal
- Redis para cache e filas
- Poetry para gerenciamento de dependências Python

### Stack Tecnológica Foundation
- **Backend:** Python 3.11+, Django, Django REST Framework
- **Frontend:** React 18+, TypeScript, Vite
- **Banco:** PostgreSQL
- **Containerização:** Docker, Docker Compose

## Contratos de Interface

### Configuração de Ambiente (.env base)
- `DATABASE_URL`: String de conexão PostgreSQL
- `SECRET_KEY`: Chave secreta Django
- `DEBUG`: Flag de desenvolvimento
- Variáveis Redis para cache/fila

### Arquivos de Configuração Core
1. `pyproject.toml` - Dependências e configurações Python/Poetry
2. `settings.py` - Configurações Django centralizadas
3. `docker-compose.yml` - Orquestração de containers
4. `.pre-commit-config.yaml` - Hooks de qualidade de código

### Padrões de Segurança Foundation
- Multi-tenancy obrigatório em todos os modelos
- Middleware de tenant para isolamento de dados
- Autenticação JWT (configuração base)
- Variáveis de ambiente para secrets

### Contratos de Teste (Factories Base)

```python
# Padrão obrigatório para Factories
class TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tenant

# Propagação de tenant mandatória
tenant = factory.SubFactory(TenantFactory)
```

## BASELINE VALIDATION T1 (Critério de Aceite)

- ✅ Estrutura do projeto funcional
- ✅ Sistema multi-tenant operacional
- ✅ Modelos base (`Tenant`, `User`, `BaseTenantModel`) migrados
- ✅ Autenticação JWT configurada
- ✅ Docker e ambiente de desenvolvimento funcionais

## Observações

O Foundation DNA é a base arquitetural crítica que define a estrutura multi-tenant, configuração de ambiente, e padrões fundamentais que todos os outros alvos dependem. Sem essa fundação sólida, nenhum desenvolvimento posterior pode prosseguir de forma consistente e segura.

---

**Contexto extraído do Blueprint Arquitetural para implementação do Alvo 0**