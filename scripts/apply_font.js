const fs = require("fs");
const path = require("path");

const FONTS = {
  jetbrains: {
    name: "JetBrains Mono",
    author: "JetBrains",
    badge: "LIGADURAS",
    importUrl: "https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300..800;1,300..800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap",
    uiFont: "'JetBrains Mono', monospace",
    sansFont: "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'JetBrains Mono', monospace",
    ligatures: true
  },
  fira: {
    name: "Fira Code",
    author: "Nikita Prokopov",
    badge: "CLÁSSICA",
    importUrl: "https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&family=Inter:wght@400;500;600;700&display=swap",
    uiFont: "'Fira Code', monospace",
    sansFont: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'Fira Code', monospace",
    ligatures: true
  },
  cascadia: {
    name: "Cascadia Code",
    author: "Microsoft",
    badge: "MODERNA",
    importUrl: "https://fonts.googleapis.com/css2?family=Cascadia+Code:ital,wght@0,300..700;1,300..700&family=Inter:wght@400;500;600&display=swap",
    uiFont: "'Cascadia Code', monospace",
    sansFont: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'Cascadia Code', monospace",
    ligatures: true
  },
  victor: {
    name: "Victor Mono",
    author: "Ruben L. Blom",
    badge: "CURSIVA & LIGS",
    importUrl: "https://fonts.googleapis.com/css2?family=Victor+Mono:ital,wght@0,400..700;1,400..700&family=Plus+Jakarta+Sans:wght@400;600&display=swap",
    uiFont: "'Victor Mono', monospace",
    sansFont: "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'Victor Mono', monospace",
    ligatures: true
  },
  source: {
    name: "Source Code Pro",
    author: "Adobe",
    badge: "ALTA CLAREZA",
    importUrl: "https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,300..800;1,300..800&family=Inter:wght@400;600&display=swap",
    uiFont: "'Source Code Pro', monospace",
    sansFont: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'Source Code Pro', monospace",
    ligatures: false
  },
  inconsolata: {
    name: "Inconsolata",
    author: "Raph Levien",
    badge: "CONDENSADA",
    importUrl: "https://fonts.googleapis.com/css2?family=Inconsolata:wght@300..800&family=Inter:wght@400;600&display=swap",
    uiFont: "'Inconsolata', monospace",
    sansFont: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'Inconsolata', monospace",
    ligatures: false
  },
  hack: {
    name: "Hack Font",
    author: "Source Foundry",
    badge: "DEV WORKHORSE",
    importUrl: "https://cdnjs.cloudflare.com/ajax/libs/hack-font/3.3.0/web/hack.min.css",
    uiFont: "'Hack', monospace",
    sansFont: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    codeFont: "'Hack', monospace",
    ligatures: false
  },
  ubuntu: {
    name: "Ubuntu Mono",
    author: "Canonical",
    badge: "LINUX VIBE",
    importUrl: "https://fonts.googleapis.com/css2?family=Ubuntu+Mono:ital,wght@0,400;0,700;1,400;1,700&family=Inter:wght@400;600&display=swap",
    uiFont: "'Ubuntu Mono', monospace",
    sansFont: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'Ubuntu Mono', monospace",
    ligatures: false
  },
  space: {
    name: "Space Mono",
    author: "Colophon / Google",
    badge: "CYBERPUNK",
    importUrl: "https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap",
    uiFont: "'Space Mono', monospace",
    sansFont: "'Space Mono', monospace",
    codeFont: "'Space Mono', monospace",
    ligatures: false
  },
  geist: {
    name: "Geist Mono",
    author: "Vercel",
    badge: "MINIMAL",
    importUrl: "https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300..800&family=Geist:wght@400;600&display=swap",
    uiFont: "'Geist Mono', monospace",
    sansFont: "'Geist', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'Geist Mono', monospace",
    ligatures: true
  },
  ibm: {
    name: "IBM Plex Mono",
    author: "IBM Design",
    badge: "RETRO INDUSTRIAL",
    importUrl: "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=Inter:wght@400;600&display=swap",
    uiFont: "'IBM Plex Mono', monospace",
    sansFont: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'IBM Plex Mono', monospace",
    ligatures: false
  },
  dm: {
    name: "DM Mono",
    author: "Colophon / Google",
    badge: "GEOMÉTRICA",
    importUrl: "https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300..500;1,300..500&family=Inter:wght@400;600&display=swap",
    uiFont: "'DM Mono', monospace",
    sansFont: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    codeFont: "'DM Mono', monospace",
    ligatures: false
  },
  system: {
    name: "System Default (SF Pro / Apple)",
    author: "Apple macOS",
    badge: "NATIVO",
    importUrl: null,
    uiFont: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    sansFont: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    codeFont: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
    ligatures: false
  }
};

const MASTER_FONTS_URL = "https://fonts.googleapis.com/css2?family=Cascadia+Code:ital,wght@0,300..700;1,300..700&family=DM+Mono:ital,wght@0,300..500;1,300..500&family=Fira+Code:wght@300..700&family=Geist+Mono:wght@300..800&family=IBM+Plex+Mono:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=Inconsolata:wght@300..800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:ital,wght@0,300..800;1,300..800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Source+Code+Pro:ital,wght@0,300..800;1,300..800&family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&family=Ubuntu+Mono:ital,wght@0,400;0,700;1,400;1,700&family=Victor+Mono:ital,wght@0,400..700;1,400..700&display=swap";
const HACK_FONT_URL = "https://cdnjs.cloudflare.com/ajax/libs/hack-font/3.3.0/web/hack.min.css";

async function main() {
  const fontKey = (process.argv[2] || "jetbrains").toLowerCase().replace(/^-+/, "");
  const scope = (process.argv[3] || "full").toLowerCase();
  const font = FONTS[fontKey] || FONTS.jetbrains;

  const possiblePortFiles = [
    "/Users/mcp/.gemini/antigravity/brain/38c03376-3545-4755-a269-82bc20b62dbc/DevToolsActivePort",
    path.join(process.env.HOME, "Library/Application Support/Antigravity/DevToolsActivePort"),
    path.join(process.env.HOME, ".gemini/config/DevToolsActivePort"),
    path.join(process.env.HOME, ".gemini/antigravity/DevToolsActivePort")
  ];

  let port = null;
  for (const f of possiblePortFiles) {
    try {
      if (fs.existsSync(f)) {
        const lines = fs.readFileSync(f, "utf-8").trim().split("\n");
        if (lines[0]) {
          port = lines[0].trim();
          break;
        }
      }
    } catch (e) {}
  }

  if (!port) {
    console.log("[i] Antigravity DevToolsActivePort não encontrado.");
    return;
  }

  let pages;
  try {
    const res = await fetch(`http://127.0.0.1:${port}/json`);
    pages = await res.json();
  } catch (err) {
    console.log("[i] Erro ao conectar no DevTools:", err.message);
    return;
  }

  const page = pages.find(p => p.type === "page");
  if (!page || !page.webSocketDebuggerUrl) {
    console.log("[i] Nenhuma página ativa encontrada!");
    return;
  }

  const primaryCodeFont = font.codeFont.split(',')[0].replace(/['"]/g, '').trim();
  const ligVal = font.ligatures ? '"liga" 1, "calt" 1' : '"liga" 0, "calt" 0';

  // In "full" mode: universal override ensures all UI, chat, buttons, prompts, tabs, code and terminal take the font
  // while safely ignoring icons (codicons, SVGs, etc.)
  const cssRules = scope === "full" ? `
    :root {
      --font-sans: ${font.uiFont} !important;
      --font-mono: ${font.codeFont} !important;
      --antigravity-font-ui: ${font.uiFont} !important;
      --antigravity-font-code: ${font.codeFont} !important;
    }

    *:not([class*="codicon"]):not([class*="icon"]):not(svg):not(path) {
      font-family: ${font.uiFont} !important;
      font-feature-settings: ${ligVal} !important;
      letter-spacing: 0px !important;
    }
  ` : `
    :root {
      --font-sans: ${font.sansFont} !important;
      --font-mono: ${font.codeFont} !important;
      --antigravity-font-ui: ${font.sansFont} !important;
      --antigravity-font-code: ${font.codeFont} !important;
    }

    body, button, input, select, textarea:not(.font-mono), div:not([class*="xterm"]):not([class*="monaco"]), p, a, h1, h2, h3, h4, h5, h6, [contenteditable="true"] {
      font-family: ${font.sansFont} !important;
    }

    code, pre, .font-mono, .monospace,
    .xterm, .xterm-rows, .xterm-screen, .xterm-viewport, [class*="xterm"], [class*="xterm"] span,
    span.token, [class*="token"], [class*="code-"], .terminal,
    .monaco-editor, .monaco-editor *,
    textarea.font-mono, [class*="font-mono"] {
      font-family: ${font.codeFont} !important;
      font-feature-settings: ${ligVal} !important;
      letter-spacing: 0px !important;
    }
  `;

  const jsCode = `
    (() => {
      // 1. Preload master font bundles in parallel if not present
      let masterLink = document.getElementById("antigravity-all-fonts-bundle");
      if (!masterLink) {
        masterLink = document.createElement("link");
        masterLink.id = "antigravity-all-fonts-bundle";
        masterLink.rel = "stylesheet";
        masterLink.href = ${JSON.stringify(MASTER_FONTS_URL)};
        document.head.appendChild(masterLink);
      }

      let hackLink = document.getElementById("antigravity-hack-fonts-bundle");
      if (!hackLink) {
        hackLink = document.createElement("link");
        hackLink.id = "antigravity-hack-fonts-bundle";
        hackLink.rel = "stylesheet";
        hackLink.href = ${JSON.stringify(HACK_FONT_URL)};
        document.head.appendChild(hackLink);
      }

      // 2. Specific font link if provided
      ${font.importUrl ? `
        let fontLink = document.getElementById("antigravity-custom-fonts-link");
        if (!fontLink) {
          fontLink = document.createElement("link");
          fontLink.id = "antigravity-custom-fonts-link";
          fontLink.rel = "stylesheet";
          fontLink.href = ${JSON.stringify(font.importUrl)};
        }
        fontLink.href = ${JSON.stringify(font.importUrl)};
      ` : ""}

      // 3. Inject CSS rules
      let fontStyle = document.getElementById("antigravity-custom-fonts-style");
      if (!fontStyle) {
        fontStyle = document.createElement("style");
        fontStyle.id = "antigravity-custom-fonts-style";
        document.head.appendChild(fontStyle);
      }
      fontStyle.textContent = ${JSON.stringify(cssRules)};

      // 4. Force font loading & layout repaint
      if (document.fonts && document.fonts.load) {
        try {
          document.fonts.load("16px " + JSON.stringify(${JSON.stringify(primaryCodeFont)}));
        } catch(e) {}
      }

      try {
        window.dispatchEvent(new Event("resize"));
      } catch(e) {}

      return { applied: true, font: "${fontKey}", name: "${font.name}", scope: "${scope}" };
    })()
  `;

  // Update active_font.json state
  const activeFontPath = path.join(process.env.HOME, ".gemini/config/active_font.json");
  try {
    fs.writeFileSync(activeFontPath, JSON.stringify({
      font: fontKey,
      name: font.name,
      scope: scope,
      author: font.author,
      updatedAt: new Date().toISOString()
    }, null, 2), "utf-8");
  } catch(e) {}

  await new Promise((resolve) => {
    const ws = new WebSocket(page.webSocketDebuggerUrl);
    let timer = setTimeout(() => {
      try { ws.close(); } catch(e) {}
      resolve();
    }, 1500);

    ws.onopen = () => {
      ws.send(JSON.stringify({
        id: 1,
        method: "Runtime.evaluate",
        params: { expression: jsCode, returnByValue: true }
      }));

      ws.send(JSON.stringify({
        id: 2,
        method: "Page.addScriptToEvaluateOnNewDocument",
        params: { source: jsCode }
      }));
    };

    ws.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data);
        if (data.id === 1) {
          clearTimeout(timer);
          if (data.result && data.result.result && data.result.result.value) {
            console.log("[✓] Fonte aplicada com sucesso:", JSON.stringify(data.result.result.value));
          }
          ws.close();
          resolve();
        }
      } catch (e) {
        clearTimeout(timer);
        ws.close();
        resolve();
      }
    };

    ws.onerror = (err) => {
      clearTimeout(timer);
      console.error("[!] Erro WebSocket DevTools:", err.message);
      resolve();
    };
  });
}

(async () => {
  try {
    await main();
  } catch (err) {
    console.error(err);
  }
})();
