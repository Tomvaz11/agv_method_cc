# Princípios Chave do Método AGV v4.0 (Lean & Strategic)

Este documento descreve os princípios fundamentais de design, arquitetura e processo que norteiam o Método AGV v4.0. Estes princípios foram refinados para refletir uma abordagem pragmática e escalável para o desenvolvimento de software assistido por IA.

## 1. Qualidade Intrínseca Como Premissa

- **Conceito:** A qualidade de código e arquitetura, em nível profissional sênior, não é um resultado, mas a **premissa** para o desenvolvimento. A velocidade e a eficiência são consequências diretas de uma fundação bem construída, não objetivos que a substituem.
- **Implicações:**
  - Adesão rigorosa a uma arquitetura robusta e modular definida no `Blueprint`.
  - Aplicação consistente de boas práticas (SOLID, DRY, KISS).
  - Ênfase em código claro, legível e com tratamento de erros robusto.
  - Minimização proativa de débito técnico.

## 2. Direção Estratégica com Planejamento Granular

- **Conceito:** Mantemos o pilar de focar no "O Quê" (objetivos, critérios) em vez de microgerenciar o "Como" na implementação. Confiamos na capacidade latente da IA para aplicar padrões de codificação.
- **Implicações:**
  - **Autonomia Guiada:** Damos autonomia à IA (`F4_ImplementadorMestre`) para resolver uma tarefa específica, mas essa autonomia é guiada por um plano de ação **granular e sequencial** gerado previamente (`F2_Orchestrator`).
  - **Controle no Planejamento, Liberdade na Execução:** O controle rigoroso é movido da fase de implementação para a fase de planejamento. Isso libera o agente implementador para focar em uma tarefa pequena e bem definida, com máxima chance de sucesso.

## 3. Fonte Única da Verdade (SSOT) Dinâmica

- **Conceito:** A Fonte Única da Verdade (SSOT) não é estática; ela **evolui junto com o projeto**. A responsabilidade pela verdade de um artefato migra do planejamento para a realidade à medida que o código é escrito.
- **Implicações:**
  - **Fase de Planejamento:** O **`Blueprint Arquitetural`** é a SSOT para a arquitetura e o design de todo o sistema. A **`Ordem de Implementação`** é a SSOT para a sequência de trabalho.
  - **Após a Implementação:** Uma vez que um componente (ex: o `README.md`, os modelos de `Customer`) é implementado, a **`codebase` se torna a nova SSOT** para aquele componente.
  - **Justificativa da "Poda":** Este princípio é a justificativa fundamental para a estratégia do "Blueprint Evolutivo". Manter a especificação de um componente já implementado no `Blueprint` cria redundância e risco de inconsistência. A "poda" elimina essa redundância.

## 4. Contexto Focado e Evolutivo (Princípio Chave da v4.0)

- **Conceito:** A janela de atenção e contexto da IA é o recurso mais valioso e limitado do processo. Seu gerenciamento ativo é um princípio fundamental, não uma otimização opcional.
- **Implicações:**
  - **O "Blueprint Evolutivo":** O `Blueprint` é um documento vivo. Após a conclusão de marcos significativos (especialmente o `Alvo 0`), as seções que se tornaram redundantes (cuja SSOT agora é a codebase) são **removidas ("podadas")**.
  - **Contexto Mínimo Viável (MVC):** O Coordenador tem a responsabilidade de fornecer a cada agente o conjunto mínimo de informações necessárias para o sucesso da tarefa. Isso significa extrair ativamente do `Blueprint Evolutivo` apenas os trechos relevantes para um determinado alvo de implementação.
  - **Benefício Direto:** Manter a IA trabalhando em um ambiente de baixo ruído cognitivo maximiza a qualidade do output, aumenta a velocidade e reduz drasticamente o risco de erros, alucinações e falhas por estouro de contexto.

## 5. Validação Humana Crítica e Curadoria de Contexto

- **Conceito:** O Coordenador humano é a peça mais importante do processo. Seu papel é elevado de mero "instrutor" para **"Arquiteto, Revisor e Curador de Contexto"**.
- **Implicações:**
  - **Validação Contínua:** Nenhum output da IA (Blueprint, Ordem, Código) é aceito sem escrutínio humano.
  - **Curadoria Ativa:** Uma das tarefas mais críticas do Coordenador é a execução da estratégia do "Blueprint Evolutivo": realizar as "podas" e preparar os "pacotes de contexto focado" para o agente implementador. A qualidade do contexto fornecido à IA é diretamente proporcional à qualidade do código gerado.

## 6. Testes Abrangentes e Estruturados

- **Conceito:** A qualidade é verificada através de uma estratégia de testes multifacetada, com responsabilidades claras para cada tipo de teste, definidos desde a fase de planejamento.
- **Implicações:**
  - **Testes Unitários (TUs):** Gerados obrigatoriamente para todo o código de produção, com meta de alta cobertura da lógica de negócio.
  - **Testes de Integração (TIs):** Gerados em pontos estratégicos (definidos pelo `Orchestrator`) para validar a colaboração entre os componentes e o cumprimento dos contratos de API.

## 7. Integração Incremental via Contratos Explícitos

- **Conceito:** As conexões entre os módulos são definidas _antecipadamente_ através de contratos (Modelos de Domínio, DTOs, ViewModels) no `Blueprint`. A implementação ocorre de forma incremental, com os componentes sendo construídos para se encaixarem perfeitamente desde o início.
- **Implicações:**
  - Promove baixo acoplamento e alta coesão.
  - Facilita a testabilidade e o desenvolvimento paralelo (ex: Frontend-First ou API-First).
  - Reduz drasticamente os riscos da fase de integração.
