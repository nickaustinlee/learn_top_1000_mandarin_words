import subprocess

# Define script paths
get_words_script = "get_words_from_wikipedia.py"
markdown_generator_script = "mandarin_markdown_generator_parallel.py"
html_converter_script = "markdown_to_html.py"

# Run get_words_from_wikipedia.py
print("🚀 Running Wikipedia scraper...")
subprocess.run(["python", get_words_script], check=True)
print("✅ Completed: Wikipedia scraper")

# Run mandarin_markdown_generator_parallel.py
print("🚀 Generating Markdown from Mandarin words...")
subprocess.run(["python", markdown_generator_script], check=True)
print("✅ Completed: Markdown generation")

# Run markdown_to_html.py
print("🚀 Converting Markdown to HTML...")
subprocess.run(["python", html_converter_script], check=True)
print("✅ Completed: Markdown to HTML conversion")

print("\n🎉 All steps completed successfully!")

