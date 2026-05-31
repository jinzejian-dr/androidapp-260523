# 术野摄像头 Android App v1.3.1

简化版手术摄像头接收端应用 - 使用外部播放器版本

## 功能特性

### v1.3.1 更新内容
- ✅ **简化构建** - 移除 ffpyplayer 依赖，构建更稳定
- ✅ **外部播放器支持** - 调用 VLC / MX Player 播放 RTSP 视频
- ✅ **设备自动发现** - UDP广播自动搜索局域网内摄像头设备
- ✅ **设备列表管理** - 显示发现的设备，一键连接
- ✅ **URL复制** - 一键复制 RTSP 地址到剪贴板

### 界面布局
```
┌─────────────────────────────┐
│  SurgeryCam v1.3.1          │  <- 标题
├─────────────────────────────┤
│                             │
│    RTSP Video Player        │  <- 提示信息
│    Click PLAY to open       │
│    external player          │
│                             │
├─────────────────────────────┤
│ RTSP: [rtsp://...        ]  │  <- 地址输入
├─────────────────────────────┤
│ [COPY URL] [SCAN] [PLAY]    │  <- 控制按钮
├─────────────────────────────┤
│ Discovered Devices:         │
│ ┌─────────────────────────┐ │
│ │ Device1 192.168.4.1    │ │  <- 设备列表
│ │ Device2 192.168.4.2    │ │
│ └─────────────────────────┘ │
├─────────────────────────────┤
│ Status: Ready               │  <- 状态显示
└─────────────────────────────┘
```

## 使用方法

### 1. 自动发现设备
点击 "SCAN DEVICES" 按钮，应用会搜索局域网内的摄像头设备

### 2. 手动输入地址
在 RTSP 输入框中输入摄像头地址，例如：
- `rtsp://192.168.4.1:8554/cam`
- `rtsp://192.168.1.100:8554/cam`

### 3. 播放视频
点击 "PLAY VIDEO" 按钮，会自动调用外部播放器（VLC 或 MX Player）

**推荐安装的外部播放器：**
- VLC for Android (免费，支持RTSP)
- MX Player (免费版)

### 4. 复制URL
点击 "COPY URL" 按钮复制 RTSP 地址到剪贴板

## 技术栈

- **UI框架**: Kivy
- **视频播放**: 外部播放器 (VLC / MX Player)
- **设备发现**: UDP广播 (端口8888)
- **打包工具**: Buildozer

## 编译说明

### GitHub Actions 自动编译
推送代码到 GitHub 后自动触发编译：
```bash
git add .
git commit -m "Update to v1.3.1"
git push origin main
```

编译完成后在 Actions 页面下载 APK 文件。

### 本地编译
```bash
# 安装依赖
pip install buildozer cython

# 编译APK
buildozer android debug

# 部署到设备
buildozer android debug deploy run
```

## 依赖项

- Python 3.10+
- Kivy
- pyjnius (用于Android API调用)

## 构建要求

- Ubuntu 22.04 (GitHub Actions)
- Python 3.10
- OpenJDK 17
- Buildozer 1.5+

## 更新日志

### v1.3.1 (2026-05-31)
- 移除 ffpyplayer 依赖，简化构建流程
- 使用外部播放器播放 RTSP 视频
- 优化 GitHub Actions 构建配置
- 改进 UI 界面

### v1.3.0 (2026-05-31)
- 基于 v1.1 稳定版本重新组织
- 修复版本路径问题

### v1.1.4 (2026-05-31)
- 修复 ffpyplayer 依赖问题
- 添加 FFmpeg 系统依赖配置

### v1.1.0 (2026-05-24)
- 添加 ffpyplayer 视频播放功能
- 添加设备自动发现功能
- 添加设备列表显示

### v1.0.0 (2026-05-23)
- 基础UI界面
- GitHub Actions 编译配置
- 首次成功编译APK

## 常见问题

### Q: 应用闪退怎么办？
A: 检查以下几点：
1. 确保设备支持 ARM64 架构
2. 检查日志输出，查看具体错误信息
3. 确保已安装 VLC 或 MX Player

### Q: 视频播放不了？
A: 
1. 确认摄像头和APP在同一WiFi网络
2. 检查 RTSP 地址是否正确
3. 确保已安装 VLC 或 MX Player
4. 检查网络防火墙设置

### Q: 设备发现不了？
A:
1. 确保摄像头已开机并连接到WiFi
2. 检查手机和摄像头是否在同一局域网
3. 尝试手动输入IP地址连接

## 调试方法

### 查看日志
```bash
# 使用 adb 查看日志
adb logcat -s python:*

# 过滤 SurgeryCam 相关日志
adb logcat | grep -i surgerycam
```

### 本地测试
使用 Genymotion 或 Android Studio 模拟器进行测试。

## 版本说明

- **v1.0** - 基础版本，仅UI框架
- **v1.1** - 添加视频播放和设备发现
- **v1.1.4** - 修复 ffpyplayer 依赖问题
- **v1.3.0** - 基于 v1.1 重新组织
- **v1.3.1** - 移除 ffpyplayer，使用外部播放器

## 许可证

MIT License
