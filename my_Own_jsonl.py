import os
import json
import logging

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("conversion.log", mode='w')
        ]
    )

def convert_json_to_jsonl(json_file_path, jsonl_file_path):
    """Converts a JSON file to a JSONL file."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
            for item in data:
                jsonl_file.write(json.dumps(item) + '\n')
        logging.info(f"Successfully converted {json_file_path} to {jsonl_file_path}")

    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from file {json_file_path}")
    except Exception as e:
        logging.error(f"Error processing file {json_file_path}: {e}")

def process_directory(directory_path):
    """Processes all JSON files within a directory and converts them to JSONL files."""
    if not os.path.exists(directory_path):
        logging.error(f"The directory {directory_path} does not exist.")
        return

    jsonl_dir = os.path.join(directory_path, 'jsonl_files')
    os.makedirs(jsonl_dir, exist_ok=True)  # Create the jsonl_files directory if it doesn't exist

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(directory_path, file_name)
            jsonl_file_name = file_name.replace('.json', '.jsonl')
            jsonl_file_path = os.path.join(jsonl_dir, jsonl_file_name)

            # Ensure uniqueness in case of name collisions
            base_name, ext = os.path.splitext(jsonl_file_name)
            counter = 1
            while os.path.exists(jsonl_file_path):
                jsonl_file_path = os.path.join(jsonl_dir, f"{base_name}_{counter}{ext}")
                counter += 1

            convert_json_to_jsonl(json_file_path, jsonl_file_path)

if __name__ == "__main__":
    setup_logging()

if __name__ == "__main__":
    directory_path = r'C:\var\mobile\Containers\Data\Application\747AFC67-824A-4188-A050-1BD50E194169\Documents\ParticlePhoton'
    process_directory(directory_path)