# Dire Straits Identity Forge

This project provides a lightweight service that helps you craft original
sentences inspired by Dire Straits' lyrical universe. Because the band's lyrics
are copyrighted we do not ship the corpus directly. Instead, the repository
contains utilities to ingest lyrics that you collected yourself and to generate
new sentences that highlight the group's characteristic storytelling, nautical
imagery, and road-weary tone.

## Project layout

```
.
├── app.py                   # FastAPI application exposing /ingest and /generate
├── requirements.txt         # Runtime dependencies
└── src/
    └── lyrics_service/
        ├── corpus_loader.py       # Helpers to load local lyric files
        ├── sentence_generator.py  # Markov-chain-based generator
        └── service.py             # High level orchestration façade
```

## Getting started

1. **Install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Collect the lyrics**

   Place your legally obtained Dire Straits lyrics in a folder. The loader
   accepts `.txt`, `.json` and `.csv` files. You can organise the files in any
   nested directory structure.

3. **Start the service**

   ```bash
   uvicorn app:app --reload
   ```

4. **Ingest the lyrics**

   ```bash
   curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" \
        -d '{"directory": "path/to/your/lyrics"}'
   ```

5. **Generate new sentences**

   ```bash
   curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" \
        -d '{"count": 3}'
   ```

   The service responds with an array of freshly generated sentences and, when
   available, the song titles inferred from the corpus.

## Running tests

```bash
pytest
```

## Notes on lyric usage

Please make sure that you comply with copyright law when collecting and storing
lyrics. The generator is designed to produce short, original phrases that evoke
Dire Straits' identity without reproducing the original texts verbatim.
