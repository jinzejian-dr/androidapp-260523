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

# 权限
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

[buildozer]
build_dir = ./.buildozer
build_mode = debug
log_level = 2
warn_on_root = 0
