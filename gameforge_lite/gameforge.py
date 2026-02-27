import sys
import argparse
from ai_engine import generate_game
from file_writer import write_project_files

def main():
    parser = argparse.ArgumentParser(description="GameForge Lite: Generate Godot 4 projects from text.")
    parser.add_argument("prompt", type=str, help="Natural language prompt for the game.")
    args = parser.parse_args()

    print(f"Generating game from prompt: '{args.prompt}'...")

    try:
        project_data = generate_game(args.prompt)
        print("Game data generated. Writing files...")

        write_project_files(project_data)
        print("Project created successfully")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
