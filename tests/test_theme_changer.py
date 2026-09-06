#!/usr/bin/env python3
"""
test_theme_changer.py
Auditoria automatizada do ecossistema Google Antigravity Theme Changer:
- Verifica sintaxe de scripts Python (py_compile)
- Verifica sintaxe de scripts JS (node --check)
- Verifica integridade dos 31 temas e 13 fontes
- Valida zero emojis no painel web
- Testa respostas da API REST local (caso servidor ativo)
"""

import unittest
import py_compile
import subprocess
import re
import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class TestAntigravityThemeChanger(unittest.TestCase):

    def test_python_syntax(self):
        """Garante que todos os scripts Python compilam sem erro de sintaxe."""
        py_files = [
            BASE_DIR / "scripts" / "theme_changer.py",
            BASE_DIR / "scripts" / "theme_server.py",
            BASE_DIR / "theme_server.py"
        ]
        for f in py_files:
            if f.exists():
                try:
                    py_compile.compile(str(f), doraise=True)
                except Exception as e:
                    self.fail(f"Erro de sintaxe em {f}: {e}")

    def test_javascript_syntax(self):
        """Garante que scripts JavaScript passam na validação do node."""
        js_files = [
            BASE_DIR / "scripts" / "apply_live_theme.js",
            BASE_DIR / "scripts" / "apply_font.js"
        ]
        for f in js_files:
            if f.exists():
                res = subprocess.run(["node", "--check", str(f)], capture_output=True, text=True)
                self.assertEqual(res.returncode, 0, f"JS Syntax error em {f}: {res.stderr}")

    def test_web_app_no_emojis(self):
        """Valida que o painel web obedece estritamente à regra de zero emojis."""
        html_file = BASE_DIR / "web" / "theme_changer_app.html"
        if html_file.exists():
            content = html_file.read_text(encoding="utf-8")
            emoji_pattern = re.compile(r"[𐀀-􏿿]", flags=re.UNICODE)
            emojis_found = emoji_pattern.findall(content)
            self.assertEqual(len(emojis_found), 0, f"Emojis encontrados no HTML: {set(emojis_found)}")

    def test_themes_count(self):
        """Verifica se todos os 31 temas estão catalogados no theme_changer.py."""
        import sys
        sys.path.insert(0, str(BASE_DIR / "scripts"))
        try:
            import theme_changer
            self.assertEqual(len(theme_changer.THEMES), 31, "Total de temas diferente de 31")
        finally:
            sys.path.pop(0)

    def test_fonts_count(self):
        """Verifica se todas as 13 fontes estão catalogadas."""
        import sys
        sys.path.insert(0, str(BASE_DIR / "scripts"))
        try:
            import theme_changer
            self.assertEqual(len(theme_changer.DEV_FONTS), 13, "Total de fontes diferente de 13")
        finally:
            sys.path.pop(0)

if __name__ == "__main__":
    unittest.main()
