# llama.cpp Vulkan 视觉修复 for AMD Strix Halo (8060S)

在 **AMD Ryzen AI Max+ 395 (Strix Halo / Radeon 8060S iGPU)** 上,自编译 llama.cpp Vulkan 后端,解决 **Qwen3-VL-8B / Qwen2.5-VL-7B / Gemma-3 视觉请求崩溃** 问题的完整方案。

## 问题现象

- **任何视觉模型**(Qwen3-VL-8B、Qwen2.5-VL-7B、Gemma-3-4B)在 8060S 上:
  - `llama-server` 收到图像请求 → 连接重置(exit 127)
  - `llama-cli` → `0xC0000409 (STATUS_STACK_BUFFER_OVERRUN / MSVC fail-fast)`
- 崩溃点:日志停在 `clip_encode: copying image 1/1 to input buffer (nx=896, ny=896)` 附近
- 纯文本请求完全正常(45+ t/s)
- CPU 模式(-ngl 0)视觉正常 → 问题锁定 **Vulkan 后端 + AMD 驱动**

## 根因

AMD 8060S 驱动(及同类 RDNA3.5 APU 的 Vulkan 驱动)在 llama.cpp Vulkan 后端的**矩阵核(Cooperative Matrix / coopmat)图像编码算子上存在 bug**,触发 fail-fast 崩溃。这与模型无关(Qwen/Gemma 全中招),与 llama.cpp 预编译/自编译无关。

## 解决方案

自编译 llama.cpp(master,MSVC 2022)+ 三个环境变量:

```bash
GGML_VK_DISABLE_COOPMAT=1        # 禁用矩阵核(核心修复)
GGML_VK_MAX_NODES_PER_SUBMIT=1   # 限制每次提交的节点数,规避 AMD APU job timeout
GGML_VK_ALLOW_SYSMEM_FALLBACK=1  # 允许系统内存回退
```

### 验证结果(本机实测)

| 模型 | 文本 | 视觉 | 速度 |
|---|---|---|---|
| Qwen3-VL-8B (Q4_K_M) | ✅ | ✅ | 1.1-1.2s |
| Qwen2.5-VL-7B (Q4_K_M) | ✅ | ✅ | 0.9-2.2s |
| Gemma-3-4B (Q4_K_M) | ✅ | ✅ | 4.5-5.7s |

显存占用 ~7GB(32GB UMA 池内),系统内存几乎不动。

## 部署为 Windows 服务 (NSSM)

```bat
nssm install Qwen3VL "C:\llama.cpp-src\build\bin\llama-server.exe"
nssm set Qwen3VL AppParameters "-m C:/models/qwen3-vl-8b/Qwen3VL-8B-Instruct-Q4_K_M.gguf --mmproj C:/models/qwen3-vl-8b/mmproj-Qwen3VL-8B-Instruct-F16.gguf -ngl 99 -c 32768 --cache-type-k q8_0 --cache-type-v q8_0 -t 16 -b 2048 -ub 4096 --jinja --host 127.0.0.1 --port 8055 --no-mmap"
nssm set Qwen3VL AppEnvironmentExtra GGML_VK_DISABLE_COOPMAT=1 GGML_VK_MAX_NODES_PER_SUBMIT=1 GGML_VK_ALLOW_SYSMEM_FALLBACK=1
nssm set Qwen3VL Start SERVICE_AUTO_START
nssm start Qwen3VL
```

## 自编译 (Windows + MSVC + Vulkan)

前置:MSVC BuildTools 2022 + Vulkan SDK + CMake + Ninja

```bat
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
set VULKAN_SDK=C:\VulkanSDK\1.4.357.0
cd build
cmake .. -DGGML_VULKAN=ON -DGGML_CUDA=OFF -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release -j 16
```

## 测试

```bash
# 文本
curl http://127.0.0.1:8055/v1/chat/completions -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"你好"}]}'

# 视觉 (base64 图像)
python test_vision.py
```

## 参考资料

- llama.cpp issue #17012 (Qwen3-VL Vulkan 冻结, closed not planned)
- llama.cpp issue #17881 (Qwen3-VL clip encoding crash, SYCL)
- llama.cpp issue #21724 (AMD APU GPU job timeout, nodes_per_submit)
