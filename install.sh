#!/usr/bin/env bash
# ==============================================================================
# Theme Changer & Font Center Studio — Google Antigravity Installer
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_SKILL_DIR="$HOME/.gemini/config/skills/theme-changer"
TARGET_SCRIPTS_DIR="$TARGET_SKILL_DIR/scripts"
TARGET_AGENTS_DIR="$HOME/.gemini/config/agents"

echo "🍏 Instalando Theme Changer Studio no Google Antigravity..."
echo "────────────────────────────────────────────────────────────"

# 1. Criar diretórios
mkdir -p "$TARGET_SCRIPTS_DIR"
mkdir -p "$TARGET_AGENTS_DIR"

# 2. Copiar scripts
echo "📦 Instalando scripts de controle e injeção CDP..."
cp "$SCRIPT_DIR/scripts/theme_changer.py" "$TARGET_SCRIPTS_DIR/theme_changer.py"
cp "$SCRIPT_DIR/scripts/apply_live_theme.js" "$TARGET_SCRIPTS_DIR/apply_live_theme.js"
cp "$SCRIPT_DIR/scripts/apply_font.js" "$TARGET_SCRIPTS_DIR/apply_font.js"
chmod +x "$TARGET_SCRIPTS_DIR/theme_changer.py"

# 3. Copiar especificação de Skill
echo "🧠 Registrando Skill no Google Antigravity..."
cp "$SCRIPT_DIR/skills/theme-changer/SKILL.md" "$TARGET_SKILL_DIR/SKILL.md"

# 4. Copiar definição do Agente
echo "🤖 Registrando Agente @theme-changer..."
cp "$SCRIPT_DIR/agents/theme-changer.md" "$TARGET_AGENTS_DIR/theme-changer.md"

echo "────────────────────────────────────────────────────────────"
echo "✨ Instalação concluída com sucesso!"
echo ""
echo "🚀 Para inicializar o Theme Studio & Font Center:"
echo "   python3 ~/.gemini/config/skills/theme-changer/scripts/theme_changer.py init"
echo ""
echo "💬 Ou simplesmente diga no chat do Antigravity:"
echo "   @theme-changer init"
echo "────────────────────────────────────────────────────────────"
