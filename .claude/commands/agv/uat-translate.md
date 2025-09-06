Analise os cenários de teste de aceitação do usuário (UAT) e o Blueprint Arquitetural para gerar scripts de teste automatizados correspondentes. Estes testes devem validar a funcionalidade descrita interagindo diretamente com os serviços da camada de aplicação e infraestrutura (backend), sem usar a UI.

FONTES DA VERDADE (SSOT):

1. Cenários UAT para Tradução: Documento de cenários gerados pelo F5-UAT-Generator
2. Blueprint Arquitetural: A autoridade máxima para arquitetura e serviços
3. Código Fonte do Projeto: Acesso ao workspace para referências de implementação

INSTRUÇÕES DETALHADAS:

1. ANÁLISE COMBINADA:
   - Para cada cenário UAT, traduza os "Passos para Execução" em uma sequência de chamadas aos serviços da Camada de Aplicação conforme descrito no Blueprint.
   - Consulte o Blueprint para entender como instanciar esses serviços e quais dependências (interfaces) eles exigem.

2. GERAÇÃO DE SCRIPTS DE TESTE:
   - Para cada cenário UAT, crie uma ou mais funções de teste no framework apropriado da stack tecnológica.
   - Use fixtures e implementações "Fake" (se disponíveis no contexto) ou "Mocks" para simular as dependências de infraestrutura (I/O de disco, etc.), permitindo um teste controlado do backend.

3. IMPLEMENTAÇÃO DE CADA TESTE:
   - a. Setup: Configure o ambiente de teste em memória (usando Fakes/Mocks) para satisfazer as "Pré-condições" do UAT.
   - b. Instanciação: Instancie os serviços da camada de aplicação, injetando as dependências fake/mockadas.
   - c. Execução: Chame os métodos dos serviços de aplicação para executar a lógica funcional do cenário.
   - d. Asserções: Verifique os "Resultados Esperados" através de asserções programáticas sobre o estado dos fakes/mocks ou os valores retornados pelos serviços.

4. BOAS PRÁTICAS:
   - Mantenha os testes independentes e use nomes descritivos.
   - Siga as convenções de estilo da linguagem definidas no Blueprint.

FORMATO DO OUTPUT:

Gere os arquivos de teste contendo os scripts de teste automatizados completos e executáveis, seguindo a estrutura de diretórios de testes definida no Blueprint.