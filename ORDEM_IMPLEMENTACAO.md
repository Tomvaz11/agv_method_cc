## Ordem de Implementação e Cenários de Teste de Integração

**Alvo 0:** Foundation DNA

**Alvo 1:** Configuração Inicial: Estrutura do Monorepo, Docker, CI/CD (`.github/workflows`), linters (`.pre-commit-config.yaml`) e dependências (`pyproject.toml`, `package.json`).

**Alvo 2:** iabank.core: Modelos (`Tenant`, `BaseTenantModel`) e Migrações iniciais.

**Alvo 3:** Configuração: Registrar app `core` em `INSTALLED_APPS`.

**Alvo 4:** iabank.users: Modelo (`User`) e Migrações.

**Alvo 5:** Configuração: Registrar app `users` em `INSTALLED_APPS`.

**Alvo 6:** iabank.users: Implementação da Autenticação JWT (Serializers, Views, URLs).

**Alvo 7:** Configuração: Registrar rotas de autenticação no URLconf principal e configurar o DRF para usar Autenticação JWT em `settings.py`.

> > > **BASELINE VALIDATION T1** (Foundation Complete) <<<

- **Módulos no Grupo:** `core`, `users`
- **Objetivo do Teste:** Validar a fundação da arquitetura, incluindo a estrutura do projeto, o sistema de multi-tenancy nos modelos base e o fluxo completo de autenticação JWT, garantindo que endpoints protegidos não sejam acessíveis sem um token válido.
- **Cenários Chave:**
  1.  **Acesso Não Autorizado:** Tentar acessar um endpoint protegido (ex: um futuro `/api/v1/customers/`) sem um token de autenticação e verificar se a resposta é `401 Unauthorized`.
  2.  **Obtenção de Token:** Enviar credenciais de um usuário (criado via `factory-boy`) para o endpoint de login e verificar se um par de tokens (access, refresh) é retornado com sucesso (`200 OK`).
  3.  **Acesso Autorizado:** Usar o token de acesso obtido no cenário 2 para acessar um endpoint de teste protegido e verificar se a resposta é `200 OK`.
  4.  **Consistência de Tenant:** Criar um `User` via `factory-boy` e verificar programaticamente que seu campo `tenant` foi corretamente associado, validando a herança de `BaseTenantModel`.

**Alvo 8:** iabank.customers: Modelos (`Customer`) e Migrações.

**Alvo 9:** Configuração: Registrar app `customers` em `INSTALLED_APPS`.

**Alvo 10:** iabank.customers: Serializers (`CustomerCreateDTO`, `CustomerListDTO`, etc.).

**Alvo 11:** iabank.customers: Views (`CustomerViewSet`) e Permissões baseadas em tenant.

**Alvo 12:** iabank.customers: Roteamento (URLs do app `customers`).

**Alvo 13:** Configuração: Registrar rotas de `customers` no URLconf principal.

> > > **PARADA DE TESTES DE INTEGRAÇÃO T2** (CRUD de Clientes com Isolamento de Tenant) <<<

- **Módulos no Grupo:** `customers`
- **Objetivo do Teste:** Validar o ciclo de vida completo (CRUD) da entidade `Customer`, garantindo que todas as operações respeitem rigorosamente o isolamento de dados imposto pela arquitetura multi-tenant.
- **Cenários Chave:**
  1.  **Criação com Tenant Correto:** Usando um usuário autenticado simulado do `tenant_A`, criar um novo cliente via `POST /api/v1/customers/`. Verificar no banco de dados que o cliente criado foi associado ao `tenant_A`.
  2.  **Listagem Isolada:** Criar clientes para `tenant_A` e `tenant_B`. Fazer uma requisição `GET /api/v1/customers/` autenticado como um usuário do `tenant_A` e verificar que a lista contém **apenas** os clientes do `tenant_A`.
  3.  **Acesso Direto Bloqueado:** Autenticado como usuário do `tenant_A`, tentar acessar os detalhes de um cliente do `tenant_B` via `GET /api/v1/customers/{customer_B_id}/`. A resposta DEVE ser `404 Not Found`.
  4.  **Atualização Restrita:** Tentar atualizar um cliente do `tenant_B` (`PUT /api/v1/customers/{customer_B_id}/`) estando autenticado como usuário do `tenant_A` e verificar se a operação falha com `404 Not Found`.

**Alvo 14:** iabank.operations: Modelos (`Consultant`) e Migrações.

**Alvo 15:** Configuração: Registrar app `operations` em `INSTALLED_APPS`.

**Alvo 16:** iabank.operations: Implementação do CRUD para `Consultant` (Serializers, Views, URLs).

**Alvo 17:** Configuração: Registrar rotas de `consultants` no URLconf principal.

> > > **PARADA DE TESTES DE INTEGRAÇÃO T3** (CRUD de Consultores) <<<

- **Módulos no Grupo:** `operations` (parcial)
- **Objetivo do Teste:** Validar a gestão da entidade `Consultant`, que possui uma relação `OneToOne` com o `User`, garantindo que a criação e listagem respeitem as regras de tenant.
- **Cenários Chave:**
  1.  **Criação de Consultor:** Dado um `User` existente no `tenant_A` que ainda não é um consultor, criar um `Consultant` associado a ele. Verificar se a relação `OneToOne` é estabelecida corretamente.
  2.  **Prevenção de Duplicidade:** Tentar criar um segundo `Consultant` para o mesmo `User` e verificar se a API retorna um erro de validação (`4xx`).
  3.  **Listagem Isolada de Consultores:** Autenticado como um usuário do `tenant_A`, listar os consultores e verificar que apenas os consultores cujo `User` associado pertence ao `tenant_A` são retornados.

**Alvo 18:** iabank.operations: Modelos (`Loan`, `Installment`) e Migrações.

**Alvo 19:** iabank.operations: Serviços de Aplicação (`LoanService` com lógica de criação de empréstimo e cálculo/geração de parcelas).

**Alvo 20:** iabank.operations: Serializers e DTOs (`LoanCreateDTO`, `LoanListDTO`).

**Alvo 21:** iabank.operations: Views (`LoanViewSet` utilizando o `LoanService` para orquestrar a criação).

**Alvo 22:** iabank.operations: Roteamento (URLs para `loans`).

**Alvo 23:** Configuração: Registrar rotas de `loans` no URLconf principal.

> > > **PARADA DE TESTES DE INTEGRAÇÃO T4** (Criação de Empréstimo e Geração de Parcelas) <<<

- **Módulos no Grupo:** `operations` (completo)
- **Objetivo do Teste:** Validar o fluxo de negócio mais crítico: a criação de um `Loan`. O teste deve verificar a orquestração do `LoanService`, a correta geração das `Installments` e a validação das relações entre `Loan`, `Customer` e `Consultant` dentro do mesmo tenant.
- **Cenários Chave:**
  1.  **Criação de Empréstimo com Sucesso:** Dado um `Customer` e um `Consultant` pertencentes ao `tenant_A`, criar um novo `Loan` via `POST /api/v1/loans/`. Verificar se o `Loan` é criado e se o número correto de `Installments` (conforme `number_of_installments`) é gerado no banco de dados, todas associadas ao novo empréstimo.
  2.  **Validação de Inconsistência de Tenant:** Tentar criar um `Loan` para um `Customer` do `tenant_A` mas associá-lo a um `Consultant` do `tenant_B`. A requisição deve falhar com um erro de validação (`4xx`), impedindo a violação de tenant.
  3.  **Lógica de Cálculo de Parcelas:** Criar um empréstimo simples (ex: 1000.00, 10% juros, 2 parcelas) e verificar se o valor (`amount_due`) da primeira parcela está matematicamente correto, conforme a lógica de negócio definida no `LoanService`.
  4.  **Proteção de Entidades Relacionadas:** Tentar deletar um `Customer` que possui um `Loan` associado e verificar que a operação é bloqueada pelo `on_delete=models.PROTECT`, retornando um erro de integridade (`4xx` ou `5xx`, dependendo do handler).

**Alvo 24:** Frontend: Estrutura de diretórios inicial (Vite, TypeScript, Tailwind, `Feature-based`).

**Alvo 25:** Frontend (UI-1): Camada `shared/ui` (Componentes puros: Button, Input, SmartTable, StatusBadge, DatePicker).

**Alvo 26:** Frontend (UI-2): Camada `shared/api` e `shared/lib` (Configuração do cliente Axios, setup do TanStack Query, hooks genéricos).

> > > **PARADA DE TESTES DE INTEGRAÇÃO T5** (UI Foundation e Component Library) <<<

- **Módulos no Grupo:** `frontend/src/shared`
- **Objetivo do Teste:** Validar a biblioteca de componentes de UI de base e a configuração da camada de comunicação com a API. Idealmente, isso é feito com testes de componentes (ex: Storybook/Jest) e não requer um backend totalmente funcional.
- **Cenários Chave:**
  1.  **Renderização de Componentes:** Verificar se componentes como `Button` e `Input` renderizam corretamente e respondem a eventos (ex: `onClick`).
  2.  **Tabela Inteligente:** Testar o componente `SmartTable` com dados mockados, validando suas funcionalidades de paginação e ordenação local.
  3.  **Configuração de API:** Fazer uma chamada mockada usando o cliente Axios configurado e verificar se os interceptadores (ex: para adicionar o token de autenticação) são acionados.

**Alvo 27:** Frontend (UI-3): Camada `entities` (Componentes `CustomerAvatar`, tipos `Customer`, hooks `useCustomer`).

**Alvo 28:** Frontend (UI-4): Camada `features` (Implementação da lógica de API para Login e CRUD de Clientes usando TanStack Query: `useLoginMutation`, `useCustomersQuery`, `useCreateCustomerMutation`).

**Alvo 29:** Frontend (UI-5): Camada `app` e `pages` (Configuração do roteador, composição da tela de Login e da página de Lista de Clientes).

> > > **PARADA DE TESTES DE INTEGRAÇÃO T6** (Fluxo E2E de Login e Listagem de Clientes) <<<

- **Módulos no Grupo:** `frontend/src` (completo para o fluxo de Clientes)
- **Objetivo do Teste:** Validar o primeiro fluxo de ponta a ponta (E2E) da aplicação, desde a autenticação do usuário até a exibição e interação com a lista de clientes, garantindo a correta integração entre o frontend (React/TanStack Query) e o backend (DRF API).
- **Cenários Chave:**
  1.  **Fluxo de Login:** Na tela de login, inserir credenciais válidas, submeter o formulário e verificar se o usuário é redirecionado para o dashboard/lista de clientes e se o token JWT é armazenado.
  2.  **Exibição de Dados da API:** Na página de lista de clientes, verificar se a tabela é populada com os dados vindos da API (`GET /api/v1/customers/`), exibindo corretamente o nome, documento, etc.
  3.  **Criação via UI:** Abrir o modal/formulário de criação de cliente, preencher os dados, submeter e verificar se a tabela é automaticamente atualizada (via revalidação do TanStack Query) com o novo cliente.
  4.  **Estado de Carregamento e Erro:** Simular uma resposta lenta ou um erro da API de listagem de clientes e verificar se a UI exibe um estado de carregamento (ex: spinner) e uma mensagem de erro apropriada, respectivamente.
