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

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Redirecionamento 302 para o painel web |
| `GET` | `/theme_changer_app.html` | Serve o painel web Apple Liquid Glass |
| `GET` | `/api/ping` | Handshake e healthcheck ultra-leve (< 1ms) Dual-Stack |
| `GET` | `/api/status` | Diagnóstico geral, porta, tema e fonte ativos |
| `GET` | `/api/list` | Catálogo completo dos 31 temas e 13 fontes |
| `GET` | `/api/current-theme` | Consulta o tema ativo e sementes de cor |
| `GET` | `/api/current-font` | Consulta a fonte ativa e o modo de escopo |
| `POST` / `GET` | `/api/set-theme` | Altera e injeta um novo tema em tempo real |
| `POST` / `GET` | `/api/set-font` | Altera e injeta uma nova fonte com ligaduras |

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
