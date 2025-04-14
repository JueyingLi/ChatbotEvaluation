import json
import logging

from ..helpers.json_helpers import read_json_file, write_txt_file, parse_gpt_response_to_json
from ..helpers.gpt_helper import connect_to_gpt
from ..helpers.sql_helper import get_data_by_id

# ----------------- Logging Setup -----------------
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# ----------------- System Prompt for GPT -----------------
system_prompt = """
Given a String describing an artifact in the museum, output a JSON object with the following structure:

- The object should contain the following category keys, each with a list of related sentences:
    - "period": Time-related info including dynasties, reigns, stylistic periods, or exact dates
    - "geography": Physical locations: cities, countries, regions, or geographical features
    - "visual_features": Descriptions of materials, artistic styles, iconography, symbols, and techniques
    - "function_context": Purpose, usage, rituals, myths, or religious/philosophical context
    - "architecture": Structural layout, components, design, and spatial elements
    - "artist": The person/culture/group that created this artifact
    - "historical_figures": People involved: rulers, donors, artists, nobles (named or attributed)
- Group the sentences under the correct category based on their meaning.
- If the list of a key is empty, remove the keys from the output.

Return a single valid JSON object containing all the processed artworks.
"""


# ----------------- Helper Functions -----------------

def enrich_transcripts_with_categories(artifact_dict, table_name, artifact_transcripts, lookup_columns):
    """
    For each transcript, retrieve the artifact name, send it to GPT for categorization,
    and store the enriched result in a dictionary.

    Args:
        artifact_dict (dict): Dict to store processed results keyed by artifact ID.
        table_name (str): SQL table to query for metadata.
        artifact_transcripts (list): List of dicts with 'id' and 'transcript_improved'.
        lookup_columns (list): List of metadata column names to retrieve.

    Returns:
        dict: Enriched artifact data keyed by artifact ID.
    """
    for artifact in artifact_transcripts:
        artifact_info = get_data_by_id(table_name, artifact["id"], lookup_columns)
        if artifact_info:
            artifact_name = artifact_info[0]["Object Name"]
            artifact["name"] = artifact_name
            gpt_output = connect_to_gpt(system_prompt, artifact["transcript_improved"])
            parsed_output = parse_gpt_response_to_json(gpt_output, artifact["id"], artifact_name)
            if parsed_output:
                parsed_output["id"] = artifact["id"]
                parsed_output["name"] = artifact_name
                artifact_dict[artifact["id"]] = parsed_output
        else:
            logging.warning(f"No metadata found for artifact ID {artifact['id']}")
    return artifact_dict


def save_sentences_by_category(artifact_data):
    """
    Organize categorized sentences by type and write each category to a text file.

    Args:
        artifact_data (dict): Dictionary of enriched artifacts with sentence categories.
    """
    grouped_sentences = {}

    for _, artifact in artifact_data.items():
        for category, sentence_list in artifact.items():
            if category in ["id", "name"] or not sentence_list:
                continue
            grouped_sentences.setdefault(category, [])
            for sentence in sentence_list:
                entry = f"artifact name: {artifact['name']}\t\t{sentence.strip()}"
                grouped_sentences[category].append(entry)

    for category, sentences in grouped_sentences.items():
        combined_text = "\n\n".join(sentences) + "\n\n"
        output_path = f"../transcript_files/met100_{category}.txt"
        write_txt_file(output_path, combined_text)


# ----------------- Main Execution -----------------

if __name__ == "__main__":
    enriched_artifacts = {}
    sql_table = "metv0.1"
    transcript_input = read_json_file("../transcript_files/transcripts_aft_GPT.json")
    metadata_columns = ["Object Name", "BasicIntro"]

    processed_data = enrich_transcripts_with_categories(enriched_artifacts, sql_table, transcript_input,
                                                        metadata_columns)
    save_sentences_by_category(processed_data)