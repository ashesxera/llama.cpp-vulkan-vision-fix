@echo off
rem Qwen3-VL-8B 视觉服务启动脚本 (AMD 8060S 修复版)
rem 需在管理员 PowerShell 中注册: nssm install ... (见 install-svc.bat)
set GGML_VK_DISABLE_COOPMAT=1
set GGML_VK_MAX_NODES_PER_SUBMIT=1
set GGML_VK_ALLOW_SYSMEM_FALLBACK=1
cd /d C:\llama.cpp-src\build\bin
llama-server.exe -m C:/models/qwen3-vl-8b/Qwen3VL-8B-Instruct-Q4_K_M.gguf --mmproj C:/models/qwen3-vl-8b/mmproj-Qwen3VL-8B-Instruct-F16.gguf -ngl 99 -c 32768 --cache-type-k q8_0 --cache-type-v q8_0 -t 16 -b 2048 -ub 4096 --jinja --host 127.0.0.1 --port 8055 --no-mmap
