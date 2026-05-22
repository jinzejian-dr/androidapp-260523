# 术野摄像头接收端 - 简化版

## 版本信息
- **版本**: 1.0.0
- **日期**: 2026-05-23
- **功能**: 仅支持 RTSP 视频播放

## 功能说明

这是术野摄像头接收端的简化版本，只保留最核心的视频播放功能：

- ✅ RTSP 视频流播放
- ✅ 手动输入连接地址
- ✅ 播放/停止控制
- ✅ 实时状态显示

## 已移除的功能

相比完整版，以下功能已被移除以简化打包：

- ❌ UDP 设备自动发现
- ❌ 设备重命名
- ❌ WiFi 配置
- ❌ 多设备列表
- ❌ 日志记录系统

## 打包步骤

### 1. 安装依赖

```bash
pip install buildozer cython
```

### 2. 进入项目目录

```bash
cd "F:\术野摄像头\监控端程序\android app\2026-05-23_v1.0.0_simple"
```

### 3. 初始化 buildozer（如需要）

```bash
buildozer init
```

### 4. 打包 APK

```bash
# 调试版本
buildozer android debug

# 打包并安装到设备
buildozer android debug deploy run
```

### 5. 查找生成的 APK

打包完成后，APK 文件位于：
```
.\bin\simplesurgerycam-1.0.0-arm64-v8a_debug.apk
```

## 使用方法

1. 打开应用
2. 在 RTSP 地址栏输入摄像头地址，例如：
   - `rtsp://192.168.4.1:8554/c`
   - `rtsp://192.168.137.241:8554/c`
3. 点击 **播放** 按钮
4. 等待连接成功，视频将显示在屏幕中央
5. 点击 **停止** 按钮结束播放

## 常见问题

### Q: 视频无法播放？
A: 检查以下几点：
1. 确保手机与摄像头在同一 WiFi 网络
2. 检查 RTSP 地址是否正确
3. 确认摄像头正在推流
4. 检查防火墙是否放行 8554 端口

### Q: 打包失败？
A: 尝试以下步骤：
```bash
# 清理缓存
buildozer android clean

# 重新打包
buildozer android debug
```

### Q: APK 安装后闪退？
A: 检查：
1. 是否授予网络权限
2. Android 版本是否 >= 6.0
3. 设备是否为 ARM64 架构

## 依赖版本

```
Python 3.10+
Kivy 2.2.1
ffpyplayer 4.5.0
OpenCV 4.8.1
```

## 文件结构

```
2026-05-23_v1.0.0_simple/
├── main.py              # 主程序
├── buildozer.spec       # 打包配置
├── README.md            # 本文件
└── .buildozer/          # 构建目录（自动生成）
    └── android/
        └── platform/
            └── build/
                └── bin/  # APK 输出目录
```

## 下一步优化

如需添加功能，可考虑：
1. 设备自动发现（UDP 广播）
2. 录像功能
3. 截图功能
4. 性能统计（FPS、延迟）
5. 多路视频同时播放
