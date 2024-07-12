import logging
import requests
import os
import uuid
import json

from constants import HEADERS
from utils import extract_json_content, read_prompt

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyzeImage(base64_image, silent=False):
    logger.info("Sending image to OpenAI API")

    # Read the prompt from the file
    system = read_prompt("./prompts/system.md")
    user = read_prompt("./prompts/user.md")

    payload = {
        "model": "gpt-4o",
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        "max_tokens": 2000,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=HEADERS, json=payload
    )
    response.raise_for_status()

    response_json = response.json()
    
    if not silent:
        logger.info(f"Received response from OpenAI API: {response_json}")

    # Extract JSON content
    message_content = (
        response_json.get("choices", [])[0].get("message", {}).get("content", "")
    )
    schema_json = extract_json_content(message_content)

    if schema_json is None:
        logger.error("Failed to extract JSON from the response")
        raise ValueError("Failed to extract JSON from the response")

    # Save response
    # Ensure the outputs directory exists
    os.makedirs("outputs", exist_ok=True)

    # Generate a unique filename
    output_filename = f"outputs/{uuid.uuid4()}.json"

    # Save the schema JSON to the file
    with open(output_filename, "w") as outfile:
        json.dump(schema_json, outfile, indent=4)

    if not silent:
        logger.info(f"Schema JSON saved to {output_filename}")

    return schema_json
