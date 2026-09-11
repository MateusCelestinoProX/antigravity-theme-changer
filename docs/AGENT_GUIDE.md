# 🤖 Guia Completo do Agente Theme Changer — Google Antigravity

O **Theme Changer** é um agente autônomo e subagente de primeira classe construído nativamente para o **Google Antigravity 2.0**. Ele gerencia toda a identidade visual, paletas de cores cromáticas e tipografia com ligaduras de programação do ambiente de desenvolvimento.

---

## 📌 Índice
1. [Visão Geral e Arquitetura do Agente](#-visão-geral-e-arquitetura-do-agente)
2. [Manifesto e Configuração YAML](#-manifesto-e-configuração-yaml)
3. [Gramática de Comandos do Agente](#-gramática-de-comandos-do-agente)
4. [Compreensão de Linguagem Natural](#-compreensão-de-linguagem-natural)
5. [Políticas de Execução e Ferramentas](#-políticas-de-execução-e-ferramentas)
6. [Fluxo de Trabalho e Ciclo de Vida](#-fluxo-de-trabalho-e-ciclo-de-vida)

---

## 🏛️ Visão Geral e Arquitetura do Agente

No Google Antigravity, agentes autônomos são definidos por arquivos de manifesto Markdown localizados em `~/.gemini/config/agents/`. O agente `theme-changer` atua como:
- **Especialista de Domínio**: Conhece profundamente o layout interno do Antigravity, os arquivos de configuração `config.json` e `antigravity_state.pbtxt`, e a injeção ao vivo via Chrome DevTools Protocol (CDP).
- **Subagente Ativável**: Pode ser acionado diretamente pelo usuário via menção `@theme-changer` ou herdado como especialista em tarefas de customização de ambiente.
- **Executor Transparente**: Altera temas e fontes em menos de 150ms sem necessidade de recarregar a IDE ou reiniciar janelas.

---

## ⚙️ Manifesto e Configuração YAML

O arquivo de configuração do agente fica em:
`~/.gemini/config/agents/theme-changer.md`

```yaml
---
name: theme-changer
description: Agente especialista em customização e troca de temas visuais e tipografia do Google Antigravity. Gerencia temas Monocromáticos (Full), Dark Mode com filtros aveludados e Light Mode com cores secundárias vibrantes, além de fontes customizadas como JetBrains Mono e Fira Code.
subagent: true
mainAgent: true
model: inherit
commandExecutionPolicy: auto
tools:
  - run_command
  - view_file
  - replace_file_content
---
```

### Detalhes dos Campos:
- `subagent: true`: Permite que o agente principal delegue subtarefas visuais diretamente ao `theme-changer`.
- `mainAgent: true`: Permite que o usuário converse diretamente com o agente no chat.
- `model: inherit`: Herda o modelo de inteligência ativo no momento (Gemini 2.5 Flash, Pro ou Ultra).
- `commandExecutionPolicy: auto`: Executa comandos CLI de forma não bloqueante e automatizada, garantindo resposta imediata ao usuário.

---

## 🎯 Gramática de Comandos do Agente

Você pode interagir com o agente usando sintaxe direta ou comandos simplificados:

### 1. Inicialização Integrada (`init`)
Inicia o servidor HTTP multithread na porta `48123` em segundo plano (se inativo), abre automaticamente o painel web Apple Liquid Glass no navegador padrão e devolve o link clicável direto.

```text
@theme-changer init
```
*Comando subjacente executado:*
```bash
python3 ~/.gemini/config/skills/theme-changer/scripts/theme_changer.py init
```

---

### 2. Consulta de Estado em Tempo Real (`status`)
Informa imediatamente qual tema está ativo, sementes de cor (background e primary), modo de contraste, fonte tipográfica ativa, modo de aplicação (total ou código) e estado do servidor web.

```text
@theme-changer status
```
*Comando subjacente executado:*
```bash
python3 ~/.gemini/config/skills/theme-changer/scripts/theme_changer.py status
```

---

### 3. Listagem de Catálogo (`list`)
Exibe o catálogo completo e categorizado de todos os 31 temas de elite e 13 fontes com ligaduras de programação.

```text
@theme-changer list
```
*Comando subjacente executado:*
```bash
python3 ~/.gemini/config/skills/theme-changer/scripts/theme_changer.py list
```

---

### 4. Troca Instantânea de Tema (`theme -[FLAG]`)
Aplica qualquer um dos 31 temas disponíveis. A alteração é persistida em `config.json`, sincronizada em `antigravity_state.pbtxt` e injetada no DOM via Chrome DevTools Protocol em <150ms.

```text
@theme-changer theme -matcha
@theme-changer theme -copper
@theme-changer theme -cappuccino
@theme-changer theme -emerald
@theme-changer theme -green
@theme-changer theme -pistachio
```

---

### 5. Troca Instantânea de Tipografia (`font -[FLAG] [-code-only]`)
Aplica fontes consagradas de engenharia de software com suporte a ligaduras.

```text
# Modo Total (Chat, Editor, Prompts, Terminal e Títulos)
@theme-changer font -jetbrains
@theme-changer font -victor
@theme-changer font -cascadia
@theme-changer font -geist

# Modo Híbrido (Mantém UI sans-serif e aplica fonte apenas no código e terminais)
@theme-changer font -fira -code-only
```

---

### 6. Agendamento e Fila Autônoma (`schedule` e `queue`)
Permite gerenciar a fila de mensagens e tarefas programadas para os agentes:

```text
# Consultar fila ativa e histórico
@theme-changer queue

# Agendar instrução para quando o agente terminar a tarefa atual
@theme-changer schedule "Rodar testes unitários e lint no repositório"

# Disparar mensagem imediatamente da fila
@theme-changer dispatch msg_a1b2c3d4
```

---

### 7. Gestão de MCPs e Conectores (`mcps`)
Consulta servidores Model Context Protocol ativos e desabilitados:

```text
@theme-changer mcps
```

---

## 🗣️ Compreensão de Linguagem Natural

O agente `theme-changer` não exige que você memorize flags exatas. Ele mapeia requisições em linguagem natural para os comandos corretos:

| Exemplo de Prompt do Usuário | Mapeamento Automático | Ação Realizada |
| :--- | :--- | :--- |
| *"Inicia o servidor e abre a página de temas"* | `init` | Inicia porta 48123 e abre navegador |
| *"Qual tema está configurado agora?"* | `status` | Retorna diagnóstico visual completo |
| *"Me mostra todas as opções de temas e fontes"* | `list` | Imprime tabela formatada de opções |
| *"Coloca o tema verde do Matrix"* | `theme -green` | Aplica Matrix CRT Green (#00FF41) |
| *"Muda para o tema de café escuro"* | `theme -cappuccino` | Aplica Dark Cappuccino (#D4A373) |
| *"Quero a fonte Victor Mono com cursiva"* | `font -victor` | Aplica Victor Mono com ligaduras cursivas |
| *"Aplica Fira Code só no editor de código"* | `font -fira -code-only` | Aplica Fira Code em modo híbrido |
| *"Volta para a fonte padrão da Apple"* | `font -system` | Restaura tipografia nativa SF Pro |

---

## 🛡️ Políticas de Execução e Ferramentas

O agente conta com um conjunto estrito de ferramentas:
1. `run_command`: Para disparar os scripts do motor `theme_changer.py` e `theme_server.py`.
2. `view_file`: Para ler o estado atual em `config.json`, `active_font.json` e `antigravity_state.pbtxt`.
3. `replace_file_content`: Para atualizar parâmetros de configuração quando necessário.

O agente sempre responde em **Português do Brasil (pt-BR)** e fornece links diretos clicáveis para qualquer interface gráfica envolvida.
