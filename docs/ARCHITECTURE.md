# 🏛️ Arquitetura Técnica — Google Antigravity Theme & Font Engine

Este documento detalha o funcionamento interno, o pipeline de renderização, os mecanismos de sincronização atômica e a injeção em tempo real da suíte **Theme Changer** no **Google Antigravity 2.0**.

---

## 📌 Índice
1. [Visão Geral da Arquitetura](#-visão-geral-da-arquitetura)
2. [Motor de Tripla Sincronização (Tri-Sync)](#-motor-de-tripla-sincronização-tri-sync)
3. [Conexão em Tempo Real via Chrome DevTools Protocol (CDP)](#-conexão-em-tempo-real-via-chrome-devtools-protocol-cdp)
4. [Injeção Dinâmica de CSS e Gestão de Estilos](#-injeção-dinâmica-de-css-e-gestão-de-estilos)
5. [Mecanismo de Tipografia com Ligaduras de Código](#-mecanismo-de-tipografia-com-ligaduras-de-código)
6. [Arquitetura do Servidor Local HTTP Multithread](#-arquitetura-do-servidor-local-http-multithread)
7. [Doutrina Visual Apple Liquid Glass](#-doutrina-visual-apple-liquid-glass)

---

## 🏗️ Visão Geral da Arquitetura

O Google Antigravity combina uma camada de interface moderna baseada em Chromium/Electron com um núcleo de execução de linguagem (*language server*) orientado a Protobuf. Modificar o tema apenas no arquivo JSON ou apenas na interface web resulta em inconsistências após reinicializações.

O Theme Changer resolve esse desafio através de um motor unificado:

```
                                  ┌────────────────────────┐
                                  │   Comando do Usuário   │
                                  │ CLI / Agente / Web App │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                                 ┌──────────────────────────┐
                                 │     theme_changer.py     │
                                 │     (Core Controller)    │
                                 └────────────┬─────────────┘
                     ┌────────────────────────┼────────────────────────┐
                     ▼                        ▼                        ▼
          ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
          │     Passo 1:        │  │     Passo 2:        │  │     Passo 3:        │
          │  config.json Sync   │  │ antigravity_state   │  │   Injeção CDP       │
          │  (Persistência JSON)│  │ (Protobuf Engine)   │  │ (WebSocket Sub-150ms)
          └─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

---

## 🔄 Motor de Tripla Sincronização (Tri-Sync)

A integridade do ambiente é garantida pela atualização atômica de três camadas independentes:

### 1. Camada de Configuração do Usuário (`config.json`)
Localizada em `~/.gemini/config/config.json`.
O script localiza e atualiza o bloco:
```json
{
  "userSettings": {
    "themeMode": "THEME_MODE_DARK",
    "customThemeSeedsDark": {
      "primary": "#84CC16",
      "background": "#0C100B",
      "foregroundOverride": "#F2FBF0",
      "primaryForegroundOverride": "#050804"
    }
  }
}
```

### 2. Camada do Language Server (`antigravity_state.pbtxt`)
Localizada em `~/.gemini/antigravity/antigravity_state.pbtxt`.
O motor realiza uma substituição regex precisa e atômica nas seções `jetbox_state_pb.CustomThemeSeeds`, garantindo que o servidor de linguagem e a barra de status reflitam as mesmas cores do tema sem corromper o formato binário/texto do Protobuf.

### 3. Camada de Injeção em Tempo Real (CDP)
Ao invés de obrigar o desenvolvedor a recarregar a janela ou reiniciar a aplicação, o script se conecta via WebSocket à instância Chromium ativa e atualiza os nós de estilo no DOM em menos de 150 milissegundos.

---

## ⚡ Conexão em Tempo Real via Chrome DevTools Protocol (CDP)

O Antigravity expõe uma porta de depuração Chromium interna. O motor localiza essa porta através de um algoritmo de descoberta dinâmica:

```
1. Busca por ~/Library/Application Support/Antigravity/DevToolsActivePort
2. Lê a porta na Linha 1 do arquivo
3. Faz fallback para escaneamento de portas ativas de depuração (9222, 9000, etc.)
4. Consulta http://127.0.0.1:<PORT>/json/list para obter o WebSocket Debugger URL
5. Abre conexão WebSocket direta com o alvo principal (Page / Workbench)
```

### Protocolo de Injeção via WebSocket
O script despacha um payload JSON-RPC 2.0 com o método `Runtime.evaluate`:

```json
{
  "id": 1,
  "method": "Runtime.evaluate",
  "params": {
    "expression": "(...código javascript otimizado...)",
    "awaitPromise": true,
    "returnByValue": true
  }
}
```

---

## 🎨 Injeção Dinâmica de CSS e Gestão de Estilos

Para evitar duplicação ou vazamentos de memória no DOM, o motor utiliza uma tag `<style>` única e idempotente identificada por:
`id="antigravity-live-theme-override"`

### Variáveis CSS Injetadas
```css
:root {
  --vscode-activityBar-background: #0C100B !important;
  --vscode-editor-background: #0C100B !important;
  --vscode-sideBar-background: #0E140D !important;
  --vscode-focusBorder: #84CC16 !important;
  --vscode-button-background: #84CC16 !important;
  --vscode-button-foreground: #050804 !important;
  --antigravity-accent-glow: rgba(132, 204, 22, 0.35) !important;
}
```

Caso a tag já exista no `<head>`, seu conteúdo interno (`textContent`) é sobrescrito instantaneamente, eliminando completamente qualquer oscilação de tela (*flash of unstyled content*).

---

## 🔤 Mecanismo de Tipografia com Ligaduras de Código

O gerenciamento de fontes opera através do script Node.js `apply_font.js`.

### 1. Injeção de Fontes Web via Google Fonts
Para fontes modernas (JetBrains Mono, Fira Code, Cascadia Code, Victor Mono, etc.), o script injeta regras `@import` com pesos variáveis (400, 500, 600, 700) e suporte a estilos itálicos cursivos.

### 2. Ativação Forçada de Ligaduras
Para garantir que ligaduras como `===`, `!==`, `=>`, `<!--` e `|>` sejam renderizadas com fidelidade máxima, o motor aplica:
```css
font-feature-settings: "liga" 1, "calt" 1, "zero" 1 !important;
font-variant-ligatures: normal !important;
-webkit-font-smoothing: antialiased !important;
```

### 3. Escopos de Aplicação (Dual-Scope)
- **Escopo Total (`scope=full`)**: Aplica a tipografia a todas as superfícies (balões de chat, interface, árvore de arquivos, abas, editor e terminal).
- **Escopo Híbrido (`scope=code`)**: Aplica a fonte exclusivamente a seletores monospaçados:
  ```css
  .monaco-editor, .monaco-editor *,
  .terminal, .xterm, .xterm *,
  code, pre, pre *, kbd
  ```
  preservando a tipografia sem serifa padrão da Apple na interface geral.

---

## 🌐 Arquitetura do Servidor Local HTTP Multithread

O componente `theme_server.py` fornece a ponte entre interfaces externas (navegador, cURL, webhooks) e o motor interno.

### Características Técnicas:
- **Tecnologia**: Python Standard Library puro (`http.server` + `socketserver.ThreadingMixIn`). Zero dependências externas pip.
- **Dual-Stack Nativo (IPv4 + IPv6)**: Classe `DualStackServer` operando em `socket.AF_INET6` com `IPV6_V6ONLY = 0`, atendendo requisições simultâneas em `::1`, `127.0.0.1` e `localhost` sem delay de preflight.
- **Persistência macOS LaunchAgent**: Serviço `com.antigravity.theme-changer.plist` em `~/Library/LaunchAgents` com `KeepAlive` para inicialização automática no boot.
- **Porta**: `48123` com suporte a reuso imediato de porta (`SO_REUSEADDR`).
- **Concorrência**: Processamento multithread em threads daemon (`daemon_threads = True`).
- **CORS & PNA Completo**: Cabeçalhos `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Private-Network: true` (compatível com Chromium/Brave) e preflight `OPTIONS`.
- **Rota de Ping**: Endpoint `/api/ping` para validação instantânea de prontidão de socket.
- **API Híbrida**: Aceita parâmetros via query string (GET) ou payloads JSON (POST).

---

## 🍏 Doutrina Visual Apple Liquid Glass

O painel web (`theme_changer_app.html`) foi projetado sob os princípios de design de vidro líquido da Apple (macOS Tahoe e visionOS):

1. **Vidro Translúcido com Desfoque Profundo**:
   `backdrop-filter: blur(36px) saturate(190%)` para criar profundidade espacial autêntica.
2. **Borda Especular de Refração**:
   Bordas com gradiente translúcido simulando a incidência de luz em superfícies de vidro bisotado.
3. **Orbes Fluidos Dinâmicos**:
   Camadas de iluminação volumétrica em background que se movem suavemente e reagem com suavidade.
4. **Sem Dependências Pesadas**:
   Arquitetura de arquivo único sem React, Vue ou bundlers. Carregamento instantâneo em qualquer navegador.
