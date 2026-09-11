#!/usr/bin/env python3
"""
tests/test_e2e_portability.py
Suíte de Testes Ponta a Ponta (E2E) para Máxima Portabilidade e Documentação:
1. Portabilidade de Código e Dependências (Zero dependências externas pip, stdlib pura)
2. Integridade dos Scripts Executáveis e Sintaxe do Instalador (bash -n install.sh)
3. Auditoria de Documentação (Links internos, consistência de rotas, temas e fontes)
4. Teste Funcional E2E do Servidor Dual-Stack & API REST do Scheduler e WebGL
"""

import unittest
import json
import urllib.request
import urllib.parse
import threading
import time
import socket
import subprocess
import os
import sys
import base64
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "scripts"))

import theme_server
import theme_changer

class TestE2EPortabilityAndDocs(unittest.TestCase):

    def test_01_pure_standard_library_portability(self):
        """Garante que nenhum script do projeto exige pacotes pip de terceiros."""
        allowed_stdlib = {
            "http", "socket", "socketserver", "urllib", "json", "os", "sys",
            "importlib", "subprocess", "re", "shutil", "time", "math",
            "threading", "uuid", "pathlib", "unittest", "py_compile", "base64",
            "webbrowser", "theme_changer", "theme_server"
        }
        py_files = [
            BASE_DIR / "scripts" / "theme_changer.py",
            BASE_DIR / "scripts" / "theme_server.py",
            BASE_DIR / "theme_server.py",
            BASE_DIR / "tests" / "test_theme_changer.py",
            BASE_DIR / "tests" / "test_e2e_portability.py"
        ]
        for pf in py_files:
            if not pf.exists():
                continue
            txt = pf.read_text(encoding="utf-8")
            for line in txt.splitlines():
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    parts = line.split()
                    mod = parts[1].split(".")[0]
                    self.assertIn(
                        mod, allowed_stdlib,
                        f"Módulo '{mod}' em {pf.name} não é standard library ou interno. Violação de portabilidade!"
                    )

    def test_02_installer_syntax_and_executables(self):
        """Garante que o script install.sh tem sintaxe bash válida e permissões corretas."""
        install_script = BASE_DIR / "install.sh"
        self.assertTrue(install_script.exists(), "install.sh não encontrado")
        res = subprocess.run(["bash", "-n", str(install_script)], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Erro de sintaxe no install.sh: {res.stderr}")

        # Permissões executáveis
        executables = [
            BASE_DIR / "install.sh",
            BASE_DIR / "scripts" / "theme_changer.py",
            BASE_DIR / "scripts" / "theme_server.py",
            BASE_DIR / "theme_server.py"
        ]
        for exe in executables:
            if exe.exists():
                mode = exe.stat().st_mode
                is_exec = bool(mode & 0o111)
                self.assertTrue(is_exec, f"Arquivo {exe.name} não possui permissão de execução")

    def test_03_documentation_links_and_files_integrity(self):
        """Valida que todos os manuais técnicos citados no README.md existem fisicamente."""
        readme = BASE_DIR / "README.md"
        self.assertTrue(readme.exists(), "README.md não encontrado")
        readme_content = readme.read_text(encoding="utf-8")

        required_docs = [
            "docs/AGENT_GUIDE.md",
            "docs/ARCHITECTURE.md",
            "docs/API_REFERENCE.md",
            "docs/SHELL_UTILITIES.md",
            "skills/theme-changer/SKILL.md",
            "agents/theme-changer.md",
            "install.sh",
            "LICENSE"
        ]
        for doc in required_docs:
            doc_path = BASE_DIR / doc
            self.assertTrue(doc_path.exists(), f"Documento referenciado '{doc}' não encontrado no disco")
            self.assertIn(doc, readme_content, f"Referência a '{doc}' ausente no README.md")

    def test_04_documentation_api_routes_coverage(self):
        """Garante que todas as rotas documentadas em API_REFERENCE.md existem no theme_server.py."""
        api_ref = BASE_DIR / "docs" / "API_REFERENCE.md"
        self.assertTrue(api_ref.exists())
        ref_text = api_ref.read_text(encoding="utf-8")

        server_code = (BASE_DIR / "theme_server.py").read_text(encoding="utf-8")
        routes_to_check = [
            "/api/ping",
            "/api/status",
            "/api/list",
            "/api/current-theme",
            "/api/current-font",
            "/api/set-theme",
            "/api/set-font",
            "/api/scheduler/queue",
            "/api/scheduler/schedule",
            "/api/scheduler/cancel",
            "/api/scheduler/dispatch-now",
            "/api/scheduler/toggle-agent-state",
            "/api/scheduler/conversations",
            "/api/scheduler/projects",
            "/api/scheduler/upload-context",
            "/api/agents",
            "/api/agents/save",
            "/api/mcps",
            "/api/mcps/save"
        ]
        for route in routes_to_check:
            self.assertIn(route, ref_text, f"Rota '{route}' ausente na documentação API_REFERENCE.md")
            self.assertIn(route, server_code, f"Rota '{route}' documentada mas não implementada em theme_server.py")

    def test_05_documentation_themes_and_fonts_consistency(self):
        """Garante que todos os 31 temas e 13 fontes estão listados no README.md e na engine."""
        readme = (BASE_DIR / "README.md").read_text(encoding="utf-8")

        for k, v in theme_changer.THEMES.items():
            short_k = k.replace("dark-", "").replace("light-", "")
            found = (f"-{k}" in readme) or (f"-{short_k}" in readme)
            self.assertTrue(found, f"Flag de tema para '{k}' ({v['name']}) ausente no catálogo do README.md")

        for k, v in theme_changer.FONTS.items():
            tag = v["tag"]
            self.assertIn(tag, readme, f"Flag de fonte '{tag}' ({v['name']}) ausente no catálogo do README.md")

    def test_06_e2e_http_server_and_scheduler_lifecycle(self):
        """Teste E2E real: inicia o servidor em porta efêmera e executa ciclo completo de APIs HTTP."""
        # Encontrar porta livre
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            test_port = s.getsockname()[1]

        # Criar instância do servidor de teste
        server = theme_server.create_server(port=test_port)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        time.sleep(0.15) # Handshake

        base_url = f"http://127.0.0.1:{test_port}"

        try:
            # 1. Healthcheck /api/ping
            with urllib.request.urlopen(f"{base_url}/api/ping", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(data.get("status"), "ok")

            # 2. Diagnóstico /api/status
            with urllib.request.urlopen(f"{base_url}/api/status", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(data.get("status"), "online")
                self.assertIn("base_dir", data)
                self.assertIn("home_dir", data)

            # 3. Servir arquivos Web e Módulos WebGL
            with urllib.request.urlopen(f"{base_url}/theme_changer_app.html", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                self.assertTrue(len(resp.read()) > 200000)

            with urllib.request.urlopen(f"{base_url}/js/ogl.js", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                self.assertIn("application/javascript", resp.headers.get("Content-Type", ""))

            with urllib.request.urlopen(f"{base_url}/js/webgl-backgrounds.js", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                self.assertIn("application/javascript", resp.headers.get("Content-Type", ""))

            # 4. Catálogo de Temas /api/list
            with urllib.request.urlopen(f"{base_url}/api/list", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(data.get("total_themes"), 31)
                self.assertEqual(data.get("total_fonts"), 13)

            # 5. Fila do Scheduler: Consulta inicial
            with urllib.request.urlopen(f"{base_url}/api/scheduler/queue", timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode("utf-8"))
                self.assertTrue(data.get("success"))
                self.assertIn("queue", data)
                self.assertIn("agent_state", data)

            # 6. Agendar Mensagem via POST /api/scheduler/schedule
            schedule_payload = json.dumps({
                "recipient": "Antigravity Core",
                "content": "Teste E2E Automatizado de Mensagem Agendada",
                "target_type": "new_chat",
                "model_tier": "flash",
                "trigger_type": "delayed",
                "delay_seconds": 3600,
                "contexts": [{"type": "file", "value": "test_file.py"}]
            }).encode("utf-8")
            req = urllib.request.Request(
                f"{base_url}/api/scheduler/schedule",
                data=schedule_payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                res_data = json.loads(resp.read().decode("utf-8"))
                self.assertTrue(res_data.get("success"))
                scheduled_id = res_data["item"]["id"]

            # 7. Validar presença da mensagem na fila
            with urllib.request.urlopen(f"{base_url}/api/scheduler/queue", timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                queued_ids = [m["id"] for m in data["queue"]]
                self.assertIn(scheduled_id, queued_ids)

            # 8. Upload de Contexto via POST /api/scheduler/upload-context
            dummy_content = b"Conteudo de teste E2E para anexo de contexto"
            b64_content = base64.b64encode(dummy_content).decode("utf-8")
            upload_payload = json.dumps({
                "filename": "e2e_test_attachment.txt",
                "content_base64": b64_content
            }).encode("utf-8")
            req_upload = urllib.request.Request(
                f"{base_url}/api/scheduler/upload-context",
                data=upload_payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req_upload, timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                upload_res = json.loads(resp.read().decode("utf-8"))
                self.assertTrue(upload_res.get("success"))
                saved_path = Path(upload_res.get("path"))
                self.assertTrue(saved_path.exists())
                self.assertEqual(saved_path.read_bytes(), dummy_content)
                # Limpeza imediata do arquivo de teste
                try:
                    saved_path.unlink()
                except Exception:
                    pass

            # 9. Cancelamento de Mensagem via POST /api/scheduler/cancel
            cancel_payload = json.dumps({"id": scheduled_id}).encode("utf-8")
            req_cancel = urllib.request.Request(
                f"{base_url}/api/scheduler/cancel",
                data=cancel_payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req_cancel, timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                cancel_res = json.loads(resp.read().decode("utf-8"))
                self.assertTrue(cancel_res.get("success"))

            # 10. Validar remoção da fila
            with urllib.request.urlopen(f"{base_url}/api/scheduler/queue", timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                queued_ids = [m["id"] for m in data["queue"]]
                self.assertNotIn(scheduled_id, queued_ids)

            # 11. Alternância de Estado do Agente POST /api/scheduler/toggle-agent-state
            state_payload = json.dumps({"status": "busy", "task": "Executando Teste E2E"}).encode("utf-8")
            req_state = urllib.request.Request(
                f"{base_url}/api/scheduler/toggle-agent-state",
                data=state_payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req_state, timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                sdata = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(sdata["agent_state"]["status"], "busy")

            # Restaurar para idle
            state_idle_payload = json.dumps({"status": "idle"}).encode("utf-8")
            req_idle = urllib.request.Request(
                f"{base_url}/api/scheduler/toggle-agent-state",
                data=state_idle_payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req_idle, timeout=3) as resp:
                self.assertEqual(resp.status, 200)
                sdata = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(sdata["agent_state"]["status"], "idle")

        finally:
            server.shutdown()
            server.server_close()

if __name__ == "__main__":
    unittest.main()
