#!/bin/bash
TOKEN=$(grep '^GITHUB_TOKEN=' ~/AppData/Local/hermes/.env | cut -d= -f2- | tr -d '\r')
curl -s -m 30 -X POST https://api.github.com/user/repos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "name": "llama.cpp-vulkan-vision-fix",
    "description": "Fix for Qwen3-VL / Qwen2.5-VL / Gemma-3 vision crash on AMD Radeon 8060S (Strix Halo) with llama.cpp Vulkan backend",
    "private": true,
    "has_issues": true,
    "has_wiki": false
  }' | python -c "import json,sys; d=json.load(sys.stdin); print('repo:', d.get('full_name'), '| url:', d.get('html_url'), '| msg:', d.get('message'))"
