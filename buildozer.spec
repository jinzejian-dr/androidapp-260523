[app]
title = 术野摄像头简化版
package.name = simplesurgerycam
package.domain = com.surgerycam
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy,ffpyplayer,opencv-python
orientation = landscape
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.release_artifact = apk
android.allow_backup = False
source.exclude_patterns = *.pyc,*.pyo,__pycache__,.git,*.md,README*
android.enable_androidx = True

[buildozer]
build_dir = ./.buildozer
build_mode = debug
log_level = 2
warn_on_root = 1
