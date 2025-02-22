# Website to Markdown

## Overview
This script is a simple web crawler that extracts content from a given website and converts it into Markdown format. It supports multi-threaded crawling to improve speed and allows customization of parameters such as maximum workers.

## Features
- Extracts the main content from web pages and converts it to Markdown.
- Crawls internal links.
- Uses multi-threading for faster execution.
- Saves the extracted content to a Markdown file.

## Installation
Ensure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage
Run the script with the following command:

```bash
python main.py <start_url> --output_file <filename> --max_workers <number>
```

Or with docker
```bash
docker run --rm -v ./:/tmp/out cuongnb14/web2md:1.0.1 <start_url> --output_file /tmp/out.md
```

### Arguments:
- `<start_url>`: The starting URL for crawling.
- `--output_file`: The output file to store the extracted content (default: `crawled_content.md`).
- `--max_workers`: The number of concurrent workers (default: `5`).
- `--rendering`: Use playwright to render page
- `--only-main`: Only use playwright for first page

### Example:
```bash
python main.py "https://example.com/docs" --output_file output.md --max_workers 10
```
