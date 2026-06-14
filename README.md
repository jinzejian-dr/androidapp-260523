# SurgeryCam Android App v1.4.0

术野摄像头Android接收端 - 内置播放器准备版本

## 版本信息

- **版本**: v1.4.0
- **日期**: 2026-06-15
- **分支**: v1.4
- **技术栈**: Kivy + Python
- **目标**: 准备集成ijkplayer实现内置RTSP播放器

## 功能特性

### 当前功能
- ✅ 设备自动发现 (UDP广播，端口8888)
- ✅ 设备列表显示
- ✅ RTSP地址管理
- ✅ 外部播放器调用 (VLC/MX Player)

### 准备集成
- 🔄 ijkplayer内置播放器
- 🔄 硬件解码支持 (MediaCodec)
- 🔄 录制功能

## 项目结构

```
.
├── main.py                 # 主程序 (Kivy UI)
├── buildozer.spec          # Buildozer构建配置
├── README.md               # 项目文档
├── .github/workflows/
│   └── build.yml           # GitHub Actions自动编译
├── main_v1.3.1.py          # v1.3.1备份 (如存在)
└── buildozer_v1.3.1.spec   # v1.3.1配置备份 (如存在)
```

## 使用方法

### 1. 自动发现设备
点击 "SCAN" 按钮搜索局域网内的摄像头设备

### 2. 播放视频
点击 "PLAY (External)" 调用外部播放器（需安装VLC或MX Player）

### 3. 手动输入
在RTSP输入框中输入地址，例如：
- `rtsp://192.168.4.1:8554/cam`

## 编译说明

### GitHub Actions自动编译
推送代码到v1.4分支自动触发编译：
```bash
git add .
git commit -m "Update to v1.4.0"
git push origin v1.4
```

在GitHub Actions页面下载APK。

### 本地编译
```bash
pip install buildozer cython
buildozer android debug
```

## 更新日志

### v1.4.0 (2026-06-15)
- 准备集成ijkplayer内置播放器
- 更新版本号到1.4.0
- 优化代码结构
- 添加GitHub Actions自动编译

### v1.3.1 (2026-05-31)
- 使用外部播放器方案
- 设备自动发现
- GitHub Actions编译

## 许可证

MIT License
