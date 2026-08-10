@echo off
rem llama.cpp 自编译 (Windows + MSVC + Vulkan)
rem 前置: MSVC BuildTools 2022 + Vulkan SDK + CMake + Ninja
rem 用法: 管理员 PowerShell 执行, 或 cmd 直接运行
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
set VULKAN_SDK=C:\VulkanSDK\1.4.357.0
set PATH=C:\Program Files\CMake\bin;%PATH%
cd /d C:\AI\llama.cpp-src
if not exist build mkdir build
cd build
cmake .. -DGGML_VULKAN=ON -DGGML_CUDA=OFF -DGGML_CPU=ON -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release -j 16
echo BUILD_DONE_%errorlevel%
