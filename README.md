# CUNY Course - RAG and LLM Core Concepts

Course materials and code examples for learning about RAG (Retrieval Augmented Generation) and LLM fundamentals.

## Setup

### Prerequisites
- Python 3.9 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Optional: Azure/OpenAI API access for the existing structured-output example

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

3. (Optional) Set up your environment variables in a `.env` file for API-based examples:
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
poetry run python CUNY_course/example_code/rag_pipeline/01_data_prep.py
poetry run python CUNY_course/example_code/rag_pipeline/02_chunking.py
poetry run python CUNY_course/example_code/rag_pipeline/03_embedding.py
poetry run python CUNY_course/example_code/rag_pipeline/04_metadata.py
poetry run python CUNY_course/example_code/rag_pipeline/05_retrieval.py
poetry run python CUNY_course/example_code/rag_pipeline/06_generation.py
poetry run python CUNY_course/example_code/rag_pipeline/pipeline_demo.py
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

Open and run:
- `CUNY_course/example_code/rag_pipeline/rag_pipeline_demo.ipynb`

### Gradio Web App (Easiest Sharing)

Run the interactive RAG app locally:

```bash
poetry run python app.py
```

Then open `http://localhost:7860`.

### Deploy for a Small Group (Hugging Face Spaces)

1. Create a new **Gradio** Space.
2. Push this repo (or at least `app.py`, `requirements.txt`, and `CUNY_course/`).
3. In Space **Settings -> Variables and secrets**, add:
	- `AZURE_OPENAI_ENDPOINT`
	- `AZURE_OPENAI_API_KEY`
	- `AZURE_OPENAI_DEPLOYMENT`
4. (Recommended) Set Space visibility to **Private** and invite your users.

The app entrypoint is `app.py` and uses the same RAG pipeline code as the notebook.

## Project Structure

```
CUNY_course/
├── CUNY_course/
│   ├── example_code/       # Python code examples
│   │   ├── structured_output.py
│   │   ├── format_errror.py
│   │   └── rag_pipeline/   # Local in-memory RG pipeline demo
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

## Local RG Pipeline Demo

- Fully local and in-memory (no API keys, no persistence layer)
- Uses open-source libraries only (`sentence-transformers`, `faiss-cpu`, `transformers`, `torch`)
- One Python file per pipeline step plus a combined notebook demo
- Default corpus file: `CUNY_course/example_data/yosemite_guide.md`
- Default chunking: character-based chunks with overlap (word-based strategy still available)

### Classroom Quick Commands

Use the included Makefile for one-command runs:

```bash
make install     # install dependencies
make rg-steps    # run all six RG step scripts
make rg-demo     # run full end-to-end RG demo
make notebook    # open the RG demo notebook
make all         # install + run full end-to-end RG demo
```

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
