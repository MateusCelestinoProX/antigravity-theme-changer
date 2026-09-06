# 🍏 Google Antigravity — Theme Studio & Font Center

<div align="center">

![Antigravity Theme Studio](https://img.shields.io/badge/Google-Antigravity_2.0-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Themes](https://img.shields.io/badge/31-Elite_Themes-10B981?style=for-the-badge)
![Fonts](https://img.shields.io/badge/13-Dev_Fonts_w%2F_Ligatures-8B5CF6?style=for-the-badge)
![UI](https://img.shields.io/badge/Apple_Liquid_Glass-VisionOS_Design-0071E3?style=for-the-badge)
![Speed](https://img.shields.io/badge/Sub--150ms-Realtime_CDP-EC4899?style=for-the-badge)
![API](https://img.shields.io/badge/REST_API-Port_48123-F59E0B?style=for-the-badge)

**A suíte definitiva de customização visual, paletas cromáticas e tipografia para o Google Antigravity.**  
Alterne instantaneamente entre **31 temas de elite** e **13 fontes de programação com ligaduras nativas**, com injeção em tempo real via Chrome DevTools Protocol (CDP), interface Apple Liquid Glass e controle total por Agente de IA.

[🚀 Início Rápido](#-início-rápido) • [🤖 Comandos do Agente](#-comandos-do-agente-theme-changer) • [🎨 Catálogo de Temas](#-catálogo-de-31-temas-de-elite) • [🔤 Catálogo de Fontes](#-catálogo-de-13-fontes-com-ligaduras) • [🏛️ Arquitetura](#️-arquitetura-técnica) • [📚 Guias & Documentação](#-guias--documentação-técnica) • [📦 Instalação](#-instalação-automatizada)

</div>

---

## 📚 Guias & Documentação Técnica

Para um mergulho profundo em cada faceta da solução, consulte nossos manuais dedicados:

- 🤖 **[Guia do Agente Autônomo (AGENT_GUIDE.md)](docs/AGENT_GUIDE.md)**: Documentação completa do agente `@theme-changer`, gramática de comandos, políticas de execução, manifesto YAML e integração com o Antigravity 2.0.
- 🏛️ **[Arquitetura do Sistema (ARCHITECTURE.md)](docs/ARCHITECTURE.md)**: Detalhamento do motor Tri-Sync, protocolo CDP WebSocket, injeção de CSS em <150ms, busca dinâmica de portas e doutrina de design Apple Liquid Glass.
- 📡 **[Referência da API REST (API_REFERENCE.md)](docs/API_REFERENCE.md)**: Especificação completa de todas as rotas HTTP locais da porta 48123 (`/api/status`, `/api/list`, `/api/set-theme`, `/api/set-font`), schemas JSON e exemplos com cURL e JavaScript.

---

## ✨ Destaques & Diferenciais

- **⚡ 31 Temas de Elite em 3 Categorias**:
  - **Full Monocromáticos (6)**: Alto contraste, saturação vibrante e estética Cyberpunk/CRT.
  - **Dark Velvet Tinted (11)**: Bases escuras aveludadas (`#080616` a `#181311`) com filtros de cor refinados (Matcha Obsidian, Basalt Copper, Ultraviolet, Tokyo Coral, Cappuccino, etc.).
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

### 1. Inicialização Integrada em 1 Clique
Para iniciar o servidor local e abrir a interface web instantaneamente:

```bash
python3 scripts/theme_changer.py init
```

Ou diretamente no chat do Antigravity com o agente:
```text
@theme-changer init
```

O servidor será ativado na porta `48123` e o painel será aberto automaticamente no seu navegador:
👉 **[http://localhost:48123/theme_changer_app.html](http://localhost:48123/theme_changer_app.html)**

---

## 🤖 Comandos do Agente Theme Changer

Você pode invocar o agente autônomo `@theme-changer` no chat do Antigravity para executar comandos rápidos:

| Comando | Descrição | Exemplo |
| :--- | :--- | :--- |
| `@theme-changer init` | Inicia o servidor interno e abre o painel web | `@theme-changer init` |
| `@theme-changer status` | Exibe tema ativo, fonte ativa, modo e status do servidor | `@theme-changer status` |
| `@theme-changer list` | Lista todos os 31 temas e 13 fontes disponíveis | `@theme-changer list` |
| `@theme-changer theme -[FLAG]` | Altera o tema instantaneamente em tempo real | `@theme-changer theme -matcha` |
| `@theme-changer font -[FLAG]` | Altera a tipografia globalmente com ligaduras | `@theme-changer font -victor` |
| `@theme-changer font -[FLAG] -code-only` | Aplica a fonte apenas no editor e terminais | `@theme-changer font -fira -code-only` |

---

## 📦 Instalação Automatizada

Para instalar a skill e o agente em qualquer máquina com Google Antigravity:

```bash
git clone https://github.com/MateusCelestinoProX/antigravity-theme-changer.git
cd antigravity-theme-changer
chmod +x install.sh
./install.sh
```

O instalador universal configura:
- Scripts em `~/.gemini/config/skills/theme-changer/scripts/`
- Skill em `~/.gemini/config/skills/theme-changer/SKILL.md`
- Agente autônomo em `~/.gemini/config/agents/theme-changer.md`

---

## 🎨 Catálogo de 31 Temas de Elite

### ⚡ 1. Temas Full Monocromáticos (6 Opções)
| Flag | Nome | Background | Primary | Destaque |
| :--- | :--- | :--- | :--- | :--- |
| `-green` | **Matrix Phosphor Green** | `#050B05` | `#00FF41` | Terminal hacker clássico CRT |
| `-red` | **Glowing Cyberpunk Red** | `#0A0002` | `#FF003C` | Laser neon vermelho puro |
| `-cyan` | **Full Tron Electric Cyan** | `#040B14` | `#00F0FF` | Neon azul elétrico de alta energia |
| `-yellow` | **Full Acid Cyber Yellow** | `#0E0D03` | `#FFE600` | Amarelo ácido vibrante cyberpunk |
| `-magenta` | **Full Synthwave Magenta** | `#100312` | `#FF007F` | Laser sintetizador anos 80 |
| `-monochrome`| **Full OLED Pure Mono** | `#000000` | `#FFFFFF` | Preto absoluto OLED com branco glacial |

### 🌙 2. Temas Dark Velvet Tinted (11 Opções)
| Flag | Nome | Background | Primary | Destaque |
| :--- | :--- | :--- | :--- | :--- |
| `-cappuccino` | **Dark Cappuccino** | `#181311` | `#D4A373` | Café expresso torrado e caramelo latte |
| `-wine` | **Dark Avermelhado Velvet** | `#120608` | `#E63946` | Vinho tinto carmim aveludado |
| `-midnight` | **Midnight Sapphire Blue** | `#090D16` | `#38BDF8` | Azul safira marinho estelar |
| `-dracula` | **Cyber Amethyst Twilight** | `#120D1C` | `#BD93F9` | Violeta profundo e ametista neon |
| `-amber` | **Amber Warm Dusk** | `#14110A` | `#F59E0B` | Âmbar crepuscular dourado |
| `-dark-emerald`| **Forest Emerald Night** | `#07140E` | `#10B981` | Verde floresta profunda e esmeralda |
| `-nordic` | **Nordic Arctic Slate** | `#0B1017` | `#22D3EE` | Ardósia polar e ciano glacial |
| `-tokyo` | **Tokyo Sunset Coral** | `#140B14` | `#FB7185` | Crepúsculo metropolitano e coral |
| `-matcha` | **Dark Matcha Obsidian** | `#0C100B` | `#84CC16` | Chá-verde matcha e obsidiana |
| `-copper` | **Dark Basalt Copper** | `#120E0A` | `#FB923C` | Basalto vulcânico e cobre metálico |
| `-ultraviolet` | **Dark Cosmic Ultraviolet**| `#080616` | `#818CF8` | Espaço cósmico e luz ultravioleta |

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
| `-terracotta` | **Light Tuscan Terracotta** | `#FDF8F6` | `#C2410C` | Linho artesanal e terracota toscana |
| `-azure` | **Light Alpine Sky Azure** | `#F0F9FF` | `#00A3FF` | Gelo glacial e azul celeste alpino |

---

## 🔤 Catálogo de 13 Fontes com Ligaduras

| Flag | Fonte | Autor / Fundição | Ligaduras | Badge |
| :--- | :--- | :--- | :---: | :--- |
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

---

## 🖥️ Uso via Linha de Comando (CLI)

```bash
# 🚀 Inicialização do Servidor & Dashboard
python3 scripts/theme_changer.py init

# 📊 Diagnóstico e Status
python3 scripts/theme_changer.py status

# 📋 Catálogo Geral
python3 scripts/theme_changer.py list

# 🎨 Troca de Temas
python3 scripts/theme_changer.py theme -matcha
python3 scripts/theme_changer.py theme -copper
python3 scripts/theme_changer.py theme -emerald

# 🔤 Troca de Fontes
python3 scripts/theme_changer.py font -jetbrains
python3 scripts/theme_changer.py font -victor
python3 scripts/theme_changer.py font -fira -code-only
```

---

## 🏛️ Arquitetura Técnica

O Theme Changer opera através de uma pipeline de tripla sincronização:

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

Para detalhes aprofundados sobre a injeção via WebSocket, consulte a documentação em **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.

---

## 💻 Central de Documentação Shell macOS Integrada

A interface frontend do **Theme Studio** integra uma seção dedicada no padrão **Apple Minimalist**, com layout de dois painéis (índice lateral navegável e painel central de conteúdo isolado), contendo guias de comandos, variações visuais e links oficiais dos utilitários de terminal instalados no macOS:

| Utilitário | Categoria | Repositório Oficial | Invocação Base |
| :--- | :--- | :--- | :--- |
| **bottom** | Monitor Gráfico em Rust | [ClementTsang/bottom](https://github.com/ClementTsang/bottom) | `btm` |
| **weathr** | Clima Procedural em ASCII | [veirt/weathr](https://github.com/veirt/weathr) | `weathr` |
| **lavat** | Simulador de Lâmpada de Lava | [AngelJumbo/lavat](https://github.com/AngelJumbo/lavat) | `lavat` |
| **pipes.sh** | Tubulações Animadas 3D | [pipeseroni/pipes.sh](https://github.com/pipeseroni/pipes.sh) | `pipes.sh` |
| **tty-clock** | Relógio Digital ncurses | [xorg62/tty-clock](https://github.com/xorg62/tty-clock) | `tty-clock` |
| **donut.c** | Toroide 3D Matemático | [a1k0n/donut](https://github.com/a1k0n/donut) | `donut` |
| **tarts** | Suíte de Screensavers em Rust | [levirs565/tarts](https://github.com/levirs565/tarts) | `tarts <efeito>` |
| **terminal-fireworks** | Física Balística de Partículas | [faeb/terminal-fireworks](https://github.com/faeb/terminal-fireworks) | `fireworks` |
| **nyancat** | Animação ANSI em Loop Cósmico | [klange/nyancat](https://github.com/klange/nyancat) | `nyancat` |
| **btop** | Monitor de Recursos Clássico | [aristocratos/btop](https://github.com/aristocratos/btop) | `btop` |
| **Combos Shell** | Setups Multi-Painel | [antigravity-theme-changer](https://github.com/MateusCelestinoProX/antigravity-theme-changer) | Multiplexing |

Todos os comandos possuem botão de **cópia em 1 clique** com feedback visual imediato e preservam integralmente as funções do customizador.

---

## 📄 Licença

Distribuído sob a licença MIT. Livre para uso pessoal e modificação.  
Desenvolvido com foco em excelência visual e engenharia de precisão para o ecossistema **Google Antigravity**.
