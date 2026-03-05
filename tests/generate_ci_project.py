import os
import subprocess

def create_mock_project():
    """Generates a minimal valid Godot project for CI testing."""
    project_path = "generated_games"
    os.makedirs(project_path, exist_ok=True)

    # project.godot
    project_godot_content = """config_version=5

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
    keystore_abs_path = os.path.abspath(keystore_path)
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

    # Create editor_settings-4.tres for Godot 4
    # This ensures Godot knows where the Android SDK is
    android_home = os.environ.get("ANDROID_HOME", "/home/runner/android-sdk")
    config_path = os.path.expanduser("~/.config/godot")
    os.makedirs(config_path, exist_ok=True)

    editor_settings_content = f"""[gd_resource type="EditorSettings" format=3]

[resource]
export/android/android_sdk_path = "{android_home}"
export/android/debug_keystore = "{keystore_abs_path}"
export/android/debug_keystore_user = "androiddebugkey"
export/android/debug_keystore_pass = "android"
"""
    with open(os.path.join(config_path, "editor_settings-4.tres"), "w") as f:
        f.write(editor_settings_content)
    print(f"Created editor settings at {os.path.join(config_path, 'editor_settings-4.tres')}")

    # export_presets.cfg (CRITICAL for Android export)
    # Using res://debug.keystore because the keystore is inside the project folder
    export_presets_content = """[preset.0]

name="Android"
platform="Android"
runnable=true
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path=""
encryption_include_filters=""
encryption_exclude_filters=""
encrypt_pck=false
encrypt_directory=false

[preset.0.options]

package/unique_name="com.example.mockgame"
package/name="Mock Game"
package/signed=false
package/app_category=1
package/retain_data_on_uninstall=false
package/exclude_from_recents=false
launcher_icons/main_192x192=""
launcher_icons/adaptive_foreground_432x432=""
launcher_icons/adaptive_background_432x432=""
graphics/opengl_debug=false
xr_features/xr_mode=0
screen/immersive_mode=true
screen/support_small=true
screen/support_normal=true
screen/support_large=true
screen/support_xlarge=true
user_data_backup/allow_backup=false
command_line/extra_args=""
apk_expansion/enable=false
apk_expansion/SALT=""
apk_expansion/public_key=""
permissions/custom_permissions=PackedStringArray()
permissions/access_checkin_properties=false
permissions/access_coarse_location=false
permissions/access_fine_location=false
permissions/access_location_extra_commands=false
permissions/access_mock_location=false
permissions/access_network_state=false
permissions/access_surface_flinger=false
permissions/access_wifi_state=false
permissions/account_manager=false
permissions/add_voicemail=false
permissions/authenticate_accounts=false
permissions/battery_stats=false
permissions/bind_accessibility_service=false
permissions/bind_appwidget=false
permissions/bind_device_admin=false
permissions/bind_input_method=false
permissions/bind_remoteviews=false
permissions/bind_text_service=false
permissions/bind_vpn_service=false
permissions/bind_wallpaper=false
permissions/bluetooth=false
permissions/bluetooth_admin=false
permissions/brick=false
permissions/broadcast_package_removed=false
permissions/broadcast_sms=false
permissions/broadcast_sticky=false
permissions/broadcast_wap_push=false
permissions/call_phone=false
permissions/call_privileged=false
permissions/camera=false
permissions/change_component_enabled_state=false
permissions/change_configuration=false
permissions/change_network_state=false
permissions/change_wifi_multicast_state=false
permissions/change_wifi_state=false
permissions/clear_app_cache=false
permissions/clear_app_user_data=false
permissions/control_location_updates=false
permissions/delete_cache_files=false
permissions/delete_packages=false
permissions/device_power=false
permissions/diagnostic=false
permissions/disable_keyguard=false
permissions/dump=false
permissions/expand_status_bar=false
permissions/factory_test=false
permissions/flashlight=false
permissions/force_back=false
permissions/get_accounts=false
permissions/get_package_size=false
permissions/get_tasks=false
permissions/global_search=false
permissions/hardware_test=false
permissions/inject_events=false
permissions/install_location_provider=false
permissions/install_packages=false
permissions/internal_system_window=false
permissions/internet=true
permissions/kill_background_processes=false
permissions/manage_accounts=false
permissions/manage_app_tokens=false
permissions/master_clear=false
permissions/modify_audio_settings=false
permissions/modify_phone_state=false
permissions/mount_format_filesystems=false
permissions/mount_unmount_filesystems=false
permissions/nfc=false
permissions/persistent_activity=false
permissions/process_outgoing_calls=false
permissions/read_calendar=false
permissions/read_contacts=false
permissions/read_external_storage=false
permissions/read_frame_buffer=false
permissions/read_history_bookmarks=false
permissions/read_input_state=false
permissions/read_logs=false
permissions/read_phone_state=false
permissions/read_profile=false
permissions/read_sms=false
permissions/read_social_stream=false
permissions/read_sync_settings=false
permissions/read_sync_stats=false
permissions/read_user_dictionary=false
permissions/reboot=false
permissions/receive_boot_completed=false
permissions/receive_mms=false
permissions/receive_sms=false
permissions/receive_wap_push=false
permissions/record_audio=false
permissions/reorder_tasks=false
permissions/restart_packages=false
permissions/send_sms=false
permissions/set_activity_watcher=false
permissions/set_alarm=false
permissions/set_always_finish=false
permissions/set_animation_scale=false
permissions/set_debug_app=false
permissions/set_orientation=false
permissions/set_pointer_speed=false
permissions/set_preferred_applications=false
permissions/set_process_limit=false
permissions/set_time=false
permissions/set_time_zone=false
permissions/set_wallpaper=false
permissions/set_wallpaper_hints=false
permissions/signal_persistent_processes=false
permissions/status_bar=false
permissions/subscribed_feeds_read=false
permissions/subscribed_feeds_write=false
permissions/system_alert_window=false
permissions/update_device_stats=false
permissions/use_credentials=false
permissions/use_sip=false
permissions/vibrate=false
permissions/wake_lock=false
permissions/write_apn_settings=false
permissions/write_calendar=false
permissions/write_contacts=false
permissions/write_external_storage=false
permissions/write_gservices=false
permissions/write_history_bookmarks=false
permissions/write_profile=false
permissions/write_secure_settings=false
permissions/write_settings=false
permissions/write_sms=false
permissions/write_social_stream=false
permissions/write_sync_settings=false
permissions/write_user_dictionary=false
architectures/armeabi-v7a=true
architectures/arm64-v8a=true
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
gradle_build/use_gradle_build=true
"""
    with open(os.path.join(project_path, "export_presets.cfg"), "w") as f:
        f.write(export_presets_content)

    print(f"Mock project generated at {os.path.abspath(project_path)}")

if __name__ == "__main__":
    create_mock_project()
