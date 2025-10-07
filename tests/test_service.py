from pathlib import Path

import pytest

from src.lyrics_service.service import DireStraitsIdentityService


@pytest.fixture()
def sample_corpus(tmp_path: Path) -> Path:
    text = """# Calling Elvis
Calling Elvis is anybody home

# Brothers in Arms
Brothers in arms laying down their lives
"""
    corpus_dir = tmp_path / "lyrics"
    corpus_dir.mkdir()
    (corpus_dir / "dire_straits.txt").write_text(text, encoding="utf-8")
    return corpus_dir


def test_service_ingest_and_generate(sample_corpus: Path):
    service = DireStraitsIdentityService(order=2)
    service.ingest(sample_corpus)
    assert service.ready()
    sentences = service.generate(count=2, seed=42)
    assert len(sentences) == 2
    assert all(sentence for sentence in sentences)
