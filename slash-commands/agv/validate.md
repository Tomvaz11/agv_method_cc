---
description: "Valida conformidade da codebase atual com o Blueprint Arquitetural"
allowed_tools: ["Read", "Grep", "Glob", "Bash"]
---

# AGV Validate - Validação de Conformidade com Blueprint

Executa validação abrangente da codebase atual contra o Blueprint Arquitetural para identificar desvios arquiteturais ou violações de padrões.

## Processo de Validação

### Etapa 1: Validação Arquitetural
Verificar se a implementação atual segue a arquitetura definida:

**Estrutura de Diretórios:**
- Comparar estrutura atual com a proposta no Blueprint
- Verificar se apps Django estão organizados corretamente
- Validar estrutura do frontend (features, shared, entities)

**Separação de Camadas:**
- Apresentação: Views e Serializers
- Aplicação: Services e DTOs  
- Domínio: Models e lógica de negócio
- Infraestrutura: Repositórios e integrações

### Etapa 2: Validação de Contratos
Verificar conformidade com contratos definidos:

**Modelos de Dados:**
- Comparar models.py com especificações do Blueprint
- Verificar relacionamentos e constraints
- Validar multi-tenancy (campo tenant em todos os modelos)

**DTOs e Serializers:**
- Verificar se DTOs implementados seguem especificação
- Validar serializers do DRF
- Confirmar ViewModels do frontend

**APIs:**
- Verificar endpoints implementados vs especificados
- Validar padrão de resposta da API (formato JSON)
- Confirmar versionamento (/api/v1/)

### Etapa 3: Validação de Padrões e Qualidade
Executar verificações de qualidade:

**Padrões de Código:**
```bash
# Executar linting no backend
ruff check backend/src/ --output-format=text

# Verificar formatação Python
black --check backend/src/

# Linting do frontend (se aplicável)
# eslint frontend/src/ --format=table
```

**Testes:**
- Verificar cobertura de testes unitários
- Validar estrutura de testes conforme Blueprint
- Confirmar factories multi-tenant corretas

**Configuração:**
- Validar arquivos de configuração (pyproject.toml, package.json)
- Verificar docker-compose.yml e Dockerfiles
- Confirmar CI/CD pipeline (.github/workflows/)

### Etapa 4: Validação de Segurança
Verificar implementação de segurança:

**Multi-tenancy:**
- Confirmar isolamento de dados por tenant
- Verificar middleware de tenant
- Validar propagação de tenant em queries

**Autenticação/Autorização:**
- Verificar implementação JWT
- Confirmar classes de permissão do DRF
- Validar controle de acesso

### Etapa 5: Validação de Observabilidade
Verificar implementação dos requisitos não-funcionais:

**Logging:**
- Confirmar structlog configurado
- Verificar logs estruturados em JSON
- Validar contexto (request_id, tenant_id)

**Métricas:**
- Verificar django-prometheus configurado
- Confirmar endpoint /metrics
- Validar métricas de negócio definidas

**Health Checks:**
- Verificar endpoint /health implementado
- Confirmar verificação de DB e Redis

## Tipos de Validação

### 🏗️ **Estrutural**
- Organização de diretórios e arquivos
- Estrutura de apps Django
- Arquitetura de camadas

### 🔒 **Contratos**
- Modelos de dados
- DTOs e Serializers
- APIs e endpoints

### 📏 **Qualidade**
- Padrões de código (PEP 8, ESLint)
- Cobertura de testes
- Documentação

### 🛡️ **Segurança**
- Multi-tenancy
- Autenticação/Autorização
- Validação de dados

### 📊 **Observabilidade**
- Logging estruturado
- Métricas de negócio
- Health checks

## Relatório de Validação

### ✅ **Conformidades Encontradas**
- Aspectos que estão corretos conforme Blueprint
- Padrões bem implementados
- Arquitetura respeitada

### ⚠️ **Desvios Identificados** 
- Violações arquiteturais encontradas
- Contratos não seguidos
- Padrões não implementados

### ❌ **Problemas Críticos**
- Violações graves do Blueprint
- Falhas de segurança
- Problemas que bloqueiam o projeto

### 🔧 **Recomendações de Correção**
- Ações específicas para corrigir cada problema
- Prioridade de correção
- Impacto estimado de cada correção

## Resultado
- Relatório completo de conformidade
- Lista de todos os desvios encontrados
- Plano de ação para correções
- Score geral de conformidade com Blueprint