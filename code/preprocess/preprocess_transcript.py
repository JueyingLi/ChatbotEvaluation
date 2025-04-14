import re
from ..helpers.json_helpers import read_json_file, write_json_file
from ..helpers.gpt_helper import connect_to_gpt

# ----------------- System Prompt for Transcript Improvement -----------------

system_prompt = """
You are an editor preparing museum audio transcripts for an immersive, interactive tour app.
Improve the transcript using the following rules:

1. Remove all speaker tags like “NARRATOR:” or names such as “GÜNTER DREYER:” and integrate the speaker's content into a seamless, third-person narrative. Do not present quoted speech — rewrite all parts as factual, descriptive content.
2. Keep the narrator’s tone — preserve the immersive, personal, and approachable style of audio tours.
3. Break long paragraphs and sentences into short, clear sentences. Each sentence should express one complete idea and be easily understood on its own.
4. Add inline explanations for any noun, person, place, or concept not widely understood by general audiences — but only if you're confident about its meaning. For example, briefly explain who a person is or what a location represents within the sentence.
5. Remove unrelated navigation instructions (e.g. “press the green button” or directions to another exhibit). Focus entirely on the current object and its historical, artistic, and cultural context.
6. Clarify how each detail relates to the object being described. Make sure the reader understands why information is relevant to this artifact.

The result should be an engaging but clear third-person description of the object, optimized for retrievability in a knowledge base for RAG systems. Prioritize clarity, completeness, and factual accuracy. Some repetition is acceptable if it improves understanding.
"""

# ----------------- Helper Functions -----------------

def extract_id_and_transcript():
    """
    Extract IIIF image ID and transcript text from the original artifact JSON.
    The result is a list of {id, transcript} dicts for processing.
    """
    source_path = "../transcript_files/met100.json"
    output_path = "../transcript_files/id_transcript.json"

    raw_data = read_json_file(source_path)
    extracted = []

    for artifact in raw_data.values():
        match = re.search(r"/iiif/(\d+)/", artifact.get("image_url", ""))
        if match:
            image_id = match.group(1)
            extracted.append({
                "id": image_id,
                "transcript": artifact["transcript"]
            })

    write_json_file(output_path, extracted)


def generate_improved_transcripts():
    """
    Send each transcript to GPT for improvement using the system prompt.
    Saves the updated transcripts with a new field `transcript_improved`.
    """
    input_path = "../transcript_files/id_transcript.json"
    output_path = "../transcript_files/transcripts_aft_GPT.json"

    data = read_json_file(input_path)

    for idx, item in enumerate(data):
        if idx % 10 == 0:
            print(f"Processing transcript {idx}...")

        raw_transcript = item["transcript"]
        improved_transcript = connect_to_gpt(system_prompt, raw_transcript)
        item["transcript_improved"] = improved_transcript

    write_json_file(output_path, data)

# ----------------- Entry Point -----------------

if __name__ == "__main__":
    extract_id_and_transcript()
    generate_improved_transcripts()