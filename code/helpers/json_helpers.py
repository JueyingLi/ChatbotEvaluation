import json
import logging
import re

# read from file
def read_json_file(file_name, rw="r"):
    with open(file_name, rw) as f:
        data = json.load(f)
        return data

# write txt to file
def write_txt_file(file_name, txt, rw="w"):
    with open(file_name, rw) as f:
        f.write(txt)

# Save json to file
def write_json_file(file_name, jsn, rw="w"):
    with open(file_name, rw) as f:
        json.dump(jsn, f, indent=4)

# txt cleaning
def replace_unicode_apostrophe(text):
    text = text.replace('\u2019', '’')
    text = text.replace('\n\n', '')
    return text

def parse_gpt_response_to_json(raw_gpt_output, artifact_id):
    try:
        parsed = json.loads(raw_gpt_output)
        return parsed
    except Exception as e:
        logging.error(f"Failed to parse GPT response for artifact ID {artifact_id}: {e}")
        return None


def safe_json_parse(bad_json_str):
    try:
        return json.loads(bad_json_str)
    except json.JSONDecodeError:
        try:
            # Extract raw values using regex
            output_match = re.search(r'"output"\s*:\s*"(.+?)"\s*,\s*"memory"', bad_json_str, re.DOTALL)
            memory_match = re.search(r'"memory"\s*:\s*"(.*?)"\s*}', bad_json_str, re.DOTALL)

            if not output_match or not memory_match:
                raise ValueError("Pattern not matched")

            output_raw = output_match.group(1)
            memory_raw = memory_match.group(1)

            # Fix unescaped inner quotes ONLY (not those already escaped)
            output_fixed = re.sub(r'(?<!\\)"', r'\\"', output_raw)

            fixed_json = {
                "output": output_fixed,
                "memory": memory_raw
            }
            return fixed_json
        except Exception as e:
            print("Manual fix failed:", e)
            return {}