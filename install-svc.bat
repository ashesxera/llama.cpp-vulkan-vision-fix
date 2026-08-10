@echo off
rem Qwen3VL NSSM 服务注册脚本 (需管理员权限运行)
rem 用法: 右键"以管理员身份运行" 或 PowerShell: Start-Process this.bat -Verb RunAs

nssm install Qwen3VL "C:\llama.cpp-src\build\bin\llama-server.exe"
nssm set Qwen3VL AppParameters "-m C:/models/qwen3-vl-8b/Qwen3VL-8B-Instruct-Q4_K_M.gguf --mmproj C:/models/qwen3-vl-8b/mmproj-Qwen3VL-8B-Instruct-F16.gguf -ngl 99 -c 32768 --cache-type-k q8_0 --cache-type-v q8_0 -t 16 -b 2048 -ub 4096 --jinja --host 127.0.0.1 --port 8055 --no-mmap"
nssm set Qwen3VL AppEnvironmentExtra GGML_VK_DISABLE_COOPMAT=1 GGML_VK_MAX_NODES_PER_SUBMIT=1 GGML_VK_ALLOW_SYSMEM_FALLBACK=1
nssm set Qwen3VL AppStdout "C:\llama.cpp\svc-qwen3vl.log"
nssm set Qwen3VL AppStderr "C:\llama.cpp\svc-qwen3vl.err"
nssm set Qwen3VL Start SERVICE_AUTO_START
nssm start Qwen3VL
echo DONE rc=%errorlevel%
