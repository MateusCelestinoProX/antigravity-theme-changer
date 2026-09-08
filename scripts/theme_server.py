#!/usr/bin/env python3
"""
Theme Changer & Font Center Server — Google Antigravity
Servidor HTTP local multithread Dual-Stack (IPv4 + IPv6) com suporte a PNA e DevTools.
"""

import http.server
import socket
import socketserver
import urllib.parse
import json
import os
import sys
import importlib
import subprocess
# Garantir PATH para Homebrew e Node.js no macOS
default_paths = ["/opt/homebrew/bin", "/opt/homebrew/sbin", "/usr/local/bin"]
cur_path = os.environ.get("PATH", "")
for p in default_paths:
    if p not in cur_path and os.path.exists(p):
        cur_path = f"{p}:{cur_path}"
os.environ["PATH"] = cur_path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR / "scripts"
if not SCRIPTS_DIR.exists():
    SCRIPTS_DIR = Path.home() / ".gemini/config/skills/theme-changer/scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(BASE_DIR))

try:
    import theme_changer
except ImportError:
    theme_changer = None

PORT = 48123

class ThemeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        global theme_changer
        parsed = urllib.parse.urlparse(self.path)

        # Rota raiz: redireciona para a interface web
        if parsed.path in ["", "/", "/index.html"]:
            self.send_response(302)
            self.send_header("Location", "/theme_changer_app.html")
            self.end_headers()
            return

        # Rota Ping rápida para handshake e healthcheck
        if parsed.path == "/api/ping":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "port": PORT}).encode("utf-8"))
            return

        # Servir a página da aplicação
        if parsed.path == "/theme_changer_app.html":
            candidate_paths = [
                BASE_DIR / "web" / "theme_changer_app.html",
                BASE_DIR.parent / "web" / "theme_changer_app.html",
                BASE_DIR / "theme_changer_app.html",
                Path.home() / ".gemini/config/skills/theme-changer/web/theme_changer_app.html",
                Path.home() / ".gemini/config/skills/theme-changer/theme_changer_app.html",
                Path.home() / ".gemini/antigravity/scratch/antigravity-theme-changer/web/theme_changer_app.html",
            ]
            for p in candidate_paths:
                if p.exists():
                    try:
                        content = p.read_bytes()
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.send_header("Content-Length", str(len(content)))
                        self.send_cors_headers()
                        self.end_headers()
                        self.wfile.write(content)
                        return
                    except Exception:
                        pass

        # API: Aplicar Tema
        if parsed.path == "/api/set-theme":
            try:
                if theme_changer:
                    importlib.reload(theme_changer)
                else:
                    import theme_changer

                params = urllib.parse.parse_qs(parsed.query)
                target = params.get("theme", [""])[0].lower()
                key = theme_changer.parse_target_theme([target])
                if not key:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": f"Tema '{target}' não reconhecido"}).encode("utf-8"))
                    return

                ok1 = theme_changer.update_config_json(key)
                ok2 = theme_changer.update_pbtxt(key)
                try:
                    theme_changer.apply_live(key)
                except Exception as live_err:
                    print("[i] Aviso na sincronização ao vivo:", live_err)
                t = theme_changer.THEMES.get(key, {})

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                resp = {
                    "success": True,
                    "theme": key,
                    "name": t.get("name", key),
                    "seeds": t.get("seeds", {}),
                    "theme_mode": t.get("theme_mode", "THEME_MODE_LIGHT"),
                    "message": f"Tema {t.get('name', key)} aplicado com sucesso no Google Antigravity!"
                }
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
                return

        # API: Obter Tema Atual
        elif parsed.path == "/api/current-theme":
            try:
                if theme_changer:
                    importlib.reload(theme_changer)
                else:
                    import theme_changer

                config_path = Path.home() / ".gemini/config/config.json"
                cur_key = "green"
                if config_path.exists():
                    try:
                        with open(config_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            bg = data.get("userSettings", {}).get("customThemeSeedsDark", {}).get("background", "").lower()
                            pri = data.get("userSettings", {}).get("customThemeSeedsDark", {}).get("primary", "").lower()
                            for k, v in theme_changer.THEMES.items():
                                if v["seeds"]["background"].lower() == bg and v["seeds"]["primary"].lower() == pri:
                                    cur_key = k
                                    break
                    except Exception:
                        pass

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                cur_theme = theme_changer.THEMES.get(cur_key, theme_changer.THEMES.get("green", {}))
                self.wfile.write(json.dumps({"current": cur_key, "theme": cur_theme}).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"current": "green", "error": str(e)}).encode("utf-8"))
                return

        # API: Aplicar Fonte
        elif parsed.path == "/api/set-font":
            try:
                params = urllib.parse.parse_qs(parsed.query)
                font_target = params.get("font", ["jetbrains"])[0].lower().replace("-", "")
                scope = params.get("scope", ["full"])[0].lower()
                valid_fonts = {
                    "jetbrains": "JetBrains Mono",
                    "fira": "Fira Code",
                    "cascadia": "Cascadia Code",
                    "victor": "Victor Mono",
                    "source": "Source Code Pro",
                    "inconsolata": "Inconsolata",
                    "hack": "Hack Font",
                    "ubuntu": "Ubuntu Mono",
                    "space": "Space Mono",
                    "geist": "Geist Mono",
                    "ibm": "IBM Plex Mono",
                    "dm": "DM Mono",
                    "system": "System Default (SF Pro)"
                }
                if font_target not in valid_fonts:
                    for k in valid_fonts:
                        if k in font_target:
                            font_target = k
                            break
                    else:
                        font_target = "jetbrains"

                candidate_scripts = [
                    SCRIPTS_DIR / "apply_font.js",
                    BASE_DIR / "scripts" / "apply_font.js",
                    Path.home() / ".gemini/config/skills/theme-changer/scripts/apply_font.js",
                    Path.home() / ".gemini/antigravity/scratch/antigravity-theme-changer/scripts/apply_font.js"
                ]
                output = ""
                for s in candidate_scripts:
                    if s.exists():
                        try:
                            res = subprocess.run(["node", str(s), font_target, scope], capture_output=True, text=True, timeout=5)
                            output = res.stdout.strip()
                        except Exception as font_err:
                            output = str(font_err)
                        break

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                resp = {
                    "success": True,
                    "font": font_target,
                    "scope": scope,
                    "name": valid_fonts[font_target],
                    "message": f"Fonte {valid_fonts[font_target]} aplicada com sucesso no Google Antigravity!",
                    "output": output
                }
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
                return

        # API: Obter Fonte Atual
        elif parsed.path == "/api/current-font":
            try:
                font_state_file = Path.home() / ".gemini/config/active_font.json"
                cur_font = "jetbrains"
                cur_name = "JetBrains Mono"
                cur_scope = "full"
                if font_state_file.exists():
                    try:
                        with open(font_state_file, "r", encoding="utf-8") as f:
                            d = json.load(f)
                            cur_font = d.get("font", "jetbrains")
                            cur_name = d.get("name", "JetBrains Mono")
                            cur_scope = d.get("scope", "full")
                    except Exception:
                        pass

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"current": cur_font, "name": cur_name, "scope": cur_scope}).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"current": "jetbrains", "name": "JetBrains Mono", "scope": "full", "error": str(e)}).encode("utf-8"))
                return

        # API: Status do Servidor e Configurações Ativas
        elif parsed.path == "/api/status":
            try:
                if theme_changer:
                    importlib.reload(theme_changer)
                else:
                    import theme_changer

                # Tema
                config_path = Path.home() / ".gemini/config/config.json"
                cur_key = "green"
                theme_mode = "THEME_MODE_DARK"
                bg = ""
                pri = ""
                if config_path.exists():
                    try:
                        with open(config_path, "r", encoding="utf-8") as f:
                            cfg = json.load(f)
                            theme_mode = cfg.get("userSettings", {}).get("themeMode", "THEME_MODE_DARK")
                            seeds = cfg.get("userSettings", {}).get("customThemeSeedsDark" if "DARK" in theme_mode else "customThemeSeedsLight", {})
                            bg = seeds.get("background", "")
                            pri = seeds.get("primary", "")
                            for k, v in theme_changer.THEMES.items():
                                if v["seeds"]["background"].lower() == bg.lower() and v["seeds"]["primary"].lower() == pri.lower():
                                    cur_key = k
                                    break
                    except Exception:
                        pass
                cur_theme = theme_changer.THEMES.get(cur_key, {})

                # Fonte
                font_state_file = Path.home() / ".gemini/config/active_font.json"
                cur_font = "jetbrains"
                cur_name = "JetBrains Mono"
                cur_scope = "full"
                if font_state_file.exists():
                    try:
                        with open(font_state_file, "r", encoding="utf-8") as f:
                            d = json.load(f)
                            cur_font = d.get("font", "jetbrains")
                            cur_name = d.get("name", "JetBrains Mono")
                            cur_scope = d.get("scope", "full")
                    except Exception:
                        pass

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                resp = {
                    "status": "online",
                    "port": PORT,
                    "dashboard_url": f"http://localhost:{PORT}/theme_changer_app.html",
                    "current_theme": cur_key,
                    "theme_mode": theme_mode,
                    "theme": cur_theme,
                    "current_font": cur_font,
                    "font_name": cur_name,
                    "font_scope": cur_scope
                }
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode("utf-8"))
                return

        # API: Catálogo Geral de Temas e Fontes
        elif parsed.path == "/api/list":
            try:
                if theme_changer:
                    importlib.reload(theme_changer)
                else:
                    import theme_changer

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                resp = {
                    "total_themes": len(theme_changer.THEMES),
                    "total_fonts": len(theme_changer.FONTS),
                    "themes": theme_changer.THEMES,
                    "fonts": theme_changer.FONTS
                }
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
                return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
        data = {}
        if body:
            try:
                data = json.loads(body)
            except Exception:
                pass

        params = urllib.parse.parse_qs(parsed.query)
        for k, v in params.items():
            if k not in data:
                data[k] = v[0]

        if parsed.path == "/api/set-theme":
            theme_val = data.get("theme", "")
            self.path = f"/api/set-theme?theme={urllib.parse.quote(str(theme_val))}"
            return self.do_GET()
        elif parsed.path == "/api/set-font":
            font_val = data.get("font", "jetbrains")
            scope_val = data.get("scope", "full")
            self.path = f"/api/set-font?font={urllib.parse.quote(str(font_val))}&scope={urllib.parse.quote(str(scope_val))}"
            return self.do_GET()
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Rota POST não encontrada"}).encode("utf-8"))

def create_server(port=PORT):
    # 1. Tenta criar servidor Dual-Stack (IPv4 + IPv6 simultâneo com IPV6_V6ONLY=0)
    try:
        class DualStackServer(http.server.ThreadingHTTPServer):
            daemon_threads = True
            allow_reuse_address = True
            address_family = socket.AF_INET6

            def server_bind(self):
                try:
                    self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
                except Exception:
                    pass
                super().server_bind()

        return DualStackServer(("::", port), ThemeHandler)
    except Exception:
        pass

    # 2. Fallback resiliente para IPv4 padrão
    class IPv4Server(http.server.ThreadingHTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    return IPv4Server(("", port), ThemeHandler)

def run():
    with create_server(PORT) as httpd:
        print(f"🍏 Theme Studio Server running on http://localhost:{PORT}/theme_changer_app.html")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
