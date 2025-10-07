from pathlib import Path

from src.lyrics_service.sentence_generator import build_markov_model, generate_sentence


def test_generate_sentence_from_sample_corpus():
    sample_text = (
        "Calling Elvis is anybody home. Calling Elvis on the radio. Brothers in arms "
        "walking down the river. Telegraph road is winding to the sea."
    )
    model = build_markov_model(sample_text, order=2)
    sentence = generate_sentence(model, seed=("calling", "elvis"))
    assert isinstance(sentence, str)
    assert sentence
    assert sentence[0].isupper()
