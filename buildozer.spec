[app]

# (str) Title of your application
title = Password Manager

# (str) Package name
package.name = passwordmanager

# (str) Package domain (غيّره إلى نطاقك إذا كان لديك)
package.domain = org.example

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas

# (list) Files to exclude
source.exclude_exts = spec

# (list) Directories to exclude
source.exclude_dirs = tests,.git,__pycache__

# (str) Application version
version = 1.0

# (list) Requirements
requirements = python3,kivy,cryptography

# (str) Orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

# (str) Icon
#icon.filename = icon.png

# (str) Presplash
#presplash.filename = presplash.png

# Android Permissions
android.permissions = INTERNET

# Android API
android.api = 34
android.minapi = 21

# Android SDK/NDK
android.ndk = 25b

# Android architecture
android.archs = arm64-v8a, armeabi-v7a

# Log level
log_level = 2

#
# -------------------------------------------------------------------
#

[buildozer]

# (int) Log level
log_level = 2

# (int) Warn on root
warn_on_root = 1