# Methodology

## Study workflow

The project was developed through six milestones (M1–M6). ECU-MSS-2 supported the initial four-class vegetation/background experiments and exploratory Grad-CAM analysis. The IMO Dataset supported a separate ecological classification experiment and the later six-species hybrid model.

## M1–M3: ECU-MSS-2

ECU-MSS-2 contains four image categories: Amphibolis, Background, Halophila and Posidonia. The work audited archive integrity and duplicates, built grouped train/validation manifests, trained a ResNet18 baseline, and inspected Grad-CAM maps on selected validation examples.

The dataset does not provide invasive/native labels or segmentation masks. Therefore these milestones do not establish ecological status classification or pixel-level localization.

## M4: Binary ecological experiment

The IMO Dataset was filtered to six selected species and mapped to Native/Invasive labels for the Galicia, Spain study context. A pretrained ResNet18 was trained as a binary classifier. The independent test partition was evaluated once and then sealed.

M4 independent test results (422 images): accuracy 86.02%, balanced accuracy 86.57%, macro F1 0.86. Error analysis found substantial false invasive alarms associated with Saccorhiza polyschides. This is an initial experiment with dataset/acquisition limitations, not a validated removal classifier.

## M5: Six-species hybrid model

The six-species model combines a ResNet18 backbone, CBAM channel/spatial attention, a normalized 256-dimensional embedding and a six-class prediction head. Training used classification loss together with triplet and supervised-contrastive objectives.

M5 used a development-only train/validation split grouped by orthomosaic. Train and validation orthomosaic groups are disjoint, but flights overlap. The M4 independent test set was not used for M5 or M6.

M5 validation results (432 images): species accuracy 86.81% (375/432), macro F1 72.03%, ecological accuracy 90.74%, ecological macro F1 84.35%. Asparagopsis armata has zero validation examples, so its validation performance is unknown.

## M6: Reference bank and interface

Species prototypes were calculated from training embeddings only. The inference pipeline reports species prediction, ecological mapping, softmax outputs, cosine similarity to species prototypes and Grad-CAM. A Gradio interface presents these outputs with a conservative decision recommendation and mandatory human-review warning.

The exploratory 0.795 threshold was examined on the same validation set and is not an independently validated or safe threshold.
