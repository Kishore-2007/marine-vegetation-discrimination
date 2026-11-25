# Architecture and design

## System architecture

Two separate pipelines: training (dataset, split, train, evaluate, save) and inference (preprocess, features,
attention, classify, ecological status, output, human review).

![Architecture](../assets/architecture.png)

## Use cases

![User use cases](../assets/usecase_user.png)
![Admin use cases](../assets/usecase_admin.png)

## Class diagram

![Class diagram](../assets/class_diagram.png)

## Sequence diagrams

Prediction flow:

![Prediction](../assets/sequence_prediction.png)

Training and evaluation (the test set is used only for final evaluation):

![Training](../assets/sequence_training.png)

Prediction and human review (a model prediction alone never authorises removal):

![Human review](../assets/sequence_human_review.png)

## Model

```mermaid
flowchart TD
    X[Input 3x224x224] --> R[ResNet-18 conv1..layer4 -> 512 x 7 x 7]
    R --> C1[CBAM channel attention]
    C1 --> C2[CBAM spatial attention 7x7]
    C2 --> P[Global average pool -> 512]
    P --> H[Linear 512-512, ReLU, Dropout 0.3, Linear 512-256]
    H --> N[L2 normalise -> embedding]
    N --> L[Linear 256-6 -> logits]
    N --> S[Cosine similarity to species prototypes]
```
