# 📡 Referência da API REST — Theme Studio Server

O **Theme Studio Server** opera localmente na porta `48123`, fornecendo uma API REST completa para troca instantânea de temas e fontes, consulta de estado e integração com scripts externos.

---

## 📌 Índice
1. [Visão Geral e Base URL](#-visão-geral-e-base-url)
2. [Tabela Resumo de Endpoints](#-tabela-resumo-de-endpoints)
3. [Detalhamento das Rotas](#-detalhamento-das-rotas)
   - [GET /api/status](#1-get-apistatus)
   - [GET /api/list](#2-get-apilist)
   - [GET /api/current-theme](#3-get-apicurrent-theme)
   - [GET /api/current-font](#4-get-apicurrent-font)
   - [POST e GET /api/set-theme](#5-post-e-get-apiset-theme)
   - [POST e GET /api/set-font](#6-post-e-get-apiset-font)
4. [Exemplos Práticos com cURL e JavaScript](#-exemplos-práticos-com-curl-e-javascript)

---

## 🌐 Visão Geral e Base URL

- **URL Base**: `http://localhost:48123`
- **Protocolo**: HTTP/1.1
- **CORS**: Habilitado para todas as origens (`Access-Control-Allow-Origin: *`)
- **Formatos Aceitos**: Query Parameters (GET) ou JSON Body (POST)
- **Content-Type da Resposta**: `application/json; charset=utf-8`

---

## 📋 Tabela Resumo de Endpoints

### 🎨 Customização Visual & Core
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Redirecionamento 302 para o painel web |
| `GET` | `/theme_changer_app.html` | Serve o painel web Apple Liquid Glass |
| `GET` | `/js/*` | Serve scripts estáticos do motor WebGL (`ogl.js`, `webgl-backgrounds.js`) |
| `GET` | `/api/ping` | Handshake e healthcheck ultra-leve (< 1ms) Dual-Stack |
| `GET` | `/api/status` | Diagnóstico geral, porta, tema e fonte ativos |
| `GET` | `/api/list` | Catálogo completo dos 31 temas e 13 fontes |
| `GET` | `/api/current-theme` | Consulta o tema ativo e sementes de cor |
| `GET` | `/api/current-font` | Consulta a fonte ativa e o modo de escopo |
| `POST` / `GET` | `/api/set-theme` | Altera e injeta um novo tema em tempo real |
| `POST` / `GET` | `/api/set-font` | Altera e injeta uma nova fonte com ligaduras |

### ⚡ Scheduler & Fila de Mensagens (`agentapi`)
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/scheduler/queue` | Retorna o estado do agente, fila ativa de mensagens e histórico de disparos |
| `POST` | `/api/scheduler/schedule` | Enfileira nova mensagem com gatilho (`on_idle`, `delayed`, `exact_time`, `cron`) |
| `POST` | `/api/scheduler/cancel` | Cancela uma mensagem enfileirada através do ID |
| `POST` | `/api/scheduler/dispatch-now` | Força o disparo imediato de uma mensagem da fila via `agentapi` |
| `POST` | `/api/scheduler/toggle-agent-state` | Alterna / simula o estado do agente (`idle` vs `busy`) para testes de gatilho |
| `GET` | `/api/scheduler/conversations` | Lista todas as conversas ativas no Antigravity para seleção de destino |
| `GET` | `/api/scheduler/projects` | Descobre projetos nativos do Antigravity com detecção de mapas Graphify |
| `POST` | `/api/scheduler/projects/create` | Registra um novo projeto nativo na barra lateral do Antigravity |
| `POST` | `/api/scheduler/upload-context` | Upload de arquivos locais do macOS para anexo de contexto em mensagens |

### 🤖 Gestão de Agentes & Servidores MCP
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/agents` | Lista todos os agentes configurados no Antigravity (`~/.gemini/config/agents/`) |
| `POST` | `/api/agents/save` | Cria ou edita o manifesto Markdown de um agente autônomo |
| `POST` | `/api/agents/toggle` | Habilita ou desabilita um agente (subagent/mainAgent) |
| `POST` | `/api/agents/delete` | Remove o arquivo de configuração de um agente |
| `GET` | `/api/mcps` | Lista servidores MCP ativos e desativados (`mcpServers`) |
| `POST` | `/api/mcps/save` | Cadastra ou atualiza configurações de servidores MCP |
| `POST` | `/api/mcps/toggle` | Alterna o status ativo/desabilitado de um servidor MCP |
| `POST` | `/api/mcps/delete` | Remove as configurações de um servidor MCP |

---

## 🔍 Detalhamento das Rotas

### 0. `GET /api/ping`
Verificação ultra-leve de conectividade HTTP (resposta < 1ms) para handshake de inicialização e healthchecks do navegador.

**Exemplo de Resposta**:
```json
{
  "status": "ok",
  "port": 48123
}
```

---

### 1. `GET /api/status`
Retorna o estado de saúde do servidor, o tema atualmente carregado e a fonte em uso.

**Exemplo de Resposta (200 OK):**
```json
{
  "status": "online",
  "port": 48123,
  "dashboard_url": "http://localhost:48123/theme_changer_app.html",
  "current_theme": "matcha",
  "theme_mode": "THEME_MODE_DARK",
  "theme": {
    "name": "Dark Matcha Obsidian",
    "category": "dark",
    "seeds": {
      "primary": "#84CC16",
      "background": "#0C100B",
      "foregroundOverride": "#F2FBF0",
      "primaryForegroundOverride": "#050804"
    }
  },
  "current_font": "jetbrains",
  "font_name": "JetBrains Mono",
  "font_scope": "full"
}
```

---

### 2. `GET /api/list`
Retorna o catálogo completo de todos os temas e fontes cadastrados no motor.

**Exemplo de Resposta (200 OK):**
```json
{
  "total_themes": 31,
  "total_fonts": 13,
  "themes": {
    "green": { "name": "Matrix Phosphor Green", "category": "full", ... },
    "matcha": { "name": "Dark Matcha Obsidian", "category": "dark", ... },
    "emerald": { "name": "Light Emerald", "category": "light", ... }
  },
  "fonts": {
    "jetbrains": { "name": "JetBrains Mono", "badge": "LIGADURAS", ... },
    "victor": { "name": "Victor Mono", "badge": "CURSIVA & LIGS", ... }
  }
}
```

---

### 3. `GET /api/current-theme`
Consulta direta para obter o identificador e a paleta do tema ativo.

**Exemplo de Resposta (200 OK):**
```json
{
  "current": "copper",
  "theme": {
    "name": "Dark Basalt Copper",
    "seeds": {
      "primary": "#FB923C",
      "background": "#120E0A"
    }
  }
}
```

---

### 4. `GET /api/current-font`
Consulta direta para obter a fonte e o escopo tipográfico ativo.

**Exemplo de Resposta (200 OK):**
```json
{
  "current": "fira",
  "name": "Fira Code",
  "scope": "full"
}
```

---

### 5. `POST` e `GET /api/set-theme`
Aplica um novo tema no Antigravity. Aceita tanto query params quanto corpo JSON.

**Parâmetros:**
- `theme` (string, obrigatório): Flag ou identificador do tema (ex: `matcha`, `copper`, `emerald`, `green`).

**Via POST (Recomendado para APIs):**
```bash
curl -X POST http://localhost:48123/api/set-theme   -H "Content-Type: application/json"   -d '{"theme": "matcha"}'
```

**Via GET (Ideal para links e tags `<a>`):**
```bash
curl "http://localhost:48123/api/set-theme?theme=matcha"
```

**Exemplo de Resposta (200 OK):**
```json
{
  "success": true,
  "theme": "matcha",
  "name": "Dark Matcha Obsidian",
  "seeds": {
    "primary": "#84CC16",
    "background": "#0C100B",
    "foregroundOverride": "#F2FBF0",
    "primaryForegroundOverride": "#050804"
  },
  "theme_mode": "THEME_MODE_DARK",
  "message": "Tema Dark Matcha Obsidian aplicado com sucesso no Google Antigravity!"
}
```

---

### 6. `POST` e `GET /api/set-font`
Aplica uma fonte com ligaduras no Antigravity.

**Parâmetros:**
- `font` (string, obrigatório): Identificador da fonte (ex: `jetbrains`, `fira`, `cascadia`, `victor`, `geist`, `system`).
- `scope` (string, opcional): `full` (todo o Antigravity) ou `code` (apenas monaco editor e terminais). Padrão: `full`.

**Via POST:**
```bash
curl -X POST http://localhost:48123/api/set-font   -H "Content-Type: application/json"   -d '{"font": "victor", "scope": "full"}'
```

**Via GET:**
```bash
curl "http://localhost:48123/api/set-font?font=victor&scope=full"
```

**Exemplo de Resposta (200 OK):**
```json
{
  "success": true,
  "font": "victor",
  "scope": "full",
  "name": "Victor Mono",
  "message": "Fonte Victor Mono aplicada com sucesso no Google Antigravity!",
  "output": "[CDP] Font Victor Mono injected successfully"
}
```

---

### 7. `GET /api/scheduler/queue`
Retorna a fila ativa de mensagens agendadas, o histórico recente de disparos e o status atual do agente.

**Exemplo de Resposta (200 OK):**
```json
{
  "agent_state": {
    "status": "idle",
    "current_agent": "Antigravity Core",
    "current_task": "Aguardando novas instruções",
    "last_change": 1789102500
  },
  "queue": [
    {
      "id": "msg_a1b2c3d4",
      "recipient": "Antigravity Core",
      "target_type": "existing_chat",
      "conversation_id": "7b932cb5-510a-4d93-af7a-7cabd8e83ac4",
      "chat_title": "Refatoração de Módulos",
      "model_tier": "inherit",
      "trigger_type": "on_idle",
      "status": "queued",
      "created_at": "2026-09-11 17:00:00"
    }
  ],
  "history": []
}
```

---

### 8. `POST /api/scheduler/schedule`
Enfileira uma nova mensagem ou tarefa para o agente autônomo com suporte a diferentes gatilhos e anexos de contexto.

**Parâmetros JSON:**
- `content` (string, obrigatório): Corpo da mensagem/prompt a ser entregue.
- `target_type` (string, opcional): `existing_chat` ou `new_chat`. Padrão: `existing_chat`.
- `conversation_id` (string, opcional): ID da conversa destino (obrigatório se `target_type == existing_chat`).
- `model_tier` (string, opcional): `inherit`, `flash_lite`, `flash`, ou `pro` (apenas para `new_chat`).
- `chat_title` (string, opcional): Título da conversa ou da notificação.
- `trigger_type` (string, opcional): `on_idle`, `delayed`, `exact_time`, ou `cron`.
- `delay_seconds` (int, opcional): Tempo de espera em segundos para o gatilho `delayed`.
- `cron_interval_seconds` (int, opcional): Intervalo de recorrência para o gatilho `cron`.
- `contexts` (array de objetos, opcional): Lista de anexos como `[{"type": "file", "value": "/path/to/file"}]`.
- `project_id` / `project_path` (string, opcional): Contexto do projeto alvo.

---

### 9. `POST /api/scheduler/cancel`
Remove uma mensagem da fila ativa pelo seu identificador único.

**Parâmetros JSON:**
- `id` (string, obrigatório): ID da mensagem a ser cancelada (ex: `msg_a1b2c3d4`).

---

### 10. `POST /api/scheduler/dispatch-now`
Força o disparo imediato de uma mensagem agendada via `agentapi`, ignorando contadores ou restrições de gatilho.

**Parâmetros JSON:**
- `id` (string, obrigatório): ID da mensagem a ser despachada.

---

### 11. `POST /api/scheduler/toggle-agent-state`
Alterna o status do agente entre `idle` e `busy` ou define uma tarefa simulada para disparar gatilhos inteligentes.

**Parâmetros JSON:**
- `status` (string, opcional): `idle` ou `busy`.
- `task` (string, opcional): Descrição da tarefa ativa.

---

### 12. `GET /api/scheduler/conversations`
Lista todas as conversas do Google Antigravity encontradas em `~/.gemini/antigravity/brain/` e `conversations/`, com título e data de modificação.

---

### 13. `GET /api/scheduler/projects` e `POST /api/scheduler/projects/create`
- **GET**: Descobre os projetos nativos cadastrados em `~/.gemini/config/projects/` e verifica se possuem mapas estruturais Graphify (`graph.json`).
- **POST**: Cadastra um novo projeto nativo na barra lateral com `name` e `folder`.

---

### 14. `POST /api/scheduler/upload-context`
Permite o upload direto de arquivos locais do macOS para serem anexados a mensagens da fila.
- `filename` (string, obrigatório): Nome do arquivo com extensão.
- `content_base64` (string, obrigatório): Conteúdo em base64 do arquivo.

---

### 15. `GET /api/agents` e `POST /api/agents/save` / `toggle` / `delete`
API completa para leitura, criação e manutenção de manifestos de agentes Markdown (`~/.gemini/config/agents/*.md`).

---

### 16. `GET /api/mcps` e `POST /api/mcps/save` / `toggle` / `delete`
API para gerenciamento do catálogo de servidores MCP ativos e desabilitados em `~/.gemini/config/config.json`.

---

## 💻 Exemplos Práticos com cURL e JavaScript

### Exemplo em JavaScript (Browser Fetch):
```javascript
// Trocar para o tema Dark Copper
async function mudarTema(nomeTema) {
  const resp = await fetch('http://localhost:48123/api/set-theme', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ theme: nomeTema })
  });
  const data = await resp.json();
  console.log('Tema aplicado:', data.name);
}

// Trocar para a fonte Fira Code em modo código apenas
async function mudarFonte(nomeFonte) {
  const resp = await fetch('http://localhost:48123/api/set-font', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ font: nomeFonte, scope: 'code' })
  });
  const data = await resp.json();
  console.log('Fonte aplicada:', data.name);
}
```

### Exemplo em Shell Script:
```bash
#!/usr/bin/env bash
# Script para alternar o Antigravity para tema noturno
curl -s -X POST http://localhost:48123/api/set-theme -d '{"theme":"midnight"}' > /dev/null
curl -s -X POST http://localhost:48123/api/set-font -d '{"font":"jetbrains","scope":"full"}' > /dev/null
echo "Tema Noturno Midnight e JetBrains Mono aplicados!"
```
