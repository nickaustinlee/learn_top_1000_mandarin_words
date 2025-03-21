import os
import time
import random
import argparse
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY is not set! Please set it in your environment.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Generate a Markdown study guide for Mandarin words.")
parser.add_argument("--input", type=str, default="mandarin_traditional_characters.txt", help="Input file containing Mandarin words")
parser.add_argument("--output", type=str, default="mandarin_study_guide.md", help="Output Markdown file")
args = parser.parse_args()

input_file = args.input
output_file = args.output

# Read the list of Traditional words from file
with open(input_file, "r", encoding="utf-8") as f:
    traditional_words = f.read().split(", ")  # Ensure proper splitting

total_words = len(traditional_words)
batch_size = 20  # Process words in batches of 20
max_workers = 5  # Limit parallel threads to 5

# Global tracking for batch order
results_dict = {}  # Stores completed batches
next_batch_to_write = 0  # Tracks which batch should be written next
processed_words = 0  # Global counter for tracking progress
lock = Lock()  # Ensures thread safety
progress_lock = Lock()  # Lock to ensure thread-safe updates

# Function to generate multiple Markdown rows for a batch of words
def generate_markdown_batch(batch_index, words, max_retries=5):
    words_list = ", ".join(words)
    
    prompt_text = f"""
    You are an advanced Mandarin language assistant. Generate a Markdown table for the following Traditional Chinese words:
    {words_list}
    
    **For each word, provide:**
    - Its **Simplified equivalent**
    - Its **Pinyin**
    - Its **English Meaning**
    - An **Example Sentence** (both Traditional and Simplified)
    - The **Pinyin** for the sentence
    - The **Sentence Meaning** in English

    **Return only the Markdown rows**, formatted exactly like this:
    | Traditional | Simplified | Pinyin | English Meaning | Example Sentence (Traditional) | Example Sentence (Simplified) | Pinyin for Sentence | Sentence Meaning |
    |------------|------------|--------|-----------------|--------------------------------|--------------------------------|----------------------|------------------|
    | 你好 | 你好 | nǐ hǎo | Hello | 你好嗎？ | 你好吗？ | Nǐ hǎo ma? | How are you? |
    | 水 | 水 | shuǐ | Water | 我喝水。 | 我喝水。 | Wǒ hē shuǐ. | I drink water. |
    
    **Do NOT add extra formatting (no markdown code blocks like ```markdown```).**
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt_text}],
                max_tokens=2048  # Increased for batch processing
            )
            markdown_rows = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if markdown_rows.startswith("```markdown"):
                markdown_rows = markdown_rows[10:]
            if markdown_rows.endswith("```"):
                markdown_rows = markdown_rows[:-3]
            
            print(f"✅ [Batch {batch_index}] Processed {len(words)} words.")

            # Store the result in dictionary and try writing to file
            with lock:
                results_dict[batch_index] = markdown_rows
                write_batches_to_file()

            return batch_index
        except Exception as e:
            print(f"⚠️ [Batch {batch_index}] Retry {attempt + 1}/{max_retries}: {e}")
            time.sleep(1 + random.uniform(0, 2))  # Backoff to avoid rate limits

    print(f"❌ [Batch {batch_index}] Failed after {max_retries} retries.")
    return batch_index

# Function to write completed batches in correct order
def write_batches_to_file():
    global next_batch_to_write, processed_words

    with open(output_file, "a", encoding="utf-8") as f:
        while next_batch_to_write in results_dict:
            batch_index = next_batch_to_write
            rows = results_dict.pop(batch_index)

            row_lines = rows.split("\n")
            clean_rows = [
                line.strip() for line in row_lines
                if not line.startswith("| Traditional") and not line.startswith("|---")
            ]
            
            row_counter = batch_index * batch_size + 1  # Ensure row numbering stays correct
            for row in clean_rows:
                row_parts = row.split("|")
                row_parts = [part.strip() for part in row_parts if part.strip()]
                if len(row_parts) > 1:
                    formatted_row = f"| {row_counter} | " + " | ".join(row_parts) + " |"
                    f.write(formatted_row + "\n")
                    row_counter += 1

            # Update progress safely
            with progress_lock:
                processed_words += len(clean_rows)
                progress_percentage = min((processed_words / total_words) * 100, 100) #May be off by 1 so I just cap it at 100%
                print(f"✅ [Batch {batch_index}] Written to file. Progress: {progress_percentage:.2f}%")

            next_batch_to_write += 1  # Move to the next batch

# Ensure the file starts fresh with the header
header = """# Mandarin Word List with Example Sentences

| # | Traditional | Simplified | Pinyin | English Meaning | Example Sentence (Traditional) | Example Sentence (Simplified) | Pinyin for Sentence | Sentence Meaning |
|---|------------|------------|--------|-----------------|--------------------------------|--------------------------------|----------------------|------------------|
"""

with open(output_file, "w", encoding="utf-8") as f:
    f.write(header)

# Use a single ThreadPoolExecutor for all batches
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {
        executor.submit(generate_markdown_batch, batch_start // batch_size, traditional_words[batch_start:batch_start + batch_size]): batch_start // batch_size
        for batch_start in range(0, total_words, batch_size)
    }

    # Wait for all tasks to complete
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"❌ Error processing batch {futures[future]}: {e}")

print(f"\n🎉 All words processed! Markdown file updated successfully: {output_file}")
