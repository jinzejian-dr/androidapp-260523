# 手动上传 GitHub 指南

## 文件清单

需要上传到 GitHub 的文件：

```
v1.1/
├── main.py                      ✅ 主程序
├── buildozer.spec               ✅ 打包配置
├── README.md                    ✅ 使用说明
├── WORK_LOG.md                  ✅ 开发记录
├── .gitignore                   ✅ Git忽略文件
└── .github/
    └── workflows/
        └── build-android.yml    ✅ GitHub Actions配置
```

## 上传步骤

### 1. 打开 GitHub 仓库
访问: https://github.com/jinzejian-dr/androidapp-260523

### 2. 上传文件
```
1. 点击 "Add file" → "Upload files"

2. 拖拽或选择以下文件到上传区域：
   - main.py
   - buildozer.spec
   - README.md
   - WORK_LOG.md
   - .gitignore

3. 点击 "Commit changes"
```

### 3. 上传 GitHub Actions 配置
```
1. 进入 .github/workflows/ 目录
   （如果没有，点击 "Add file" → "Create new file"）
   
2. 文件名输入: .github/workflows/build-android.yml

3. 复制 build-android.yml 的内容粘贴进去

4. 点击 "Commit new file"
```

### 4. 创建 Release（可选）
```
1. 点击右侧 "Releases"
2. 点击 "Create a new release"
3. 标签: v1.1.0
4. 标题: 术野摄像头 v1.1.0
5. 描述: 见下方模板
6. 点击 "Publish release"
```

## Release 描述模板

```markdown
## 术野摄像头 Android App v1.1.0

### 新增功能
- ✅ RTSP视频播放 - 使用 ffpyplayer 实现实时视频流播放
- ✅ 设备自动发现 - UDP广播自动搜索局域网内摄像头设备
- ✅ 设备列表管理 - 显示发现的设备，一键连接
- ✅ 播放控制 - 播放/停止按钮控制视频流

### 使用方法
1. 下载 APK 安装到手机
2. 确保手机和摄像头在同一WiFi网络
3. 点击"发现设备"搜索摄像头
4. 选择设备或手动输入RTSP地址
5. 点击"播放"开始观看

### 技术栈
- UI框架: Kivy
- 视频播放: ffpyplayer
- 设备发现: UDP广播

### 注意事项
- 首次启动可能需要几秒钟初始化视频解码器
- 如果视频播放卡顿，检查网络连接质量

### 版本历史
- v1.1.0 (2026-05-24) - 添加视频播放和设备发现
- v1.0.0 (2026-05-23) - 基础UI框架
```

## 本地文件位置

所有文件都在：
```
F:\术野摄像头\监控端程序\android app\v1.1\
```

## 编译说明

上传后 GitHub Actions 会自动编译：
- 编译时间: 30-45 分钟（含 FFmpeg）
- 输出: APK 文件
- 下载位置: Actions 页面 → 最新运行 → Artifacts

---

准备时间: 2026-05-24 12:12
