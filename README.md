# Website to Markdown

## Overview
This script is a simple web crawler that extracts content from a given website and converts it into Markdown format. It supports multi-threaded crawling to improve speed and allows customization of parameters such as maximum workers.

## Features
- Extracts the main content from web pages and converts it to Markdown.
- Crawls internal links.
- Uses multi-threading for faster execution.
- Saves the extracted content to a Markdown file.
- Displays execution time and total pages crawled.

## Installation
Ensure you have Python installed, then install the required dependencies:

```bash
pip install trafilatura beautifulsoup4 requests markdownify
```

## Usage
Run the script with the following command:

```bash
python main.py <start_url> --output_file <filename> --max_workers <number>
```

### Arguments:
- `<start_url>`: The starting URL for crawling.
- `--output_file`: The output file to store the extracted content (default: `crawled_content.md`).
- `--max_workers`: The number of concurrent workers (default: `5`).

### Example:
```bash
python main.py "https://example.com/docs" --output_file output.md --max_workers 10
```

## Output
- The script crawls the given URL and its internal links.
- Extracted content is stored in the specified Markdown file.
- At the end of execution, the script prints the total time taken and the number of pages crawled.

## License
This project is open-source and available under the MIT License.

## Contributions
Feel free to submit pull requests or report issues if you find any bugs or have suggestions for improvements.

