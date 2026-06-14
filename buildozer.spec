[app]
title = SurgeryCam
package.name = surgerycam
package.domain = com.surgerycam
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,so
version = 1.4.0

requirements = python3,kivy,pyjnius

orientation = landscape
fullscreen = 1

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

source.exclude_patterns = *.pyc,*.pyo,__pycache__,.git

[buildozer]
build_dir = ./.buildozer
build_mode = debug
log_level = 2
warn_on_root = 0
