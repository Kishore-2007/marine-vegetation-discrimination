# Fine-Grained Discrimination of Invasive and Native Marine Vegetation

**Project title:** Fine-Grained Discrimination of Invasive and Native Marine Vegetation Using a Hybrid Deep Learning Model for Selective Underwater Plant Removal

Academic mini-project · B.Tech Artificial Intelligence and Data Science · Saveetha Engineering College, Chennai, India

> **Project status:** M1–M6 experiments, integration and the Gradio demonstration are complete and frozen. This repository documents an academic research prototype. It is not a validated underwater plant-removal system.

## 1. Project overview

Marine vegetation plays an important role in coastal ecosystems. However, some non-native or invasive species can threaten local biodiversity. This project investigates whether image-based deep learning can help distinguish selected marine macroalgae species and group them into native or invasive categories for a human-supervised ecological decision-support workflow.

We developed the project incrementally rather than beginning with a single final model. The work progressed from dataset auditing and a conventional ResNet18 baseline (M1–M2), through exploratory visual explanation (M3), a separate binary ecological classification experiment (M4), a six-species hybrid attention and metric-learning model (M5), and finally a prototype-based inference and Gradio demonstration with conservative decision logic (M6).

**Important scope distinction:** the project title describes the intended application. The implemented work performs image classification and decision support. It does not perform pixel-level plant segmentation, operate an underwater robot, or physically remove vegetation.

## 2. Development milestones: M1 to M6

### M1 — Dataset inspection, cleaning and split preparation

**Dataset:** ECU-MSS-2 ([official dataset page](https://ro.ecu.edu.au/datasets/141/))

We began by inspecting the ECU-MSS-2 archive collection and understanding its four available image categories:

- Amphibolis
- Background
- Halophila
- Posidonia

The eight training/testing archives contained 5,201 JPEG images. We checked archive contents and image integrity, then investigated exact and perceptual duplicates so that near-identical images would not leak across data partitions.

The duplicate investigation identified 137 perceptual-hash candidate pairs. After visual confirmation, these were grouped into 132 connected components representing the same underlying image despite differences such as crop, orientation, layout or resolution. We then created group-aware manifests to keep related images together.

**Final M1 split:**

| Partition | Images |
|---|---:|
| Training | 3,290 |
| Validation | 824 |
| Clean test | 1,002 |
| **Total** | **5,116** |

The train and validation partitions had zero exact/perceptual duplicate-group overlap. The clean test set was also deduplicated.

**Why M1 mattered:** it established a more reliable data foundation before model training and reduced the risk of inflated validation performance caused by duplicate or near-duplicate images crossing partitions.

**Dataset limitation identified at this stage:** ECU-MSS-2 has no native/invasive ecological labels and no pixel-level segmentation masks. It can support the initial four-class image-classification work, but not the proposed ecological decision or supervised segmentation task by itself.

### M2 — ResNet18 baseline classification

After preparing the grouped dataset, we trained a conventional **ResNet18** classifier as the baseline. This gave us a reference point before introducing attention or metric learning.

The model learned the four ECU-MSS-2 classes: Amphibolis, Background, Halophila and Posidonia. We selected the best checkpoint using validation performance and evaluated it on the clean test partition.

**Results:**

| Evaluation partition | Correct | Total | Accuracy |
|---|---:|---:|---:|
| Validation | 820 | 824 | **99.51%** |
| Clean test | 869 | 1,002 | **86.73%** |

The clean test macro F1 was 0.8693. The difference between validation and test accuracy was approximately 12.79 percentage points. The test errors included 109 vegetation images predicted as Background.

**What we learned:** the baseline performed very strongly on validation data, but the lower clean-test result exposed a generalization gap. This was an important finding: validation accuracy alone was not enough to claim reliable real-world performance. We retained this baseline as a reference rather than presenting its validation score as the final project result.

### M3 — Exploratory explainability using Grad-CAM

We next explored **Gradient-weighted Class Activation Mapping (Grad-CAM)** to inspect which image regions influenced the ResNet18 predictions.

Grad-CAM was generated for 60 correctly classified validation images. We saved the original images, activation heatmaps and overlays, and examined spatial concentration and correct-versus-error diagnostics.

The resulting maps were sometimes diffuse and did not provide precise object boundaries. This was an exploratory explainability exercise, not a segmentation experiment.

**What M3 established:**

- We could inspect image regions contributing to a model prediction.
- Visual explanations could help identify whether the network appeared to focus on meaningful image content.
- The available dataset had no ground-truth segmentation masks, so localization quality could not be validated against annotated plant boundaries.

**Boundary of the claim:** Grad-CAM is an indication of influential regions. It is not a segmentation mask and cannot define a safe or precise plant-removal boundary.

### M4 — Initial binary Native/Invasive ecological classification

The ECU-MSS-2 dataset did not contain ecological native/invasive labels. We therefore introduced a second dataset for a separate ecological classification experiment.

**Dataset:** IMO Dataset — *Dataset of high resolution images of Intertidal MacrOalgae* ([Zenodo record](https://doi.org/10.5281/zenodo.14185867), CC BY 4.0).

The IMO Dataset contains intertidal macroalgae imagery from Galicia, Spain, including UAV and in-situ acquisition. We selected six species and mapped them into two ecological groups for the Galicia study context:

| Species | Study label |
|---|---|
| *Asparagopsis armata* | Invasive |
| *Sargassum muticum* | Invasive |
| *Bifurcaria bifurcata* | Native |
| *Codium* spp. | Native |
| *Ericaria selaginoides* | Native |
| *Saccorhiza polyschides* | Native |

The ecological mapping is region-specific. Native/invasive status must not be assumed to be the same in every geographic location.

We selected 3,199 images across the six species (2,751 native and 448 invasive) and created train, validation and independent test partitions:

| Partition | Images |
|---|---:|
| Training | 1,528 |
| Validation | 1,249 |
| Independent test | 422 |
| **Total** | **3,199** |

We trained a pretrained ResNet18 for binary classification using weighted cross-entropy, Adam (learning rate 0.0001, weight decay 0.0001), 224 × 224 input images and a 10-epoch training schedule. The best checkpoint was selected at epoch 2.

**Independent test results (422 images):**

| Metric | Result |
|---|---:|
| Accuracy | **86.02%** |
| Balanced accuracy | **86.57%** |
| Macro F1 | **0.86** |

Independent-test confusion matrix (rows = actual class; columns = predicted class; order = Native, Invasive):

```
                 Predicted
               Native  Invasive
Actual Native    174      50
       Invasive    9     189
```

The error analysis showed that 49 of the 50 false invasive alarms came from *Saccorhiza polyschides*. This suggested a possible species/acquisition confounding pattern and showed why aggregate binary accuracy alone could be misleading.

**M4 was closed as an initial binary ecological classification experiment with limitations.** Its independent test partition was evaluated exactly once and then sealed. It was not used for M5 or M6 training, validation, model selection, threshold calibration or further testing.

**Dataset/application limitation:** IMO is an intertidal macroalgae dataset, not a validated underwater robotic-removal dataset. The originally proposed *Caulerpa taxifolia* versus native *Caulerpa* comparison was not available in the selected IMO data.

### M5 — Hybrid CBAM attention and metric-learning model

After the binary experiment, we developed a more detailed six-species model. Rather than predicting only Native or Invasive, M5 predicts one of the six selected species. The ecological category is then derived from the Galicia-specific species mapping.

**Model architecture:**

1. **ResNet18 backbone** extracts image features.
2. **CBAM (Convolutional Block Attention Module)** applies channel and spatial attention to refine feature representations.
3. **Embedding head** generates a 256-dimensional L2-normalized feature vector.
4. **Six-class classification head** predicts the species.

**Training objective:** we combined three learning signals:

- Cross-entropy classification loss.
- Triplet loss to encourage separation between different species and compactness within a species.
- Supervised contrastive loss to structure the embedding space using labelled examples.

The combined objective used classification loss + 0.5 × triplet loss + 0.1 × supervised contrastive loss. Training used species-aware batches containing examples from all six classes (6 classes × 4 examples per class), for 20 epochs.

**M5 data split:**

| Partition | Images | Orthomosaic groups |
|---|---:|---:|
| Training | 2,345 | 13 |
| Validation | 432 | 4 |

Train and validation orthomosaic groups were disjoint. However, flights overlapped between the partitions, so this split does not establish unseen-flight or unseen-location generalization. The sealed M4 independent test set was not accessed.

**M5 validation results (432 images):**

| Metric | Result |
|---|---:|
| Species accuracy | **86.81%** (375/432) |
| Species macro F1 | **72.03%** |
| Ecological classification accuracy | **90.74%** |
| Ecological macro F1 | **84.35%** |

The species-level validation confusion analysis showed that errors were concentrated particularly among *Sargassum muticum* and *Saccorhiza polyschides*. Also, the validation split contained no *Asparagopsis armata* examples, so its validation performance cannot be assessed.

We extracted normalized embeddings for the training and validation images and examined class-wise similarity patterns. Correct predictions generally had stronger similarity to their actual class representation, but some incorrect predictions also had very high similarity to a wrong class. Therefore, similarity scores cannot be interpreted as calibrated confidence.

**M5 result:** the hybrid model provided a six-species representation and a stronger basis for the integrated prototype-based workflow. Its reported figures are validation metrics, not independent-test results.

### M6 — Prototype reference bank, explainability and Gradio integration

M6 converted the frozen M5 model into an image-analysis demonstration. No new model training was performed.

**Step 1 — Build a species reference bank**

We calculated one reference prototype per species using the M5 training embeddings only. The reference bank contains the six species and their training-example counts:

| Species | Training embeddings |
|---|---:|
| *Asparagopsis armata* | 22 |
| *Bifurcaria bifurcata* | 501 |
| *Codium* spp. | 359 |
| *Ericaria selaginoides* | 803 |
| *Saccorhiza polyschides* | 513 |
| *Sargassum muticum* | 147 |

No validation or sealed M4 test embeddings were used to construct the prototypes.

**Step 2 — Implement image inference**

The inference pipeline accepts an image, applies the M5 preprocessing and model, and returns the predicted species, mapped ecological category, class probabilities and cosine similarities to the species prototypes.

**Step 3 — Examine similarity behaviour**

We inspected a difficult *Saccorhiza polyschides* example that was predicted as *Ericaria selaginoides*. The incorrect prediction had a high softmax score and high similarity to the predicted class prototype. This demonstrated that neither score should be presented as a calibrated measure of correctness.

**Step 4 — Add Grad-CAM visualization**

We integrated Grad-CAM into the restored M5 model and generated heatmap/overlay visualizations for uploaded images. These maps are intended to help a human inspect influential image regions; they do not identify exact plant boundaries.

**Step 5 — Add a conservative decision policy**

The interface maps predictions to provisional recommendations. A predicted Native species receives a provisional protect recommendation. A predicted Invasive species is described only as a potential removal candidate requiring human review and expert approval.

An exploratory softmax threshold of 0.795 was examined on the M5 validation set. The threshold was assessed on the same validation data used in the analysis, so it is not an unbiased calibration result and must not be treated as a validated safety threshold. No threshold was found that justified autonomous action.

**Step 6 — Integrate the Gradio interface**

The final Gradio demonstration brings together:

- Image upload and preprocessing.
- Six-species prediction.
- Galicia-context Native/Invasive mapping.
- Softmax class scores.
- Cosine similarities to train-only species prototypes.
- Grad-CAM heatmap and overlay.
- Provisional decision recommendation.
- Human-verification and expert-approval warnings.

The restored M5 checkpoint was loaded without retraining. Integration checks confirmed that the checkpoint remained unchanged, the M4 independent test set was not accessed, and automatic removal remained disabled.

**M6 outcome:** an integrated, human-supervised image-analysis prototype. It is not an autonomous ecological decision system or a plant-removal controller.

## 3. Results at a glance

These metrics come from different experiments and partitions. They must be interpreted separately.

| Milestone | Dataset / partition | Main result |
|---|---|---|
| M2 | ECU-MSS-2 validation (824) | 99.51% accuracy |
| M2 | ECU-MSS-2 clean test (1,002) | 86.73% accuracy |
| M4 | IMO independent test (422) | 86.02% accuracy; 86.57% balanced accuracy; 0.86 macro F1 |
| M5 | IMO validation (432) | 86.81% species accuracy; 72.03% species macro F1 |
| M5 | IMO validation (432) | 90.74% ecological accuracy; 84.35% ecological macro F1 |

Do not combine M4 independent-test accuracy and M5 validation accuracy into one test-performance claim.

## 4. System workflow

```text
ECU-MSS-2
   |
   +--> M1: archive audit, duplicate grouping, clean manifests
   |
   +--> M2: ResNet18 four-class baseline
   |
   +--> M3: exploratory Grad-CAM analysis

IMO Dataset (Galicia, Spain)
   |
   +--> M4: initial binary Native/Invasive ResNet18 experiment
   |       |
   |       +--> independent test evaluated once and sealed
   |
   +--> M5: six-species ResNet18 + CBAM + metric learning
           |
           +--> train-only species prototype reference bank
           |
           +--> M6: inference + Grad-CAM + conservative policy
                   |
                   +--> Gradio image-analysis demonstration
                   |
                   +--> mandatory human verification
                   +--> expert approval before any intervention
                   +--> automatic removal disabled
```

## 5. Repository contents

```text
marine-vegetation-discrimination/
├── README.md
├── .gitignore
├── Mini_Project_clean.ipynb
└── docs/
    ├── methodology.md
    ├── experimental-results.md
    └── limitations-and-safety.md
```

The cleaned notebook is the main consolidated project workfile. The supporting documents provide the methodology, results and limitations in a more readable form.

## 6. Reproducibility and execution notes

The experiments were developed in Google Colab using Google Drive storage under `/content/drive/MyDrive/Marine_Project`. The notebook refers to datasets, manifests, checkpoints and other artifacts stored in that environment.

**Cloning this repository alone is not sufficient to reproduce every experiment or launch the final Gradio demonstration.** The original datasets and model artifacts are not included because of their size and because they are maintained separately. To reproduce the work, a user must obtain the cited datasets, recreate the expected project artifact structure, and use the relevant saved checkpoints and manifests.

The notebook is a record of the completed workflow; it should not be run from top to bottom blindly. In particular:

- Do not rerun the sealed M4 independent test evaluation.
- Do not use the M4 test set for M5/M6 training, validation, tuning or calibration.
- Do not interpret validation metrics as independent-test performance.
- Do not describe Grad-CAM as segmentation or confidence scores as calibrated confidence.

## 7. Limitations and responsible-use safeguards

- **Dataset domain:** ECU-MSS-2 and the IMO Dataset have different purposes and image domains. IMO imagery is intertidal macroalgae imagery, including UAV/in-situ acquisitions; it is not a validated underwater robotic-removal dataset.
- **Regional ecology:** the native/invasive mapping is specific to Galicia, Spain. Local ecological experts must verify status before applying the workflow elsewhere.
- **No segmentation:** no ground-truth segmentation masks or supervised segmentation model were available or implemented.
- **No Caulerpa case study:** the originally proposed *Caulerpa taxifolia* versus native *Caulerpa* pair was not present in the selected IMO dataset.
- **Generalization:** M2 showed a validation-to-test gap. M5 train/validation orthomosaic groups are disjoint but flights overlap. External and unseen-location generalization remains unproven.
- **Class coverage:** M5 validation has no *Asparagopsis armata* examples.
- **No calibrated confidence:** softmax outputs and cosine similarities are scores, not calibrated probabilities of correctness.
- **Closed-set limitation:** the six-class classifier cannot reliably recognize unknown or unsupported species.
- **Explainability limitation:** Grad-CAM highlights influential regions but does not define a plant boundary.
- **Human oversight:** every prediction requires human verification. Expert approval is required before any ecological intervention.
- **No autonomous removal:** an invasive prediction is only a potential removal candidate. Automatic removal, robot control and physical plant removal are not implemented or validated.
- **Threshold limitation:** 0.795 is exploratory and was examined on the same validation data; it is not a validated safety threshold.

## 8. Future work

1. Collect larger and more diverse underwater datasets across regions, depths, visibility conditions and acquisition devices.
2. Obtain expert-annotated segmentation masks and evaluate pixel-level segmentation.
3. Evaluate on independent external datasets and genuinely unseen flights/locations.
4. Investigate calibrated uncertainty estimation and open-set recognition for unknown species.
5. Select and evaluate decision thresholds using a separate calibration set.
6. Validate regional ecological labels with marine ecologists.
7. Only after extensive independent field validation, investigate human-supervised ROV integration.

## 9. References

1. ECU-MSS-2 dataset: https://ro.ecu.edu.au/datasets/141/
2. IMO Dataset, *Dataset of high resolution images of Intertidal MacrOalgae*: https://doi.org/10.5281/zenodo.14185867

## 10. Project information

- **Programme:** B.Tech Artificial Intelligence and Data Science
- **Institution:** Saveetha Engineering College, Chennai, India
- **Project type:** Academic mini-project and research study
- **Team number:** 160
- **Faculty guide:** Dr. R. Augustian Isaac, Professor, Department of AIML

---

**Research disclaimer:** This repository documents the experiments and prototype implementation completed for an academic project. It does not claim validated underwater segmentation, calibrated confidence, autonomous operation, robotic control, or safe/approved physical plant removal.
