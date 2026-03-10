.PHONY: install rg-steps rg-demo notebook all

install:
	poetry install

rg-steps:
	poetry run python CUNY_course/example_code/rag_pipeline/01_data_prep.py
	poetry run python CUNY_course/example_code/rag_pipeline/02_chunking.py
	poetry run python CUNY_course/example_code/rag_pipeline/03_embedding.py
	poetry run python CUNY_course/example_code/rag_pipeline/04_metadata.py
	poetry run python CUNY_course/example_code/rag_pipeline/05_retrieval.py
	poetry run python CUNY_course/example_code/rag_pipeline/06_generation.py

rg-demo:
	poetry run python CUNY_course/example_code/rag_pipeline/pipeline_demo.py

notebook:
	poetry run jupyter notebook CUNY_course/example_code/rag_pipeline/rag_pipeline_demo.ipynb

all: install rg-demo
