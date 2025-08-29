# Roteiro Estratégico do Método AGV: Desenvolvimento e Evolução (v4.0)

**Versão do Documento:** 4.0
**Data da Última Atualização:** [Data Atual da Nossa Interação]
**Status:** Atualizado para refletir a consolidação do Método AGV v4.0 (Lean & Strategic com Gestão Ativa de Contexto).

## 1. Introdução e Propósito

Este Roteiro Estratégico alinha a visão, define metas e acompanha a evolução do Método AGV. É um "documento vivo" que reflete nosso entendimento atual e direciona nossos esforços para aprimorar a colaboração humano-IA no desenvolvimento de software de alta qualidade, de forma escalável e robusta.

## 2. Filosofia e Visão Central (v4.0)

A filosofia do Método AGV evoluiu para a **"Direção Estratégica com Contexto Otimizado"**, fundamentada nos seguintes pilares:

- **Qualidade Como Premissa:** Padrões de engenharia de software de nível sênior desde o início.
- **Colaboração Estratégica:** Usar prompts que definem o "quê" (objetivos, critérios) e não o "como", confiando na capacidade latente da IA.
- **Gestão Ativa de Contexto:** O reconhecimento de que a janela de contexto da IA é o recurso mais crítico. A estratégia do **"Blueprint Evolutivo"** (poda de contexto) é central para a escalabilidade do método.
- **SSOT Dinâmica e Curadoria Humana:** O Coordenador é o arquiteto, revisor e, crucialmente, o **curador de contexto**, garantindo que a IA sempre opere com informações enxutas e relevantes.

**Visão de Longo Prazo:** Evoluir o Método AGV para que um Coordenador possa orquestrar a criação de sistemas complexos e prontos para produção com máxima eficiência e qualidade, superando os limites de contexto das ferramentas de IA.

## 3. Estado Atual (Consolidação da Estratégia v4.0)

**Onde Estamos:**

A jornada para o v4.0 foi marcada por uma descoberta fundamental sobre os limites da abordagem "Lean" e a necessidade de uma gestão de contexto mais sofisticada.

- **A Crise de Contexto Original:** O método inicial, com prompts de microgerenciamento, falhava devido à sobrecarga de contexto.
- **A Solução Parcial (A Abordagem "Lean"):** A transição para prompts "Lean" (focados no "O Quê") foi um sucesso para componentes pequenos e médios, resolvendo a crise inicial.
- **O Retorno da Crise de Contexto:** Ao aplicar o método "Lean" a projetos grandes e complexos (como o IABANK), descobrimos que o **próprio `Blueprint` se tornou o vilão**. Um `Blueprint` completo e detalhado, quando fornecido como contexto para cada tarefa de implementação, recriou a crise de sobrecarga, degradando a qualidade do output da IA.
- **A Solução Definitiva (O "Blueprint Evolutivo"):** O aprendizado chave foi que a solução não era menos detalhe no `Blueprint`, mas sim **gerenciar ativamente o `Blueprint` como um documento vivo**.

**Principal Aprendizado: A Primazia da Janela de Contexto.**
A otimização do contexto não é um "nice-to-have", é a disciplina mais importante do método. A solução para a escalabilidade é a **"poda"** do `Blueprint` após marcos de implementação, garantindo que o agente implementador sempre trabalhe com um contexto mínimo e relevante.

**Consequências Práticas (O Método v4.0):**

- **Fluxo de Trabalho:** O processo agora inclui uma etapa explícita de **"Poda do Blueprint"** após o Alvo 0.
- **Agentes Especializados:** O agente `F4` foi dividido em `F4-Scaffolder` (para o Alvo 0) e `F4-ImplementadorMestre` (para os demais), criando ferramentas mais focadas.
- **Papel do Coordenador:** O papel do Coordenador foi elevado para incluir a **"Curadoria de Contexto"** como uma responsabilidade primária.

## 4. Objetivos Estratégicos e Plano de Ação

Com a filosofia e o fluxo do v4.0 definidos, nossos objetivos se concentram em consolidar, validar e expandir o método.

### 4.1. Foco Imediato: Consolidação e Formalização do Método v4.0 (EM ANDAMENTO)

- **Estratégia:** Garantir que toda a documentação e ferramentas do Método AGV reflitam de forma precisa e consistente a nova abordagem v4.0.
- **Ações Chave:**
  1. **Atualizar Documentos Fundamentais:** Finalizar a atualização do `README.md`, `Principios_Chave.md`, `Workflow.md` e deste `Roteiro.md` para a versão 4.0. **(Esta tarefa está em andamento).**
  2. **Formalizar Novos Prompts:**
     - Criar o arquivo de prompt `Prompts/Templates/F4_Scaffolder_v1.0.md`.
     - Refatorar o `Prompt_F4_Implementador_Mestre` para remover a lógica do Alvo 0 e salvá-lo como uma nova versão.

### 4.2. Próximo Passo: Validação Prática em Larga Escala

- **Estratégia:** Aplicar o Método AGV v4.0 completo, do início ao fim, em um projeto complexo para validar a eficácia e a ergonomia da nova disciplina de "poda" do Blueprint.
- **Ações Chave:**
  1. **Retomar a Implementação do Projeto IABANK:** Utilizar o `Blueprint` detalhado e a `Ordem de Implementação` já gerados.
  2. Executar o fluxo v4.0 estritamente:
     - Usar o `F4-Scaffolder` para o Alvo 0.
     - Realizar a "poda" do `Blueprint` para criar a versão evolutiva.
     - Para cada alvo subsequente, praticar a curadoria de contexto, fornecendo ao `F4-Implementador` apenas as informações relevantes.
  3. **Coletar Métricas e Observações:** Documentar a experiência de usar o fluxo de "poda". É um processo fluido? Demanda muito esforço? A qualidade do output da IA se mantém alta ao longo do projeto?

### 4.3. Objetivos Futuros (Pós-Validação)

- **Estratégia:** Explorar novas otimizações e a automação de etapas do fluxo de trabalho.
- **Ações Chave (Exploratórias):**
  1. **Automatizar a Curadoria de Contexto:** Investigar a viabilidade de um agente `F3 - ContextFocuser`, que poderia automatizar a extração de contexto relevante do `Blueprint` para cada alvo.
  2. **Explorar Ferramentas e LLMs:** Avaliar continuamente novas LLMs e ferramentas de desenvolvimento (IDEs com IA, etc.) que possam se integrar ou aprimorar o Método AGV.
  3. **Refinar o Ciclo de Manutenção:** Aprimorar o prompt `F7 - Evolucionista` com base nos aprendizados da implementação do IABANK.

## 5. Revisão deste Roteiro

Este documento será revisado e atualizado nos seguintes marcos:

- Após a conclusão da "Fase de Consolidação" (quando todos os documentos e prompts estiverem atualizados para v4.0).
- Após a conclusão do projeto piloto IABANK.
- Quando houver uma mudança substancial na estratégia ou nas capacidades das ferramentas de IA.
