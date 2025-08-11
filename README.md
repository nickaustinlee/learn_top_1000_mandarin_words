# Mandarin Study Guide Automation

This project gets the most common Mandarin words from Wikipedia, enriches them with GenAI (GPT), puts the information into markdown, and produces a nicely formatted HTML page for your studies.

I created this study guide to find an efficient way to learn the most Chinese words with the least effort. Instead of focusing on character memorization (which is somewhat boring), this guide focuses on character combinations that create the most popular words. With pinyin and repeated exposure to characters, the student should be able to begin improving character recognition naturally.

Fun fact: Figures vary, but it's estimated that you'll have an 80% understanding of Chinese after learning the first 1000 most common words. Continuing to 3000 words will get you to ~90%, and continuing to 7000 will get you to ~95%. To get to full fluency, you'd need 10,000+ words. Characters and words are not the same --words are composed of combinations of a narrow set of characters. Students should grow their character recognition and word recognition.

Disclaimer: The code was last tested with OpenAI's APIs in March 2025 and GPT-4o. If their API changes, you may need to adjust the code.

Web Version of Study Guides: 

[Words 0-1000](https://nickaustinlee.github.io/learn_top_1000_mandarin_words/ready_made_study_guides/mandarin_study_guide_0_1000.html)

[Words 1001-2000](https://nickaustinlee.github.io/learn_top_1000_mandarin_words/ready_made_study_guides/mandarin_study_guide_1001_2000.html)

[Words 2001-3000](https://nickaustinlee.github.io/learn_top_1000_mandarin_words/ready_made_study_guides/mandarin_study_guide_2001_3000.html)

## 🚀 Features
- **Obtains the Top 1000 Mandarin words** from [Wikipedia](https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/1-1000)
- **Generates structured Markdown** study guides with translations and example sentences
- **Converts Markdown into HTML** with a **fixed header and styled table**
- **Automates the entire process** with a single command

---

## 🛠️ Installation

### **Install Python**
Ensure you have **Python 3.13+** installed. If not, download it from [python.org](https://www.python.org/downloads/).

### **Install Required Libraries**
Run the following command to install all dependencies:

```bash
pip install beautifulsoup4 requests openai markdown
```

If you encounter issues with compatibility, you can use this to create a virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

---

## 📌 Usage

- **Ensure your OpenAI API key is set** as an environment variable before running the Markdown generator.

```bash
export OPENAI_API_KEY="<your_key_here>"
```

Run everything in order with a single command:

```bash
python run_all.py
```

This will:
1. **Scrape Mandarin words from Wikipedia** (`get_words_from_wikipedia.py`)
2. **Generate a Markdown study guide** (`mandarin_markdown_generator_parallel.py`)
3. **Convert Markdown to a formatted HTML page** (`markdown_to_html.py`)
4. **Open the final study guide in a web browser**

Note: Call run_all.py sparingly; each run of mandarin_markdown_generator_parallel.py will incur OpenAI API costs.

Alternatively, you can run each step manually as described below.

### **Step 1: Scrape Mandarin Words from Wikipedia**
```bash
python get_words_from_wikipedia.py
```
- This script scrapes a list of Mandarin words from Wikipedia and saves them to `mandarin_traditional_characters.txt`. You can also specify the output file as an input argument. 

### **Step 2: Generate a Markdown Study Guide**
```bash
python mandarin_markdown_generator_parallel.py --input mandarin_traditional_characters.txt --output mandarin_study_guide.md
```
- This script processes the words, fetches translations, and generates a **formatted Markdown study guide**.

### **Step 3: Convert Markdown to HTML**
```bash
python markdown_to_html.py --input mandarin_study_guide.md --output mandarin_study_guide.html
```
- Converts the Markdown study guide into a **styled HTML webpage**.

---

## 🎯 Final Output
Once all steps are completed, your formatted **HTML study guide** will be available as:
```
mandarin_study_guide.html
```
Open it in any browser to see the **styled table with sticky headers**.

---

## 💡 Notes

- You can modify the **CSS in `markdown_to_html.py`** to customize the table’s appearance.

---

## 🏆 Done! Enjoy Your Mandarin Study Guide! 🎉


