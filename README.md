# 🍏 Google Antigravity — Theme Studio & Font Center

<div align="center">

![Antigravity Theme Studio](https://img.shields.io/badge/Google-Antigravity-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Themes](https://img.shields.io/badge/31-Elite_Themes-10B981?style=for-the-badge)
![Fonts](https://img.shields.io/badge/13-Dev_Fonts_w%2F_Ligatures-8B5CF6?style=for-the-badge)
![UI](https://img.shields.io/badge/Apple_Liquid_Glass-VisionOS_Design-0071E3?style=for-the-badge)
![Speed](https://img.shields.io/badge/Sub--150ms-Realtime_CDP-EC4899?style=for-the-badge)

**A suíte definitiva de customização visual, paletas cromáticas e tipografia para o Google Antigravity.**  
Alterne instantaneamente entre 31 temas de alto padrão e 13 fontes de programação com ligaduras nativas, com injeção em tempo real via Chrome DevTools Protocol e interface Apple Liquid Glass.

[🚀 Início Rápido](#-início-rápido) • [🎨 Catálogo de Temas](#-catálogo-de-31-temas-de-elite) • [🔤 Catálogo de Fontes](#-catálogo-de-13-fontes-com-ligaduras) • [🏛️ Arquitetura](#️-arquitetura-técnica) • [📦 Instalação](#-instalação-automatizada)

</div>

---

## ✨ Destaques & Diferenciais

- **⚡ 31 Temas de Elite em 3 Categorias**:
  - **Full Monocromáticos (6)**: Alto contraste, saturação vibrante e estética Cyberpunk/CRT.
  - **Dark Velvet Tinted (11)**: Bases escuras aveludadas (`#080616` a `#181311`) com filtros de cor refinados (Matcha, Basalt Copper, Ultraviolet, Tokyo Coral, etc.).
  - **Light Luminary (14)**: Bases claras suaves e frescas com cores secundárias intensificadas e legibilidade cristalina (Pistachio Gelato, Tuscan Terracotta, Alpine Azure, etc.).
- **🔤 13 Fontes de Programação com Ligaduras Nativas**:
  - JetBrains Mono, Fira Code, Cascadia Code, Victor Mono (itálico cursivo), Source Code Pro, Hack, Inconsolata, Geist Mono, IBM Plex Mono, Space Mono, Ubuntu Mono, DM Mono e SF Pro Apple.
  - Suporte a dois modos: **Total** (aplica na interface completa, chat e prompts) e **Código & Terminal** (mantém a interface sans-serif).
- **🍏 Interface Web Apple Liquid Glass**:
  - Design ultra minimalista inspirado no visionOS e macOS Tahoe.
  - Superfícies translúcidas com `backdrop-filter: blur(36px)`, bordas com realce especular de refração e orbes fluidos em background.
  - Mini-janelas interativas com renderização fiel de paleta e badges hexadecimais.
- **⚡ Injeção Sub-150ms em Tempo Real**:
  - Sem necessidade de recarregar a janela do Antigravity.
  - Conexão direta via Chrome DevTools Protocol (CDP) com sincronização bidirecional em `config.json` e `antigravity_state.pbtxt`.
- **🚀 Ativação em 1 Comando (`init`)**:
  - Inicializa o servidor interno multithread e abre a página no navegador com apenas uma instrução.

---

## 🚀 Início Rápido

### 1. Comando Único `init` (Recomendado)
Para iniciar o servidor local e abrir a interface web instantaneamente:

```bash
python3 scripts/theme_changer.py init
```

Ou diretamente no chat do Antigravity:
```text
@theme-changer init
```

O servidor será ativado na porta `48123` e o painel será aberto automaticamente no seu navegador:
👉 **[http://localhost:48123/theme_changer_app.html](http://localhost:48123/theme_changer_app.html)**

---

## 📦 Instalação Automatizada

Para instalar a skill e o agente em qualquer instalação do Google Antigravity:

```bash
git clone https://github.com/MateusCelestinoProX/antigravity-theme-changer.git
cd antigravity-theme-changer
chmod +x install.sh
./install.sh
```

O instalador configura:
- Scripts em `~/.gemini/config/skills/theme-changer/scripts/`
- Skill em `~/.gemini/config/skills/theme-changer/SKILL.md`
- Agente em `~/.gemini/config/agents/theme-changer.md`

---

## 🎨 Catálogo de 31 Temas de Elite

### ⚡ 1. Temas Full Monocromáticos (6 Opções)
| Flag | Nome | Background | Primary | Destaque |
| :--- | :--- | :--- | :--- | :--- |
| `-green` | **Matrix Phosphor Green** | `#050B05` | `#00FF41` | Terminal hacker clássico CRT |
| `-red` | **Glowing Cyberpunk Red** | `#0A0002` | `#FF003C` | Laser neon vermelho puro |
| `-cyan` | **Full Tron Electric Cyan** | `#040B14` | `#00F0FF` | Neon azul elétrico de alta energia |
| `-amber` | **Vintage Amber Phosphor** | `#0D0B02` | `#FFB000` | Terminal IBM/DEC monocromático |
| `-magenta` | **Vaporwave Hot Magenta** | `#0D030C` | `#FF007F` | Laser sintetizador anos 80 |
| `-pureblack` | **OLED True Pure Black** | `#000000` | `#22C55E` | Preto absoluto com acentos esmeralda |

### 🌙 2. Temas Dark Velvet Tinted (11 Opções)
| Flag | Nome | Background | Primary | Destaque |
| :--- | :--- | :--- | :--- | :--- |
| `-emerald` | **Dark Velvet Emerald** | `#0D1410` | `#10B981` | Verde floresta profundo e aveludado |
| `-sapphire` | **Dark Velvet Sapphire** | `#0D1117` | `#38BDF8` | Azul marinho estelar refinado |
| `-ruby` | **Dark Velvet Ruby** | `#140C0E` | `#F43F5E` | Vermelho carmim e vinho aveludado |
| `-lavender` | **Dark Velvet Lavender** | `#130F1A` | `#A855F7` | Roxo ametista crepuscular |
| `-sunburst` | **Dark Velvet Sunburst** | `#16130B` | `#FBBF24` | Dourado âmbar sofisticado |
| `-latte` | **Dark Velvet Latte** | `#14100E` | `#FB923C` | Tons terrosos de café expresso |
| `-rose` | **Dark Velvet Rosé** | `#140D10` | `#FB7185` | Rosé refinado e aveludado |
| `-tokyo` | **Tokyo Sunset Coral** | `#130D14` | `#FB7185` | Crepúsculo metropolitano e coral |
| `-matcha` | **Dark Matcha Obsidian** | `#0C100B` | `#84CC16` | Chá-verde matcha e obsidiana |
| `-copper` | **Dark Basalt Copper** | `#120E0A` | `#FB923C` | Basalto vulcânico e cobre metálico |
| `-ultraviolet` | **Dark Cosmic Ultraviolet**| `#080616` | `#818CF8` | Espaço cósmico e radiação UV |

### ☀️ 3. Temas Light Luminary (14 Opções)
| Flag | Nome | Background | Primary | Destaque |
| :--- | :--- | :--- | :--- | :--- |
| `-white` | **Pure Clean White** | `#FFFFFF` | `#111827` | Branco minimalista puro e nítido |
| `-emerald` | **Light Emerald** | `#F7FDF9` | `#059669` | Menta suave e verde esmeralda |
| `-sapphire` | **Light Sapphire** | `#F0F9FF` | `#0284C7` | Base cristalina e azul safira executivo |
| `-ruby` | **Light Ruby** | `#FFF1F2` | `#E11D48` | Energizante com vermelho rubi |
| `-lavender` | **Light Lavender** | `#F5F3FF` | `#7C3AED` | Lavanda suave e violeta real |
| `-sunburst` | **Light Amber Sunburst** | `#FFFBEB` | `#D97706` | Luz solar dourada acolhedora |
| `-latte` | **Light Coffee Latte** | `#FAF5F0` | `#9A3412` | Marfim aveludado e café latte |
| `-rose` | **Light Rosé Wine** | `#FFF5F7` | `#BE123C` | Champagne rosé francês |
| `-teal` | **Light Ocean Teal** | `#F2FBF9` | `#0D9488` | Azul turquesa oceânico límpido |
| `-coral` | **Light Coral Peach** | `#FFF9F6` | `#EA580C` | Laranja coral e pêssego aquecido |
| `-indigo` | **Light Electric Indigo** | `#F8F9FE` | `#4F46E5` | Índigo elétrico de alta definição |
| `-pistachio` | **Light Pistachio Gelato** | `#F8FAF0` | `#65A30D` | Creme marfim e pistache siciliano |
| `-terracotta` | **Light Tuscan Terracotta** | `#FDF8F6` | `#C2410C` | Linho artesanal e terracota queimada|
| `-azure` | **Light Alpine Sky Azure** | `#F0F9FF` | `#00A3FF` | Gelo glacial e azul celeste alpino |

---

## 🔤 Catálogo de 13 Fontes com Ligaduras

| Flag | Fonte | Autor / Fundição | Ligaduras | Badge |
| :--- | :--- | :--- | :--- | :--- |
| `-jetbrains` | **JetBrains Mono** | JetBrains | Sim | `LIGADURAS PRO` |
| `-fira` | **Fira Code** | Nikita Prokopov | Sim | `CLÁSSICA` |
| `-cascadia` | **Cascadia Code** | Microsoft | Sim | `MODERNA` |
| `-victor` | **Victor Mono** | Ruben L. Blom | Sim (Cursiva) | `CURSIVA & LIGS` |
| `-source` | **Source Code Pro** | Adobe | Não | `ALTA CLAREZA` |
| `-inconsolata`| **Inconsolata** | Raph Levien | Não | `CONDENSADA` |
| `-hack` | **Hack Font** | Source Foundry | Não | `DEV WORKHORSE` |
| `-ubuntu` | **Ubuntu Mono** | Canonical | Não | `LINUX VIBE` |
| `-space` | **Space Mono** | Colophon / Google | Não | `CYBERPUNK` |
| `-geist` | **Geist Mono** | Vercel | Sim | `MINIMAL` |
| `-ibm` | **IBM Plex Mono** | IBM Design | Não | `RETRO INDUSTRIAL` |
| `-dm` | **DM Mono** | Colophon / Google | Não | `GEOMÉTRICA` |
| `-system` | **System Default** | Apple macOS (SF Pro) | Não | `NATIVO` |

### Modos de Aplicação da Tipografia
- **Modo Total (`scope=full`)**: Aplica a tipografia no ambiente integral do Antigravity (Chat, Balões, Prompts, Títulos, Abas, Editor e Terminal).
- **Modo Híbrido (`scope=code`)**: Mantém a interface do usuário com a fonte sem serifa limpa e aplica a tipografia apenas em blocos de código e terminais.

---

## 🖥️ Uso via Linha de Comando (CLI)

### Trocar Tema
```bash
python3 scripts/theme_changer.py theme -emerald
python3 scripts/theme_changer.py theme -matcha
python3 scripts/theme_changer.py theme -copper
python3 scripts/theme_changer.py theme -cappuccino
```

### Trocar Fonte
```bash
# Modo Total (Padrão)
python3 scripts/theme_changer.py font -jetbrains
python3 scripts/theme_changer.py font -victor
python3 scripts/theme_changer.py font -geist

# Modo Apenas Código & Terminal
python3 scripts/theme_changer.py font -fira -code-only
```

### Listar Opções Disponíveis
```bash
python3 scripts/theme_changer.py list
```

---

## 🏛️ Arquitetura Técnica

O Theme Changer atua através de uma pipeline de tripla sincronização:

```
┌─────────────────────────────────────────────────────────────┐
│                 Theme Changer Controller                     │
│                   (theme_changer.py)                         │
└──────┬───────────────────────┬────────────────────────┬─────┘
       │                       │                        │
       ▼                       ▼                        ▼
┌───────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ config.json   │     │ antigravity_     │     │ Chrome DevTools │
│               │     │ state.pbtxt      │     │ Protocol (CDP)  │
│ Define sementes     │ Sincroniza blocos│     │ Injeta estilos  │
│ customizadas  │     │ protobuf para o  │     │ CSS e fontes    │
│ de tema       │     │ language server  │     │ em < 150ms      │
└───────────────┘     └──────────────────┘     └─────────────────┘
```

1. **Persistência do Tema**: Sincroniza `~/.gemini/config/config.json` (`userSettings.customThemeSeedsDark`, `customThemeSeedsLight`, `themeMode`).
2. **Sincronização Protobuf**: Atualiza atomicamente `~/.gemini/antigravity/antigravity_state.pbtxt` no bloco `jetbox_state_pb.CustomThemeSeeds`.
3. **Injeção Dinâmica CDP**: Detecta o socket ativo em `DevToolsActivePort`, conecta ao WebSocket do Chrome DevTools do Antigravity e avalia regras CSS com variáveis semitransparentes e ligaduras de tipografia em tempo de execução sem piscar a tela.

---

## 🤖 Integração com o Agente Theme Changer

Você pode invocar o agente especialista a qualquer momento dentro do Google Antigravity:

- `@theme-changer init`
- `@theme-changer theme -matcha`
- `@theme-changer theme -pistachio`
- `@theme-changer font -victor`

---

## 📄 Licença

Distribuído sob a licença MIT. Livre para uso pessoal e modificação.
Desenvolvido com foco em excelência visual e engenharia de precisão para o ecossistema Google Antigravity.
