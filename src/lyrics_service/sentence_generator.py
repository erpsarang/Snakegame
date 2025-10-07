"""Sentence generation utilities tailored for Dire Straits inspired text."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple
import random
import re


_TOKEN_PATTERN = re.compile(r"[\w']+|[.!?]")


@dataclass
class MarkovModel:
    order: int
    transitions: Dict[Tuple[str, ...], List[str]] = field(default_factory=dict)

    def next_tokens(self, prefix: Tuple[str, ...]) -> List[str]:
        return self.transitions.get(prefix, [])


def tokenise(text: str) -> List[str]:
    """Tokenise text while keeping punctuation as separate tokens."""

    tokens = _TOKEN_PATTERN.findall(text.lower())
    return tokens


def build_markov_model(text: str, order: int = 2) -> MarkovModel:
    if order < 1:
        raise ValueError("order must be >= 1")

    tokens = tokenise(text)
    transitions: Dict[Tuple[str, ...], List[str]] = defaultdict(list)

    if len(tokens) <= order:
        return MarkovModel(order=order, transitions={})

    for i in range(len(tokens) - order):
        prefix = tuple(tokens[i : i + order])
        suffix = tokens[i + order]
        transitions[prefix].append(suffix)

    return MarkovModel(order=order, transitions=dict(transitions))


def _select_start_prefix(model: MarkovModel) -> Tuple[str, ...]:
    candidates = [prefix for prefix in model.transitions if prefix[0][0].isalpha()]
    if not candidates:
        candidates = list(model.transitions.keys())
    return random.choice(candidates) if candidates else tuple()


def _is_sentence_end(token: str) -> bool:
    return token in {".", "!", "?"}


def generate_sentence(
    model: MarkovModel,
    min_tokens: int = 6,
    max_tokens: int = 40,
    seed: Tuple[str, ...] | None = None,
) -> str:
    """Generate a single sentence using the provided Markov model."""

    if not model.transitions:
        raise ValueError("model contains no transitions; feed it with lyrics first")

    prefix = seed or _select_start_prefix(model)
    if not prefix:
        raise ValueError("unable to determine a start prefix for the sentence")

    generated: List[str] = list(prefix)

    while len(generated) < max_tokens:
        suffixes = model.next_tokens(tuple(generated[-model.order :]))
        if not suffixes:
            break
        next_token = random.choice(suffixes)
        generated.append(next_token)
        if len(generated) >= min_tokens and _is_sentence_end(next_token):
            break

    sentence = " ".join(_post_process_tokens(generated))
    return sentence.capitalize()


def _post_process_tokens(tokens: Sequence[str]) -> List[str]:
    """Fix spacing around punctuation."""

    if not tokens:
        return []

    result: List[str] = []
    for token in tokens:
        if token in {".", "!", "?", ","} and result:
            result[-1] = result[-1] + token
        else:
            result.append(token)
    return result


__all__ = ["MarkovModel", "build_markov_model", "generate_sentence", "tokenise"]
