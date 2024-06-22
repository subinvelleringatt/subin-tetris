[app]

# (str) Title of your application
title = Tetris Game

# (str) Package name
package.name = tetris

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source files included in the package
source.include_exts = py,png,jpg,kv,atlas

# (list) List of requirements
requirements = python3,kivy

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = True

[buildozer]

# (int) Android API to use
android.api = 29

# (int) Minimum API required
android.minapi = 21

# (str) Android SDK version to use
android.sdk = 24

# (str) Android NDK version to use
android.ndk = 19b
