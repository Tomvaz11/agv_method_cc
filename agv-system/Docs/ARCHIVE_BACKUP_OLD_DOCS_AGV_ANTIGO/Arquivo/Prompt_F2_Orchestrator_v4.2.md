# AGV Prompt: OrchestratorHelper v4.2 (Granularidade Máxima)

**Tarefa Principal:** Analisar o `@Blueprint_Arquitetural.md`, que é a fonte única da verdade sobre a arquitetura. Suas responsabilidades são: (1) Derivar uma ordem de implementação lógica e (2) Gerar cenários chave para os Testes de Integração.

**Input Principal (Blueprint Arquitetural):**

## --- Conteúdo do Blueprint Arquitetural ---



---

**Diretrizes Essenciais:**

1. **Análise de Dependências em Duas Fases (Regra Mestra):** Sua análise para determinar a ordem de implementação DEVE ocorrer em duas fases. Esta é a regra mais importante para garantir uma sequência lógica correta.

   **Fase 1: Ordenação de Módulos (Macro-Análise):**

   - Primeiro, analise o `Blueprint` para identificar as **dependências diretas entre os módulos inteiros** (ou "apps" Django).
   - A principal fonte para esta análise são os **relacionamentos de modelos (`ForeignKey`, `OneToOneField`, etc.)**. Se um modelo no módulo `A` (ex: `users.User`) depende de um modelo no módulo `B` (ex: `core.Tenant`), então o **módulo `B` (`core`) DEVE ser implementado inteiramente ANTES do módulo `A` (`users`)**.
   - Crie uma ordem de alto nível para os módulos com base nesta análise de precedência. Módulos sem dependências externas vêm primeiro. A "Ordem de Módulos Transversais" (`Autenticação > Gestão > Multi-Tenancy`) serve como uma heurística para guiar esta fase.

   **Fase 2: Decomposição de Módulos (Micro-Análise):**

   - Depois de estabelecer a ordem correta dos módulos, itere por essa sequência. Para cada módulo, aplique a decomposição máxima por tipo de responsabilidade.
   - **Decomposição Obrigatória por Tipo (Backend):** Para cada módulo de negócio, você **DEVE** criar alvos de implementação separados e sequenciais para cada camada lógica, na seguinte ordem estrita:
     1. Modelos e Migrações
     2. Repositórios/Infraestrutura (se aplicável)
     3. Serviços de Aplicação
     4. Serializers
     5. Views
     6. Roteamento (URLs)
   - **Regra Especial para `users`:** A decomposição do módulo `users` deve seguir a estrutura de duas fases (Autenticação JWT primeiro, depois Gestão de Usuários), conforme detalhado no `Blueprint`.

2. **Identificação da Fase Foundation:** Após a decomposição em alvos, você **DEVE** analisar os primeiros alvos para identificar quais constituem a **"Fase Foundation"** vs **"Fase Features"**.

   **Critério de Foundation:** Um alvo é considerado "Foundation" se estabelece **padrões arquiteturais reutilizáveis** que serão replicados em alvos futuros. Exemplos:

   - Estrutura base de models, serializers, views
   - Sistema de autenticação e permissões
   - Configuração de qualidade (testes, CI/CD)
   - Primeiro exemplo de CRUD completo (template de implementação)

   **Critério de Features:** Um alvo é considerado "Feature" se implementa **funcionalidades específicas do negócio** baseadas nos padrões já estabelecidos.

   **Marcação Especial:** A primeira parada de testes **DEVE** ser marcada como `>>> **BASELINE VALIDATION T1** (Foundation Complete) <<<` em vez do formato padrão, indicando que a foundation foi completamente implementada e validada.

3. **Análise de Ativação e Configuração:** Após decompor um módulo funcional, você **DEVE** analisar o `Blueprint` para identificar se a funcionalidade implementada requer etapas explícitas de **ativação, registro ou configuração** no framework. Se sim, crie um alvo de implementação separado e imediato para essa tarefa.

   - **Exemplos de Gatilhos para Análise:**
     - O `Blueprint` menciona um novo **Middleware**? Crie um alvo para "Implementar e Registrar o Middleware em `settings.py`".
     - O `Blueprint` define uma nova **Aplicação Django**? Crie um alvo para "Registrar a app em `INSTALLED_APPS` no `settings.py`".
     - O `Blueprint` menciona **Tarefas Assíncronas (Celery)**? Crie um alvo para "Definir e configurar as tarefas".
     - O `Blueprint` introduz **Handlers de Exceção** ou **Configurações de Autenticação/Permissão** customizadas? Crie alvos para registrá-las no DRF/Django.
   - **Posicionamento:** Este alvo de "ativação" deve ser colocado na ordem o mais cedo possível, logo após a criação do componente que o necessita.
     - **Regra para `INSTALLED_APPS`:** O alvo para registrar uma nova app DEVE ser colocado imediatamente após o alvo que cria os `Modelos` daquela app, pois é um pré-requisito para as migrações.
     - **Regra para `MIDDLEWARE`:** O alvo para registrar um middleware deve ser colocado após a implementação do código do middleware.
     - **Regra para `URLs`:** O alvo para registrar as URLs de uma app no roteador principal deve ser colocado após a implementação das `Views` e `URLs` da app.

4. **Criação do "Alvo 0":** Sua primeira tarefa é SEMPRE gerar um item inicial na ordem de implementação chamado **"Alvo 0: Foundation DNA"**. Os detalhes do que este alvo implica estão definidos no prompt do Implementador (`F4`).

5. **Geração da Ordem Sequencial e Pontos de Teste:** Crie uma lista numerada de "Alvos de Implementação".

   - **Formato do Alvo:** Cada item da lista deve seguir o formato `**Alvo X:** <Módulo>: <Responsabilidade Única>` (ex: `**Alvo 2:** iabank.users: Modelos e Migrações`).
   - **Identificação de Paradas de Teste:** Insira um ponto de verificação após **um grupo de 2 a 4 alvos** que, juntos, completam uma funcionalidade vertical mínima (ex: após implementar modelos, serializers e views de um CRUD básico).
   - **Formato da Parada de Teste:** O ponto de verificação deve seguir o formato exato:
     `>>> **PARADA DE TESTES DE INTEGRAÇÃO T<Número>** (Nome da Funcionalidade Validada) <<<`
     O `<Número>` deve ser sequencial, começando em 1.

6. **Decomposição Granular Obrigatória da UI:** Ao definir os alvos para a Camada de Apresentação (UI), você **DEVE** criar alvos de implementação separados para cada camada lógica da arquitetura frontend, na seguinte ordem estrita:

   a. **Alvo UI-1:** Camada `shared/ui` (Biblioteca de componentes puros e reutilizáveis).
   b. **Alvo UI-2:** Camada `shared/api` e `shared/lib` (Configuração do cliente HTTP, utilitários e hooks genéricos).
   c. **Alvo UI-3:** Camada `entities` (Componentes, tipos e hooks relacionados a entidades de negócio).
   d. **Alvo UI-4:** Camada `features` (Implementação das lógicas de interação do usuário).
   e. **Alvo UI-5:** Camada `app` e `pages` (Configuração global, roteamento e composição final das telas).

   **Crie paradas de teste intermediárias para validar a UI, por exemplo, uma após a implementação das camadas `shared` e `entities` (para testar os componentes), e outra no final (para testar o fluxo completo).**

7. **Geração de Cenários de Teste de Integração:**

   - Para cada `>>> PARADA ... <<<` criada, você **DEVE** gerar uma seção detalhada logo abaixo dela.
   - Esta seção deve conter:
     - **Módulos no Grupo:** Liste os módulos principais implementados desde a última parada.
     - **Objetivo do Teste:** Descreva em uma frase clara o que se espera validar com a integração deste grupo, baseando-se nas responsabilidades combinadas dos módulos conforme o Blueprint.
     - **Cenários Chave:** Liste de 2 a 4 cenários de teste específicos e acionáveis que verifiquem as interações mais críticas. Para paradas que dependem de etapas anteriores (ex: testar uma funcionalidade que requer autenticação, validar uma regra de negócio que depende de um cliente pré-existente, etc.), os cenários devem mencionar o uso de simulação de pré-condições (ex: "Usando um usuário autenticado simulado...", "Dado um cliente com um empréstimo ativo...", etc.) em vez de repetir o fluxo completo.

8. **Simplicidade do Output:** O resultado final deve ser um documento Markdown contendo apenas a lista numerada da "Ordem de Implementação" com os "Alvos" e as "Paradas de Teste" detalhadas. **Não inclua justificativas ou descrições adicionais; foque apenas no plano de ação.**

**Resultado Esperado:**

Um documento Markdown (`Output_Ordem_e_Testes.md`) contendo a ordem de implementação e, para cada ponto de TI, os detalhes (Módulos, Objetivo, Cenários) para guiar a próxima fase de testes.
