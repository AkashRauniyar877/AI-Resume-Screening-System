# AI Resume Screening - Experimentation & Research Notebooks

This directory contains Jupyter Notebooks used for model exploration, algorithm prototyping, feature engineering, NLP validation, and evaluation of the AI Resume Screening System.

## Notebook Structure

- `01_resume_data_cleaning.ipynb` - Dataset loading, data cleaning, and resume corpus exploratory data analysis.
- `02_nlp_preprocessing.ipynb` - Text normalization, stopword removal, lemmatization, and tokenization.
- `03_tfidf_matching.ipynb` - TF-IDF vectorization and cosine similarity matching experimentations.
- `04_skill_extraction.ipynb` - Skill extraction rules, entity recognition, and dictionary matching.
- `05_experience_extraction.ipynb` - Experience regex patterns, date range extraction, and duration calculation.
- `06_final_candidate_ranking.ipynb` - Multi-criteria candidate ranking and score aggregation.
- `07_semantic_matching.ipynb` - Transformer embeddings and semantic vector similarity.
- `08_hybrid_matching.ipynb` - Hybrid scoring formula tuning (TF-IDF + Semantic + Skill + Experience).
- `09_resume_information_extraction.ipynb` - Name, email, phone, and education structured field extraction.
- `10_job_description_analysis.ipynb` - Parsing and requirement extraction from Job Descriptions.
- `11_model_evaluation.ipynb` - Performance metrics, benchmark validation, and precision evaluation.

> [!NOTE]  
> Production AI logic is deployed in the `ai_engine/` package. These notebooks serve as research documentation and historical experiment validation.
