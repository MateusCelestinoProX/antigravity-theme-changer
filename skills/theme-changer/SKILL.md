---
name: theme-changer
description: >
  Controla e alterna instantaneamente os temas visuais do Google Antigravity. Use sempre que o usuário mencionar
  troca de tema, "theme -green", "theme -red", "theme -white", "theme -emerald", "theme -sapphire", "theme -ruby",
  "theme -lavender", "theme -sunburst", "theme -latte", "theme -rose", "theme -teal", "@theme-changer" ou quiser
  alterar as cores da interface do Antigravity.
---

# Skill: Theme Changer — Google Antigravity

### 🚀 Inicialização Completa em 1 Comando:
```bash
python3 /Users/mcp/.gemini/config/skills/theme-changer/scripts/theme_changer.py init
```
Inicia o servidor interno multithread e abre automaticamente o **Theme Studio & Font Center** no navegador padrão.

Permite alternar instantaneamente entre a suíte completa de temas e fontes no Google Antigravity:

### ⚡ Temas Full Monocromáticos (6 Opções):
1. **Verde Matrix (`-green`)**: Fundo preto abissal (#050B05) com verde fósforo CRT (#00FF41).
2. **Vermelho Neon Cyberpunk (`-red`)**: Fundo carmesim (#0A0002) com tipografia laser neon (#FF003C / #FF2A55).
3. **Full Tron Electric Cyan (`-cyan`)**: Fundo azul abissal (#040B14) com ciano laser neon (#00F0FF).
4. **Full Acid Cyber Yellow (`-yellow`)**: Fundo preto grafite (#0E0D03) com amarelo ácido neon (#FFE600).
5. **Full Synthwave Magenta (`-magenta`)**: Fundo violeta abissal (#100312) com magenta neon brilhante (#FF007F).
6. **Full OLED Pure Mono (`-monochrome`)**: Fundo preto absoluto OLED (#000000) com branco glacial (#FFFFFF).

### 🌙 Modo Escuro Velvet Tinted (11 Opções):
7. **Dark Cappuccino (`-cappuccino`)**: Fundo café expresso (#181311) com caramelo latte e torrado (#D4A373).
8. **Dark Avermelhado Velvet (`-wine`)**: Fundo vinho veludo (#120608) com carmesim aveludado (#E63946).
9. **Midnight Sapphire Blue (`-midnight`)**: Fundo safira abissal (#090D16) com azul safira (#38BDF8).
10. **Cyber Amethyst Twilight (`-dracula`)**: Fundo violeta escuro (#120D1C) com ametista néon (#BD93F9).
11. **Amber Warm Dusk (`-amber`)**: Fundo crepúsculo (#14110A) com âmbar dourado solar (#F59E0B).
12. **Forest Emerald Night (`-dark-emerald`)**: Fundo verde floresta profunda (#07140E) com esmeralda nórdica (#10B981).
13. **Nordic Arctic Slate (`-nordic`)**: Fundo ardósia polar (#0B1017) com ciano glacial (#22D3EE).
14. **Tokyo Sunset Coral (`-tokyo`)**: Fundo crepúsculo metropolitano (#140B14) com coral crepúsculo (#FB7185).
15. **Dark Matcha Obsidian (`-matcha`)**: Fundo chá-verde obsidiana (#0C100B) com verde matcha japonês (#84CC16).
16. **Dark Basalt Copper (`-copper`)**: Fundo basalto vulcânico (#120E0A) com cobre incandescente (#FB923C).
17. **Dark Cosmic Ultraviolet (`-ultraviolet`)**: Fundo espaço cósmico (#080616) com luz ultravioleta & índigo (#818CF8).

### ☀️ Modo Claro Luminary + Cor Secundária (13 Opções):
18. **Pure Clean White (`-white`)**: Fundo puro branco (#FFFFFF) com tipografia cinza ardósia (#111827).
19. **Light Emerald (`-emerald`)**: Base clara refrescante com cor secundária em verde esmeralda (#059669).
20. **Light Sapphire (`-sapphire`)**: Base clara cristalina com cor secundária em azul safira executivo (#0284C7).
21. **Light Ruby (`-ruby`)**: Base clara energizante com cor secundária em vermelho rubi contemporâneo (#E11D48).
22. **Light Lavender (`-lavender`)**: Base clara suave com cor secundária em violeta ametista real (#7C3AED).
23. **Light Amber Sunburst (`-sunburst`)**: Base clara acolhedora com cor secundária em âmbar solar (#D97706).
24. **Light Coffee Latte (`-latte`)**: Base marfim suave com cor secundária em café latte e caramelo (#9A3412).
25. **Light Rosé Wine (`-rose`)**: Base clara aveludada com cor secundária em rosé champagne (#BE123C).
26. **Light Ocean Teal (`-teal`)**: Base clara arejada com cor secundária em teal oceânico cristalino (#0D9488).
27. **Light Coral Peach (`-coral`)**: Base pêssego suave com cor secundária em coral vibrante (#EA580C).
28. **Light Electric Indigo (`-indigo`)**: Base linho com cor secundária em índigo elétrico (#4F46E5).
29. **Light Pistachio Gelato (`-pistachio`)**: Base creme marfim com cor secundária em pistache siciliano (#65A30D).
30. **Light Tuscan Terracotta (`-terracotta`)**: Base linho toscano com cor secundária em terracota queimada (#C2410C).
31. **Light Alpine Sky Azure (`-azure`)**: Base gelo alpino com cor secundária em azul celeste puro (#00A3FF).

### 🔤 Fontes de Programação com Ligaduras (13 Fontes):
1. **JetBrains Mono (`-jetbrains`)**: Ligaduras de código profissionais da JetBrains.
2. **Fira Code (`-fira`)**: A clássica e pioneira das ligaduras de programação.
3. **Cascadia Code (`-cascadia`)**: A fonte oficial do Windows Terminal e VS Code.
4. **Victor Mono (`-victor`)**: Elegância cursiva em itálico com ligaduras completas.
5. **Source Code Pro (`-source`)**: Alta clareza e equilíbrio visual da Adobe.
6. **Inconsolata (`-inconsolata`)**: Monospace condensada de alta precisão de Raph Levien.
7. **Hack (`-hack`)**: Projetada para legibilidade máxima em terminais.
8. **Ubuntu Mono (`-ubuntu`)**: Estilo clássico humanista do terminal Ubuntu.
9. **Space Mono (`-space`)**: Geométrica brutalista/cyberpunk da Colophon/Google.
10. **Geist Mono (`-geist`)**: Minimalismo cirúrgico do ecossistema Vercel.
11. **IBM Plex Mono (`-ibm`)**: Clássico industrial moderno da IBM.
12. **DM Mono (`-dm`)**: Geométrica contemporânea da Google.
13. **System Default (`-system`)**: Restaura o padrão SF Pro / Apple do macOS.

## Como Executar a Troca

Para trocar o tema imediatamente, execute via terminal:

```bash
python3 /Users/mcp/.gemini/config/skills/theme-changer/scripts/theme_changer.py theme -emerald
```

Para trocar a fonte imediatamente:

```bash
python3 /Users/mcp/.gemini/config/skills/theme-changer/scripts/theme_changer.py font -victor
```

## Como a Mágica Acontece (Arquitetura)

O tema do Google Antigravity é controlado por duas configurações sincronizadas:
- `~/.gemini/config/config.json`: armazena `userSettings.customThemeSeedsDark`, `userSettings.customThemeSeedsLight` e `userSettings.themeMode`.
- `~/.gemini/antigravity/antigravity_state.pbtxt`: armazena a estrutura protobuf `jetbox_state_pb.CustomThemeSeeds` que alimenta diretamente o `language_server` do Antigravity.

O script `theme_changer.py` altera ambos os arquivos de forma atômica e coerente.
