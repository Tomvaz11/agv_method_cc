---
description: "Executa Alvo com validação automática (usa Blueprint completo por padrão, --context para contexto extraído)"
allowed_tools: ["Task", "Write", "LS", "Bash"]
---

# AGV Scaffold + Validação Automática

Executa um Alvo específico (ex: Foundation DNA) seguido de **validação automática profunda** linha por linha vs Blueprint.

## Uso

**Comando Básico (Blueprint Completo - Padrão):**
```bash
/agv:scaffold 0    # Usa iabank/BLUEPRINT_ARQUITETURAL.md (~1088 linhas)
```

**Comando com Contexto Extraído:**
```bash
/agv:scaffold 0 --context    # Usa contextos-extraidos/contexto-alvo-0.md (~200 linhas)
```

## Argumentos
- **Número do Alvo** (obrigatório): `0`, `1`, `2`, etc.
- **`--context`** (opcional): Usa contexto extraído ao invés do Blueprint completo

## Fluxo Automatizado com Validação

### Etapa 1: Extração de Contexto de Setup

Primeiro, vou extrair do Blueprint apenas as seções relevantes para o setup inicial:

- Estrutura de Diretórios Proposta
- Arquivos de Configuração (.gitignore, README.md, LICENSE)
- Configurações de Ambiente (pyproject.toml, package.json, docker-compose.yml)
- Estrutura de Testes (diretórios e arquivos base)

### Etapa 1.2: Sistema Automático de Validação v3.0 - NOVA ARQUITETURA MODULAR

O sistema agora usa ValidatorGenerator v3.0 com arquitetura modular avançada:

- **Geração Automática**: ValidatorGenerator cria validador customizado por Blueprint
- **67+ Validações Especializadas**: Sistema modular com generators específicos  
- **Profiles Configuráveis**: development (65%), production (85%), architecture_review (95%)
- **Integração Total**: Automação completa pós-scaffold sem intervenção manual

### Etapa 1.3: Seleção de Fonte de Informação

**Parâmetro de Controle de Fonte:**

- **`/agv:scaffold X`** (padrão): Usa Blueprint Completo (`iabank/BLUEPRINT_ARQUITETURAL.md`)
- **`/agv:scaffold X --context`**: Usa Contexto Extraído (`contextos-extraidos/contexto-alvo-X.md`)

### Etapa 1.4: Contagem de Linhas e Delegação

Primeiro, conte as linhas dos arquivos para informar o usuário:

Execute os seguintes comandos para contar as linhas dos arquivos:

```bash
# Contar linhas do Blueprint (sempre)
BLUEPRINT_LINES=$(wc -l iabank/BLUEPRINT_ARQUITETURAL.md | cut -d' ' -f1)

# Se comando contém --context, contar também o contexto extraído
if [argumentos contêm "--context"]; then
    CONTEXT_LINES=$(wc -l contextos-extraidos/contexto-alvo-$1.md | cut -d' ' -f1)
fi
```

**Se comando NÃO contém `--context`:**
📄 **Fonte: Blueprint Completo** (`iabank/BLUEPRINT_ARQUITETURAL.md` - $BLUEPRINT_LINES linhas)

Delegue para o subagent "agv-scaffolder" a tarefa de executar o Alvo $1 completo baseado no:
- Blueprint Completo: `iabank/BLUEPRINT_ARQUITETURAL.md`

**Se comando contém `--context`:**
🎯 **Fonte: Contexto Extraído** (`contextos-extraidos/contexto-alvo-$1.md` - $CONTEXT_LINES linhas)  
📊 **Redução de contexto:** $BLUEPRINT_LINES → $CONTEXT_LINES linhas

Delegue para o subagent "agv-scaffolder" a tarefa de executar o Alvo $1 completo baseado no:
- Contexto Extraído: `contextos-extraidos/contexto-alvo-$1.md`

### Etapa 2: Validação Automática Profunda

Após o scaffold, executo automaticamente o validador profundo que:

- ✅ Analisa **100+ verificações** linha por linha
- ✅ Valida conteúdo real vs especificações Blueprint
- ✅ Verifica JSON/YAML válidos
- ✅ Confirma dependências exatas
- ✅ Sistema de pontuação ponderado por severidade

### Etapa 3: Aprovação/Rejeição

Primeiro, obtenho o threshold atual dinamicamente:

```bash
CURRENT_THRESHOLD=$(python agv-system/scripts/validation_config.py threshold)
echo "Threshold ativo: $CURRENT_THRESHOLD"
```

- **Score ≥ Threshold Ativo:** Scaffold aprovado, pode prosseguir
- **Score < Threshold Ativo:** Scaffold rejeitado, corrigir antes de prosseguir

## Processo de Execução

### Fluxo Automático Integrado - ValidatorGenerator v3.0

O sistema está **100% automatizado**. O hook pós-scaffold executa automaticamente:

1. **ValidatorGenerator v3.0**: Gera validador customizado por Blueprint
2. **Validação Profunda**: 67+ verificações especializadas
3. **Sistema de Pontuação**: Baseado em profiles configuráveis
4. **Aprovação/Rejeição**: Automática baseada em threshold ativo

### Executar Scaffold

Após gerar o validador customizado, delegue para o subagent "agv-scaffolder" (AGV-BaselineFoundation) a tarefa de executar o Alvo 0 completo baseado no Blueprint Arquitetural.

## Resultado Esperado do Foundation DNA

- Estrutura completa de diretórios
- Todos os arquivos de configuração
- Classes base funcionais (BaseModel, BaseSerializer, etc.)
- Exemplo funcional mínimo que demonstre os padrões
- Estrutura de testes com exemplo funcional
- Aplicação executável ao final

### Executar Validação Profunda

Após o scaffold, execute automaticamente:

```bash
python agv-system/scripts/post_scaffold_validation.py
```

Este script irá:

1. Executar validação profunda (`validate_scaffold.py`)
2. Analisar 100+ verificações
3. Gerar relatório detalhado
4. Aprovar/rejeitar baseado no score

## Resultado Esperado

**Verificação Dinâmica do Threshold:**

```bash
CURRENT_THRESHOLD=$(python agv-system/scripts/validation_config.py threshold)
echo "Usando threshold: $CURRENT_THRESHOLD"
```

**Se Score ≥ Threshold Ativo:**

- ✅ Scaffold aprovado
- ✅ Relatório de conformidade
- ✅ Pronto para Alvo 1

**Se Score < Threshold Ativo:**

- ❌ Scaffold rejeitado
- 📋 Lista detalhada de problemas
- 🔧 Recomendações de correção
- ⚠️ Bloqueio para próximos alvos

**Gerenciamento de Profiles:**
```bash
python agv-system/scripts/validation_config.py list        # Ver profiles disponíveis
python agv-system/scripts/validation_config.py threshold   # Ver threshold atual
python agv-system/scripts/validation_config.py switch development  # Trocar para development (65%)
```
