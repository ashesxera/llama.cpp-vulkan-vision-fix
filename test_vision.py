# -*- coding: utf-8 -*-
"""视觉测试脚本: 对本地 llama-server 发送文本+图像请求"""
import json, base64, sys, time, urllib.request

URL = "http://127.0.0.1:8055/v1/chat/completions"

def chat(messages, max_tokens=100):
    body = json.dumps({"messages": messages, "max_tokens": max_tokens, "temperature": 0.2}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read().decode("utf-8"))
    return d["choices"][0]["message"]["content"], time.time() - t0

# 1. 文本
print("=== 1. 文本 ===")
c, dt = chat([{"role": "user", "content": "用一句话介绍你自己"}])
print(f"[{dt:.1f}s] {c}")

# 2. 视觉 (需要一张测试图, 可用 PIL 生成或传入路径)
img_path = sys.argv[1] if len(sys.argv) > 1 else "test.png"
try:
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    print(f"[SKIP] 找不到图片 {img_path}, 跳过视觉测试")
    sys.exit(0)

print(f"\n=== 2. 视觉 ({img_path}) ===")
c, dt = chat([{"role": "user", "content": [
    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
    {"type": "text", "text": "图片上写的什么?用中文回答。"}
]}])
print(f"[{dt:.1f}s] {c}")
print("\nALL DONE")
