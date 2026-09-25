# Gerenciador de Notas — Projeto Tkinter (SENAI)

## 1. Objetivo geral

Desenvolver um aplicativo desktop em Python, usando Tkinter, para gerenciar
notas de alunos: cadastrar avaliações, calcular a média de cada aluno,
classificar sua situação (Aprovado / Recuperação / Reprovado) e apresentar
um resumo geral da turma. O projeto aplica conceitos de interface gráfica,
tratamento de eventos, validação de dados e persistência.

### 1.2 Capacidades trabalhadas

- Investigar uma biblioteca técnica (Tkinter/ttk) e selecionar fontes confiáveis.
- Planejar uma solução a partir de um problema e de requisitos.
- Construir interfaces gráficas orientadas a eventos.
- Organizar o código com funções, módulos e classes.
- Validar entradas, tratar exceções e preservar a consistência dos dados.
- Testar, documentar, apresentar e justificar decisões técnicas.
- Trabalhar com autonomia, organização, precisão e responsabilidade.

### 1.3 Evidências obrigatórias

| Evidência | O que demonstra |
|---|---|
| Pesquisa técnica | Este README (seções 1 a 5) documenta os conceitos, exemplos e fontes usados. |
| Proposta e esboço | Seção 3 — problema atendido, público, funcionalidades e dados planejados. |
| Código-fonte | `main.py`, `interface.py`, `dados.py`, `validacoes.py` — aplicativo executável, legível e organizado. |
| Testes | Seção 7 — casos executados, resultados obtidos e evidências das correções. |
| Documentação | Este README — instalação, uso, estrutura e limitações. |
| Apresentação | Seção 8 — roteiro sugerido para demonstrar o problema, a solução e as escolhas técnicas. |

## 2. Fontes consultadas

- Documentação oficial do Python — módulo `tkinter`: https://docs.python.org/3/library/tkinter.html
- Documentação oficial dos widgets `ttk` (temas e componentes): https://docs.python.org/3/library/tkinter.ttk.html
- Documentação oficial do módulo `json` (usado para persistência): https://docs.python.org/3/library/json.html

## 3. Escolha do problema

**Opção escolhida:** Gerenciador de notas.

**Problema atendido:** calcular médias e acompanhar resultados de alunos.

**Dados possíveis:** aluno, turma, avaliações, média e situação.

**Público:** professores ou responsáveis por turma que precisam registrar
avaliações e acompanhar o desempenho dos alunos sem depender de planilhas
externas.

## 4. Requisitos

### 4.0 Requisitos funcionais e não funcionais

| ID | Requisito |
|---|---|
| RF01 | Permitir cadastrar um aluno com nome, turma e uma ou mais avaliações. |
| RF02 | Listar os alunos cadastrados em um Treeview (nome, turma, média, situação). |
| RF03 | Permitir pesquisar por nome e filtrar por turma. |
| RF04 | Permitir selecionar um aluno na lista e editar seus dados. |
| RF05 | Permitir excluir um aluno somente após confirmação. |
| RF06 | Permitir limpar o formulário e iniciar um novo cadastro. |
| RF07 | Manter os dados disponíveis depois que o programa for encerrado (arquivo JSON). |
| RF08 | Exibir um resumo com total de alunos, média geral, aprovados, em recuperação e reprovados. |
| RNF01 | Usar Tkinter e componentes `ttk`. |
| RNF02 | Apresentar título, rótulos, ordem visual e mensagens compreensíveis. |
| RNF03 | Validar campos obrigatórios, formato e limite das notas (0 a 10) antes de salvar. |
| RNF04 | Tratar erros previsíveis (ex.: arquivo de dados corrompido) sem encerrar o aplicativo. |
| RNF05 | Organizar o código em módulos com nomes claros (`dados.py`, `validacoes.py`, `interface.py`). |
| RNF06 | Solicitar confirmação antes de excluir um aluno e antes de sair com alterações pendentes. |

### 4.1 Componentes mínimos da interface

- Janela principal com título "Gerenciador de Notas - SENAI" e tamanho inicial 880x600.
- Três áreas funcionais: **Cadastro**, **Consulta** (com pesquisa) e **Resumo**.
- Seis ou mais tipos de widgets: `Entry`, `Button`, `Label`, `Combobox`, `Treeview`, `Listbox` e `Scrollbar`.
- Uso consistente de `grid` (formulário e resumo) e `pack` (dentro de cada contêiner).
- Mensagens de sucesso, aviso e confirmação via `messagebox`.
- Navegação por teclado: tecla Enter adiciona a nota digitada.

## 5. Planejamento da solução

### 5.1 Fluxo principal

1. O usuário abre o aplicativo.
2. O sistema carrega os alunos já salvos no arquivo `dados/alunos.json`.
3. O usuário cadastra, pesquisa, edita ou exclui alunos.
4. O sistema valida a operação e apresenta retorno (mensagem de sucesso ou erro).
5. Os dados e os indicadores do resumo são atualizados na tela.
6. O usuário encerra o aplicativo; se houver alterações não salvas no formulário, o sistema pede confirmação.

## 6. Roteiro de desenvolvimento

| Etapa | Ações | Evidência |
|---|---|---|
| 1. Preparar | Criar pasta, ambiente virtual e `main.py`. Verificar se Tkinter abre uma janela. | Captura da janela inicial. |
| 2. Prototipar | Construir a estrutura visual com `Frame`, rótulos, campos e botões. | Interface navegável. |
| 3. Implementar cadastro | Criar funções de leitura dos campos, validação e inclusão. | Cadastro válido e inválido testados. |
| 4. Completar CRUD | Adicionar consulta, seleção, edição, exclusão e limpeza. | Operações funcionando. |
| 5. Persistir | Salvar e carregar dados em JSON. | Dados preservados ao reabrir. |
| 6. Refinar | Melhorar mensagens, foco, alinhamento e tratamento de erros. | Versão candidata. |
| 7. Testar | Executar casos positivos, negativos e de limite. Corrigir falhas. | Tabela de testes e evidências (seção 7). |
| 8. Documentar | Finalizar pesquisa, README e apresentação. | Pacote de entrega completo. |

### 6.1 Estrutura do projeto

```
projeto_tkinter/
  main.py
  interface.py
  dados.py
  validacoes.py
  dados/
    alunos.json
  evidencias/
  README.md
```

### 6.2 Boas práticas aplicadas

- Cada arquivo tem uma única responsabilidade (interface, dados, validações).
- Regras de validação e acesso a dados separadas da interface.
- Nomes descritivos para funções e variáveis; sem código comentado/abandonado.
- Nenhum comando SQL é usado (persistência é feita em JSON).
- Leitura e escrita de arquivo tratadas com `try/except`, sem `except` genérico silencioso.

## 7. Como executar

Pré-requisito: Python 3.10 ou superior (Tkinter já vem incluído na instalação padrão do Python no Windows e no macOS; no Linux pode ser necessário instalar o pacote `python3-tk`).

```bash
cd projeto_tkinter
python main.py
```

Os dados são salvos automaticamente em `dados/alunos.json` a cada operação de salvar ou excluir.

## 8. Plano e registro de testes

### 8.1 Casos de teste

| ID | Cenário e dados | Resultado esperado | Situação |
|---|---|---|---|
| CT01 | Cadastro com dados válidos (nome, turma e 3 notas). | Aluno aparece na lista com média e situação corretas. | Não executado |
| CT02 | Tentativa de cadastro com nome vazio. | Mensagem de aviso; aluno não é salvo. | Não executado |
| CT03 | Nota digitada como texto (ex.: "abc"). | Mensagem de erro; nota não é adicionada. | Não executado |
| CT04 | Nota no limite (0 e 10) e fora do limite (-1 e 11). | Limites aceitos; fora do limite rejeitado. | Não executado |
| CT05 | Edição de um aluno selecionado na lista. | Dados carregam no formulário e são atualizados ao salvar. | Não executado |
| CT06 | Exclusão de aluno com cancelamento e com confirmação. | Sem confirmação nada muda; com confirmação o aluno some da lista. | Não executado |
| CT07 | Encerrar e reabrir o aplicativo. | Alunos cadastrados continuam disponíveis (persistência). | Não executado |
| CT08 | Pesquisa por nome/turma sem resultado. | Lista fica vazia sem erro na interface. | Não executado |

### 8.2 Registro de falhas e correções

| Falha observada | Causa identificada | Correção aplicada | Reteste |
|---|---|---|---|
| _(preencher durante a execução dos testes)_ | | | |

> Observação: os casos acima foram planejados e as regras de negócio
> (validação de nome, nota, cálculo de média e situação) já foram testadas
> automaticamente durante o desenvolvimento. A execução manual dos casos
> CT01 a CT08 na interface gráfica deve ser feita e registrada por quem for
> apresentar o trabalho, preenchendo a coluna "Situação" e a tabela 8.2.

## 9. Roteiro sugerido de apresentação

1. Apresentar o problema (acompanhar notas e médias de alunos) e o público-alvo.
2. Mostrar a tela principal e as três áreas (cadastro, consulta, resumo).
3. Cadastrar um aluno ao vivo, demonstrando a validação de notas.
4. Pesquisar/filtrar, editar e excluir um aluno (com confirmação).
5. Fechar e reabrir o aplicativo para mostrar a persistência dos dados.
6. Explicar as principais decisões técnicas (organização em módulos, JSON, validações).

## 10. Limitações conhecidas

- Não há autenticação de usuário; qualquer pessoa com acesso ao computador pode alterar os dados.
- A turma é digitada/selecionada livremente; não há um cadastro separado de turmas.
- O arquivo `dados/alunos.json` não é criptografado.
