# Método AGV: Fluxo de Trabalho v5.0 (Lean & Strategic)

Este documento descreve o fluxo de trabalho passo a passo para desenvolver software usando o Método AGV v5.0. Ele foi atualizado para incorporar a estratégia do **"Blueprint Evolutivo"** e a especialização dos agentes, garantindo um processo escalável e otimizado para o gerenciamento de contexto.

## Visão Geral do Fluxo (v5.0)

O fluxo v5.0 é centrado na **Direção Estratégica** e na **Gestão Ativa de Contexto**. O Coordenador guia a IA através de um planejamento detalhado e, crucialmente, "poda" o contexto à medida que o projeto avança, garantindo que os agentes de implementação sempre trabalhem com a máxima eficiência.

```mermaid
graph TD
    subgraph Fase de Planejamento Estratégico
        A[Coordenador: Definição Inicial] --> B(F1-Tocrisna: Arquitetura);
        B -- Blueprint Mestre (v1.0) --> C{Validação Humana};
        C -- Aprova --> D[F2-Orchestrator: Sequência];
        D -- Ordem de Implementação Geral --> E{Validação Humana};
        E -- Aprova --> F[Início da Fase de Setup];
    end

    subgraph "Fase 3: Setup e Poda (Execução Única)"
        direction LR
        F --> G[F4-Scaffolder: Executa Alvo 0];
        G -- Scaffolding Completo --> H[Coordenador: Realiza a "Poda"];
        H -- Blueprint Evolutivo (v1.1) --> I[Início do Ciclo de Implementação];
    end

    subgraph "Fase 4: Ciclo de Implementação Focado (Iterativo)"
        direction LR
        I1[Coordenador: Seleciona Próximo Alvo] --> J[Coordenador: Prepara Contexto Focado];
        J -- Blueprint Evolutivo + Código Relevante --> K[F4-Implementador: Implementa Alvo + TUs];
        K -- Código + TUs --> L{Validação Humana};
        L -- Aprova --> M[Commit & Próximo];
        L -- Rejeita/Ajusta --> J;
    end

    I --> I1
    M --> I1
```

## Papéis dos Agentes e do Coordenador (v5.0)

- **Coordenador (Humano):** Estrategista, Arquiteto-Chefe, Revisor Crítico e **Curador de Contexto**. Define a visão, valida os artefatos e, crucialmente, realiza a "poda" do Blueprint e prepara os pacotes de contexto focado para cada tarefa.
- **F1 - Tocrisna (IA - Arquiteta):** Gera o **Blueprint Mestre**, o documento arquitetural completo e inicial.
- **F2 - OrchestratorHelper (IA - Planejadora Granular):** Gera a **Ordem de Implementação Geral** a partir do Blueprint.
- **F4-Scaffolder (IA - Engenheira de Setup):** Executa **apenas o Alvo 0**, criando a estrutura do projeto.
- **F4 - ImplementadorMestre (IA - Engenheira de Implementação):** Implementa os alvos funcionais (1 em diante) usando o contexto focado fornecido pelo Coordenador.

## Fases Detalhadas (v5.0)

### Fase 1: Definição Inicial (Coordenador)

- **Objetivo:** Estabelecer a visão, escopo e stack tecnológica do projeto.
- **Output:** Documento de Visão e Definição Inicial.

### Fase 2: Planejamento Arquitetural (F1 & F2)

- **Objetivo:** Criar o mapa mestre e o plano de trabalho do projeto.
- **Atividades:**
  1. Coordenador executa o `Prompt_F1_Tocrisna` para gerar o **`Blueprint_Mestre_v1.0.md`**.
  2. Coordenador valida criticamente o Blueprint.
  3. Coordenador executa o `Prompt_F2_Orchestrator` com o Blueprint como input para gerar a **`Ordem_De_Implementacao_Geral.md`**.
  4. Coordenador valida a lógica da ordem de implementação.

---

## **INÍCIO DA IMPLEMENTAÇÃO**

### Fase 3: Setup e Preparação de Contexto (F4-Scaffolder & Coordenador)

- **Objetivo:** Criar a estrutura base do projeto e otimizar o contexto para as fases seguintes. Esta fase é executada **apenas uma vez** no início.
- **Atividades:**
  1. **Setup (F4-Scaffolder):** O Coordenador executa o `Prompt_F4_Scaffolder` com o `Alvo 0` da Ordem de Implementação. A IA gera toda a estrutura de diretórios e arquivos de configuração (`.gitignore`, `README.md`, etc.).
  2. **PODA DO BLUEPRINT (Coordenador):** Após validar e commitar o scaffolding, o Coordenador realiza a primeira e mais importante "poda":
     - Cria uma cópia do `Blueprint_Mestre_v1.0.md` chamada **`Blueprint_Evolutivo_v1.1.md`**.
     - Nesta nova versão, **remove** todas as seções que foram materializadas pelo Scaffolder (ex: `Estrutura de Diretórios`, `Conteúdo do README.md`, `Conteúdo do .gitignore`, etc.).
- **Output:** O **`Blueprint Evolutivo`**, uma versão mais enxuta e focada do documento arquitetural, que será a principal fonte de contexto para o resto do projeto.

### Fase 4: Ciclo de Implementação Focado (F4-ImplementadorMestre & Coordenador)

- **Objetivo:** Implementar iterativamente as funcionalidades do sistema, mantendo a carga cognitiva da IA no mínimo.
- **Atividades (para cada alvo da Ordem de Implementação, a partir do Alvo 1):**
  1. **Seleção:** O Coordenador seleciona o próximo alvo a ser implementado.
  2. **Preparação de Contexto (Coordenador):** O Coordenador prepara o **Contexto Mínimo Viável (MVC)** para a tarefa. Isso envolve:
     - Extrair do **`Blueprint Evolutivo`** apenas as seções relevantes para o alvo atual (ex: a definição de um modelo, um DTO e um ViewModel específicos).
     - Identificar os arquivos de código já existentes que são dependências diretas.
  3. **Execução (F4-ImplementadorMestre):** O Coordenador executa o `Prompt_F4_Implementador_Mestre` fornecendo o alvo e o pacote de contexto focado. A IA implementa a funcionalidade e seus testes unitários.
  4. **Validação (Coordenador):** O Coordenador revisa o código gerado, executa os testes e garante que ele adere à arquitetura. O ciclo pode se repetir com feedback até a aprovação.
  5. **Commit:** O código validado é versionado.
  6. **(Opcional) Poda Adicional:** Em marcos maiores (ex: após finalizar todo o backend), o Coordenador pode realizar mais "podas" no `Blueprint Evolutivo`, simplificando as seções já implementadas para manter o documento sempre relevante e enxuto.

### Fase 5: Testes de Integração e Validação de Marcos

- **Gatilho:** Ao atingir uma "PARADA PARA TESTES DE INTEGRAÇÃO" na Ordem de Implementação.
- **Atividades:**
  1. Coordenador executa o prompt do agente `IntegradorTester` (`F4.1`), usando os cenários já definidos na Ordem de Implementação.
  2. Coordenador valida e executa os testes de integração gerados.

### Fase 6: Ciclo de Vida (Manutenção e Evolução)

- O método pode ser reaplicado para adicionar novas funcionalidades (geralmente começando na Fase 4) ou para corrigir/refatorar código (usando o agente `F7-Evolucionista`). O `Blueprint Evolutivo` deve ser atualizado se a arquitetura for modificada.
