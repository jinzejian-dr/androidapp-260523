[app]
title = SurgeryCam
package.name = simplesurgerycam
package.domain = com.surgerycam
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.2.0

# 添加 ffpyplayer 用于视频播放
requirements = python3,kivy,pyjnius,ffpyplayer,setuptools

orientation = portrait
fullscreen = 0

# 添加存储权限用于视频录制/截图
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.release_artifact = apk
android.allow_backup = False

# 排除不需要的文件
source.exclude_patterns = *.pyc,*.pyo,__pycache__,.git,*.md,README*,logs_*,*.zip

# 启用 AndroidX
android.enable_androidx = True

# FFmpeg 相关配置 - 用于视频解码
android.gradle_dependencies = com.google.android.exoplayer:exoplayer:2.19.1

# 添加 FFmpeg 库支持
android.add_aars = 

# 如果需要使用 OpenCV 进行图像处理，取消下面注释
# android.add_libs_arm64_v8a = libs/arm64-v8a/libopencv_java4.so

[buildozer]
build_dir = ./.buildozer
build_mode = debug
log_level = 2
warn_on_root = 1

# 构建优化 - 使用国内镜像加速
android.accept_sdk_license = True

# 添加 p4a 特定配置 - 确保 ffpyplayer 正确编译
p4a.local_recipes = 
p4a.hook = 

# 如果需要指定特定版本的 ffpyplayer，可以在这里设置
# p4a.ffpyplayer_version = v4.5.1
