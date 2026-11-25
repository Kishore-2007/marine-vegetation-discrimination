"""Metric-learning losses used by the M5 hybrid model.

Total loss = CE + 0.5 * batch-hard triplet (margin 0.3) + 0.1 * SupCon (T = 0.07).
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

classification_loss = nn.CrossEntropyLoss()


def batch_hard_triplet_loss(embeddings, labels, margin=0.3):
    """Hardest positive and hardest negative for every sample in the batch."""
    distances = torch.cdist(embeddings, embeddings, p=2)
    labels = labels.view(-1, 1)
    same_class = labels.eq(labels.T)
    identity = torch.eye(len(labels), dtype=torch.bool, device=labels.device)

    positive_mask = same_class & ~identity
    negative_mask = ~same_class

    hardest_positive = distances.masked_fill(~positive_mask, float("-inf")).max(dim=1)[0]
    hardest_negative = distances.masked_fill(~negative_mask, float("inf")).min(dim=1)[0]

    valid = positive_mask.any(dim=1) & negative_mask.any(dim=1)
    if not valid.any():
        return embeddings.sum() * 0.0
    return F.relu(hardest_positive[valid] - hardest_negative[valid] + margin).mean()


def supervised_contrastive_loss(embeddings, labels, temperature=0.07):
    embeddings = F.normalize(embeddings, p=2, dim=1)
    labels = labels.view(-1, 1)

    similarity = torch.matmul(embeddings, embeddings.T) / temperature
    self_mask = torch.eye(embeddings.shape[0], dtype=torch.bool, device=embeddings.device)
    positive_mask = labels.eq(labels.T) & ~self_mask

    logits = similarity.masked_fill(self_mask, float("-inf"))
    log_prob = logits - torch.logsumexp(logits, dim=1, keepdim=True)

    positive_count = positive_mask.sum(dim=1)
    valid = positive_count > 0
    if not valid.any():
        return embeddings.sum() * 0.0

    positive_log_prob = (log_prob.masked_fill(~positive_mask, 0.0).sum(dim=1)
                         / positive_count.clamp(min=1))
    return -positive_log_prob[valid].mean()


def combined_loss(outputs, labels, w_triplet=0.5, w_supcon=0.1):
    ce = classification_loss(outputs["logits"], labels)
    tri = batch_hard_triplet_loss(outputs["embedding"], labels)
    con = supervised_contrastive_loss(outputs["embedding"], labels)
    return ce + w_triplet * tri + w_supcon * con
