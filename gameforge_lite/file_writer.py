import os

def create_project_structure(project_name):
    """Creates the project directory structure."""
    base_path = os.path.join(os.path.dirname(__file__), "generated_games", project_name)
    os.makedirs(base_path, exist_ok=True)
    return base_path

def write_project_files(project_data):
    """Writes the project files based on the project data."""
    project_name = project_data["project_name"]
    main_script = project_data["main_script"]

    project_path = create_project_structure(project_name)
    templates_path = os.path.join(os.path.dirname(__file__), "templates")

    # Write project.godot
    with open(os.path.join(templates_path, "project.godot.template"), "r") as f:
        project_godot_template = f.read()

    project_godot_content = project_godot_template.replace("GAME_NAME", project_name)

    with open(os.path.join(project_path, "project.godot"), "w") as f:
        f.write(project_godot_content)

    # Write main.tscn
    with open(os.path.join(templates_path, "main.tscn.template"), "r") as f:
        main_tscn_content = f.read()

    with open(os.path.join(project_path, "main.tscn"), "w") as f:
        f.write(main_tscn_content)

    # Write main.gd
    with open(os.path.join(project_path, "main.gd"), "w") as f:
        f.write(main_script)
