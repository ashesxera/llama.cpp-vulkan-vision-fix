# llama.cpp Vulkan 视觉修复 (AMD Strix Halo / 8060S)

> 解决 Radeon 8060S (Ryzen AI Max+ 395) 上 llama.cpp Vulkan 视觉模型崩溃问题

## 快速开始

1. **自编译**: 运行 `build-vulkan.bat`(需 MSVC 2022 + Vulkan SDK + CMake + Ninja)
2. **启动服务**: `start-qwen3vl.bat`(前台) 或 `install-svc.bat`(NSSM 服务)
3. **测试**: `python test_vision.py [图片路径]`

详见 [README.md](README.md)。
