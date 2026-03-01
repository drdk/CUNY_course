# CUNY Course - RAG and LLM Core Concepts

Course materials and code examples for learning about RAG (Retrieval Augmented Generation) and LLM fundamentals.

## Setup

### Prerequisites
- Python 3.9 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Azure OpenAI API access (or OpenAI API)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/drdk/CUNY_course.git
cd CUNY_course
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up your environment variables in a `.env` file:
```bash
# For Azure OpenAI
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_DEPLOYMENT=your_deployment_name

# Or for OpenAI
OPENAI_API_KEY=your_key_here
```

## Running Code Examples

### Using Poetry

Run Python scripts directly:
```bash
poetry run python CUNY_course/example_code/structured_output.py
poetry run python CUNY_course/example_code/format_errror.py
```

Or activate the virtual environment first:
```bash
poetry shell
python CUNY_course/example_code/structured_output.py
```

### Using Jupyter

Start Jupyter:
```bash
poetry run jupyter notebook
```

## Project Structure

```
CUNY_course/
├── CUNY_course/
│   ├── example_code/       # Python code examples
│   │   ├── structured_output.py
│   │   └── format_errror.py
│   ├── example_data/       # Sample data files
│   │   ├── 10languages.txt
│   │   ├── usconstitution.txt
│   │   └── ...
│   ├── data_types/         # Pydantic models and schemas
│   │   └── person.py
│   ├── outline.md          # Course outline
│   └── links.md            # Useful links and resources
├── pyproject.toml          # Poetry dependencies
└── README.md               # This file
```

## Key Files

- **`structured_output.py`** - Demonstrates how to extract structured data from text using LLMs with Pydantic models
- **`format_errror.py`** - Simple example showing Python data structures
- **`person.py`** - Pydantic models for representing people and relationships
- **`outline.md`** - Full course outline with lecture topics
- **`example_data/`** - Various text files for experimentation

## Development

### Code Formatting
```bash
poetry run black .
```

### Running Tests
```bash
poetry run pytest
```

## Resources

- See [outline.md](CUNY_course/outline.md) for the full course outline and lecture structure
- See [links.md](CUNY_course/links.md) for useful tools and resources

## License

See the LICENSE file for details.
