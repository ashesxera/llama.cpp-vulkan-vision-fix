#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查公开仓库中是否有隐私泄露"""
import json, os, urllib.request

TOKEN = ""
with open(os.path.expanduser("~/AppData/Local/hermes/.env"), encoding="utf-8", errors="ignore") as f:
    for line in f:
        if line.startswith("GITHUB_TOKEN="):
            TOKEN = line.split("=", 1)[1].strip()
            break

REPO = "ashesxera/llama.cpp-vulkan-vision-fix"

# 获取仓库树
url = f"https://api.github.com/repos/{REPO}/git/trees/main?recursive=1"
req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {TOKEN}")
with urllib.request.urlopen(req, timeout=30) as r:
    tree = json.loads(r.read().decode("utf-8"))

files = [t["path"] for t in tree["tree"] if t["type"] == "blob"]
print("仓库文件:", files)
print()

# 敏感模式
patterns = {
    "token/密钥 (sk-/ghp_/hf_/ark-等)": [r"sk-[A-Za-z0-9]{10,}", r"ghp_[A-Za-z0-9]{20,}", r"hf_[A-Za-z0-9]{20,}", r"ark-[A-Za-z0-9-]{20,}", r"api[_-]?key\s*[=:]\s*\S+"],
    "用户名 GMKAdmin": [r"GMKAdmin", r"Users\\[A-Za-z]"],
    "本机路径 C:\\AI": [r"C:\\AI", r"C:/AI", r"llama\.cpp-src"],
    "env 文件路径": [r"AppData/Local/hermes", r"\.env"],
    "IP 地址": [r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"],
    "端口": [r"port\s+\d{4,5}", r":\d{4,5}"],
    "token 变量赋值": [r"TOKEN\s*=\s*.{10,}"],
}

for path in files:
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode("utf-8"))
    content = ""
    try:
        import base64
        content = base64.b64decode(d["content"]).decode("utf-8", errors="ignore")
    except Exception:
        pass
    print(f"--- {path} ({len(content)} chars) ---")
    for label, pats in patterns.items():
        import re
        for p in pats:
            for m in re.finditer(p, content):
                snippet = content[max(0, m.start()-30):m.end()+30].replace("\n", " ")
                print(f"  [{label}] ...{snippet}...")
    print()
