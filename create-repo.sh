#!/bin/bash
# 创建 GitHub 仓库 (用法: GITHUB_TOKEN=xxx ./create-repo.sh)
# 注意: token 通过环境变量传入, 不要写入脚本
TOKEN="${GITHUB_TOKEN:?请先设置 GITHUB_TOKEN 环境变量}"
curl -s -m 30 -X POST https://api.github.com/user/repos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "name": "llama.cpp-vulkan-vision-fix",
    "description": "Fix for Qwen3-VL / Qwen2.5-VL / Gemma-3 vision crash on AMD Radeon 8060S (Strix Halo) with llama.cpp Vulkan backend",
    "private": true,
    "has_issues": true,
    "has_wiki": false
  }' | python3 -c "import json,sys; d=json.load(sys.stdin); print('repo:', d.get('full_name'), '| url:', d.get('html_url'), '| msg:', d.get('message'))"
