import os
import json
from google import genai
from google.genai import types

def generate_game(prompt):
    """
    Generates a game project structure from a natural language prompt using Gemini.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    system_instruction = """
    You are a Godot 4 game generator.
    Output must be JSON only.
    Schema:
    {
      "project_name": "string",
      "main_script": "valid GDScript code",
      "main_scene_nodes": [
          {
            "type": "Node2D",
            "name": "Main"
          }
      ]
    }
    """

    full_prompt = f"{system_instruction}\n\nUser Prompt: {prompt}"

    response = client.models.generate_content(
        model="gemini-1.5-pro-latest",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Fallback if the response isn't pure JSON (though response_mime_type should handle it)
        # Attempt to clean code blocks if present
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        return json.loads(text)
