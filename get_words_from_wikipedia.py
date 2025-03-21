import requests
from bs4 import BeautifulSoup
import sys

# URL of the Wiktionary frequency list
url = "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/1-1000"

# Fetch the page content
response = requests.get(url)
if response.status_code != 200:
    print("Failed to retrieve the page.")
    exit()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find the table
table = soup.find("table", {"class": "wikitable"})
if not table:
    print("Could not find the word list table.")
    exit()

# Get the header row to dynamically find the "Traditional" column
header_row = table.find("tr")
headers = [th.text.strip() for th in header_row.find_all("th")]

# Find the correct column index for Traditional characters
try:
    traditional_index = headers.index("Traditional")
except ValueError:
    print("Could not find the 'Traditional' column in the table.")
    exit()

# Extract only Traditional characters
words = []
for row in table.find_all("tr")[1:]:  # Skip header row
    columns = row.find_all("td")
    if len(columns) > traditional_index:  # Ensure column exists
        traditional_td = columns[traditional_index]
        
        # Extract only the Traditional character inside <span class="Hant">
        traditional_char_span = traditional_td.find("span", class_="Hant")
        if traditional_char_span:
            traditional_char = traditional_char_span.get_text(strip=True)
            words.append(traditional_char)

# Convert list to a comma-separated string
word_list_str = ", ".join(words)

# Get output file from command line arguments, default if not provided
output_file = sys.argv[1] if len(sys.argv) > 1 else "mandarin_traditional_characters.txt"

# Save to a text file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(word_list_str)

print(f"✅ Extracted {len(words)} traditional Mandarin words successfully! Saved to {output_file}")

