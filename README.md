# LICENTA


> **Important:** Make sure you are on the `official/v3` branch before following the steps below:
> ```bash
> git checkout official/v3
> ```

---

## Prerequisites

- **OS**: Linux
- **Python**: 3.10+ (recommended to use a virtualenv)
- **Node.js + npm**: recent LTS (for the Vue frontend)
- **Ollama**: running locally on `http://localhost:11434`

Install Ollama from the official site and ensure it works:

```bash
curl https://ollama.com/install.sh | sh    # or follow the manual steps from their site
ollama --version
```

Pull the default model used by this project (LLaMA 3):

```bash
ollama pull llama3
```

---

## 1. Running the Django backend

Backend code lives in `Webapp/backend/` (Django project `ttlbackend` and app `graph`).

```bash
cd /Webapp/backend

# (optional but recommended)
python -m venv .venv
source .venv/bin/activate

pip install django djangorestframework django-cors-headers

# Apply migrations and start the dev server
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

The API will be available on `http://localhost:8000/`.

---

## 2. Running the Vue webapp (frontend)

Frontend code lives in `Webapp/ttl-graph-app/` (Vue 3 + Vite).

```bash
cd /Webapp/ttl-graph-app
npm install
npm run dev
```

By default Vite exposes the app on `http://localhost:5173/` (check the terminal output).  
Make sure the Django backend is running on `http://localhost:8000` so the frontend can reach the API.

---

## 3. LLM pipeline & scraper (Ollama‑based backend logic)

The more advanced LLM logic and scraping utilities live under `take2/`.  
They use **Ollama** via HTTP on `http://localhost:11434` and expect the `llama3` model to be available.

Before running anything in `take2/`, make sure:

- Ollama is installed and running (see next section).
- You have Python dependencies installed (example, from one of the requirements files):

```bash
cd /take2
python -m venv .venv
source .venv/bin/activate

pip install -r agents/scrape/requirements.txt
pip install requests spacy transformers torch duckduckgo-search nltk SPARQLWrapper wikipedia streamlit
```

Example entry points you may want to run from `take2/`:

- `main.py` – orchestrator for the pipeline
- `streamlit_app/streamlit_app.py` – Streamlit UI for experiments
- `agents/classic/trainer.py` – training classic models

Run Streamlit UI (example):

```bash
cd /take2
source .venv/bin/activate
streamlit run streamlit_app/streamlit_app.py
```

Make sure Ollama is up before using any of the LLM‑powered scripts.

---

## 4. Running Ollama and keeping it alive on Linux

### 4.1. Quick start (manual)

After installing Ollama and pulling `llama3`:

```bash
# start the Ollama server in the foreground
ollama serve
```

or simply run a model once (which starts the server too):

```bash
ollama run llama3
```

The project’s code expects Ollama at:

- **URL**: `http://localhost:11434/api/generate`
- **Model name**: `llama3`

For development it is usually enough to keep `ollama serve` running in a terminal.  
If you want it to start automatically on boot, you can still create a custom `systemd` service yourself following the official Ollama/Linux documentation.

---

## 5. Delta tables and Apache Spark usage

Parts of the `take2/` pipeline (for example `dataset_to_delta.py`, `silver_hop.py`, and the `streamlit_app`) use:

- **Apache Spark** (via `pyspark`) for large‑scale data processing.
- **Delta Lake** tables (via the `delta-spark` Python package) stored under the `take2/delta/` folder (`all_news`, `fake_news`, `real_news`, `silver_cleaned_news`).

These are mainly used to **prepare and clean the fake/real news datasets** and to feed the Streamlit exploration app.  
If you only want to **run the webapp + Django backend + Ollama‑powered inference on new claims**, you do **not** need Spark/Delta; the precomputed Delta tables already exist in `take2/delta/`.

You only need Spark/Delta if:

- You want to **rebuild or modify** the datasets (e.g. run `dataset_to_delta.py` or `silver_hop.py`).
- You want to run the **full Streamlit app** that reads directly from the Delta tables using Spark.

To install Spark/Delta dependencies (inside the same `take2` virtualenv):

```bash
pip install pyspark delta-spark
```

Useful references:

- **Apache Spark**: https://spark.apache.org/
- **Delta Lake (delta-spark)**: https://delta.io/
