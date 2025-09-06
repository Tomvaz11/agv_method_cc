---
description: "Extrai e salva o contexto específico para um alvo em arquivo (útil para implementação focada)"
allowed_tools: ["Task", "Read", "Grep", "Write"]
---

# AGV Context - Extração e Salvamento de Contexto

Extrai o contexto otimizado do Blueprint para um alvo específico e salva em arquivo, mantendo o terminal limpo e organizando os contextos para consulta posterior.

## Extração e Salvamento

### Contexto do Alvo $1 → Arquivo

Execute as seguintes etapas para extrair e salvar o contexto do Alvo $1:

1. **Extração**: Use o agv-context-analyzer para extrair o contexto específico do Alvo $1 do Blueprint Arquitetural

2. **Organização**: Crie a pasta 'contextos-extraidos/' se não existir

3. **Salvamento**: Salve o contexto extraído no arquivo 'contextos-extraidos/contexto-alvo-$1.md'

4. **Confirmação**: Retorne APENAS uma confirmação concisa:
   ✅ Contexto do Alvo $1 extraído e salvo em: contextos-extraidos/contexto-alvo-$1.md
   📊 Redução: [linhas originais] → [linhas extraídas] ([percentual]% de redução)

**IMPORTANTE**: NÃO mostre o conteúdo do contexto no terminal - apenas confirme o salvamento do arquivo.

## Argumentos
- **$1**: Número do alvo para extração de contexto (obrigatório)
  - Exemplo: `/agv:context 5` (extrai contexto do Alvo 5)
  - Exemplo: `/agv:context 12` (extrai contexto do Alvo 12)

## Benefícios

**Terminal Limpo:**
- Elimina poluição visual com centenas de linhas
- Mantém conversação organizada e navegável
- Foco na confirmação de ação executada

**Organização:**
- Contextos salvos na pasta 'contextos-extraidos/'
- Nomenclatura padronizada: 'contexto-alvo-X.md'
- Facilita comparação entre diferentes alvos
- Permite versionamento e compartilhamento

**Eficiência:**
- Contexto disponível quando necessário
- Não ocupa espaço na conversa
- Permite consulta posterior sem re-extração

## Estrutura de Arquivo Gerado
```
contextos-extraidos/
├── contexto-alvo-0.md    # Foundation DNA
├── contexto-alvo-1.md    # Primeiro alvo funcional  
├── contexto-alvo-5.md    # Quinto alvo
└── ...
```

## Resultado
- ✅ Confirmação de arquivo criado
- 📊 Estatísticas de redução de contexto
- 📁 Arquivo organizado para consulta posterior