"""ResNet-18 + CBAM + metric-learning embedding (the M5 hybrid model).

Extracted from notebooks/Mini_Project.ipynb (M5). The only change is that the
ImageNet weights are loaded from torchvision by default instead of a Google
Drive path.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models


class ChannelAttention(nn.Module):
    def __init__(self, channels, reduction=16):
        super().__init__()
        self.shared_mlp = nn.Sequential(
            nn.Linear(channels, channels // reduction),
            nn.ReLU(inplace=True),
            nn.Linear(channels // reduction, channels),
        )

    def forward(self, x):
        avg_pool = F.adaptive_avg_pool2d(x, 1).flatten(1)
        max_pool = F.adaptive_max_pool2d(x, 1).flatten(1)
        attention = torch.sigmoid(self.shared_mlp(avg_pool) + self.shared_mlp(max_pool))
        return x * attention.unsqueeze(-1).unsqueeze(-1)


class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super().__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size=kernel_size,
                              padding=kernel_size // 2, bias=False)

    def forward(self, x):
        avg_map = torch.mean(x, dim=1, keepdim=True)
        max_map = torch.max(x, dim=1, keepdim=True)[0]
        attention = torch.sigmoid(self.conv(torch.cat([avg_map, max_map], dim=1)))
        return x * attention


class CBAM(nn.Module):
    """Convolutional Block Attention Module (channel then spatial attention)."""

    def __init__(self, channels):
        super().__init__()
        self.channel_attention = ChannelAttention(channels)
        self.spatial_attention = SpatialAttention()

    def forward(self, x):
        return self.spatial_attention(self.channel_attention(x))


class M5HybridModel(nn.Module):
    """ResNet-18 backbone -> CBAM -> 256-d L2-normalised embedding -> classifier."""

    def __init__(self, embedding_dim=256, num_species=6, imagenet_weights=True,
                 weights_path=None):
        super().__init__()
        backbone = models.resnet18(weights=None)
        if weights_path is not None:
            backbone.load_state_dict(
                torch.load(weights_path, map_location="cpu", weights_only=True), strict=True)
        elif imagenet_weights:
            backbone = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

        self.backbone = nn.Sequential(
            backbone.conv1, backbone.bn1, backbone.relu, backbone.maxpool,
            backbone.layer1, backbone.layer2, backbone.layer3, backbone.layer4,
        )
        self.cbam = CBAM(512)
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.embedding_head = nn.Sequential(
            nn.Linear(512, 512), nn.ReLU(inplace=True), nn.Dropout(0.3),
            nn.Linear(512, embedding_dim),
        )
        self.classifier = nn.Linear(embedding_dim, num_species)

    def forward(self, x):
        features = self.cbam(self.backbone(x))
        pooled = self.pool(features).flatten(1)
        embedding = F.normalize(self.embedding_head(pooled), p=2, dim=1)
        return {"embedding": embedding, "logits": self.classifier(embedding)}
