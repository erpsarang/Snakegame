"""Utilities for loading and normalising Dire Straits lyric corpora.

The loader is intentionally flexible: it can read raw text files, JSON
collections or even CSV exports.  The goal of the module is to aggregate the
lyrics into one clean block of text that can be consumed by the sentence
generator.

Because we cannot ship the copyrighted lyrics as part of the repository, the
loader focuses on providing helpers to ingest lyrics that the user collected on
their own.  In addition, it offers lightweight pre-processing helpers that aim
at keeping stylistic markers (nautical imagery, references to the road, etc.)
which are key to Dire Straits' identity.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence
import json
import re


DEFAULT_EXTENSIONS = {".txt", ".json", ".csv"}


@dataclass
class Corpus:
    """Container returned by :func:`load_corpus`.

    Attributes
    ----------
    songs:
        A list of song titles.
    text:
        The aggregated and lightly normalised corpus.
    """

    songs: List[str]
    text: str


def _normalise_whitespace(text: str) -> str:
    """Collapse redundant whitespace while keeping stanza separation."""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def _load_text_file(path: Path) -> str:
    with path.open("r", encoding="utf-8") as handle:
        return handle.read()


def _load_json_file(path: Path) -> str:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if isinstance(payload, dict):
        candidates: Iterable[str] = payload.values()
    elif isinstance(payload, list):
        candidates = payload
    else:
        raise TypeError("Unsupported JSON structure for lyrics corpus")

    collected: List[str] = []
    for value in candidates:
        if isinstance(value, str):
            collected.append(value)
        elif isinstance(value, dict):
            collected.extend(str(v) for v in value.values())
        else:
            collected.append(str(value))
    return "\n".join(collected)


def _load_csv_file(path: Path) -> str:
    with path.open("r", encoding="utf-8") as handle:
        rows = handle.read().splitlines()

    if not rows:
        return ""

    # Skip header if present
    if "," in rows[0]:
        rows = rows[1:]
    return "\n".join(rows)


def _collect_songs_from_text(text: str) -> List[str]:
    """Best-effort extraction of song titles from inline metadata."""

    song_pattern = re.compile(r"^\s*(?:#|title:)(?P<title>.+)$", re.IGNORECASE)
    songs = []
    for line in text.splitlines():
        match = song_pattern.match(line)
        if match:
            songs.append(match.group("title").strip())
    return songs


def load_corpus(
    directory: Path,
    extensions: Sequence[str] | None = None,
) -> Corpus:
    """Load every lyric file contained in *directory*.

    Parameters
    ----------
    directory:
        Path to a folder containing the lyric files.
    extensions:
        Optional whitelist of file extensions.  If omitted the loader falls back
        to :data:`DEFAULT_EXTENSIONS`.
    """

    exts = set(extensions or DEFAULT_EXTENSIONS)
    if not directory.exists():
        raise FileNotFoundError(directory)

    aggregated_texts: List[str] = []
    song_titles: List[str] = []

    for path in sorted(directory.rglob("*")):
        if path.is_dir():
            continue
        if path.suffix.lower() not in exts:
            continue

        if path.suffix.lower() == ".txt":
            text = _load_text_file(path)
        elif path.suffix.lower() == ".json":
            text = _load_json_file(path)
        elif path.suffix.lower() == ".csv":
            text = _load_csv_file(path)
        else:
            # Guard for callers that pass custom extension sets.
            text = _load_text_file(path)

        aggregated_texts.append(text)
        song_titles.extend(_collect_songs_from_text(text))

    raw_corpus = "\n\n".join(aggregated_texts)
    normalised_corpus = _normalise_whitespace(raw_corpus)
    return Corpus(songs=song_titles, text=normalised_corpus)


__all__ = ["Corpus", "load_corpus"]
