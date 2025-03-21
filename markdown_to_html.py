import argparse
import markdown

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Convert a Markdown file to an HTML file with a full-page flowing table.")
parser.add_argument("--input", type=str, default="mandarin_study_guide.md", help="Input Markdown file")
parser.add_argument("--output", type=str, default="mandarin_study_guide.html", help="Output HTML file")
args = parser.parse_args()

input_file = args.input
output_file = args.output

# Read the Markdown file
with open(input_file, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert Markdown to HTML with table support
html_content = markdown.markdown(md_content, extensions=["tables"])

# Improved CSS for a full-page flow with a sticky header
css_styles = """
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f8f9fa;
        margin: 40px;
    }
    h1 {
        text-align: center;
        font-size: 28px;
        margin-bottom: 20px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 18px;
        text-align: center;
        background-color: #ffffff;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    thead {
        position: sticky;
        top: 0;
        background-color: #007bff;
        color: white;
        z-index: 100;
    }
    th, td {
        border: 1px solid #dee2e6;
        padding: 12px;
    }
    th {
        font-weight: bold;
        text-transform: uppercase;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    tr:hover {
        background-color: #e2e6ea;
        transition: 0.3s ease-in-out;
    }
</style>
"""

# Wrap HTML content with styling
html_output = f"""
<!DOCTYPE html>
<html>
<head>
    {css_styles}
</head>
<body>
    {html_content}
</body>
</html>
"""

# Write the HTML output
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅ Conversion complete! Output saved to {output_file}")

