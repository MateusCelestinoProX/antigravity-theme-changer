# 💻 Central de Utilitários de Terminal & Screensavers Estéticos macOS

Guia técnico aprofundado dos 10 utilitários de linha de comando e suítes visuais instalados no ambiente macOS, com flags de comunidade, configurações de alta densidade gráfica, atalhos de controle em tempo real e combinações multi-painel para iTerm2, Kitty, WezTerm e Tmux.

---

## 📑 Sumário

1. [bottom (btm) — Monitor Gráfico em Rust](#1-bottom-btm--monitor-gráfico-em-rust)
2. [weathr — Previsão Meteorológica em Arte ASCII](#2-weathr--previsão-meteorológica-em-arte-ascii)
3. [lavat — Simulador Físico de Metaballs / Lava Lamp](#3-lavat--simulador-físico-de-metaballs--lava-lamp)
4. [pipes.sh — Tubulações Tridimensionais Procedurais](#4-pipessh--tubulações-tridimensionais-procedurais)
5. [tty-clock — Relógio Digital ncurses de Alta Precisão](#5-tty-clock--relógio-digital-ncurses-de-alta-precisão)
6. [donut.c — Toroide 3D Matemático Rotatório](#6-donutc--toroide-3d-matemático-rotatório)
7. [tarts — Suíte de Screensavers em Rust (Braille Canvas)](#7-tarts--suíte-de-screensavers-em-rust-braille-canvas)
8. [terminal-fireworks — Simulador Pirotécnico Balístico](#8-terminal-fireworks--simulador-pirotécnico-balístico)
9. [nyancat — Animação ANSI Clássica com Telemetria](#9-nyancat--animação-ansi-clássica-com-telemetria)
10. [fastfetch — Utilitário de Telemetria de Sistema em C](#10-fastfetch--utilitário-de-telemetria-de-sistema-em-c)
11. [Setups Multi-Painel Recomendados](#11-setups-multi-painel-recomendados)

---

## 1. bottom (btm) — Monitor Gráfico em Rust

- **Repositório Oficial**: [ClementTsang/bottom](https://github.com/ClementTsang/bottom)
- **Linguagem**: Rust
- **Invocação Base**: `btm`
- **Descrição**: Monitor de recursos do sistema multiplataforma e personalizável, com foco em extrema eficiência de memória e taxas de amostragem sub-segundo.

### Exemplos Práticos de Linha de Comando:
```bash
# Alta performance com widget de bateria (ideal para MacBook) e taxa de 500ms
btm --battery -a -r 500

# Modo básico minimalista sem gráficos contínuos (estilo htop ultra-limpo)
btm --basic

# Iniciar diretamente com a árvore hierárquica de processos em foco
btm --tree -d proc

# Agrupamento inteligente de processos por binário e contagem de threads ativas
btm --group_processes --get_threads

# Modo expandido com foco no módulo de processamento (CPU)
btm --expanded -d cpu

# Paleta térmica quente Gruvbox com atualização de 1s e medição em Celsius
btm -c -r 1000 --color gruvbox

# Paleta ártica fria Nord com escala temporal auto-oculta
btm -c -r 750 --color nord --autohide_time
```

### Controles & Atalhos em Tempo Real:
| Atalho | Ação |
| :--- | :--- |
| `Tab` / `Shift + Tab` | Alterna foco sequencial entre os painéis (CPU, RAM, Rede, Processos) |
| `e` | Expande o widget sob o cursor para tela inteira / Restaura |
| `t` | Alterna a tabela de processos em modo Árvore (Tree view) |
| `/` | Abre a barra de pesquisa e filtro de processos em tempo real |
| `+` / `-` | Zoom in / Zoom out na escala temporal dos gráficos |
| `dd` | Envia sinal de terminação (SIGKILL) ao processo selecionado |
| `?` | Exibe o modal integrado de ajuda rápida e atalhos |
| `q` | Encerra a execução e retorna ao shell |

---

## 2. weathr — Previsão Meteorológica em Arte ASCII

- **Repositório Oficial**: [veirt/weathr](https://github.com/veirt/weathr)
- **Linguagem**: Rust / C
- **Invocação Base**: `weathr`
- **Descrição**: Utilitário de previsão do tempo em tempo real com renderização visual animada procedural de fenômenos climáticos e integração com a Open-Meteo API.

### Exemplos Práticos de Linha de Comando:
```bash
# Noite de tempestade elétrica severa com relâmpagos e chuva
weathr -s thunderstorm -n

# Inverno noturno zen com neve contínua sem HUD de telemetria
weathr -s snow -n --hide-hud

# Céu limpo de outono com partículas de folhas ao vento
weathr -s clear -l

# Chuva suave contínua com unidades métricas (°C, km/h)
weathr -s rain --metric

# Tempestade com precipitação de granizo noturno
weathr -s thunderstorm-hail -n

# Cerração atmosférica densa sem identificação geográfica no cabeçalho
weathr -s fog --hide-location

# Garoa noturna silenciosa sem alertas sonoros
weathr -s drizzle -n --silent

# Detecção automática da sua localização geográfica via IP
weathr --auto-location --metric
```

---

## 3. lavat — Simulador Físico de Metaballs / Lava Lamp

- **Repositório Oficial**: [AngelJumbo/lavat](https://github.com/AngelJumbo/lavat)
- **Linguagem**: C
- **Invocação Base**: `lavat`
- **Descrição**: Simulação física de fluidos via metaballs em 2D com gradientes Truecolor, convecção térmica, dinâmica gravitacional e caracteres customizados.

### Exemplos Práticos de Linha de Comando:
```bash
# Gradiente violeta e ciano com convecção térmica por gravidade
lavat -g -G -c 8A2BE2 -k 00FFFF -s 6 -r 6 -b 14

# Fósforo verde terminal hacker com caracteres sustenido (#) e borda dupla
lavat -g -c 00FF41 -k 003B00 -F "#" -s 7 -b 15 -R 2

# Magma vulcânico térmico com bolhas de grande raio e contorno espesso
lavat -g -G -c FF3300 -k FFCC00 -s 4 -r 7 -b 12 -R 3

# Transição suave magenta e azul celeste a 16 metaballs ativas
lavat -g -c FF007F -k 00F0FF -s 5 -r 5 -b 16

# Monocromático puro OLED com contenção estrita nas bordas da janela
lavat -g -c FFFFFF -k 555555 -s 3 -r 8 -b 8 -C

# Ciano oceânico de alta velocidade e partículas menores
lavat -g -c 00F0FF -k 003366 -s 8 -r 4 -b 18 -R 1

# Veludo carmesim profundo e azul marinho com física de subida e descida
lavat -g -G -c E63946 -k 1D3557 -s 5 -r 6 -b 12

# Ciclo automático contínuo de paletas cromáticas em alta rotação
lavat -p 1 -s 8 -r 6 -b 18
```

### Controles & Atalhos em Tempo Real:
| Atalho | Ação |
| :--- | :--- |
| `+` / `-` | Aumenta ou diminui a velocidade da simulação física |
| `i` / `d` | Incrementa ou reduz o raio das metaballs |
| `Shift + I` / `Shift + D` | Aumenta ou reduz a espessura da linha de contorno |
| `m` / `l` | Adiciona ou remove o número de bolhas simultâneas |
| `c` / `k` | Alterna dinamicamente a cor da lava e a cor do contorno |
| `p` | Ativa/desativa o modo contínuo de rotação de paleta |
| `q` | Encerra a simulação e retorna ao terminal |

---

## 4. pipes.sh — Tubulações Tridimensionais Procedurais

- **Repositório Oficial**: [pipeseroni/pipes.sh](https://github.com/pipeseroni/pipes.sh)
- **Linguagem**: Bash / C
- **Invocação Base**: `pipes.sh`
- **Descrição**: O clássico protetor de tela de tubulações animadas com geração procedural de ramificações, curvas suaves e suporte a taxas fluidas de atualização.

### Exemplos Práticos de Linha de Comando:
```bash
# 5 fluxos multicolores a 85 FPS com spawn aleatório e retenção de caminho
pipes.sh -p 5 -t 1 -c 1 2 3 4 5 6 -f 85 -R -K

# Tubulações espessas retrô arcade com curvas amplas
pipes.sh -p 3 -t 3 -c 2 3 6 -s 10 -f 70 -R

# Tubos finos sem reset de tela em tons de azul e violeta
pipes.sh -p 6 -t 0 -c 4 5 6 -f 90 -s 14 -r 0 -R -K

# Densidade máxima com 8 tubos simultâneos a 100 FPS
pipes.sh -p 8 -t 4 -f 100 -s 8 -R

# Estilo trilhos de ferrovia (Railway) em branco puro
pipes.sh -p 2 -t 8 -c 7 -s 15 -f 60 -R

# Estilo articulado knobby com nós em tons de âmbar e ciano
pipes.sh -p 4 -t 9 -c 3 5 6 -s 12 -f 80 -R

# Traçado retilíneo com alta probabilidade de linhas retas contínuas
pipes.sh -p 4 -t 0 -c 2 -s 15 -f 75 -R -K

# Linhas finas duplas com reset programado a cada 3000 caracteres
pipes.sh -p 5 -t 2 -c 1 7 -f 65 -s 9 -r 3000
```

---

## 5. tty-clock — Relógio Digital ncurses de Alta Precisão

- **Repositório Oficial**: [xorg62/tty-clock](https://github.com/xorg62/tty-clock)
- **Linguagem**: C (ncurses)
- **Invocação Base**: `tty-clock`
- **Descrição**: Relógio digital elegante em arte ASCII com suporte a animação de ricochete, segundo plano, molduras geométricas e formatação strftime.

### Exemplos Práticos de Linha de Comando:
```bash
# Centralizado em ciano com segundos ativos e dois pontos piscantes
tty-clock -c -C 6 -s -B -b

# Moldura retangular sólida em tom âmbar brilhante
tty-clock -c -x -C 3 -s -b

# Modo screensaver com ricochete contínuo pelas bordas da janela
tty-clock -S -r -C 5 -s -B -b

# Data extensa personalizada em branco glacial
tty-clock -c -C 7 -s -f "%A, %d de %B de %Y" -b

# Formato civil 12 horas (AM/PM) em azul safira
tty-clock -c -t -C 4 -s -B

# Horário Universal Coordenado (UTC / Militar) com contorno em vermelho
tty-clock -c -u -C 1 -s -x

# Modo ultra-minimalista apenas com dígitos (sem rodapé de calendário)
tty-clock -c -C 2 -s -D -B -b
```

### Controles & Atalhos em Tempo Real:
| Atalho | Ação |
| :--- | :--- |
| `c` | Alterna a centralização na janela |
| `s` | Exibe ou oculta o contador de segundos |
| `t` | Alterna entre o formato militar 24h e o civil 12h (AM/PM) |
| `b` | Alterna a intensidade de brilho (Bold) dos dígitos |
| `r` | Ativa ou desativa o ricochete contínuo (Bounce) |
| `0` a `7` | Altera a cor do relógio instantaneamente |
| `q` | Fecha o aplicativo e retorna ao prompt |

---

## 6. donut.c — Toroide 3D Matemático Rotatório

- **Repositório Oficial**: [a1k0n/donut](https://github.com/a1k0n/donut)
- **Linguagem**: C
- **Invocação Base**: `donut`
- **Descrição**: O célebre algoritmo de Andy Sloane que calcula e projeta um toroide tridimensional rotativo iluminado com sombreamento vetorial direto em caracteres ASCII.

### Exemplos Práticos de Linha de Comando:
```bash
# Rotação balanceada clássica a ~33 FPS (30ms)
donut

# Modo turbo acelerado com 10ms de intervalo de cálculo
donut 10

# Rotação suave lenta a 60ms para uso discreto em segundo plano
donut 60

# Modo ultra-zen a 10 FPS (100ms) com impacto nulo em bateria
donut 100

# Animação cinemática a 60 FPS (15ms) para terminais modernos acelerados
donut 15

# Integração através do filtro Lolcat para gradiente contínuo
donut | lolcat

# Animação cromática com ondas de cores dinâmicas
donut 20 | lolcat -a -d 1
```

---

## 7. tarts — Suíte de Screensavers em Rust (Braille Canvas)

- **Repositório Oficial**: [levirs565/tarts](https://github.com/levirs565/tarts)
- **Linguagem**: Rust
- **Invocação Base**: `tarts <efeito>`
- **Descrição**: Suíte de screensavers de alta densidade gráfica utilizando os 8 pontos da matriz de caracteres Braille Unicode como pixels virtuais.

### Comandos de Destaque:
```bash
# Chuva digital estilo Matrix com renderização em Rust
tarts matrix

# Voo contínuo infinito sobre relevo topográfico tridimensional
tarts terrain

# Observatório cósmico com estrelas conectadas por constelações
tarts constellation

# Simulação biológica de bando com vetores de atração e coesão (Boids)
tarts boids
```

### Catálogo Completo dos 12 Efeitos:
| Efeito | Comando | Descrição |
| :--- | :--- | :--- |
| **Matrix Rain** | `tarts matrix` | Chuva de dados estilo Matrix de alta taxa de quadros |
| **3D Cube** | `tarts cube` | Cubo rotativo tridimensional com perspectiva em Braille |
| **Boids** | `tarts boids` | Simulação biológica de revoada de pássaros e cardumes |
| **Constelações**| `tarts constellation`| Céu estelar com linhas de gravidade interconectadas |
| **Plasma** | `tarts plasma` | Ondas fluidas de campo de energia oscilante |
| **Fogo** | `tarts fire` | Lareira com convecção de calor e brasas ascendentes |
| **Tubulações** | `tarts pipes` | Crescimento procedural de canos ramificados |
| **Game of Life**| `tarts life` | Autômato celular clássico com regras de John Conway |
| **Terreno 3D** | `tarts terrain` | Voo rasante sobre montanhas geradas por ruído Perlin |
| **Caranguejos** | `tarts crab` | Crustáceos animados caminhando pelo terminal |
| **Donut Rust** | `tarts donut` | Versão nativa do toroide acelerada em Rust |
| **Labirinto** | `tarts maze` | Geração procedural e resolução autônoma de labirintos |

---

## 8. terminal-fireworks — Simulador Pirotécnico Balístico

- **Repositório Oficial**: [faeb/terminal-fireworks](https://github.com/faeb/terminal-fireworks)
- **Linguagem**: C++ / Rust
- **Invocação Base**: `fireworks`
- **Descrição**: Simulação de espetáculo pirotécnico com cálculo de balística parabólica, detonação aérea e dispersão gravitacional de centelhas.

### Exemplos Práticos de Linha de Comando:
```bash
# Disparos de alta cadência (0.4s de intervalo) a 35 FPS
fireworks --gap 0.4 --framerate 35

# Gravidade reduzida com tempo de queima de fagulhas prolongado (0.8s)
fireworks --gravity 0.06 --decay-time 0.8 --gap 0.8

# Foguetes de grande altitude detonando próximo ao topo da janela
fireworks --explosion-height 0.15 --speed 1.3

# Alta propulsão com empuxo acelerado na decolagem
fireworks --speed 2.0 --delta-v 4.5

# Tempestade pirotécnica caótica a 60 FPS com rápida atração gravitacional
fireworks --gap 0.2 --framerate 60 --gravity 0.4

# Zero gravidade / Órbita com expansão esférica pura por 1.5s
fireworks --gravity 0.03 --decay-time 1.5 --gap 1.0

# Show relaxante e contemplativo com explosões no centro geométrico
fireworks --explosion-height 0.5 --speed 0.8 --gap 1.5
```

---

## 9. nyancat — Animação ANSI Clássica com Telemetria

- **Repositório Oficial**: [klange/nyancat](https://github.com/klange/nyancat)
- **Linguagem**: C
- **Invocação Base**: `nyancat`
- **Descrição**: A animação clássica em 256 cores ANSI com arco-íris estelar e contador regressivo/progressivo de permanência cósmica.

### Exemplos Práticos de Linha de Comando:
```bash
# Voo clássico padrão com contador de tempo ativo
nyancat

# Inicialização com a vinheta clássica de apresentação
nyancat -i

# Modo minimalista estético ocultando a barra de tempo
nyancat -n

# Modo silencioso absoluto (sem campainhas de terminal)
nyancat -n -s

# Fixação da área útil em 80 colunas por 24 linhas (padrão VT100)
nyancat -w 80 -h 24

# Execução temporizada em 300 quadros (~10 segundos) com saída automática
nyancat -f 300 -n -s

# Limitação em 500 quadros e retorno automático ao shell
nyancat -f 500
```

---

## 10. fastfetch — Utilitário de Telemetria de Sistema em C

- **Repositório Oficial**: [fastfetch-cli/fastfetch](https://github.com/fastfetch-cli/fastfetch)
- **Linguagem**: C (Alta Performance)
- **Invocação Base**: `fastfetch`
- **Descrição**: Utilitário moderno e ultra-rápido de telemetria em C para exibição estética de informações do sistema operacional e hardware, sucessor veloz do Neofetch com suporte a logos ASCII nativos e presets estruturados em JSONC.

### Exemplos Práticos de Linha de Comando:
```bash
# Execução padrão completa com logotipo oficial do macOS e resumo de hardware
fastfetch

# Preset clássico no consagrado formato Neofetch com blocos de paleta cromática
fastfetch -c neofetch

# Modo Paleofetch ultra-limpo focado na telemetria essencial de CPU, GPU, Uptime e Bateria
fastfetch -c paleofetch

# Telemetria profunda de engenharia com todos os módulos de hardware ativos
fastfetch -c all

# Versão compacta com logo ASCII reduzido (ideal para janelas de terminal menores ou sidebars)
fastfetch --logo-type small

# Seleção customizada em linha única focando apenas nos componentes essenciais
fastfetch --structure OS:Host:Kernel:Uptime:CPU:GPU:Memory:Disk

# Modo minimalista sem logotipo gráfico (puramente os dados alinhados à esquerda)
fastfetch --logo none

# Exportação completa de todos os dados do computador em formato JSON estruturado
fastfetch --format json
```

### Comandos de Inspeção & Ajuda:
| Comando | Descrição |
| :--- | :--- |
| `fastfetch -h` | Exibe todas as opções de linha de comando e módulos suportados |
| `fastfetch --list-presets` | Lista todos os presets oficiais integrados (paleofetch, neofetch, all, ci, etc.) |
| `fastfetch --list-logos` | Lista todos os logotipos de sistemas operacionais e distribuições suportados |
| `fastfetch --gen-config` | Gera o arquivo de configuração customizável em `~/.config/fastfetch/config.jsonc` |

---

## 11. Setups Multi-Painel Recomendados

Configurações otimizadas para dividir o emulador de terminal (iTerm2, WezTerm, Kitty ou Tmux) em 2 ou 3 divisões simultâneas, harmonizando telemetria, arte matemática e relógio digital:

### 🌟 Setup 1: Telemetria & Clima Noturno
- **Painel Superior**: `btm --battery -r 500`
- **Painel Inferior Esquerdo**: `weathr -s thunderstorm -n`
- **Painel Inferior Direito**: `tty-clock -c -C 6 -s -B -b`

### 🌀 Setup 2: Física de Partículas & Geometria 3D
- **Painel Superior Esquerdo**: `tarts matrix`
- **Painel Superior Direito**: `donut`
- **Painel Inferior**: `fireworks --gap 0.5`

### 🕹️ Setup 3: Retrô Nostálgico & Fluidos
- **Painel Superior Esquerdo**: `nyancat -n`
- **Painel Superior Direito**: `pipes.sh -p 5 -t 1 -c 1 2 3 4 5 6 -f 85 -R -K`
- **Painel Inferior**: `lavat -g -G -c FF007F -k 00F0FF -s 5 -r 6 -b 14`

### 🖤 Setup 4: Hacker Monocromático Puro
- **Painel Superior**: `tty-clock -c -C 7 -s -x -b`
- **Painel Inferior Esquerdo**: `lavat -g -c FFFFFF -k 555555 -s 3 -r 8 -b 8 -C`
- **Painel Inferior Direito**: `btm --basic`

### 🌌 Setup 5: Observatório Cósmico & Gravidade Zero
- **Painel Superior**: `tarts constellation`
- **Painel Inferior Esquerdo**: `fireworks --gravity 0.03 --decay-time 1.5 --gap 1.0`
- **Painel Inferior Direito**: `weathr -s clear -n --hide-hud`

### ⚡ Setup 6: Suíte de Alta Performance Rust
- **Painel Superior**: `btm --tree -d proc`
- **Painel Inferior Esquerdo**: `tarts plasma`
- **Painel Inferior Direito**: `tarts terrain`

---

*Documentação mantida pela equipe do Antigravity Theme Studio.*
