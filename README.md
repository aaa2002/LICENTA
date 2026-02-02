# LICENTA


> **Important:** Make sure you are on the `official/v3` branch before following the steps below:
> ```bash
> cd /home/alex/VSC/LICENTA
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
cd /home/alex/VSC/LICENTA/Webapp/backend

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
cd /home/alex/VSC/LICENTA/Webapp/ttl-graph-app
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
cd /home/alex/VSC/LICENTA/take2
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
cd /home/alex/VSC/LICENTA/take2
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

### 4.2. Run Ollama as a systemd service (recommended)

To keep Ollama running automatically in the background on Linux, create a custom systemd service.  
Run:

```bash
sudo nano /etc/systemd/system/ollama-local.service
```

Paste something like:

```ini
[Unit]
Description=Ollama LLM Server
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME
ExecStart=/usr/bin/ollama serve
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Replace `YOUR_USERNAME` and `ExecStart` path if `ollama` is installed somewhere else (run `which ollama` to check).

Then enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama-local
sudo systemctl start ollama-local

# Check status and logs
systemctl status ollama-local
journalctl -u ollama-local -f
```

With this in place, Ollama will start on boot and stay running in the background, so all scripts in `take2/` and the rest of the project can use the `llama3` model without manual intervention.
