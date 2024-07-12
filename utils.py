import base64
import json
import pkg_resources
import sys
import os
import inspect

def encodeImage(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


def extract_json_content(text):
    # Check if the text contains a JSON block wrapped in "```json" and "```"
    start = text.find("```json")
    if start != -1:
        start += len("```json")
        end = text.find("```", start)
        if end != -1:
            json_content = text[start:end].strip()
            try:
                return json.loads(json_content)
            except json.JSONDecodeError:
                pass
    # If no wrapped JSON block, try to parse as is
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def read_prompt(relative_path):
    if is_running_in_pex():
        return pkg_resources.resource_string(__name__, relative_path).decode("utf-8")
    else:
        # Get the file path of the caller
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        caller_path = os.path.abspath(os.path.dirname(caller_module.__file__))

        # Construct the full path relative to the caller
        full_path = os.path.join(caller_path, relative_path)

        with open(full_path, "r", encoding="utf-8") as file:
            return file.read()


def is_running_in_pex():
    return hasattr(sys, "argv0") and "pex" in sys.argv0 or "__pex__" in os.environ
