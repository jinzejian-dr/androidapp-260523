# Android App v1.1 开发工作记录

## 日期
2026-05-24

## 项目概述
术野摄像头 Android 接收端 App - v1.1 版本

**工作目录**: `F:\术野摄像头\监控端程序\android app\v1.1`

---

## 版本管理

| 版本 | 目录 | 状态 | 说明 |
|------|------|------|------|
| v1.0 | `2026-05-23_v1.0.0_simple/` | ✅ 稳定 | 基础UI框架 |
| v1.1 | `v1.1/` | 🔄 开发中 | 视频播放+设备发现 |

---

## 已完成工作

### 1. 视频播放功能 ✅
- **VideoWidget 组件** - 基于 ffpyplayer 的视频显示
- **RTSP 流播放** - 支持 TCP 传输模式，低延迟配置
- **播放控制** - 播放/停止按钮功能
- **视频帧更新** - 30fps 实时更新

### 2. 设备发现功能 ✅
- **UDP 广播监听** - 自动接收设备广播信息
- **主动发现机制** - 点击按钮主动搜索设备
- **设备列表显示** - 滚动列表展示发现的设备
- **一键连接** - 点击设备自动填充 RTSP 地址

### 3. UI 优化 ✅
- **视频显示区域** - 占据屏幕上半部分
- **设备列表区域** - 可滚动的设备列表
- **状态显示** - 实时显示当前状态
- **日志显示** - 操作日志记录

---

## 文件结构

```
v1.1/
├── main.py                      # Android 主程序
├── buildozer.spec               # 打包配置
├── README.md                    # 使用说明
├── WORK_LOG.md                  # 本文件
└── .github/
    └── workflows/
        └── build-android.yml    # GitHub Actions 配置
```

---

## 技术实现

### 视频播放 (ffpyplayer)
```python
opts = {
    'rtsp_transport': 'tcp',
    'fflags': 'nobuffer',
    'flags': 'low_delay'
}
player = MediaPlayer(url, ffopts=opts)
```

### 设备发现 (UDP)
```python
# 监听端口 8888
sock.bind(('', 8888))

# 发送广播
sock.sendto(request.encode('utf-8'), ('255.255.255.255', 8888))
```

---

## 依赖项

### Python 包
- kivy - UI框架
- ffpyplayer - 视频播放
- setuptools - 构建依赖

### 系统依赖
- FFmpeg
- libavcodec-dev
- libavformat-dev
- libavdevice-dev
- libavutil-dev
- libswscale-dev
- libswresample-dev
- libavfilter-dev

---

## GitHub 仓库

- 仓库地址: https://github.com/jinzejian-dr/androidapp-260523
- 建议创建新分支或标签: `v1.1`

---

## 下一步计划

### v1.2 计划功能
- [ ] 录制功能 - 保存视频到本地
- [ ] 截图功能 - 抓取当前画面
- [ ] 全屏播放 - 双击全屏切换
- [ ] 设置页面 - 配置参数保存
- [ ] 设备管理 - 保存常用设备

---

## 已知问题

| 问题 | 状态 | 说明 |
|------|------|------|
| ffpyplayer 编译时间 | ⏳ 待观察 | 首次编译可能需要较长时间 |
| 视频延迟 | ⏳ 待测试 | 需要实际测试 RTSP 延迟 |
| 设备发现可靠性 | ⏳ 待测试 | 需要多设备环境测试 |

---

**记录时间**: 2026-05-24 12:10
**记录人**: AI Assistant
**版本**: v1.1
