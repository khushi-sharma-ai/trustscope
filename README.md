# TrustScope

Pooled AUROC for LLM answer-reliability signals hides within-question performance. This repo serves the saved results and a single-page view of them, so the findings can be shown locally.

## Run it locally

Python 3.10 or newer is required.

```
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open http://127.0.0.1:8000

The app only reads saved results. It does not rerun the model.

## Folder layout

- `data/results_auroc.csv`: pooled, within-question and between-question AUROC for each signal (from the Kaggle notebook).
- `data/confidently_wrong.json` (optional): confidently wrong examples, as a list of objects with `question`, `model_answer` and `correct_answer`.
- `backend/app.py`: FastAPI server that serves the data and the frontend.
- `frontend/index.html`: the results page, with no external dependencies.

## Method (short)

Model: Qwen2.5-1.5B-Instruct, fp16. Data: 500 TriviaQA validation questions, 10 sampled answers per question (temperature 1.0, top-p 0.95). Answers are grouped into meaning clusters using a bidirectional NLI check. Signals: mean token log-probability, answer agreement, semantic entropy, and two linear probes on hidden states (one on the answer, one on the question alone). Within-question AUROC compares correct and incorrect answers to the same question; between-question AUROC compares across questions.

## Limitations

One model, one dataset, 500 questions. Grading uses normalized answer aliases, so some correct answers may be marked wrong.
