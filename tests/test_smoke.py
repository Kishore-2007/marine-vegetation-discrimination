"""Smoke tests (run: pytest -q). Uses random data only; no datasets required."""
import torch
from marine_veg import M5HybridModel, combined_loss, decision_engine


def test_model_shapes():
    model = M5HybridModel(imagenet_weights=False).eval()
    with torch.no_grad():
        out = model(torch.randn(4, 3, 224, 224))
    assert out["embedding"].shape == (4, 256)
    assert out["logits"].shape == (4, 6)
    assert torch.allclose(out["embedding"].norm(dim=1), torch.ones(4), atol=1e-5)


def test_combined_loss_is_finite():
    labels = torch.tensor([0] * 4 + [1] * 4 + [2] * 4 + [3] * 4 + [4] * 4 + [5] * 4)
    emb = torch.nn.functional.normalize(torch.randn(24, 256), dim=1)
    loss = combined_loss({"embedding": emb, "logits": torch.randn(24, 6)}, labels)
    assert torch.isfinite(loss)


def test_decision_never_authorises_removal():
    probs = {"Sargassum muticum": 0.99, "Ericaria selaginoides": 0.01}
    d = decision_engine("Sargassum muticum", probs)
    assert d["automatic_removal_authorized"] is False
    assert d["human_verification"] == "MANDATORY"
    assert d["review_priority"] == "HIGH"
