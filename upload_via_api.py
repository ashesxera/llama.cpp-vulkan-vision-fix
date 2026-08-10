#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""用 GitHub Contents API 上传文件(绕开被墙的 git push)"""
import base64, json, os, urllib.request

TOKEN = ""
with open(os.path.expanduser("~/AppData/Local/hermes/.env"), encoding="utf-8", errors="ignore") as f:
    for line in f:
        if line.startswith("GITHUB_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip()
            break

REPO = "ashesxera/llama.cpp-vulkan-vision-fix"
BASE = r"C:\AI\llama.cpp-fix-project"

FILES = [
    "README.md",
    "build-vulkan.bat",
    "start-qwen3vl.bat",
    "install-svc.bat",
    "test_vision.py",
    "docs/quickstart.md",
    "create-repo.sh",
]

def upload(path, content_b64):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    body = json.dumps({
        "message": f"Add {path}",
        "content": content_b64,
        "branch": "main",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="PUT")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode("utf-8"))
            print(f"OK  {path} -> {d.get('content',{}).get('name','?')}")
            return True
    except Exception as e:
        print(f"FAIL {path}: {e}")
        return False

ok = True
for rel in FILES:
    fp = os.path.join(BASE, rel)
    if not os.path.exists(fp):
        print(f"SKIP {rel} (not found)")
        continue
    with open(fp, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ok = upload(rel.replace("\\", "/"), b64) and ok

print("\nALL DONE" if ok else "\nSOME FAILED")
