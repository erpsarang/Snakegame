"""Utilities to build Dire Straits inspired text generation services."""

from .corpus_loader import Corpus, load_corpus
from .sentence_generator import MarkovModel, build_markov_model, generate_sentence
from .service import DireStraitsIdentityService

__all__ = [
    "Corpus",
    "load_corpus",
    "MarkovModel",
    "build_markov_model",
    "generate_sentence",
    "DireStraitsIdentityService",
]
