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

const THEMES_CSS = {
  // === CATEGORIA 1: FULL MONOCROMÁTICO ===
  green: {
    name: "Matrix Phosphor Green",
    category: "full",
    bg: "#050B05",
    fg: "#00FF41",
    primary: "#00FF41",
    primaryFg: "#000000",
    sidebar: "#030703",
    card: "#081208",
    border: "#00FF41",
    tint: "#00FF41"
  },
  red: {
    name: "Glowing Neon Red",
    category: "full",
    bg: "#0A0002",
    fg: "#FF2A55",
    primary: "#FF003C",
    primaryFg: "#FFFFFF",
    sidebar: "#060001",
    card: "#120004",
    border: "#FF003C",
    tint: "#FF003C"
  },
  cyan: {
    name: "Full Tron Electric Cyan",
    category: "full",
    bg: "#020B0E",
    fg: "#00F0FF",
    primary: "#00F0FF",
    primaryFg: "#020B0E",
    sidebar: "#010608",
    card: "#04141A",
    border: "#00F0FF",
    tint: "#00F0FF"
  },
  yellow: {
    name: "Full Acid Cyber Yellow",
    category: "full",
    bg: "#0D0C02",
    fg: "#FFE600",
    primary: "#FFE600",
    primaryFg: "#0D0C02",
    sidebar: "#080701",
    card: "#171504",
    border: "#FFE600",
    tint: "#FFE600"
  },
  magenta: {
    name: "Full Synthwave Magenta",
    category: "full",
    bg: "#0F020B",
    fg: "#FF007F",
    primary: "#FF007F",
    primaryFg: "#FFFFFF",
    sidebar: "#080106",
    card: "#1A0413",
    border: "#FF007F",
    tint: "#FF007F"
  },
  monochrome: {
    name: "Full OLED Pure Mono",
    category: "full",
    bg: "#000000",
    fg: "#FFFFFF",
    primary: "#FFFFFF",
    primaryFg: "#000000",
    sidebar: "#000000",
    card: "#0D0D0D",
    border: "#FFFFFF",
    tint: "#FFFFFF"
  },

  // === CATEGORIA 2: DARK VELVET TINTED ===
  cappuccino: {
    name: "Dark Cappuccino",
    category: "dark",
    bg: "#181311",
    fg: "#EDE0D4",
    primary: "#D4A373",
    primaryFg: "#181311",
    sidebar: "#130E0D",
    card: "#211A17",
    border: "rgba(212, 163, 115, 0.25)",
    tint: "#D4A373"
  },
  wine: {
    name: "Dark Avermelhado Velvet",
    category: "dark",
    bg: "#120608",
    fg: "#FCE7EA",
    primary: "#E63946",
    primaryFg: "#FFFFFF",
    sidebar: "#0D0305",
    card: "#1C0A0D",
    border: "rgba(230, 57, 70, 0.25)",
    tint: "#E63946"
  },
  midnight: {
    name: "Midnight Sapphire Blue",
    category: "dark",
    bg: "#090D16",
    fg: "#E0F2FE",
    primary: "#38BDF8",
    primaryFg: "#090D16",
    sidebar: "#060910",
    card: "#0F1624",
    border: "rgba(56, 189, 248, 0.25)",
    tint: "#38BDF8"
  },
  dracula: {
    name: "Cyber Amethyst Twilight",
    category: "dark",
    bg: "#120D1C",
    fg: "#F3E8FF",
    primary: "#BD93F9",
    primaryFg: "#120D1C",
    sidebar: "#0C0813",
    card: "#1B132B",
    border: "rgba(189, 147, 249, 0.25)",
    tint: "#BD93F9"
  },
  amber: {
    name: "Amber Warm Dusk",
    category: "dark",
    bg: "#14110A",
    fg: "#FEF3C7",
    primary: "#F59E0B",
    primaryFg: "#14110A",
    sidebar: "#0E0C06",
    card: "#1D190E",
    border: "rgba(245, 158, 11, 0.25)",
    tint: "#F59E0B"
  },
  "dark-emerald": {
    name: "Forest Emerald Night",
    category: "dark",
    bg: "#06120B",
    fg: "#D1FAE5",
    primary: "#10B981",
    primaryFg: "#06120B",
    sidebar: "#040D07",
    card: "#0C1D13",
    border: "rgba(16, 185, 129, 0.25)",
    tint: "#10B981"
  },
  nordic: {
    name: "Nordic Arctic Slate",
    category: "dark",
    bg: "#0B1117",
    fg: "#E2E8F0",
    primary: "#38BDF8",
    primaryFg: "#0B1117",
    sidebar: "#070C10",
    card: "#121A22",
    border: "rgba(56, 189, 248, 0.25)",
    tint: "#38BDF8"
  },
  tokyo: {
    name: "Tokyo Sunset Coral",
    category: "dark",
    bg: "#130D14",
    fg: "#FFE4E6",
    primary: "#FB7185",
    primaryFg: "#130D14",
    sidebar: "#0D080E",
    card: "#1C131D",
    border: "rgba(251, 113, 133, 0.25)",
    tint: "#FB7185"
  },
  "dark-matcha": {
    name: "Dark Matcha Obsidian",
    category: "dark",
    bg: "#0C100B",
    fg: "#F0FDF4",
    primary: "#84CC16",
    primaryFg: "#0C100B",
    sidebar: "#080B07",
    card: "#131A11",
    border: "rgba(132, 204, 22, 0.26)",
    tint: "#84CC16"
  },
  "dark-copper": {
    name: "Dark Basalt Copper",
    category: "dark",
    bg: "#120E0A",
    fg: "#FFF7ED",
    primary: "#FB923C",
    primaryFg: "#120E0A",
    sidebar: "#0D0A07",
    card: "#1B150F",
    border: "rgba(251, 146, 60, 0.26)",
    tint: "#FB923C"
  },
  "dark-ultraviolet": {
    name: "Dark Cosmic Ultraviolet",
    category: "dark",
    bg: "#080616",
    fg: "#EEF2FF",
    primary: "#818CF8",
    primaryFg: "#080616",
    sidebar: "#050410",
    card: "#100D26",
    border: "rgba(129, 140, 248, 0.28)",
    tint: "#818CF8"
  },

  // === CATEGORIA 3: LIGHT LUMINARY ===
  "light-emerald": {
    name: "Light Emerald",
    category: "light",
    bg: "#F7FDF9",
    fg: "#064E3B",
    primary: "#059669",
    primaryFg: "#FFFFFF",
    sidebar: "#EAF8EF",
    card: "#FFFFFF",
    border: "rgba(5, 150, 105, 0.25)",
    tint: "#059669"
  },
  "light-sapphire": {
    name: "Light Sapphire",
    category: "light",
    bg: "#F8FAFC",
    fg: "#0F172A",
    primary: "#0284C7",
    primaryFg: "#FFFFFF",
    sidebar: "#EFF6FF",
    card: "#FFFFFF",
    border: "rgba(2, 132, 199, 0.25)",
    tint: "#0284C7"
  },
  "light-ruby": {
    name: "Light Ruby",
    category: "light",
    bg: "#FFF8F8",
    fg: "#1E293B",
    primary: "#E11D48",
    primaryFg: "#FFFFFF",
    sidebar: "#FFE4E8",
    card: "#FFFFFF",
    border: "rgba(225, 29, 72, 0.25)",
    tint: "#E11D48"
  },
  "light-lavender": {
    name: "Light Lavender",
    category: "light",
    bg: "#FAF8FF",
    fg: "#1E1B4B",
    primary: "#7C3AED",
    primaryFg: "#FFFFFF",
    sidebar: "#F3EEFF",
    card: "#FFFFFF",
    border: "rgba(124, 58, 237, 0.25)",
    tint: "#7C3AED"
  },
  "light-amber": {
    name: "Light Amber Sunburst",
    category: "light",
    bg: "#FFFDF5",
    fg: "#1C1917",
    primary: "#D97706",
    primaryFg: "#FFFFFF",
    sidebar: "#FEF9E7",
    card: "#FFFFFF",
    border: "rgba(217, 119, 6, 0.25)",
    tint: "#D97706"
  },
  "light-latte": {
    name: "Light Coffee Latte",
    category: "light",
    bg: "#FAF7F2",
    fg: "#291E1A",
    primary: "#9A3412",
    primaryFg: "#FFFFFF",
    sidebar: "#F2EBE1",
    card: "#FFFFFF",
    border: "rgba(154, 52, 18, 0.25)",
    tint: "#9A3412"
  },
  "light-rose": {
    name: "Light Rosé Wine",
    category: "light",
    bg: "#FFF5F7",
    fg: "#1F1116",
    primary: "#BE123C",
    primaryFg: "#FFFFFF",
    sidebar: "#FFE6EC",
    card: "#FFFFFF",
    border: "rgba(190, 18, 60, 0.25)",
    tint: "#BE123C"
  },
  "light-teal": {
    name: "Light Ocean Teal",
    category: "light",
    bg: "#F2FBF9",
    fg: "#0F172A",
    primary: "#0D9488",
    primaryFg: "#FFFFFF",
    sidebar: "#E1F6F2",
    card: "#FFFFFF",
    border: "rgba(13, 148, 136, 0.25)",
    tint: "#0D9488"
  },
  "light-coral": {
    name: "Light Coral Peach",
    category: "light",
    bg: "#FFF9F6",
    fg: "#1C1917",
    primary: "#EA580C",
    primaryFg: "#FFFFFF",
    sidebar: "#FDEEE7",
    card: "#FFFFFF",
    border: "rgba(234, 88, 12, 0.25)",
    tint: "#EA580C"
  },
  "light-indigo": {
    name: "Light Electric Indigo",
    category: "light",
    bg: "#F8F9FE",
    fg: "#0F172A",
    primary: "#4F46E5",
    primaryFg: "#FFFFFF",
    sidebar: "#EDEFFD",
    card: "#FFFFFF",
    border: "rgba(79, 70, 229, 0.25)",
    tint: "#4F46E5"
  },
  white: {
    name: "Pure Clean White",
    category: "light",
    bg: "#FFFFFF",
    fg: "#111827",
    primary: "#111827",
    primaryFg: "#FFFFFF",
    sidebar: "#F9FAFB",
    card: "#FFFFFF",
    border: "#E5E7EB",
    tint: "#111827"
  },
  "light-pistachio": {
    name: "Light Pistachio Gelato",
    category: "light",
    bg: "#F8FAF0",
    fg: "#1A2E05",
    primary: "#65A30D",
    primaryFg: "#FFFFFF",
    sidebar: "#EEF4DD",
    card: "#FFFFFF",
    border: "rgba(101, 163, 13, 0.28)",
    tint: "#65A30D"
  },
  "light-terracotta": {
    name: "Light Tuscan Terracotta",
    category: "light",
    bg: "#FDF8F6",
    fg: "#27140B",
    primary: "#C2410C",
    primaryFg: "#FFFFFF",
    sidebar: "#FCEBE4",
    card: "#FFFFFF",
    border: "rgba(194, 65, 12, 0.28)",
    tint: "#C2410C"
  },
  "light-azure": {
    name: "Light Alpine Sky Azure",
    category: "light",
    bg: "#F0F9FF",
    fg: "#082F49",
    primary: "#00A3FF",
    primaryFg: "#FFFFFF",
    sidebar: "#E0F2FE",
    card: "#FFFFFF",
    border: "rgba(0, 163, 255, 0.28)",
    tint: "#00A3FF"
  }
};

async function main() {
  const themeKey = (process.argv[2] || "green").toLowerCase().replace(/^-+/, "");
  const theme = THEMES_CSS[themeKey] || THEMES_CSS.green;

  const possiblePortFiles = [
    path.join(process.env.HOME, "Library/Application Support/Antigravity/DevToolsActivePort"),
    path.join(process.env.HOME, ".gemini/antigravity/DevToolsActivePort"),
    path.join(process.env.HOME, ".gemini/config/DevToolsActivePort")
  ];

  // Busca adicional dinâmica em sessões ativas do Antigravity
  try {
    const brainBase = path.join(process.env.HOME, ".gemini/antigravity/brain");
    if (fs.existsSync(brainBase)) {
      const dirs = fs.readdirSync(brainBase);
      for (const d of dirs) {
        const pFile = path.join(brainBase, d, "DevToolsActivePort");
        if (fs.existsSync(pFile)) {
          possiblePortFiles.push(pFile);
        }
      }
    }
  } catch (e) {}

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
    console.log("[i] Antigravity DevToolsActivePort não encontrado (app fechado).");
    return;
  }

  let pages;
  try {
    const res = await fetch(`http://127.0.0.1:${port}/json`);
    pages = await res.json();
  } catch (err) {
    console.log("[i] Não foi possível conectar ao DevTools do Antigravity:", err.message);
    return;
  }

  const page = pages.find(p => p.type === "page");
  if (!page || !page.webSocketDebuggerUrl) {
    console.log("[i] Nenhuma página ativa encontrada no DevTools.");
    return;
  }

  // Read active font and scope
  const activeFontPath = path.join(process.env.HOME, ".gemini/config/active_font.json");
  let activeFontKey = "cascadia";
  let activeScope = "full";
  if (fs.existsSync(activeFontPath)) {
    try {
      const d = JSON.parse(fs.readFileSync(activeFontPath, "utf-8"));
      if (d.font && FONTS[d.font]) activeFontKey = d.font;
      if (d.scope) activeScope = d.scope;
    } catch(e) {}
  }
  const font = FONTS[activeFontKey] || FONTS.cascadia;
  const ligVal = font.ligatures ? '"liga" 1, "calt" 1' : '"liga" 0, "calt" 0';
  const primaryCodeFont = font.codeFont.split(',')[0].replace(/['"]/g, '').trim();

  const ws = new WebSocket(page.webSocketDebuggerUrl);

  const fontCssRules = activeScope === "full" ? `
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
      const root = document.documentElement;
      const theme = ${JSON.stringify(theme)};
      
      const vars = {
        "--background": theme.bg,
        "--foreground": theme.fg,
        "--primary": theme.primary,
        "--primary-foreground": theme.primaryFg,
        "--secondary": "color-mix(in srgb, " + (theme.tint || "#ffffff") + " 18%, " + theme.bg + ")",
        "--secondary-foreground": "color-mix(in srgb, " + theme.fg + " 85%, " + theme.bg + ")",
        "--muted": "color-mix(in srgb, " + (theme.tint || "#ffffff") + " 9%, " + theme.bg + ")",
        "--muted-foreground": "color-mix(in srgb, " + theme.fg + " 60%, " + theme.bg + ")",
        "--placeholder": "color-mix(in srgb, " + theme.fg + " 40%, " + theme.bg + ")",
        "--sidebar": theme.sidebar,
        "--sidebar-secondary": "color-mix(in srgb, " + (theme.tint || "#ffffff") + " 16%, " + theme.sidebar + ")",
        "--sidebar-muted": "color-mix(in srgb, " + (theme.tint || "#ffffff") + " 7%, " + theme.sidebar + ")",
        "--content": theme.bg,
        "--card": theme.card,
        "--card-border": "color-mix(in srgb, " + theme.primary + " 22%, var(--card))",
        "--color-primary": theme.primary,
        "--color-background": theme.bg
      };

      for (const [k, v] of Object.entries(vars)) {
        root.style.setProperty(k, v);
      }

      let style = document.getElementById("antigravity-active-theme");
      if (!style) {
        style = document.createElement("style");
        style.id = "antigravity-active-theme";
        document.head.appendChild(style);
      }
      style.textContent = \`
        :root {
          --background: \${theme.bg} !important;
          --foreground: \${theme.fg} !important;
          --primary: \${theme.primary} !important;
          --primary-foreground: \${theme.primaryFg} !important;
          --sidebar: \${theme.sidebar} !important;
          --color-primary: \${theme.primary} !important;
          --color-background: \${theme.bg} !important;
        }
        body {
          background-color: \${theme.bg} !important;
          color: \${theme.fg} !important;
        }
        .bg-background { background-color: \${theme.bg} !important; }
        .text-foreground { color: \${theme.fg} !important; }
        .bg-sidebar { background-color: \${theme.sidebar} !important; }
        .border-border { border-color: \${theme.border} !important; }
        
        a, .text-primary {
          color: \${theme.primary} !important;
        }
        button.bg-primary, .bg-primary {
          background-color: \${theme.primary} !important;
          color: \${theme.primaryFg} !important;
        }
        .xterm-rows { color: \${theme.fg} !important; }
        .xterm-cursor-block { background-color: \${theme.primary} !important; }
      \`;

      // Simultaneously preserve active font
      if (${JSON.stringify(font.importUrl)}) {
        let fontLink = document.getElementById("antigravity-custom-fonts-link");
        if (!fontLink) {
          fontLink = document.createElement("link");
          fontLink.id = "antigravity-custom-fonts-link";
          fontLink.rel = "stylesheet";
          document.head.appendChild(fontLink);
        }
        fontLink.href = "${font.importUrl || ""}";
      }

      let fontStyle = document.getElementById("antigravity-custom-fonts-style");
      if (!fontStyle) {
        fontStyle = document.createElement("style");
        fontStyle.id = "antigravity-custom-fonts-style";
        document.head.appendChild(fontStyle);
      }
      fontStyle.textContent = ${JSON.stringify(fontCssRules)};

      if (document.fonts && document.fonts.load) {
        try {
          document.fonts.load("16px " + JSON.stringify(${JSON.stringify(primaryCodeFont)}));
        } catch(e) {}
      }

      try {
        window.dispatchEvent(new Event("resize"));
      } catch(e) {}

      return { applied: true, theme: "${themeKey}", name: "${theme.name}", font: "${activeFontKey}", scope: "${activeScope}" };
    })()
  `;

  await new Promise((resolve) => {
    let closed = false;
    let timer = setTimeout(() => {
      closed = true;
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
          closed = true;
          if (data.result && data.result.result && data.result.result.value) {
            console.log("[✓] Tema & Fonte sincronizados ao vivo:", data.result.result.value);
          }
          ws.close();
          resolve();
        }
      } catch (e) {
        clearTimeout(timer);
        closed = true;
        ws.close();
        resolve();
      }
    };

    ws.onerror = (err) => {
      if (!closed) {
        clearTimeout(timer);
        console.error("[!] Erro WebSocket DevTools:", err.message);
        resolve();
      }
    };
  });
}

main().catch(console.error);
