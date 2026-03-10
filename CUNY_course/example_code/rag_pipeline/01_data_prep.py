from CUNY_course.example_code.rag_pipeline import (
    data_prep_step as _data_prep_step,
)

prepare_documents = _data_prep_step.prepare_documents
run_demo = _data_prep_step.run_demo


if __name__ == "__main__":
    run_demo()
