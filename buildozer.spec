[app]

# 应用标题
title = 术野摄像头简化版

# 包名
package.name = simplesurgerycam
package.domain = com.surgerycam

# 源代码目录
source.dir = .

# 包含的文件扩展名
source.include_exts = py,png,jpg,kv,atlas

# 应用版本
version = 1.0.0

# 依赖项 - 最小化依赖
requirements = python3,kivy==2.2.1,ffpyplayer,opencv-python

# 屏幕方向 (landscape/portrait/all)
orientation = landscape

# 是否全屏
fullscreen = 0

# Android权限 - 最小化权限
android.permissions = INTERNET

# Android API版本
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# 目标架构
android.archs = arm64-v8a

# 优化APK体积
android.release_artifact = apk
android.allow_backup = False

# 排除不需要的文件
source.exclude_patterns = 
    *.pyc,
    *.pyo,
    __pycache__,
    .git,
    *.md,
    README*

# 启用AndroidX
android.enable_androidx = True

[buildozer]

# 构建目录
build_dir = ./.buildozer

# 打包模式
build_mode = debug

# 日志级别
log_level = 2

# 警告为错误
warn_on_root = 1
