import json

import google.generativeai as genai

from config import GEMINI_API_KEY
from prompts.prompts import FACT_EXTRACTION_PROMPT
from tools.chunker import chunk_text

genai.configure(api_key=GEMINI_API_KEY)


def extract_chunk(chunk):

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(FACT_EXTRACTION_PROMPT + "\n\n" + chunk)

    cleaned = response.text.replace("```json", "").replace("```", "").strip()

    return json.loads(cleaned)


def merge_facts(results):

    merged = {}

    for result in results:
        for key, value in result.items():
            if value in [None, "", [], {}, "MISSING"]:
                continue

            if key not in merged:
                merged[key] = value

            else:
                # Merge lists
                if isinstance(value, list) and isinstance(merged[key], list):
                    merged[key] = list(set(merged[key] + value))

    return merged


def extract_facts(text):

    chunks = chunk_text(text, chunk_size=12000)

    print(f"\nTotal chunks: {len(chunks)}")

    results = []

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}")

        try:
            result = extract_chunk(chunk)

            results.append(result)

        except Exception as e:
            print(f"Chunk {i + 1} failed: {e}")

            results.append({"error": str(e)})

    return merge_facts(results)
