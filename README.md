# Marine Vegetation Discrimination

**Fine-Grained Discrimination of Invasive and Native Marine Vegetation Using a Hybrid Deep Learning Model for Selective Underwater Plant Removal**

Academic mini-project · B.Tech Artificial Intelligence and Data Science · Saveetha Engineering College

> **Status:** M1–M6 experiments and the image-analysis demonstration are complete and frozen. This is an academic research prototype and decision-support demonstration—not a validated underwater plant-removal system.

## Project overview

This project investigates species-level classification of marine macroalgae and ecological grouping into native and invasive categories. The completed workflow includes dataset auditing, a ResNet18 baseline, exploratory Grad-CAM diagnostics, a binary ecological classification experiment, a hybrid CBAM + metric-learning model, and an integrated Gradio demonstration.

The ecological mapping for the IMO dataset is specific to **Galicia, Spain**. Invasive/native status is region-dependent and must not be generalized to other locations without local ecological verification.

## Completed milestones

| Milestone | Completed work | Result / qualification |
|---|---|---|
| M1 — Dataset audit | Audited ECU-MSS-2 archives, image integrity, duplicates and grouped manifests. | Four classes: Amphibolis, Background, Halophila and Posidonia. No invasive/native labels or segmentation masks. |
| M2 — Baseline | ResNet18 classification experiment on ECU-MSS-2. | Validation accuracy **99.51%** (820/824); clean test accuracy **86.73%** (869/1002). The gap indicates a generalization limitation. |
| M3 — Explainability | Exploratory Grad-CAM diagnostics on selected validation images. | Weak localization exploration only; not segmentation. |
| M4 — Binary ecological experiment | ResNet18 Native/Invasive experiment on selected IMO images. | Independent test: **86.02% accuracy**, **86.57% balanced accuracy**, **0.86 macro F1** (422 images). |
| M5 — Hybrid model | ResNet18 + CBAM, 256D embedding, classification + metric-learning objectives; six species. | Validation species accuracy **86.81%**, macro F1 **72.03%**; ecological accuracy **90.74%**. |
| M6 — Integration | Train-only species prototypes, inference, Grad-CAM, decision logic and Gradio demo. | Human-supervised decision support. Automatic removal disabled. |

**Do not compare or combine metrics from different experiments as if they came from one test set.** M4's 86.02% is independent-test performance; M5's metrics above are validation performance.

## Datasets

### ECU-MSS-2
Used for M1–M3. The four image classes are Amphibolis, Background, Halophila and Posidonia. The dataset does not provide invasive/native ecological labels or segmentation masks.

Source: [ECU-MSS-2 dataset](https://ro.ecu.edu.au/datasets/141/).

### IMO Dataset
Used for M4–M5. Dataset of high-resolution intertidal macroalgae images, DOI [10.5281/zenodo.14185867](https://doi.org/10.5281/zenodo.14185867), CC BY 4.0 according to its record.

Six selected species and the ecological mapping used in this study:

| Species | Study label (Galicia context) |
|---|---|
| *Asparagopsis armata* | Invasive |
| *Sargassum muticum* | Invasive |
| *Bifurcaria bifurcata* | Native |
| *Codium* spp. | Native |
| *Ericaria selaginoides* | Native |
| *Saccorhiza polyschides* | Native |

The IMO imagery is intertidal macroalgae imagery (including UAV/in-situ acquisition), not a validated underwater robotic-removal dataset. M4's independent test split was sealed and was not used for M5/M6 training, validation, selection or tuning. M5 train/validation orthomosaic groups are disjoint, but flights overlap; unseen-flight/location generalization is not established.

## M5 hybrid architecture

- ResNet18 feature backbone.
- CBAM channel and spatial attention.
- 256-dimensional normalized embedding.
- Six-species classification head.
- Combined classification, triplet and supervised-contrastive objectives.

M5 validation set: 432 images; species accuracy 86.81% (375/432), species macro F1 72.03%, ecological accuracy 90.74%, ecological macro F1 84.35%. No *Asparagopsis armata* examples occur in this validation split, so its validation performance is not established.

## M6 demonstration

The restored Gradio interface accepts an image and displays the predicted species/category, softmax probabilities, cosine similarities to train-only species prototypes, Grad-CAM visualization and a provisional decision recommendation.

### Safety and interpretation limits

- Softmax probability and cosine similarity are **not calibrated confidence**.
- High similarity can occur for an incorrect prediction.
- Grad-CAM indicates influential regions; it is not a segmentation mask or precise removal boundary.
- The six-class closed-set classifier cannot reliably identify unknown or unsupported species.
- An invasive prediction is only a potential removal candidate, never authorization to remove a plant.
- Human verification is mandatory for every prediction; expert approval is required before ecological action.
- Automatic removal is disabled. No robot control or physical removal was implemented or validated.
- The exploratory 0.795 threshold was examined on the same validation data and is not an unbiased or validated safety threshold.

## Repository contents

The primary working notebook is being prepared for publication as a cleaned notebook with saved cell outputs removed. Supporting source modules, result figures and setup instructions should be added as separately documented files. Raw datasets, extracted image collections and large model checkpoints are not stored in this Git repository.

Suggested structure:

```text
marine-vegetation-discrimination/
├── README.md
├── .gitignore
├── notebooks/
│   └── Mini_Project_clean.ipynb
├── src/
├── docs/
│   ├── methodology.md
│   ├── experimental-results.md
│   └── limitations-and-safety.md
└── results/
    └── figures/
```

## Reproducibility

The completed notebook was developed in Google Colab and uses Google Drive paths under `/content/drive/MyDrive/Marine_Project`. The current notebook depends on the author's Drive artifacts, datasets and saved checkpoints. Cloning this repository alone is not yet sufficient to reproduce all experiments or launch the Gradio demo. Dataset acquisition, artifact placement and environment setup instructions must be followed once published.

Do not rerun training or evaluate the sealed M4 test set as part of routine demonstration setup.

## Future work

- Add labelled segmentation masks and evaluate pixel-level segmentation.
- Expand datasets across regions, acquisition devices, depths and visibility conditions.
- Conduct independent external and unseen-flight/location evaluation.
- Investigate calibrated uncertainty and open-set/unknown-species detection.
- Evaluate thresholds on a separate calibration set.
- Validate ecological labels with local marine experts.
- Only after extensive field validation, investigate human-supervised ROV integration.

## References

1. [ECU-MSS-2 dataset](https://ro.ecu.edu.au/datasets/141/).
2. [IMO Dataset, Zenodo DOI 10.5281/zenodo.14185867](https://doi.org/10.5281/zenodo.14185867).

## Project information

- Programme: B.Tech Artificial Intelligence and Data Science
- Institution: Saveetha Engineering College, Chennai, India
- Project type: Academic mini-project and research study
- Team number: 160
- Faculty guide: Dr. R. Augustian Isaac, Professor, Department of AIML

---
**Research disclaimer:** This repository documents an academic prototype and recorded experiments. It does not claim validated underwater segmentation, calibrated confidence, autonomous operation, robotic control, or safe/approved physical plant removal.
