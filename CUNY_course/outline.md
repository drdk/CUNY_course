# Lecture Series: RAG and LLM Core Concepts

## Lecture 1: The Core Concepts

### 1. Introduction _(5 min)_
- Who am I and what am I doing here?
- What will we learn during the two lectures?

### 2. The Limits of the LLM _(10 min)_
- Fixed Knowledge
- Generalist
- The context window
- Unpredictable output format
- The LLM is always right (or so it thinks...)

### 3. Introduction to RAG - A Teaser _(10 min)_
- The mental model of RAG
- Common applications
- "RAG Light": Partial or "hidden" RAG in existing products

### 4. Core Concept 1: Structured Output _(25 min)_
- How to make LLMs boring and predictable - and powerful
- **🏋️ EXERCISE:** Define a schema for extracting specific information using LLamaExtract

---

**BREAK** _(10 min)_

---

### 5. Core Concept 2: Embeddings and Semantic Search _(25 min)_
- Understanding the difference between classical and semantic search
- **🏋️ EXERCISE:** Explore embeddings using Semantic Galaxy / Tensorflow
- Embedding Stores and vector databases

### 6. Case Study: The DR SourceSeeker _(20 min)_
- The power of Structured output and Semantic Search in one neat package
- Using structured output to analyze articles and generate metadata
- Using semantic search to find sources and quotes

### 7. Discussion/Poll/Brainstorm _(10 min)_
- **💬 DISCUSSION:** What other products/services/features might be achieved using structured output and/or semantic search?

---

## Lecture 2: The RAG Pipeline

### 8. Short Recap of Previous Lecture _(5 min)_

### 9. Introduction to the RAG Pipeline _(5 min)_

### 10. RAG Step 1: Data Collection and Preparation _(10 min)_
- What is good data for RAG? And what is not?
- Languages
- Parsing and preprocessing

### 11. RAG Step 2: Chunking _(20 min)_
- Know your data
- Chunking strategies
- **💬 DISCUSSION:** What are the pros/cons of each?
- The importance of context
- **🏋️ EXERCISE:** Try out chunking yourself on the US Constitution
- Embedding & saving to DB

### 12. RAG Step 3: Embedding
- Choosing the model
- Choosing the database

### 13. RAG Step 4: Classification and Metadata _(15 min)_
- Definitions
- The importance of metadata
- **📊 POLL:** Why would you need it?
- Metadata that you already have
- Metadata that you can generate
- **💬 DISCUSSION/POLL:** Given examples - what metadata would be important?

---

**BREAK** _(10 min)_

---

### 14. RAG Step 5: Retrieval _(10 min)_
- Query expansion: Humans can be idiots
- **🏋️ EXERCISE/POLL:** Play the role of the Query Expander-LLM - how would you interpret the query?
- Getting results - semantic search in action. How much? how little?
- Reranking

### 15. RAG Step 6: Generation _(10 min)_
- Building the prompt
- Adding citations

### 16. So Now We Have a Full RAG Pipeline - What Could Possibly Go Wrong? _(15 min)_
- **📊 POLL:** What is the weakest link?
- Bad data quality
- Bad chunking strategy
- Bad search results
- Bad generation

### 17. Evaluating RAG: How Do We Know When It Works (and When It Doesn't)? _(10 min)_
- Evaluating retrieval
- Evaluating generation

### 18. Breakout Discussion _(10 min)_
- **💬 DISCUSSION:** What applications do you see in your area?

### 19. Wrap Up _(5 min)_

---

## Resources

### Tools and Visualizations
- **Chunking Visualization:** [ChunkViz](https://chunkviz.up.railway.app/)
- **Embedding Projector:** [TensorFlow Projector](https://projector.tensorflow.org/)
- **Semantic Galaxy:** [HuggingFace Space](https://huggingface.co/spaces/webml-community/semantic-galaxy)


