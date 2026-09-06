#!/usr/bin/env python3
"""
Antigravity Theme & Font Changer Engine
Full, Dark & Light Mode themes + 13 Coding Fonts with Ligatures.
"""

import sys
import json
import re
import subprocess
import socket
import time
import webbrowser
import os
from pathlib import Path

FONTS = {
    "jetbrains": {
        "name": "JetBrains Mono",
        "author": "JetBrains",
        "badge": "LIGADURAS",
        "tag": "-jetbrains",
        "desc": "A fonte de código #1 para IDEs, com altura-x generosa e ligaduras precisas."
    },
    "fira": {
        "name": "Fira Code",
        "author": "Nikita Prokopov",
        "badge": "CLÁSSICA",
        "tag": "-fira",
        "desc": "A pioneira histórica das ligaduras de programação (===, !==, =>, |>)."
    },
    "cascadia": {
        "name": "Cascadia Code",
        "author": "Microsoft",
        "badge": "MODERNA",
        "tag": "-cascadia",
        "desc": "A fonte moderna do Windows Terminal & VS Code com ligaduras suaves."
    },
    "victor": {
        "name": "Victor Mono",
        "author": "Ruben L. Blom",
        "badge": "CURSIVA & LIGS",
        "tag": "-victor",
        "desc": "Estilo cursivo fluido em itálicos e ligaduras ricas para estética pro."
    },
    "source": {
        "name": "Source Code Pro",
        "author": "Adobe",
        "badge": "ALTA CLAREZA",
        "tag": "-source",
        "desc": "A obra-prima de legibilidade e ergonomia visual da Adobe."
    },
    "inconsolata": {
        "name": "Inconsolata",
        "author": "Raph Levien",
        "badge": "CONDENSADA",
        "tag": "-inconsolata",
        "desc": "Monospace condensada de alta precisão perfeita para terminais densos."
    },
    "hack": {
        "name": "Hack Font",
        "author": "Source Foundry",
        "badge": "DEV WORKHORSE",
        "tag": "-hack",
        "desc": "Desenhada especificamente para código em qualquer resolução."
    },
    "ubuntu": {
        "name": "Ubuntu Mono",
        "author": "Canonical",
        "badge": "LINUX VIBE",
        "tag": "-ubuntu",
        "desc": "A personalidade aconchegante e humanista do clássico terminal Ubuntu."
    },
    "space": {
        "name": "Space Mono",
        "author": "Colophon / Google",
        "badge": "CYBERPUNK",
        "tag": "-space",
        "desc": "Geométrica retro-futurista e brutalista de altíssimo impacto visual."
    },
    "geist": {
        "name": "Geist Mono",
        "author": "Vercel",
        "badge": "MINIMAL",
        "tag": "-geist",
        "desc": "Minimalismo ultra-nítido e cirúrgico do ecossistema Next.js da Vercel."
    },
    "ibm": {
        "name": "IBM Plex Mono",
        "author": "IBM Design",
        "badge": "RETRO INDUSTRIAL",
        "tag": "-ibm",
        "desc": "Herança industrial clássica das máquinas de escrever modernizada."
    },
    "dm": {
        "name": "DM Mono",
        "author": "Colophon / Google",
        "badge": "GEOMÉTRICA",
        "tag": "-dm",
        "desc": "Design Google leve, despojado e contemporâneo para leitura prolongada."
    },
    "system": {
        "name": "System Default (SF Pro / Apple)",
        "author": "Apple macOS",
        "badge": "NATIVO",
        "tag": "-system",
        "desc": "Restaura a tipografia padrão do macOS e do Antigravity."
    }
}

THEMES = {
    # === CATEGORIA 1: FULL MONOCROMÁTICO ===
    "green": {
        "name": "Matrix Phosphor Green",
        "category": "full",
        "description": "Terminal Matrix clássico com fundo preto profundo e verde fósforo fluorescente.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#050B05",
            "primary": "#00FF41",
            "foregroundOverride": "#00FF41",
            "primaryForegroundOverride": "#000000"
        }
    },
    "red": {
        "name": "Glowing Neon Red",
        "category": "full",
        "description": "Vermelho brilhante neon cyberpunk com fundo carmesim escuro e alto contraste.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#0A0002",
            "primary": "#FF003C",
            "foregroundOverride": "#FF2A55",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "cyan": {
        "name": "Full Tron Electric Cyan",
        "category": "full",
        "description": "Cyberpunk elétrico Tron com fundo abissal e ciano neon de altíssima vibração.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#020B0E",
            "primary": "#00F0FF",
            "foregroundOverride": "#00F0FF",
            "primaryForegroundOverride": "#020B0E"
        }
    },
    "yellow": {
        "name": "Full Acid Cyber Yellow",
        "category": "full",
        "description": "Amarelo ácido de alta voltagem estilo hazard/cyberpunk com contraste total.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#0D0C02",
            "primary": "#FFE600",
            "foregroundOverride": "#FFE600",
            "primaryForegroundOverride": "#0D0C02"
        }
    },
    "magenta": {
        "name": "Full Synthwave Magenta",
        "category": "full",
        "description": "Estética synthwave anos 80 com magenta laser e preto profundo.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#0F020B",
            "primary": "#FF007F",
            "foregroundOverride": "#FF007F",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "monochrome": {
        "name": "Full OLED Pure Mono",
        "category": "full",
        "description": "Monocromático absoluto preto e branco para telas OLED e contraste extremo.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#000000",
            "primary": "#FFFFFF",
            "foregroundOverride": "#FFFFFF",
            "primaryForegroundOverride": "#000000"
        }
    },

    # === CATEGORIA 2: MODO ESCURO (DARK COM FILTRO AVELUDADO) ===
    "cappuccino": {
        "name": "Dark Cappuccino",
        "category": "dark",
        "description": "Dark mode com filtro quente de café expresso, caramelo torrado e creme de latte.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#181311",
            "primary": "#D4A373",
            "foregroundOverride": "#EDE0D4",
            "primaryForegroundOverride": "#181311"
        }
    },
    "wine": {
        "name": "Dark Avermelhado Velvet",
        "category": "dark",
        "description": "Dark mode com filtro aveludado de vinho/carmesim profundo, elegante e relaxante.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#120608",
            "primary": "#E63946",
            "foregroundOverride": "#FCE7EA",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "midnight": {
        "name": "Midnight Sapphire Blue",
        "category": "dark",
        "description": "Dark mode noturno com filtro safira azul profundo, focado e calmo.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#090D16",
            "primary": "#38BDF8",
            "foregroundOverride": "#E0F2FE",
            "primaryForegroundOverride": "#090D16"
        }
    },
    "dracula": {
        "name": "Cyber Amethyst Twilight",
        "category": "dark",
        "description": "Dark mode com filtro violeta/ametista néon, estilo Dracula moderno.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#120D1C",
            "primary": "#BD93F9",
            "foregroundOverride": "#F3E8FF",
            "primaryForegroundOverride": "#120D1C"
        }
    },
    "amber": {
        "name": "Amber Warm Dusk",
        "category": "dark",
        "description": "Dark mode com filtro âmbar dourado de crepúsculo, eliminando luz azul cansativa.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#14110A",
            "primary": "#F59E0B",
            "foregroundOverride": "#FEF3C7",
            "primaryForegroundOverride": "#14110A"
        }
    },
    "dark-emerald": {
        "name": "Forest Emerald Night",
        "category": "dark",
        "description": "Floresta noturna com base em esmeralda profundo e toques mentolados suaves.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#06120B",
            "primary": "#10B981",
            "foregroundOverride": "#D1FAE5",
            "primaryForegroundOverride": "#06120B"
        }
    },
    "nordic": {
        "name": "Nordic Arctic Slate",
        "category": "dark",
        "description": "Ardósia nórdica glacial com acentos em ciano polar ártico.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#0B1117",
            "primary": "#38BDF8",
            "foregroundOverride": "#E2E8F0",
            "primaryForegroundOverride": "#0B1117"
        }
    },
    "tokyo": {
        "name": "Tokyo Sunset Coral",
        "category": "dark",
        "description": "Crepúsculo de Tóquio com base berinjela profunda e destaques em coral néon.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#130D14",
            "primary": "#FB7185",
            "foregroundOverride": "#FFE4E6",
            "primaryForegroundOverride": "#130D14"
        }
    },
    "dark-matcha": {
        "name": "Dark Matcha Obsidian",
        "category": "dark",
        "description": "Dark mode com base obsidiana chá-verde e acentos vibrantes em matcha japonês.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#0C100B",
            "primary": "#84CC16",
            "foregroundOverride": "#F0FDF4",
            "primaryForegroundOverride": "#0C100B"
        }
    },
    "dark-copper": {
        "name": "Dark Basalt Copper",
        "category": "dark",
        "description": "Dark mode vulcânico com basalto preto e acentos metálicos em cobre forjado.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#120E0A",
            "primary": "#FB923C",
            "foregroundOverride": "#FFF7ED",
            "primaryForegroundOverride": "#120E0A"
        }
    },
    "dark-ultraviolet": {
        "name": "Dark Cosmic Ultraviolet",
        "category": "dark",
        "description": "Dark mode abissal cósmico com acentos fluorescentes em luz ultravioleta e índigo.",
        "theme_mode": "THEME_MODE_DARK",
        "seeds": {
            "background": "#080616",
            "primary": "#818CF8",
            "foregroundOverride": "#EEF2FF",
            "primaryForegroundOverride": "#080616"
        }
    },

    # === CATEGORIA 3: MODO CLARO (LIGHT + COR SECUNDÁRIA) ===
    "light-emerald": {
        "name": "Light Emerald",
        "category": "light",
        "description": "Modo claro refinado com base pura e cor secundária em verde esmeralda vibrante.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#F7FDF9",
            "primary": "#059669",
            "foregroundOverride": "#064E3B",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-sapphire": {
        "name": "Light Sapphire",
        "category": "light",
        "description": "Modo claro cristalino com base suave e cor secundária em azul safira executivo.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#F8FAFC",
            "primary": "#0284C7",
            "foregroundOverride": "#0F172A",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-ruby": {
        "name": "Light Ruby",
        "category": "light",
        "description": "Modo claro energizante com base pura e cor secundária em vermelho rubi contemporâneo.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#FFF8F8",
            "primary": "#E11D48",
            "foregroundOverride": "#1E293B",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-lavender": {
        "name": "Light Lavender",
        "category": "light",
        "description": "Modo claro moderno e harmônico com cor secundária em violeta ametista suave.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#FAF8FF",
            "primary": "#7C3AED",
            "foregroundOverride": "#1E1B4B",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-amber": {
        "name": "Light Amber Sunburst",
        "category": "light",
        "description": "Modo claro acolhedor com cor secundária em âmbar solar dourado.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#FFFDF5",
            "primary": "#D97706",
            "foregroundOverride": "#1C1917",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-latte": {
        "name": "Light Coffee Latte",
        "category": "light",
        "description": "Modo claro marfim suave com cor secundária em café latte e caramelo expresso.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#FAF7F2",
            "primary": "#9A3412",
            "foregroundOverride": "#291E1A",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-rose": {
        "name": "Light Rosé Wine",
        "category": "light",
        "description": "Modo claro delicado e requintado com cor secundária em vinho rosé champagne.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#FFF5F7",
            "primary": "#BE123C",
            "foregroundOverride": "#1F1116",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-teal": {
        "name": "Light Ocean Teal",
        "category": "light",
        "description": "Modo claro arejado inspirado em águas marinhas com cor secundária em teal límpido.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#F2FBF9",
            "primary": "#0D9488",
            "foregroundOverride": "#0F172A",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-coral": {
        "name": "Light Coral Peach",
        "category": "light",
        "description": "Modo claro aquecido com acentos em laranja coral e pêssego ensolarado.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#FFF9F6",
            "primary": "#EA580C",
            "foregroundOverride": "#1C1917",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-indigo": {
        "name": "Light Electric Indigo",
        "category": "light",
        "description": "Modo claro contemporâneo de alto contraste com tinta azul índigo e violeta.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#F8F9FE",
            "primary": "#4F46E5",
            "foregroundOverride": "#0F172A",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "white": {
        "name": "Pure Clean White",
        "category": "light",
        "description": "Tema totalmente branco minimalista, puro e com tipografia ultra nítida.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#FFFFFF",
            "primary": "#111827",
            "foregroundOverride": "#111827",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-pistachio": {
        "name": "Light Pistachio Gelato",
        "category": "light",
        "description": "Modo claro aveludado com base marfim suave e acentos gourmet em verde pistache siciliano.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#F8FAF0",
            "primary": "#65A30D",
            "foregroundOverride": "#1A2E05",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-terracotta": {
        "name": "Light Tuscan Terracotta",
        "category": "light",
        "description": "Modo claro toscano acolhedor com base linho e acentos artesanais em terracota queimada.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#FDF8F6",
            "primary": "#C2410C",
            "foregroundOverride": "#27140B",
            "primaryForegroundOverride": "#FFFFFF"
        }
    },
    "light-azure": {
        "name": "Light Alpine Sky Azure",
        "category": "light",
        "description": "Modo claro alpino glacial cristalino com acentos em azul cerúleo e céu radiante.",
        "theme_mode": "THEME_MODE_LIGHT",
        "seeds": {
            "background": "#F0F9FF",
            "primary": "#00A3FF",
            "foregroundOverride": "#082F49",
            "primaryForegroundOverride": "#FFFFFF"
        }
    }
}

def parse_target_font(args):
    raw = " ".join(args).lower().strip()
    if "victor" in raw: return "victor"
    if "jetbrains" in raw or "jet-brains" in raw: return "jetbrains"
    if "fira" in raw: return "fira"
    if "cascadia" in raw: return "cascadia"
    if "source" in raw or "adobe" in raw: return "source"
    if "inconsolata" in raw: return "inconsolata"
    if "hack" in raw: return "hack"
    if "ubuntu" in raw: return "ubuntu"
    if "space" in raw: return "space"
    if "geist" in raw or "vercel" in raw: return "geist"
    if "ibm" in raw or "plex" in raw: return "ibm"
    if "dm" in raw or "deepmind" in raw: return "dm"
    if "system" in raw or "padrao" in raw or "padrão" in raw or "apple" in raw: return "system"
    return None

def parse_target_theme(args):
    raw = " ".join(args).lower().strip()
    
    # Full / Monochromatic
    if "cyan" in raw or "tron" in raw:
        return "cyan"
    elif "yellow" in raw or "amarelo" in raw or "acid" in raw:
        return "yellow"
    elif "magenta" in raw or "synthwave" in raw:
        return "magenta"
    elif "monochrome" in raw or "oled" in raw or "preto-e-branco" in raw:
        return "monochrome"
        
    # Dark Mode Variations
    elif "dark-emerald" in raw or "floresta" in raw or "forest" in raw:
        return "dark-emerald"
    elif "nordic" in raw or "artico" in raw or "arctic" in raw:
        return "nordic"
    elif "tokyo" in raw or "sunset" in raw:
        return "tokyo"
    elif "-cappucc" in raw or "cappucc" in raw or "cafe" in raw or "coffee" in raw:
        return "cappuccino"
    elif "-wine" in raw or "wine" in raw or "-avermelh" in raw or "avermelh" in raw or "vinho" in raw or "dark-red" in raw:
        return "wine"
    elif "-mid" in raw or "midnight" in raw or "safira" in raw or "azul" in raw or "-blue" in raw:
        return "midnight"
    elif "-drac" in raw or "dracula" in raw or "-purple" in raw or "roxo" in raw or "ametista" in raw:
        return "dracula"
    elif "-amber" in raw or "amber" in raw or "-dourad" in raw or "dourado" in raw or "gold" in raw or "ambar" in raw:
        return "amber"
    elif "-green" in raw or "green" in raw or "verde" in raw or "matrix" in raw:
        return "green"
    elif "-red" in raw or "red" in raw or "vermelho" in raw:
        return "red"
    elif "matcha" in raw or "cha-verde" in raw or "chá-verde" in raw:
        return "dark-matcha"
    elif "copper" in raw or "cobre" in raw or "basalt" in raw or "basalto" in raw or "bronze" in raw:
        return "dark-copper"
    elif "ultraviolet" in raw or "uv" in raw or "cosmic" in raw or "cosmico" in raw or "cósmico" in raw:
        return "dark-ultraviolet"
        
    # Light Mode Variations
    elif "pistachio" in raw or "pistache" in raw:
        return "light-pistachio"
    elif "terracotta" in raw or "terracota" in raw or "toscano" in raw or "tuscan" in raw or "argila" in raw:
        return "light-terracotta"
    elif "azure" in raw or "azur" in raw or "alpino" in raw or "alpine" in raw or "ceu" in raw or "céu" in raw:
        return "light-azure"
    elif "coral" in raw or "pessego" in raw or "peach" in raw:
        return "light-coral"
    elif "indigo" in raw or "eletrico" in raw:
        return "light-indigo"
    elif "emerald" in raw or "light-green" in raw or "light-verd" in raw or "verde-clar" in raw or "menta" in raw:
        return "light-emerald"
    elif "sapphire" in raw or "light-blue" in raw or "light-azul" in raw or "azul-clar" in raw or "safira-clar" in raw:
        return "light-sapphire"
    elif "ruby" in raw or "light-red" in raw or "light-verm" in raw or "vermelho-clar" in raw or "rubi" in raw:
        return "light-ruby"
    elif "lavender" in raw or "light-purple" in raw or "violet" in raw or "roxo-clar" in raw:
        return "light-lavender"
    elif "sunburst" in raw or "light-amber" in raw or "dourado-clar" in raw or "ambar-clar" in raw or "sol" in raw:
        return "light-amber"
    elif "latte" in raw or "light-cappucc" in raw or "cafe-clar" in raw or "creme" in raw:
        return "light-latte"
    elif "rose" in raw or "light-wine" in raw or "vinho-clar" in raw or "champagne" in raw:
        return "light-rose"
    elif "teal" in raw or "ocean" in raw or "light-teal" in raw or "ciano-clar" in raw:
        return "light-teal"
    elif "-white" in raw or "white" in raw or "branco" in raw:
        return "white"
        
    return None

def update_config_json(theme_key):
    theme = THEMES[theme_key]
    config_path = Path.home() / ".gemini/config/config.json"
    if not config_path.exists():
        return False

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "userSettings" not in data:
            data["userSettings"] = {}

        seeds = theme["seeds"]
        data["userSettings"]["customThemeSeedsDark"] = seeds
        data["userSettings"]["customThemeSeedsLight"] = seeds
        data["userSettings"]["themeMode"] = theme["theme_mode"]

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        return True
    except Exception as e:
        print("[!] Erro ao atualizar config.json:", e)
        return False

def update_pbtxt(theme_key):
    theme = THEMES[theme_key]
    pbtxt_path = Path.home() / ".gemini/antigravity/antigravity_state.pbtxt"
    if not pbtxt_path.exists():
        return False

    try:
        with open(pbtxt_path, "r", encoding="utf-8") as f:
            content = f.read()

        seeds = theme["seeds"]
        bg = seeds["background"]
        pri = seeds["primary"]
        fg = seeds["foregroundOverride"]
        pfg = seeds["primaryForegroundOverride"]
        mode = theme["theme_mode"]

        new_blocks = f"""theme_mode: {mode}
custom_theme_seeds_dark: {{
  background: "{bg}"
  primary: "{pri}"
  foreground_override: "{fg}"
  primary_foreground_override: "{pfg}"
}}
custom_theme_seeds_light: {{
  background: "{bg}"
  primary: "{pri}"
  foreground_override: "{fg}"
  primary_foreground_override: "{pfg}"
}}"""

        pattern = r"theme_mode: [A-Z_]+\ncustom_theme_seeds_dark: \{[^}]+\}\ncustom_theme_seeds_light: \{[^}]+\}"
        if re.search(pattern, content):
            content = re.sub(pattern, new_blocks, content)
        else:
            uuid_pat = r'(installation_uuid: "[^"]+")'
            if re.search(uuid_pat, content):
                content = re.sub(uuid_pat, r'\1\n' + new_blocks, content)
            else:
                content += "\n" + new_blocks + "\n"

        with open(pbtxt_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print("[!] Erro ao atualizar antigravity_state.pbtxt:", e)
        return False

def get_script_path(name):
    p1 = Path(__file__).resolve().parent / name
    if p1.exists():
        return p1
    p2 = Path.home() / ".gemini/config/skills/theme-changer/scripts" / name
    if p2.exists():
        return p2
    return p1

def get_server_script():
    # 1. Mesma pasta scripts
    p1 = Path(__file__).resolve().parent / "theme_server.py"
    if p1.exists():
        return p1
    # 2. Pasta raiz do projeto/skill
    p2 = Path(__file__).resolve().parent.parent / "theme_server.py"
    if p2.exists():
        return p2
    # 3. Pasta padrão global de scripts do Antigravity
    p3 = Path.home() / ".gemini/config/skills/theme-changer/scripts/theme_server.py"
    if p3.exists():
        return p3
    p4 = Path.home() / ".gemini/config/skills/theme-changer/theme_server.py"
    if p4.exists():
        return p4
    return p1

def apply_live(theme_key):
    script_path = get_script_path("apply_live_theme.js")
    if script_path.exists():
        try:
            res = subprocess.run(["node", str(script_path), theme_key], capture_output=True, text=True, timeout=5)
            if res.stdout:
                print(res.stdout.strip())
        except Exception as e:
            print("[i] Aviso ao sincronizar ao vivo:", e)

def apply_font_live(font_key, scope="full"):
    script_path = get_script_path("apply_font.js")
    if script_path.exists():
        try:
            res = subprocess.run(["node", str(script_path), font_key, scope], capture_output=True, text=True, timeout=5)
            if res.stdout:
                print(res.stdout.strip())
            return True
        except Exception as e:
            print("[!] Erro ao aplicar fonte:", e)
            return False
    return False

SERVER_SCRIPT = get_server_script()
APP_URL = "http://localhost:48123/theme_changer_app.html"
PORT = 48123

def is_server_running(port=PORT):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False

def handle_init():
    print("━" * 60)
    print("🍏 GOOGLE ANTIGRAVITY — THEME STUDIO & FONT CENTER")
    print("━" * 60)

    # 1. Verifica e ativa o servidor local
    if is_server_running():
        print(f"[✓] Servidor interno multithread já está ativo na porta {PORT}.")
    else:
        log_candidates = [
            Path.home() / ".gemini/antigravity/theme_server.log",
            Path.home() / ".gemini/config/skills/theme-changer/theme_server.log",
            Path("/tmp/antigravity_theme_server.log")
        ]
        f_out = None
        for cand in log_candidates:
            try:
                cand.parent.mkdir(parents=True, exist_ok=True)
                f_out = open(cand, "a", encoding="utf-8")
                break
            except Exception:
                continue

        server_path = get_server_script()
        stdout_target = f_out if f_out is not None else subprocess.DEVNULL
        try:
            subprocess.Popen(
                [sys.executable, str(server_path)],
                stdout=stdout_target,
                stderr=subprocess.STDOUT,
                cwd=str(server_path.parent),
                start_new_session=True
            )
        except Exception as err:
            print(f"[!] Erro ao iniciar processo do servidor: {err}")

        started = False
        for _ in range(25):
            time.sleep(0.1)
            if is_server_running():
                started = True
                break

        if started:
            print(f"[✓] Servidor interno inicializado com sucesso na porta {PORT}!")
        else:
            print(f"[!] Servidor disparado em segundo plano. Verifique {APP_URL}")

    # 2. Abre a página visual no navegador padrão
    print(f"[*] Abrindo Theme Studio no seu navegador padrão...")
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", APP_URL], check=False)
        else:
            webbrowser.open(APP_URL)
        print(f"[✓] Painel web aberto com sucesso!")
    except Exception as e:
        print(f"[!] Aviso ao abrir navegador automaticamente: {e}")

    print("\n✨ Tudo pronto! Acesse o painel pelo link abaixo com apenas 1 clique:")
    print(f"👉 {APP_URL}")
    print("━" * 60)

def main():
    args = sys.argv[1:]
    raw_args = " ".join(args).lower().strip()

    # Special command: init
    if "init" in raw_args or (args and args[0].lower() in ["init", "--init", "-init"]):
        handle_init()
        return

    # Scope detection
    scope = "code" if ("scope=code" in raw_args or "-code-only" in raw_args) else "full"

    # Check font intent
    font_target = parse_target_font(args)
    is_font_intent = "font" in raw_args or font_target is not None

    if is_font_intent:
        if not font_target:
            font_target = "jetbrains"
        f = FONTS[font_target]
        print(f"[*] Aplicando fonte '{f['name']}' no Google Antigravity (Modo: {scope.upper()})...")
        ok = apply_font_live(font_target, scope)
        if ok:
            print(f"\n✨ SUCESSO: Fonte {f['name']} ({f['badge']}) ativada no Google Antigravity!")
            print(f"🔤 Autor: {f['author']}")
            print(f"🎯 Modo:  {'Total (Chat + Prompts + Código + Terminal)' if scope == 'full' else 'Híbrido (Apenas Código & Terminal)'}")
            print(f"📋 Descrição: {f['desc']}")
        else:
            print("[!] Não foi possível aplicar a fonte no momento.")
        return

    # Check theme intent
    theme_target = parse_target_theme(args)
    if not theme_target:
        print("=== THEME & FONT CHANGER STUDIO — GOOGLE ANTIGRAVITY ===")
        print("Uso:")
        print("  Trocar Tema:  python3 theme_changer.py theme -[FLAG]")
        print("  Trocar Fonte: python3 theme_changer.py font -[NOME]")
        print("\n🎨 Categorias de Temas (30 Opções de Elite):")
        print("  - Full Monocromático (6): -green, -red, -cyan, -yellow, -magenta, -monochrome")
        print("  - Dark Velvet Tinted (11): -cappuccino, -wine, -midnight, -dracula, -amber, -dark-emerald, -nordic, -tokyo, -matcha, -copper, -ultraviolet")
        print("  - Light Luminary (13):   -emerald, -sapphire, -ruby, -lavender, -sunburst, -latte, -rose, -teal, -coral, -indigo, -pistachio, -terracotta, -azure, -white")
        print("\n🔤 Fontes Disponíveis (13 Fontes de Elite):")
        for k, v in FONTS.items():
            print(f"  - {v['tag']:<14} {v['name']:<28} [{v['badge']}] ({v['author']})")
        sys.exit(1)

    t = THEMES[theme_target]
    print(f"[*] Aplicando tema '{t['name']}' no Google Antigravity...")
    ok1 = update_config_json(theme_target)
    ok2 = update_pbtxt(theme_target)
    apply_live(theme_target)

    if ok1 and ok2:
        print(f"\n✨ SUCESSO: Tema {theme_target.upper()} ({t['name']}) aplicado com sucesso!")
        print(f"🎨 Paleta ativa:")
        print(f"   - Background: {t['seeds']['background']}")
        print(f"   - Primary:    {t['seeds']['primary']}")
        print(f"   - Text/FG:    {t['seeds']['foregroundOverride']}")
        print(f"   - Button FG:  {t['seeds']['primaryForegroundOverride']}")
        print(f"   - Modo:       {t['theme_mode']}")
        print("\nA interface do Antigravity foi atualizada em tempo real preservando a sua fonte ativa!")
    else:
        print("[!] Ocorreu um erro ao atualizar os arquivos de configuração.")
        sys.exit(1)

if __name__ == "__main__":
    main()
