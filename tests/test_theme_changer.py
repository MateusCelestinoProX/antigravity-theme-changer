#!/usr/bin/env python3
"""
test_theme_changer.py
Auditoria automatizada do ecossistema Google Antigravity Theme Changer:
- Verifica sintaxe de scripts Python (py_compile)
- Verifica sintaxe de scripts JS (node --check)
- Verifica integridade dos 31 temas e 13 fontes
- Valida zero emojis no painel web
- Valida os 11 tópicos e utilitários shell no HTML
"""

import unittest
import py_compile
import subprocess
import re
import json
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
        self.assertTrue(html_file.exists(), "theme_changer_app.html não encontrado em web/")
        content = html_file.read_text(encoding="utf-8")
        emoji_pattern = re.compile(r"[\U00010000-\U0010ffff]", flags=re.UNICODE)
        emojis_found = emoji_pattern.findall(content)
        self.assertEqual(len(emojis_found), 0, f"Emojis encontrados no HTML: {set(emojis_found)}")

    def test_themes_count_and_categories(self):
        """Verifica se todos os 31 temas estão catalogados nas 3 categorias."""
        import sys
        sys.path.insert(0, str(BASE_DIR / "scripts"))
        try:
            import theme_changer
            self.assertEqual(len(theme_changer.THEMES), 31, "Total de temas diferente de 31")
            
            categories = {"full": 0, "dark": 0, "light": 0}
            for k, v in theme_changer.THEMES.items():
                cat = v.get("category", "")
                if cat in categories:
                    categories[cat] += 1
            
            self.assertEqual(categories["full"], 6, "Categoria Full deve ter 6 temas")
            self.assertEqual(categories["dark"], 11, "Categoria Dark deve ter 11 temas")
            self.assertEqual(categories["light"], 14, "Categoria Light deve ter 14 temas")
        finally:
            sys.path.pop(0)

    def test_fonts_count(self):
        """Verifica se todas as 13 fontes estão catalogadas."""
        import sys
        sys.path.insert(0, str(BASE_DIR / "scripts"))
        try:
            import theme_changer
            self.assertEqual(len(theme_changer.FONTS), 13, "Total de fontes diferente de 13")
        finally:
            sys.path.pop(0)

    def test_shell_utilities_catalog_in_html(self):
        """Valida que todos os 11 tópicos e utilitários shell estão no HTML."""
        html_file = BASE_DIR / "web" / "theme_changer_app.html"
        content = html_file.read_text(encoding="utf-8")
        expected_utilities = [
            "bottom",
            "weathr",
            "lavat",
            "pipes",
            "ttyclock",
            "donut",
            "tarts",
            "fireworks",
            "nyancat",
            "btop",
            "combos"
        ]
        for util in expected_utilities:
            self.assertIn(f'id: "{util}"', content, f"Utilitário '{util}' não encontrado no DOCS_DATA do HTML")

if __name__ == "__main__":
    unittest.main()
