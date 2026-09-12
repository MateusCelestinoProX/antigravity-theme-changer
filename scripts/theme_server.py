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
import re
import shutil
import time
import math
import threading
import uuid
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

# ==========================================
# GESTÃO DE AGENTES DO GOOGLE ANTIGRAVITY
# ==========================================

def parse_frontmatter(text):
    data = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
            current_list_key = None
            for line in fm_text.splitlines():
                line_str = line.strip()
                if not line_str or line_str.startswith("#"):
                    continue
                if line_str.startswith("- ") and current_list_key:
                    data[current_list_key].append(line_str[2:].strip())
                elif ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip()
                    if v == "":
                        data[k] = []
                        current_list_key = k
                    else:
                        current_list_key = None
                        if v.lower() == "true":
                            data[k] = True
                        elif v.lower() == "false":
                            data[k] = False
                        else:
                            data[k] = v.strip("\"'")
    return data, body

def build_agent_md(name, description, tools, model="inherit", policy="auto", mainAgent=True, subagent=True, system_prompt=""):
    lines = ["---"]
    lines.append(f"name: {name}")
    lines.append(f"description: {description}")
    lines.append(f"subagent: {'true' if subagent else 'false'}")
    lines.append(f"mainAgent: {'true' if mainAgent else 'false'}")
    lines.append(f"model: {model}")
    lines.append(f"commandExecutionPolicy: {policy}")
    lines.append("tools:")
    for t in tools:
        t_clean = str(t).strip()
        if t_clean:
            lines.append(f"  - {t_clean}")
    lines.append("---")
    lines.append("")
    lines.append(system_prompt.strip())
    lines.append("")
    return "\n".join(lines)

def list_agents_from_disk():
    agent_dir = Path.home() / ".gemini/config/agents"
    agents = []
    seen = set()
    if agent_dir.exists():
        for f in agent_dir.glob("*.md"):
            try:
                txt = f.read_text(encoding="utf-8")
                fm, body = parse_frontmatter(txt)
                name = fm.get("name", f.stem)
                if name in seen:
                    continue
                seen.add(name)
                agents.append({
                    "name": name,
                    "filename": f.name,
                    "description": fm.get("description", ""),
                    "subagent": fm.get("subagent", True),
                    "mainAgent": fm.get("mainAgent", True),
                    "model": fm.get("model", "inherit"),
                    "commandExecutionPolicy": fm.get("commandExecutionPolicy", "auto"),
                    "tools": fm.get("tools", []),
                    "system_prompt": body,
                    "modified_at": int(f.stat().st_mtime * 1000)
                })
            except Exception as e:
                print(f"[i] Erro ao ler agente {f}:", e)
    agents.sort(key=lambda x: str(x["name"]).lower())
    return agents

def save_agent_to_disk(name, description, tools, model="inherit", policy="auto", mainAgent=True, subagent=True, system_prompt="", original_name=""):
    slug = re.sub(r'[^a-zA-Z0-9_\-]', '-', str(name).strip()).strip('-').lower()
    if not slug:
        raise ValueError("Nome de agente inválido")
    
    agent_dirs = [
        Path.home() / ".gemini/config/agents",
        Path.home() / ".gemini/config/.agents/agents",
        Path.home() / ".gemini/config/agent/agents"
    ]
    
    content = build_agent_md(
        name=slug,
        description=description,
        tools=tools,
        model=model,
        policy=policy,
        mainAgent=True,  # Garante presença no seletor do Antigravity
        subagent=True,
        system_prompt=system_prompt
    )
    
    # Se o nome original foi alterado, remove o arquivo antigo
    if original_name and original_name != slug:
        for ad in agent_dirs:
            for old_cand in [f"{original_name}.md", f"{original_name.replace('-', '_')}.md"]:
                old_file = ad / old_cand
                if old_file.exists():
                    try:
                        old_file.unlink()
                    except Exception:
                        pass
                        
    saved_paths = []
    for ad in agent_dirs:
        try:
            ad.mkdir(parents=True, exist_ok=True)
            target = ad / f"{slug}.md"
            target.write_text(content, encoding="utf-8")
            saved_paths.append(str(target))
        except Exception as e:
            print(f"[i] Erro ao salvar agente em {ad}:", e)
            
    return slug, saved_paths

def delete_agent_from_disk(name):
    slug = re.sub(r'[^a-zA-Z0-9_\-]', '-', str(name).strip()).strip('-').lower()
    agent_dirs = [
        Path.home() / ".gemini/config/agents",
        Path.home() / ".gemini/config/.agents/agents",
        Path.home() / ".gemini/config/agent/agents"
    ]
    deleted = 0
    for ad in agent_dirs:
        for candidate in [f"{slug}.md", f"{slug.replace('-', '_')}.md", f"{slug.replace('_', '-')}.md"]:
            p = ad / candidate
            if p.exists():
                try:
                    p.unlink()
                    deleted += 1
                except Exception:
                    pass
    return deleted > 0

# ==========================================
# GESTÃO DE SKILLS DO GOOGLE ANTIGRAVITY
# ==========================================

SKILLS_CACHE = None
SKILLS_CACHE_TIME = 0

def get_skills_catalog(query="", page=1, limit=48):
    global SKILLS_CACHE, SKILLS_CACHE_TIME
    now = time.time()
    skills_dir = Path.home() / ".gemini/config/skills"
    
    if SKILLS_CACHE is None or (now - SKILLS_CACHE_TIME) > 120:
        catalog = []
        if skills_dir.exists():
            for d in sorted(skills_dir.iterdir(), key=lambda x: x.name.lower()):
                if d.is_dir():
                    skill_file = d / "SKILL.md"
                    if skill_file.exists():
                        desc = ""
                        display_name = d.name
                        try:
                            with open(skill_file, "r", encoding="utf-8", errors="ignore") as sf:
                                head_lines = [sf.readline() for _ in range(25)]
                            head_text = "".join(head_lines)
                            fm, _ = parse_frontmatter(head_text)
                            if "name" in fm and fm["name"]:
                                display_name = str(fm["name"])
                            if "description" in fm and fm["description"]:
                                desc = str(fm["description"])
                        except Exception:
                            pass
                        catalog.append({
                            "name": d.name,
                            "display_name": display_name,
                            "description": desc,
                            "modified_at": int(skill_file.stat().st_mtime * 1000)
                        })
        SKILLS_CACHE = catalog
        SKILLS_CACHE_TIME = now
        
    filtered = SKILLS_CACHE
    if query:
        q = query.lower().strip()
        filtered = [s for s in SKILLS_CACHE if q in s["name"].lower() or q in s["description"].lower()]
        
    total = len(filtered)
    limit = int(limit)
    page = int(page)
    if limit > 0:
        start = (page - 1) * limit
        end = start + limit
        paginated = filtered[start:end]
    else:
        paginated = filtered
        
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": math.ceil(total / limit) if limit > 0 else 1,
        "skills": paginated
    }

def get_skill_detail(name):
    skill_file = Path.home() / f".gemini/config/skills/{name}/SKILL.md"
    if not skill_file.exists():
        d = Path.home() / f".gemini/config/skills/{name}"
        if not d.exists() or not (d / "SKILL.md").exists():
            raise FileNotFoundError(f"Skill '{name}' não encontrada")
        skill_file = d / "SKILL.md"
    return skill_file.read_text(encoding="utf-8")

def save_skill_content(name, content):
    global SKILLS_CACHE
    skill_dir = Path.home() / f".gemini/config/skills/{name}"
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(content, encoding="utf-8")
    SKILLS_CACHE = None
    return True

def delete_skill_folder(name):
    global SKILLS_CACHE
    skill_dir = Path.home() / f".gemini/config/skills/{name}"
    if skill_dir.exists() and skill_dir.is_dir():
        shutil.rmtree(skill_dir)
        SKILLS_CACHE = None
        return True
    return False

# ==========================================
# GESTÃO DE SERVIDORES MCP (MODEL CONTEXT PROTOCOL)
# ==========================================

def get_all_mcps():
    config_file = Path.home() / ".gemini/config/mcp_config.json"
    schemas_dir = Path.home() / ".gemini/antigravity/mcp"
    
    active_mcps = {}
    disabled_mcps = {}
    
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                c_data = json.load(f)
                active_mcps = c_data.get("mcpServers", {})
                disabled_mcps = c_data.get("disabledMcpServers", {})
        except Exception as e:
            print("[i] Erro ao ler config mcp_config.json:", e)
            
    tools_map = {}
    if schemas_dir.exists():
        for sdir in schemas_dir.iterdir():
            if sdir.is_dir():
                tool_files = list(sdir.glob("*.json"))
                tool_names = [tf.stem for tf in tool_files]
                tools_map[sdir.name] = tool_names
                
    result = {
        "active": [],
        "disabled": [],
        "total_active": len(active_mcps),
        "total_disabled": len(disabled_mcps)
    }
    
    for name, cfg in active_mcps.items():
        tools = tools_map.get(name, [])
        result["active"].append({
            "name": name,
            "status": "active",
            "command": cfg.get("command", ""),
            "args": cfg.get("args", []),
            "env": cfg.get("env", {}),
            "tools_count": len(tools),
            "tools": tools
        })
        
    for name, cfg in disabled_mcps.items():
        tools = tools_map.get(name, [])
        result["disabled"].append({
            "name": name,
            "status": "disabled",
            "command": cfg.get("command", ""),
            "args": cfg.get("args", []),
            "env": cfg.get("env", {}),
            "tools_count": len(tools),
            "tools": tools
        })
        
    return result

def toggle_mcp_server(name, target_state=None):
    config_file = Path.home() / ".gemini/config/mcp_config.json"
    antigravity_file = Path.home() / ".gemini/antigravity/mcp_config.json"
    
    with open(config_file, "r", encoding="utf-8") as f:
        cfg_data = json.load(f)
        
    active_servers = cfg_data.get("mcpServers", {})
    disabled_servers = cfg_data.get("disabledMcpServers", {})
    
    antigravity_data = {"mcpServers": {}}
    if antigravity_file.exists():
        try:
            with open(antigravity_file, "r", encoding="utf-8") as af:
                antigravity_data = json.load(af)
        except Exception:
            pass
            
    is_currently_active = name in active_servers
    should_activate = (target_state == "active") if target_state else (not is_currently_active)
    
    if should_activate:
        srv = disabled_servers.pop(name, None)
        if not srv and name in active_servers:
            srv = active_servers[name]
        if srv:
            srv_copy = dict(srv)
            srv_copy.pop("disabled", None)
            active_servers[name] = srv_copy
            antigravity_data.setdefault("mcpServers", {})[name] = srv_copy
    else:
        srv = active_servers.pop(name, None)
        if not srv and name in disabled_servers:
            srv = disabled_servers[name]
        if srv:
            srv_copy = dict(srv)
            srv_copy["disabled"] = True
            disabled_servers[name] = srv_copy
            if "mcpServers" in antigravity_data and name in antigravity_data["mcpServers"]:
                antigravity_data["mcpServers"].pop(name, None)
                
    cfg_data["mcpServers"] = active_servers
    cfg_data["disabledMcpServers"] = disabled_servers
    
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(cfg_data, f, indent=2)
    with open(antigravity_file, "w", encoding="utf-8") as af:
        json.dump(antigravity_data, af, indent=2)
        
    return True, "active" if should_activate else "disabled"

def delete_mcp_server(name):
    config_file = Path.home() / ".gemini/config/mcp_config.json"
    antigravity_file = Path.home() / ".gemini/antigravity/mcp_config.json"
    
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            cfg_data = json.load(f)
        cfg_data.get("mcpServers", {}).pop(name, None)
        cfg_data.get("disabledMcpServers", {}).pop(name, None)
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(cfg_data, f, indent=2)
            
    if antigravity_file.exists():
        with open(antigravity_file, "r", encoding="utf-8") as af:
            ag_data = json.load(af)
        ag_data.get("mcpServers", {}).pop(name, None)
        with open(antigravity_file, "w", encoding="utf-8") as af:
            json.dump(ag_data, af, indent=2)
            
    return True

def save_mcp_server(data):
    config_file = Path.home() / ".gemini/config/mcp_config.json"
    antigravity_file = Path.home() / ".gemini/antigravity/mcp_config.json"
    
    name = str(data.get("name", "")).strip()
    original_name = str(data.get("original_name", "")).strip()
    if not name:
        raise ValueError("Nome do servidor MCP é obrigatório")
        
    command = str(data.get("command", "")).strip()
    args = data.get("args", [])
    if isinstance(args, str):
        args = [a.strip() for a in args.split() if a.strip()]
    env = data.get("env", {})
    is_active = data.get("active", True)
    
    with open(config_file, "r", encoding="utf-8") as f:
        cfg_data = json.load(f)
    active_servers = cfg_data.get("mcpServers", {})
    disabled_servers = cfg_data.get("disabledMcpServers", {})
    
    if original_name and original_name != name:
        active_servers.pop(original_name, None)
        disabled_servers.pop(original_name, None)
        
    server_entry = {
        "command": command,
        "args": args
    }
    if env:
        server_entry["env"] = env
        
    if is_active:
        active_servers[name] = server_entry
        disabled_servers.pop(name, None)
    else:
        server_entry["disabled"] = True
        disabled_servers[name] = server_entry
        active_servers.pop(name, None)
        
    cfg_data["mcpServers"] = active_servers
    cfg_data["disabledMcpServers"] = disabled_servers
    
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(cfg_data, f, indent=2)
        
    if antigravity_file.exists():
        with open(antigravity_file, "r", encoding="utf-8") as af:
            ag_data = json.load(af)
        ag_active = ag_data.setdefault("mcpServers", {})
        if original_name and original_name != name:
            ag_active.pop(original_name, None)
        if is_active:
            ag_active[name] = {k: v for k, v in server_entry.items() if k != "disabled"}
        else:
            ag_active.pop(name, None)
        with open(antigravity_file, "w", encoding="utf-8") as af:
            json.dump(ag_data, af, indent=2)
            
    return True

# ==========================================
# GESTÃO DO AGENDADOR & FILA DE MENSAGENS (COM AGENTAPI NATIVO)
# ==========================================

SCHEDULER_FILE = SCRIPTS_DIR / "scheduler_messages.json"
SCHEDULER_LOCK = threading.Lock()

AGENTAPI_BIN = Path(shutil.which("agentapi") or (Path.home() / ".gemini/antigravity/bin/agentapi"))
if not AGENTAPI_BIN.exists():
    _app_bin = Path("/Applications/Antigravity.app/Contents/Resources/bin/language_server")
    if _app_bin.exists():
        AGENTAPI_BIN = _app_bin

ANTIGRAVITY_BRAIN = Path.home() / ".gemini/antigravity/brain"
ANTIGRAVITY_CONVERSATIONS = Path.home() / ".gemini/antigravity/conversations"
CURRENT_CONVERSATION_ID = "7b932cb5-510a-4d93-af7a-7cabd8e83ac4"

SCHEDULER_STATE = {
    "agent_state": {
        "status": "idle",  # "idle" ou "busy"
        "current_agent": "Antigravity Core",
        "current_task": "Aguardando novas instruções",
        "last_change": time.time()
    },
    "queue": [],
    "history": []
}

def list_antigravity_conversations():
    """Descobre e lista todas as conversas existentes no Google Antigravity para seleção de destino."""
    conversations = []
    seen_ids = set()
    
    if ANTIGRAVITY_BRAIN.exists():
        for item in sorted(ANTIGRAVITY_BRAIN.iterdir(), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True):
            if not item.is_dir() or item.name.startswith(".") or item.name == "tempmediaStorage":
                continue
            conv_id = item.name
            seen_ids.add(conv_id)
            title = "Nova Conversa"
            preview = ""
            created_at = time.strftime("%Y-%m-%d %H:%M", time.localtime(item.stat().st_mtime))
            
            transcript_file = item / ".system_generated" / "logs" / "transcript.jsonl"
            if transcript_file.exists():
                try:
                    with open(transcript_file, "r", encoding="utf-8", errors="ignore") as tf:
                        for line in tf:
                            if not line.strip():
                                continue
                            data = json.loads(line)
                            if data.get("type") == "USER_INPUT":
                                raw_text = data.get("content", "")
                                clean_text = re.sub(r"<[^>]+>", "", raw_text).strip()
                                clean_text = re.sub(r"\s+", " ", clean_text)
                                if clean_text:
                                    preview = clean_text[:100]
                                    title = clean_text[:45] + ("..." if len(clean_text) > 45 else "")
                                    break
                except Exception:
                    pass
            
            conversations.append({
                "id": conv_id,
                "title": title or f"Chat {conv_id[:8]}",
                "preview": preview or "Conversa do Antigravity",
                "updated_at": created_at,
                "is_current": (conv_id == CURRENT_CONVERSATION_ID)
            })
            
    if ANTIGRAVITY_CONVERSATIONS.exists():
        for db_file in sorted(ANTIGRAVITY_CONVERSATIONS.glob("*.db"), key=lambda p: p.stat().st_mtime, reverse=True):
            conv_id = db_file.stem
            if conv_id in seen_ids or conv_id.startswith("."):
                continue
            seen_ids.add(conv_id)
            created_at = time.strftime("%Y-%m-%d %H:%M", time.localtime(db_file.stat().st_mtime))
            conversations.append({
                "id": conv_id,
                "title": f"Chat {conv_id[:8]}",
                "preview": f"Conversa registrada em banco {conv_id[:8]}...",
                "updated_at": created_at,
                "is_current": (conv_id == CURRENT_CONVERSATION_ID)
            })

    current = [c for c in conversations if c["is_current"]]
    others = sorted([c for c in conversations if not c["is_current"]], key=lambda x: x["updated_at"], reverse=True)
    return current + others

def get_antigravity_ls_env():
    """Obtém as variáveis de ambiente necessárias para o agentapi se comunicar com o Antigravity Language Server."""
    env = os.environ.copy()
    if env.get("ANTIGRAVITY_LS_ADDRESS"):
        return env

    env_file = Path.home() / ".gemini/antigravity/antigravity_env.json"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("ANTIGRAVITY_LS_ADDRESS"):
                    env.update(data)
                    return env
        except Exception:
            pass

    try:
        ps_out = subprocess.check_output(["ps", "-eo", "pid,args"], text=True)
        for line in ps_out.splitlines():
            if "language_server" in line and "--override_ide_name antigravity" in line:
                pid = line.strip().split()[0]
                lsof_out = subprocess.check_output(["lsof", "-Pan", "-p", pid, "-i"], text=True)
                for l in lsof_out.splitlines():
                    if "LISTEN" in l and "127.0.0.1:" in l:
                        port = l.split("127.0.0.1:")[1].split()[0]
                        env["ANTIGRAVITY_LS_ADDRESS"] = f"localhost:{port}"
                        env["ANTIGRAVITY_PROJECT_ID"] = "outside-of-project"
                        m_token = re.search(r"--csrf_token\s+([a-zA-Z0-9-]+)", line)
                        if m_token:
                            env["ANTIGRAVITY_CSRF_TOKEN"] = m_token.group(1)
                        try:
                            with open(env_file, "w", encoding="utf-8") as f:
                                json.dump({
                                    "ANTIGRAVITY_LS_ADDRESS": f"localhost:{port}",
                                    "ANTIGRAVITY_CSRF_TOKEN": env.get("ANTIGRAVITY_CSRF_TOKEN", ""),
                                    "ANTIGRAVITY_PROJECT_ID": "outside-of-project"
                                }, f, indent=2)
                        except Exception:
                            pass
                        return env
    except Exception as e:
        print(f"[Scheduler] Erro na detecção dinâmica de portas: {e}")

    env["ANTIGRAVITY_LS_ADDRESS"] = "localhost:53446"
    env["ANTIGRAVITY_PROJECT_ID"] = env.get("ANTIGRAVITY_PROJECT_ID") or "outside-of-project"
    return env

def format_interval_label(seconds):
    """Retorna uma string legível para intervalos de recorrência."""
    try:
        s = int(seconds)
    except Exception:
        return f"{seconds}s"
    if s >= 31536000:
        return f"{s // 31536000} ano(s)"
    if s >= 86400:
        return f"{s // 86400} dia(s)"
    if s >= 3600:
        return f"{s // 3600} hora(s)"
    if s >= 60:
        return f"{s // 60} minuto(s)"
    return f"{s}s"

def discover_antigravity_projects():
    """Descobre apenas os projetos nativos do Antigravity (~/.gemini/config/projects/*.json)."""
    projects = []
    seen_ids = set()

    # 1. Projetos Nativos do Antigravity (exibidos na barra lateral Projects)
    proj_dir = Path.home() / ".gemini/config/projects"
    if proj_dir.exists():
        for p in sorted(proj_dir.glob("*.json")):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    p_id = data.get("id") or p.stem
                    name = data.get("name") or p_id
                    
                    # Ignora outside-of-project da lista de projetos específicos nativos
                    if p_id == "outside-of-project":
                        continue

                    folder = ""
                    res = data.get("projectResources", {}).get("resources", [])
                    for r in res:
                        if "gitFolder" in r:
                            folder = r["gitFolder"].get("folderUri", "").replace("file://", "")
                    
                    has_graph = False
                    if folder and Path(folder).exists():
                        has_graph = (Path(folder) / "graphify-out" / "graph.json").exists()

                    projects.append({
                        "id": p_id,
                        "name": name,
                        "path": folder,
                        "has_graphify": has_graph,
                        "category": "native",
                        "description": f"Projeto Nativo do Antigravity ({name})",
                        "is_native": True
                    })
                    seen_ids.add(p_id)
            except Exception:
                pass

    return projects

def save_antigravity_project(name, folder=""):
    """Registra um novo projeto nativo no Antigravity (~/.gemini/config/projects/<id>.json)."""
    if not name:
        raise ValueError("Nome do projeto é obrigatório")
    proj_dir = Path.home() / ".gemini/config/projects"
    proj_dir.mkdir(parents=True, exist_ok=True)
    
    clean_id = re.sub(r'[^a-zA-Z0-9_-]', '-', name.lower().strip()).strip('-')
    if not clean_id:
        clean_id = str(uuid.uuid4())
        
    folder_path = ""
    resources = []
    if folder:
        f_obj = Path(folder).expanduser().resolve()
        f_obj.mkdir(parents=True, exist_ok=True)
        folder_path = str(f_obj)
        resources.append({
            "gitFolder": {
                "folderUri": f"file://{folder_path}"
            }
        })
        
    proj_data = {
        "id": clean_id,
        "name": name,
        "projectResources": {
            "resources": resources
        },
        "settings": {},
        "isWorkspaceOnly": False
    }
    
    proj_file = proj_dir / f"{clean_id}.json"
    with open(proj_file, "w", encoding="utf-8") as f:
        json.dump(proj_data, f, indent=2)
        
    return {
        "id": clean_id,
        "name": name,
        "folder": folder_path,
        "file": str(proj_file)
    }

def execute_agentapi_dispatch(msg):
    """Executa o envio real da mensagem agendada usando o CLI nativo agentapi do Antigravity."""
    target_type = msg.get("target_type", "existing_chat")
    content = msg.get("content", "").strip()
    title = msg.get("chat_title", "").strip() or "Mensagem Agendada Antigravity"
    
    contexts = msg.get("contexts", [])
    project_id = str(msg.get("project_id", "")).strip()
    project_path = str(msg.get("project_path", "")).strip()
    project_name = str(msg.get("project_name", "")).strip()
    
    if not content:
        return {"success": False, "error": "Conteúdo da mensagem vazio"}
        
    dispatch_content = content
    ctx_lines = []
    
    # Inclusão explícita de contexto do projeto alvo
    if project_name or project_path or project_id:
        p_name = project_name or project_id or (Path(project_path).name if project_path else "Projeto")
        p_info = f"[PROJETO ANTIGRAVITY]: {p_name}"
        if project_id and project_id != "outside-of-project":
            p_info += f" (ID: {project_id})"
        if project_path:
            p_info += f" [{project_path}]"
        ctx_lines.append(p_info)
        if project_path and Path(project_path).exists():
            ctx_lines.append(f"- @folder:{project_path}")
            graph_file = Path(project_path) / "graphify-out" / "graph.json"
            if graph_file.exists():
                ctx_lines.append(f"- @graphify: Mapa estrutural de código ({graph_file})")

    if contexts and isinstance(contexts, list) and len(contexts) > 0:
        for c in contexts:
            if not isinstance(c, dict):
                continue
            c_type = c.get("type", "")
            c_val = str(c.get("value", "")).strip()
            c_label = str(c.get("label", "")).strip() or c_val
            if c_type == "conversation":
                ctx_lines.append(f'- @[conversation:"{c_label}"] (ID: {c_val})')
            elif c_type == "file":
                ctx_lines.append(f'- @file:{c_val}')
            elif c_type in ["folder", "workspace"]:
                ctx_lines.append(f'- @folder:{c_val}')
            elif c_type == "skill":
                ctx_lines.append(f'- @skill:{c_val}')
            elif c_type == "graphify":
                ctx_lines.append(f'- @graphify: Mapa de arquitetura do projeto ({c_val})')
            elif c_type == "artifact":
                ctx_lines.append(f'- @artifact:{c_val} ({c_label})')
            else:
                ctx_lines.append(f'- @{c_type}:{c_val}')

    if ctx_lines:
        dispatch_content = "<CONTEXT_ATTACHMENTS>\n" + "\n".join(ctx_lines) + "\n</CONTEXT_ATTACHMENTS>\n\n" + content

    cmd = []
    if target_type == "new_chat":
        cmd = [str(AGENTAPI_BIN), "new-conversation"]
        model = msg.get("model_tier", "inherit")
        if model in ["flash_lite", "flash", "pro"]:
            cmd.append(f"--model={model}")
        cmd.append(f"--title={title}")
        cmd.append(dispatch_content)
    else:
        recipient_id = msg.get("conversation_id", "").strip() or CURRENT_CONVERSATION_ID
        cmd = [str(AGENTAPI_BIN), "send-message", f"--title={title}", recipient_id, dispatch_content]
        
    print(f"[Scheduler] Executando comando real agentapi: {' '.join(cmd[:4])} (projeto: {project_name or project_id or 'padrão'}, com {len(contexts)} contextos)...")
    try:
        proc_env = get_antigravity_ls_env()
        exec_cwd = None
        if project_path and Path(project_path).is_dir():
            exec_cwd = str(Path(project_path).resolve())

        if project_id and project_id != "outside-of-project":
            proc_env["ANTIGRAVITY_PROJECT_ID"] = project_id
        else:
            proc_env["ANTIGRAVITY_PROJECT_ID"] = "outside-of-project"

        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=25,
            env=proc_env,
            cwd=exec_cwd
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        # Fallback de segurança para sessões ativas do Antigravity
        if proc.returncode != 0 and ("does not match target project_id" in stderr or "does not match target project_id" in stdout):
            print(f"[Scheduler] Sessão da GUI do Antigravity está em outside-of-project. Executando fallback seguro com contexto...")
            proc_env["ANTIGRAVITY_PROJECT_ID"] = "outside-of-project"
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=25,
                env=proc_env,
                cwd=exec_cwd
            )
            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()

        print(f"[Scheduler] Resultado agentapi (código {proc.returncode}): {stdout[:120]}")
        if proc.returncode == 0:
            return {
                "success": True,
                "output": stdout,
                "command": " ".join(cmd[:3]),
                "target_type": target_type,
                "project_id": project_id,
                "project_name": project_name,
                "project_path": project_path,
                "conversation_id": msg.get("conversation_id", CURRENT_CONVERSATION_ID) if target_type == "existing_chat" else "new"
            }
        else:
            return {
                "success": False,
                "error": stderr or stdout or f"Código de saída {proc.returncode}",
                "target_type": target_type
            }
    except Exception as e:
        print(f"[Scheduler] Erro ao invocar agentapi: {e}")
        return {
            "success": False,
            "error": str(e),
            "target_type": target_type
        }

def load_scheduler_data():
    global SCHEDULER_STATE
    if SCHEDULER_FILE.exists():
        try:
            with open(SCHEDULER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                with SCHEDULER_LOCK:
                    SCHEDULER_STATE["queue"] = data.get("queue", [])
                    SCHEDULER_STATE["history"] = data.get("history", [])
                    if "agent_state" in data:
                        SCHEDULER_STATE["agent_state"].update(data["agent_state"])
        except Exception as e:
            print(f"Erro ao carregar agendador: {e}")

def save_scheduler_data():
    try:
        with open(SCHEDULER_FILE, "w", encoding="utf-8") as f:
            json.dump(SCHEDULER_STATE, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar agendador: {e}")

def process_scheduler_tick():
    now = time.time()
    with SCHEDULER_LOCK:
        agent_status = SCHEDULER_STATE["agent_state"]["status"]
        dispatched_any = False
        remaining_queue = []
        for msg in SCHEDULER_STATE["queue"]:
            trigger = msg.get("trigger_type", "on_idle")
            should_dispatch = False
            dispatch_reason = ""

            if trigger in ["delayed", "exact_time"]:
                sched_time = msg.get("scheduled_at_timestamp", 0)
                if now >= sched_time:
                    should_dispatch = True
                    dispatch_reason = "Horário programado atingido" if trigger == "exact_time" else "Tempo de espera atingido"
            elif trigger == "on_idle":
                if agent_status == "idle":
                    should_dispatch = True
                    dispatch_reason = "Agente concluiu o trabalho e ficou livre"
            elif trigger == "cron":
                sched_time = msg.get("scheduled_at_timestamp", 0)
                if now >= sched_time:
                    should_dispatch = True
                    dispatch_reason = "Ciclo recorrente disparado"
                    interval = int(msg.get("cron_interval_seconds", 60))
                    next_msg = dict(msg)
                    next_msg["id"] = f"msg_{uuid.uuid4().hex[:8]}"
                    next_msg["scheduled_at_timestamp"] = now + interval
                    next_msg["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    next_msg["scheduled_at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now + interval))
                    remaining_queue.append(next_msg)
            elif trigger == "immediate":
                should_dispatch = True
                dispatch_reason = "Disparo forçado manual"

            if should_dispatch:
                # Executa disparo REAL via agentapi
                dispatch_res = execute_agentapi_dispatch(msg)
                msg["dispatch_result"] = dispatch_res
                msg["status"] = "delivered" if dispatch_res.get("success") else "failed"
                msg["delivered_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                msg["delivered_at_timestamp"] = now
                msg["delivery_reason"] = dispatch_reason
                SCHEDULER_STATE["history"].insert(0, msg)
                dispatched_any = True
            else:
                remaining_queue.append(msg)

        if dispatched_any:
            SCHEDULER_STATE["queue"] = remaining_queue
            SCHEDULER_STATE["history"] = SCHEDULER_STATE["history"][:100]
            save_scheduler_data()

_worker_started = False
def start_scheduler_worker():
    global _worker_started
    if _worker_started:
        return
    _worker_started = True
    load_scheduler_data()
    def _worker():
        while True:
            try:
                process_scheduler_tick()
            except Exception as e:
                pass
            time.sleep(1.0)
    t = threading.Thread(target=_worker, daemon=True)
    t.start()

class ThemeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")

    def send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

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
                Path.home() / ".gemini/antigravity/scratch/antigravity-theme-changer/theme_changer_app.html",
                BASE_DIR.parent / "theme_changer_app.html",
                BASE_DIR.parent / "web" / "theme_changer_app.html",
                BASE_DIR / "web" / "theme_changer_app.html",
                BASE_DIR / "theme_changer_app.html",
                Path.home() / ".gemini/config/skills/theme-changer/theme_changer_app.html",
                Path.home() / ".gemini/config/skills/theme-changer/web/theme_changer_app.html",
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

        # Servir scripts JS estáticos (ex: webgl-backgrounds.js)
        if parsed.path.startswith("/js/"):
            rel_file = parsed.path[4:].lstrip("/")
            candidate_paths = [
                Path.home() / ".gemini/antigravity/scratch/antigravity-theme-changer/js" / rel_file,
                BASE_DIR.parent / "js" / rel_file,
                BASE_DIR / "js" / rel_file,
                BASE_DIR / "web" / "js" / rel_file,
                Path.home() / ".gemini/config/skills/theme-changer/js" / rel_file,
                Path.home() / ".gemini/config/skills/theme-changer/web/js" / rel_file,
                Path.home() / ".gemini/antigravity/scratch/antigravity-theme-changer/web/js" / rel_file,
                Path.home() / ".gemini/antigravity/scratch/mcp-os/js" / rel_file,
            ]
            for p in candidate_paths:
                if p.exists() and p.is_file():
                    try:
                        content = p.read_bytes()
                        self.send_response(200)
                        self.send_header("Content-Type", "application/javascript; charset=utf-8")
                        self.send_header("Content-Length", str(len(content)))
                        self.send_header("Cache-Control", "no-cache")
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
                    "font_scope": cur_scope,
                    "base_dir": str(BASE_DIR.resolve()),
                    "home_dir": str(Path.home().resolve())
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

        # API: Listar Agentes do Google Antigravity
        elif parsed.path == "/api/agents":
            try:
                agents = list_agents_from_disk()
                return self.send_json({"success": True, "total": len(agents), "agents": agents})
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # API: Catálogo de Skills do Google Antigravity
        elif parsed.path == "/api/skills":
            try:
                params = urllib.parse.parse_qs(parsed.query)
                q = params.get("q", params.get("query", [""]))[0]
                page = int(params.get("page", ["1"])[0])
                limit = int(params.get("limit", ["100"])[0])
                catalog = get_skills_catalog(query=q, page=page, limit=limit)
                return self.send_json({"success": True, **catalog})
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # API: Obter conteúdo de uma Skill
        elif parsed.path == "/api/skills/get":
            try:
                params = urllib.parse.parse_qs(parsed.query)
                name = params.get("name", [""])[0]
                if not name:
                    return self.send_json({"success": False, "error": "Parâmetro 'name' é obrigatório"}, 400)
                content = get_skill_detail(name)
                return self.send_json({"success": True, "name": name, "content": content})
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # API: Servidores MCP (Ativos e Desativados)
        elif parsed.path == "/api/mcps":
            try:
                mcps = get_all_mcps()
                return self.send_json({"success": True, **mcps})
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # API: Obter mensagens / fila do Agendador
        elif parsed.path in ["/api/scheduler/messages", "/api/scheduler/queue"]:
            with SCHEDULER_LOCK:
                delayed_count = sum(1 for m in SCHEDULER_STATE["queue"] if m.get("trigger_type") == "delayed")
                exact_time_count = sum(1 for m in SCHEDULER_STATE["queue"] if m.get("trigger_type") == "exact_time")
                on_idle_count = sum(1 for m in SCHEDULER_STATE["queue"] if m.get("trigger_type") == "on_idle")
                cron_count = sum(1 for m in SCHEDULER_STATE["queue"] if m.get("trigger_type") == "cron")
                return self.send_json({
                    "success": True,
                    "current_conversation_id": CURRENT_CONVERSATION_ID,
                    "agent_state": SCHEDULER_STATE["agent_state"],
                    "queue": SCHEDULER_STATE["queue"],
                    "history": SCHEDULER_STATE["history"],
                    "stats": {
                        "queue_count": len(SCHEDULER_STATE["queue"]),
                        "delivered_count": len(SCHEDULER_STATE["history"]),
                        "delayed_count": delayed_count,
                        "exact_time_count": exact_time_count,
                        "on_idle_count": on_idle_count,
                        "cron_count": cron_count
                    }
                })

        # API: Obter lista de conversas existentes do Antigravity
        elif parsed.path == "/api/scheduler/conversations":
            try:
                convs = list_antigravity_conversations()
                return self.send_json({
                    "success": True,
                    "current_conversation_id": CURRENT_CONVERSATION_ID,
                    "conversations": convs,
                    "total": len(convs)
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # API: Sugestões e opções de contextos suportados pelo Antigravity
        elif parsed.path == "/api/scheduler/context-options":
            try:
                ws_dir = str(Path.home() / ".gemini/antigravity/scratch/antigravity-theme-changer")
                key_files = [
                    {"label": "theme_changer_app.html (App Frontend)", "value": f"{ws_dir}/theme_changer_app.html"},
                    {"label": "scripts/theme_server.py (Backend Server)", "value": f"{ws_dir}/scripts/theme_server.py"},
                    {"label": "SKILL.md (Instruções da Skill)", "value": str(Path.home() / ".gemini/config/skills/theme-changer/SKILL.md")},
                    {"label": "README.md (Documentação)", "value": f"{ws_dir}/README.md"}
                ]
                skills_list = ["theme-changer", "graphify", "ab-testing", "git-pr-review", "deep-research", "api-designer"]
                return self.send_json({
                    "success": True,
                    "workspace": ws_dir,
                    "key_files": key_files,
                    "skills": skills_list,
                    "graphify": "Grafo estrutural do projeto ativo"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # API: Projetos e workspaces disponíveis para atribuição
        elif parsed.path == "/api/scheduler/projects":
            try:
                projects = discover_antigravity_projects()
                active_ws = str(Path.home() / ".gemini/antigravity/scratch/antigravity-theme-changer")
                return self.send_json({
                    "success": True,
                    "active_workspace": active_ws,
                    "projects": projects,
                    "total": len(projects)
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

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

        # POST API: Salvar ou Criar Agente
        elif parsed.path == "/api/agents/save":
            try:
                name = data.get("name", "").strip()
                if not name:
                    return self.send_json({"success": False, "error": "Nome do agente é obrigatório"}, 400)
                desc = data.get("description", "")
                tools = data.get("tools", [])
                model = data.get("model", "inherit")
                policy = data.get("commandExecutionPolicy", "auto")
                prompt = data.get("system_prompt", "")
                orig_name = data.get("original_name", "")

                slug, paths = save_agent_to_disk(
                    name=name,
                    description=desc,
                    tools=tools,
                    model=model,
                    policy=policy,
                    mainAgent=True,
                    subagent=True,
                    system_prompt=prompt,
                    original_name=orig_name
                )
                return self.send_json({
                    "success": True,
                    "name": slug,
                    "saved_paths": paths,
                    "message": f"Agente '{slug}' salvo com sucesso e registrado no seletor do Antigravity!"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Apagar Agente
        elif parsed.path == "/api/agents/delete":
            try:
                name = data.get("name", "").strip()
                if not name:
                    return self.send_json({"success": False, "error": "Nome do agente é obrigatório"}, 400)
                ok = delete_agent_from_disk(name)
                return self.send_json({
                    "success": True,
                    "message": f"Agente '{name}' apagado com sucesso do Antigravity!"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Salvar Skill
        elif parsed.path == "/api/skills/save":
            try:
                name = data.get("name", "").strip()
                content = data.get("content", "")
                if not name:
                    return self.send_json({"success": False, "error": "Nome da skill é obrigatório"}, 400)
                save_skill_content(name, content)
                return self.send_json({
                    "success": True,
                    "message": f"Skill '{name}' atualizada com sucesso!"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Apagar Skill
        elif parsed.path == "/api/skills/delete":
            try:
                name = data.get("name", "").strip()
                if not name:
                    return self.send_json({"success": False, "error": "Nome da skill é obrigatório"}, 400)
                ok = delete_skill_folder(name)
                return self.send_json({
                    "success": True,
                    "message": f"Skill '{name}' apagada com sucesso!"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Alternar MCP (Ativar/Desativar)
        elif parsed.path == "/api/mcps/toggle":
            try:
                name = data.get("name", "").strip()
                target_state = data.get("target_state", None)
                if not name:
                    return self.send_json({"success": False, "error": "Nome do servidor MCP é obrigatório"}, 400)
                ok, new_status = toggle_mcp_server(name, target_state)
                label = "ativado" if new_status == "active" else "desativado"
                return self.send_json({
                    "success": True,
                    "name": name,
                    "status": new_status,
                    "message": f"Servidor MCP '{name}' {label} com sucesso!"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Apagar MCP
        elif parsed.path == "/api/mcps/delete":
            try:
                name = data.get("name", "").strip()
                if not name:
                    return self.send_json({"success": False, "error": "Nome do servidor MCP é obrigatório"}, 400)
                ok = delete_mcp_server(name)
                return self.send_json({
                    "success": True,
                    "name": name,
                    "message": f"Servidor MCP '{name}' removido das configurações com sucesso!"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Salvar MCP (Criar ou Editar)
        elif parsed.path == "/api/mcps/save":
            try:
                ok = save_mcp_server(data)
                return self.send_json({
                    "success": True,
                    "message": f"Servidor MCP '{data.get('name')}' salvo com sucesso!"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Agendar nova mensagem
        elif parsed.path == "/api/scheduler/schedule":
            try:
                recipient = data.get("recipient", "Antigravity Core").strip()
                content = data.get("content", "").strip()
                target_type = data.get("target_type", "existing_chat").strip()
                conversation_id = data.get("conversation_id", CURRENT_CONVERSATION_ID).strip()
                chat_title = data.get("chat_title", "").strip()
                model_tier = data.get("model_tier", "inherit").strip()
                trigger_type = data.get("trigger_type", "on_idle").strip()
                delay_seconds = int(data.get("delay_seconds", 0))
                cron_interval_seconds = int(data.get("cron_interval_seconds", 60))
                priority = data.get("priority", "normal").strip()
                project_id = str(data.get("project_id", "")).strip()
                project_path = str(data.get("project_path", "")).strip()
                project_name = str(data.get("project_name", "")).strip()
                if project_path and not project_name:
                    project_name = Path(project_path).name

                contexts = data.get("contexts", [])
                if not isinstance(contexts, list):
                    contexts = []

                if not content:
                    return self.send_json({"success": False, "error": "O conteúdo da mensagem é obrigatório"}, 400)

                now = time.time()
                scheduled_timestamp = now

                if trigger_type == "delayed":
                    scheduled_timestamp = now + max(1, delay_seconds)
                    label_scheduled = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(scheduled_timestamp))
                elif trigger_type == "exact_time":
                    raw_ts = data.get("scheduled_timestamp")
                    if raw_ts:
                        scheduled_timestamp = float(raw_ts)
                    else:
                        scheduled_timestamp = now + max(1, delay_seconds)
                    label_scheduled = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(scheduled_timestamp))
                elif trigger_type == "cron":
                    scheduled_timestamp = now + max(5, cron_interval_seconds)
                    label_scheduled = f"A cada {format_interval_label(cron_interval_seconds)} (Próximo: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(scheduled_timestamp))})"
                else: # on_idle
                    scheduled_timestamp = now
                    label_scheduled = "Ao liberar o agente"

                new_msg = {
                    "id": f"msg_{uuid.uuid4().hex[:8]}",
                    "recipient": recipient,
                    "target_type": target_type,
                    "conversation_id": conversation_id,
                    "chat_title": chat_title or ("Novo Chat" if target_type == "new_chat" else f"Chat {conversation_id[:8]}"),
                    "model_tier": model_tier,
                    "project_id": project_id,
                    "project_path": project_path,
                    "project_name": project_name,
                    "content": content,
                    "contexts": contexts,
                    "trigger_type": trigger_type,
                    "delay_seconds": delay_seconds,
                    "cron_interval_seconds": cron_interval_seconds,
                    "priority": priority,
                    "status": "queued",
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "created_at_timestamp": now,
                    "scheduled_at": label_scheduled,
                    "scheduled_at_timestamp": scheduled_timestamp
                }

                with SCHEDULER_LOCK:
                    SCHEDULER_STATE["queue"].append(new_msg)
                    save_scheduler_data()

                process_scheduler_tick()
                return self.send_json({"success": True, "message": "Mensagem agendada com sucesso na fila", "item": new_msg})
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Upload direto de arquivo do Mac para anexo de contexto
        elif parsed.path == "/api/scheduler/upload-context":
            try:
                filename = data.get("filename", "").strip()
                content_b64 = data.get("content_base64", "").strip()
                if not filename:
                    return self.send_json({"success": False, "error": "Nome do arquivo não informado"}, 400)
                if not content_b64:
                    return self.send_json({"success": False, "error": "Conteúdo do arquivo não fornecido"}, 400)

                import base64
                if "," in content_b64:
                    content_b64 = content_b64.split(",", 1)[1]
                file_bytes = base64.b64decode(content_b64)

                upload_dir = BASE_DIR / "uploads"
                if not upload_dir.exists():
                    upload_dir = Path.home() / ".gemini/config/skills/theme-changer/uploads"
                upload_dir.mkdir(parents=True, exist_ok=True)

                safe_name = Path(filename).name.replace(" ", "_")
                timestamp = int(time.time())
                dest_file = upload_dir / f"{timestamp}_{safe_name}"

                with open(dest_file, "wb") as f:
                    f.write(file_bytes)

                abs_path = str(dest_file.resolve())
                return self.send_json({
                    "success": True,
                    "filename": filename,
                    "saved_file": dest_file.name,
                    "path": abs_path,
                    "size": len(file_bytes),
                    "message": f"Arquivo '{filename}' enviado do Mac com sucesso!"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Registrar novo Projeto Nativo no Antigravity (~/.gemini/config/projects/)
        elif parsed.path == "/api/scheduler/projects/create":
            try:
                p_name = data.get("name", "").strip()
                p_folder = data.get("folder", "").strip()
                if not p_name:
                    return self.send_json({"success": False, "error": "Nome do projeto é obrigatório"}, 400)
                
                created = save_antigravity_project(p_name, p_folder)
                return self.send_json({
                    "success": True,
                    "project": created,
                    "message": f"Projeto '{p_name}' registrado com sucesso na barra lateral do Antigravity!"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Cancelar mensagem agendada
        elif parsed.path == "/api/scheduler/cancel":
            try:
                msg_id = data.get("id", "").strip()
                if not msg_id:
                    return self.send_json({"success": False, "error": "ID da mensagem é obrigatório"}, 400)
                with SCHEDULER_LOCK:
                    before_len = len(SCHEDULER_STATE["queue"])
                    SCHEDULER_STATE["queue"] = [m for m in SCHEDULER_STATE["queue"] if m.get("id") != msg_id]
                    if len(SCHEDULER_STATE["queue"]) < before_len:
                        save_scheduler_data()
                        return self.send_json({"success": True, "message": f"Mensagem {msg_id} cancelada com sucesso"})
                    else:
                        return self.send_json({"success": False, "error": "Mensagem não encontrada na fila ativa"}, 404)
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Disparar mensagem imediatamente
        elif parsed.path == "/api/scheduler/dispatch-now":
            try:
                msg_id = data.get("id", "").strip()
                if not msg_id:
                    return self.send_json({"success": False, "error": "ID da mensagem é obrigatório"}, 400)
                with SCHEDULER_LOCK:
                    for m in SCHEDULER_STATE["queue"]:
                        if m.get("id") == msg_id:
                            m["trigger_type"] = "immediate"
                            break
                process_scheduler_tick()
                return self.send_json({"success": True, "message": f"Mensagem {msg_id} disparada com sucesso"})
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        # POST API: Alternar / Simular estado do agente
        elif parsed.path == "/api/scheduler/toggle-agent-state":
            try:
                new_status = data.get("status", "")
                task_name = data.get("task", "")
                agent_name = data.get("agent", "")
                with SCHEDULER_LOCK:
                    curr = SCHEDULER_STATE["agent_state"]["status"]
                    if not new_status:
                        new_status = "busy" if curr == "idle" else "idle"
                    SCHEDULER_STATE["agent_state"]["status"] = new_status
                    if task_name:
                        SCHEDULER_STATE["agent_state"]["current_task"] = task_name
                    elif new_status == "busy":
                        SCHEDULER_STATE["agent_state"]["current_task"] = "Executando refatoração e testes de código"
                    else:
                        SCHEDULER_STATE["agent_state"]["current_task"] = "Aguardando novas instruções"
                    if agent_name:
                        SCHEDULER_STATE["agent_state"]["current_agent"] = agent_name
                    SCHEDULER_STATE["agent_state"]["last_change"] = time.time()
                    save_scheduler_data()

                if new_status == "idle":
                    process_scheduler_tick()

                return self.send_json({
                    "success": True,
                    "agent_state": SCHEDULER_STATE["agent_state"],
                    "message": f"Status do agente alterado para {new_status}"
                })
            except Exception as e:
                return self.send_json({"success": False, "error": str(e)}, 500)

        else:
            return self.send_json({"error": "Rota POST não encontrada"}, 404)

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
    start_scheduler_worker()
    with create_server(PORT) as httpd:
        print(f"[Theme Studio] Server running on http://localhost:{PORT}/theme_changer_app.html")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
