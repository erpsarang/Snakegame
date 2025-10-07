"""High level service orchestrating lyric aggregation and generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import random

from .corpus_loader import Corpus, load_corpus
from .sentence_generator import MarkovModel, build_markov_model, generate_sentence


@dataclass
class DireStraitsIdentityService:
    """Facade combining corpus loading and sentence generation."""

    order: int = 2
    model: Optional[MarkovModel] = None
    corpus: Optional[Corpus] = None

    def ingest(self, directory: Path) -> None:
        """Load a corpus from *directory* and update the Markov model."""

        self.corpus = load_corpus(directory)
        self.model = build_markov_model(self.corpus.text, order=self.order)

    def ready(self) -> bool:
        return self.model is not None and bool(self.model.transitions)

    def generate(self, count: int = 1, seed: Optional[int] = None) -> List[str]:
        """Generate *count* sentences inspired by the Dire Straits corpus."""

        if not self.ready():
            raise RuntimeError("service is not ready; call ingest() first")

        if seed is not None:
            random.seed(seed)

        sentences: List[str] = []
        assert self.model is not None  # for type checkers
        for _ in range(count):
            sentences.append(generate_sentence(self.model))
        return sentences


__all__ = ["DireStraitsIdentityService"]
