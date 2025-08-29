# Método AGV v4.0 (Lean & Strategic) - Desenvolvimento de Software com IA

![Status](https://img.shields.io/badge/Status-Validado%20e%20em%20Uso-blue)
![Versão do Método](<https://img.shields.io/badge/Método-v4.0%20(Lean%20%26%20Strategic)-brightgreen>)

## 1. Introdução

Bem-vindo ao repositório do **Método AGV (Assistência Generativa à Velocidade)**. Este projeto documenta uma metodologia estruturada e iterativa para desenvolver software de **qualidade profissional sênior**, através da colaboração estratégica entre um coordenador humano e Modelos de Linguagem Grandes (LLMs) atuando como assistentes especializados ("Agentes").

O objetivo é superar a qualidade de um desenvolvimento apressado, focando rigorosamente em código limpo, arquitetura robusta e escalável, e alta cobertura de testes. O método foi extensivamente validado e refinado através de múltiplos projetos.

## 2. Filosofia e Visão Central (Lean & Strategic)

A versão 4.0 do método representa uma evolução filosófica fundamental, passando do "microgerenciamento" para a **"Direção Estratégica com Contexto Otimizado"**.

- **Confiança na Capacidade Latente da IA:** Confiamos que LLMs de ponta já possuem um vasto conhecimento de boas práticas (SOLID, padrões de design, etc.). Não precisamos soletrar cada passo da implementação.
- **Foco no "O Quê", Não no "Como":** Nossos prompts definem os **objetivos, requisitos e critérios de qualidade** (`O Quê`), dando à IA autonomia para determinar `Como` alcançar o resultado.
- **Gestão Ativa do Contexto (Princípio do "Blueprint Evolutivo"):** Reconhecemos que a janela de contexto da IA é um recurso precioso e finito.
  - O **Blueprint Arquitetural** é a fonte da verdade, mas ele é um **documento vivo**.
  - Após a implementação de marcos (como o setup inicial do projeto), as seções correspondentes do Blueprint são "podadas" ou removidas.
  - Isso garante que a IA sempre trabalhe com um **contexto enxuto e relevante**, maximizando a qualidade e minimizando o risco de erros por sobrecarga cognitiva.
- **Fonte Única da Verdade (SSOT) Dinâmica:** A SSOT de uma funcionalidade **migra** do `Blueprint` para a `codebase` assim que ela é implementada, justificando a "poda" do Blueprint.

➡️ **Para detalhes aprofundados sobre a filosofia, consulte:**
[`Guides/AGV_Method_Principios_Chave_v4.0.md`](./Guides/AGV_Method_Principios_Chave_v4.0.md)

## 3. Os Agentes AGV (v4.0)

O trabalho é orquestrado através de prompts especializados que invocam "agentes" com papéis claros:

- **F1 - Tocrisna (IA - Arquiteta):** Define a arquitetura técnica completa, componentes, modelos, DTOs e ViewModels no **Blueprint Arquitetural inicial**.
  - _Prompt:_ `Prompts/Templates/F1_Tocrisna_Architecture_vX.X.md` (versão atualizada)
- **F2 - OrchestratorHelper (IA - Planejadora Granular):** Analisa o Blueprint e gera a sequência de implementação detalhada, camada por camada, com pontos de parada para testes.
  - _Prompt:_ `Prompts/Templates/F2_Orchestrator_vX.X_granular.md`
- **F4-Scaffolder (NOVO) (IA - Engenheira de Setup):** Executa **apenas o Alvo 0**, criando toda a estrutura de diretórios, arquivos de configuração e o "andaime" do projeto.
  - _Prompt:_ `Prompts/Templates/F4_Scaffolder_v1.0.md` (a ser criado)
- **F4 - ImplementadorMestre (IA - Engenheira de Implementação):** Implementa um componente funcional e seus testes unitários, seguindo a ordem e o contexto focado.
  - _Prompt:_ `Prompts/Templates/F4_Implementador_Mestre_vX.X.md` (refatorado sem o Alvo 0)
- **F7 - Evolucionista (IA - Engenheira de Manutenção):** Modifica, corrige ou adiciona funcionalidades a uma codebase existente, respeitando estritamente o Blueprint e a arquitetura.
  - _Prompt:_ `Prompts/Templates/F7_Evolucionista_v1.0.md`

## 4. Fluxo de Trabalho Resumido (v4.0 com Blueprint Evolutivo)

1. **Definição (Coordenador):** Visão, escopo e stack tecnológica.
2. **Arquitetura (F1 - Tocrisna):** Geração do **Blueprint Mestre (v1.0)**, completo e detalhado. _[Validação Humana Crítica]_
3. **Planejamento (F2 - OrchestratorHelper):** Geração da **Ordem de Implementação Geral**. _[Validação Humana]_
4. **Setup do Projeto (F4-Scaffolder):**
   - a. IA executa o `Alvo 0` para criar o scaffolding do projeto.
   - b. **PODA DO BLUEPRINT (Coordenador):** O Coordenador cria o **Blueprint Evolutivo (v1.1)** removendo as seções de setup (README, .gitignore, etc.) que já foram materializadas na codebase.
5. **Ciclo de Implementação e Validação (Iterativo):**
   - a. **Implementação (F4 - ImplementadorMestre):** IA implementa o alvo atual usando o **Blueprint Evolutivo** como contexto.
   - b. **Validação (Coordenador):** O Coordenador valida o código e os testes. _[Ciclo de Refinamento até a aprovação]_
6. **Commit e Próximo Item:** Após a validação, o código é versionado e o ciclo continua. O Coordenador pode realizar mais "podas" no Blueprint em marcos maiores.

➡️ **Para o fluxo detalhado, consulte:**
[`Guides/AGV_Method_Workflow_v4.0.md`](./Guides/AGV_Method_Workflow_v4.0.md)

## 5. Como Usar o Método AGV (v4.0)

1. **Familiarize-se:** Leia os documentos em `Guides/`.
2. **Fase 1 e 2:** Use `F1_Tocrisna` e `F2_Orchestrator` para gerar o planejamento inicial.
3. **Setup:** Use o novo `F4_Scaffolder` para executar o Alvo 0.
4. **PODA:** Crie a primeira versão do seu **Blueprint Evolutivo**, removendo o conteúdo do Alvo 0. Este se torna seu principal documento de contexto.
5. **Implemente:** Siga a ordem de implementação usando o `F4_ImplementadorMestre` e o **Blueprint Evolutivo** como contexto.
6. **Evolua:** À medida que o projeto cresce, continue a "podar" o Blueprint para mantê-lo enxuto e relevante. Use o `F7_Evolucionista` para manutenções e novas features.

## 6. Status Atual e Próximos Passos (do Método)

- **Validação da Abordagem "Blueprint Evolutivo":** A estratégia de "podar" o Blueprint para otimizar o contexto foi identificada como a solução chave para escalar o método para projetos grandes e complexos, resolvendo a crise de sobrecarga de contexto de forma pragmática.
- **Especialização dos Agentes:** O `ImplementadorMestre` foi dividido em `F4-Scaffolder` e `F4-ImplementadorMestre`, criando ferramentas mais especializadas e eficientes.
- **Próximos Passos:**
  1. **Consolidar a Documentação (EM ANDAMENTO):** Finalizar a atualização de todos os documentos do método (`Workflow`, `Princípios`, `Roteiro`) para a versão 4.0.
  2. **Formalizar Novos Prompts:** Criar o arquivo `F4_Scaffolder_v1.0.md` e refatorar o `F4_Implementador_Mestre`.
  3. **Aplicar no Projeto Piloto:** Implementar o projeto IABANK usando o fluxo v4.0 completo, validando a eficácia da "poda" do Blueprint na prática.
