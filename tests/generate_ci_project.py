import os
import subprocess

def create_mock_project():
    """Generates a minimal valid Godot project for CI testing."""
    project_path = "generated_games"
    os.makedirs(project_path, exist_ok=True)

    # project.godot
    project_godot_content = """; Engine Configuration File
; Godot version: 4.3

[application]
config/name="MockGame"
run/main_scene="res://main.tscn"
config/features=PackedStringArray("4.3", "Mobile")
config/icon="res://icon.svg"

[display]
window/size/viewport_width=1152
window/size/viewport_height=648
window/stretch/mode="canvas_items"

[dotnet]
project/assembly_name="MockGame"
"""
    with open(os.path.join(project_path, "project.godot"), "w") as f:
        f.write(project_godot_content)

    # main.tscn
    main_tscn_content = """[gd_scene load_steps=2 format=3 uid="uid://cxydw2y4k5q1"]

[ext_resource type="Script" path="res://main.gd" id="1_main"]

[node name="Main" type="Node2D"]
script = ExtResource("1_main")
"""
    with open(os.path.join(project_path, "main.tscn"), "w") as f:
        f.write(main_tscn_content)

    # main.gd
    main_gd_content = """extends Node2D

func _ready():
    print("Hello from Mock Game!")
"""
    with open(os.path.join(project_path, "main.gd"), "w") as f:
        f.write(main_gd_content)

    # Generate debug.keystore
    keystore_path = os.path.join(project_path, "debug.keystore")
    if not os.path.exists(keystore_path):
        print("Generating debug.keystore...")
        subprocess.run([
            "keytool", "-genkey", "-v",
            "-keystore", keystore_path,
            "-alias", "androiddebugkey",
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-storepass", "android",
            "-keypass", "android",
            "-dname", "CN=Android Debug,O=Android,C=US"
        ], check=True)
        print("✅ debug.keystore created")

    # export_presets.cfg — include_filter اور exclude_filter شامل
    export_presets_content = """[preset.0]

name="Android"
platform="Android"
runnable=true
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path="../build.apk"

[preset.0.options]

architectures/arm64-v8a=true
architectures/armeabi-v7a=false
architectures/x86=false
architectures/x86_64=false
keystore/debug="res://debug.keystore"
keystore/debug_user="androiddebugkey"
keystore/debug_password="android"
keystore/release=""
keystore/release_user=""
keystore/release_password=""
version/code=1
version/name="1.0"
package/unique_name="com.example.mockgame"
package/name="Mock Game"
package/signed=false
package/app_category=2
package/retain_data_on_uninstall=false
package/exclude_from_recents=false
package/show_in_android_tv=false
package/show_in_app_library=true
package/is_game=true
screen/immersive_mode=true
screen/support_small=true
screen/support_normal=true
screen/support_large=true
screen/support_xlarge=true
gradle_build/use_gradle_build=true
"""
    with open(os.path.join(project_path, "export_presets.cfg"), "w") as f:
        f.write(export_presets_content)

    print(f"✅ Mock project generated at {os.path.abspath(project_path)}")
    print("Files created:")
    for f in os.listdir(project_path):
        print(f"  - {f}")

if __name__ == "__main__":
    create_mock_project()
