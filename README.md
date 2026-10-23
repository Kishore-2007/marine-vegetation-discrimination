# Fine-Grained Discrimination of Invasive and Native Marine Vegetation Using a Hybrid Deep Learning Model for Selective Underwater Plant Removal

## Overview

Marine ecosystems are threatened by invasive vegetation that can compete with native species for light, space, and nutrients. Removing invasive plants is challenging because they may resemble beneficial native vegetation in colour, texture, branching patterns, and overall morphology.

Existing removal methods, including manual diver intervention and mechanical harvesting, can be labour-intensive or risk damaging native vegetation and surrounding marine habitats.

This research proposes a hybrid deep learning system to distinguish invasive marine vegetation from visually similar native species. The proposed approach combines underwater image enhancement, plant detection and segmentation, attention-based feature extraction, and metric learning to support fine-grained classification.

The system is designed to identify marine vegetation, predict its invasive or native status, provide a confidence score, and flag uncertain predictions for human review. It aims to establish a foundation for future selective underwater plant removal.

## Objectives

- Develop a computer vision pipeline for underwater marine vegetation analysis.
- Improve underwater image quality through colour correction, contrast enhancement, and denoising.
- Detect and segment marine vegetation from underwater backgrounds.
- Distinguish visually similar invasive and native marine plant species.
- Investigate attention mechanisms to emphasize discriminative visual features.
- Use metric learning to improve feature-space separation between similar species.
- Generate classification confidence scores and flag uncertain cases for human review.
- Evaluate the proposed approach against suitable baseline models.
- Establish a foundation for future integration with underwater robotic systems.

## Proposed Methodology

The proposed system follows a sequence of image processing and deep learning stages.

### 1. Image Data Collection

Collect suitable underwater marine vegetation images from accessible datasets or other appropriately authorized sources. Identify the available species categories and prepare labels for model development.

### 2. Underwater Image Enhancement

Underwater images may contain colour distortion, low contrast, backscatter, blur, and particulate noise. The proposed preprocessing stage will investigate:

- Colour correction and restoration.
- Contrast enhancement using techniques such as CLAHE.
- Denoising and visual detail improvement.
- Assessment of image quality before and after enhancement.

### 3. Plant Detection and Segmentation

Identify marine vegetation in the underwater scene and separate the target plant regions from surrounding water, coral, and other background objects. Detection and segmentation approaches will be selected according to dataset availability and project requirements.

### 4. Hybrid Fine-Grained Deep Learning Model

The proposed hybrid model will investigate the combination of:

- **Deep feature extraction:** Learning useful visual representations from marine vegetation images.
- **Attention mechanism:** Emphasizing important regions and features that help distinguish visually similar species.
- **Metric learning:** Learning an embedding space that encourages similar species representations to be appropriately grouped and different classes to be separated.
- **Classification:** Predicting the relevant species category and its invasive or native status.

The final architecture will be documented after implementation and experimentation.

### 5. Species Classification and Confidence Scoring

The system is intended to produce:

- Predicted marine vegetation species or category.
- Invasive or native classification.
- Prediction confidence score.
- Human-review flag for uncertain predictions.

A confidence threshold will be defined and evaluated during experimentation. Predictions below the selected threshold will be referred for human review rather than treated as reliable removal decisions.

### 6. Model Evaluation and Testing

The proposed system will be evaluated using appropriate classification and detection metrics, depending on the implemented components.

Planned classification metrics include:

- Accuracy
- Precision
- Recall
- Specificity
- F1-score
- Matthews Correlation Coefficient (MCC)

Where appropriate, the project will compare the proposed approach with baseline CNN classifiers and relevant detection or segmentation models, including YOLO and Mask R-CNN.

Actual performance values and comparisons will be reported only after experiments have been completed.

## Proposed System Workflow

```text
Underwater Image Collection
            |
            v
Image Preprocessing
            |
            v
Underwater Image Enhancement
            |
            v
Marine Plant Detection
            |
            v
Plant Segmentation
            |
            v
Deep Feature Extraction
            |
            v
Attention + Metric Learning
            |
            v
Species Classification
            |
            v
Invasive / Native Prediction
            |
            v
Confidence Score and Evaluation
            |
            v
Human Review for Uncertain Cases
            |
            v
Foundation for Future Selective Removal
```

## Functional Requirements

- Accept underwater images of marine vegetation.
- Improve image quality using suitable preprocessing techniques.
- Detect and localize marine vegetation.
- Segment plant regions from the surrounding environment.
- Extract discriminative visual features.
- Classify invasive and native vegetation.
- Generate confidence scores and human-review flags.
- Evaluate model performance using appropriate metrics.
- Support comparison with baseline approaches.

## Non-Functional Requirements

- **Accuracy:** Reliable discrimination between visually similar species.
- **Robustness:** Evaluation under different visibility and image-quality conditions.
- **Reliability:** Confidence-aware predictions and handling of uncertain cases.
- **Scalability:** Potential to incorporate additional species as labelled data becomes available.
- **Efficiency:** Consideration of computational requirements for future practical deployment.
- **Safety:** No automatic removal decision based solely on an uncertain classification.
- **Extensibility:** Future integration with underwater robotic monitoring and removal systems.

## Expected Outcomes

The project aims to investigate whether combining underwater image enhancement, segmentation, attention-based feature extraction, and metric learning can improve invasive–native marine vegetation discrimination.

Expected outcomes include:

- Improved visual feature quality for underwater plant analysis.
- More reliable identification of visually similar marine vegetation.
- Confidence-aware classification with uncertain-case handling.
- Quantitative evaluation against selected baseline approaches.
- A foundation for future AI-assisted selective marine vegetation management.

These are research objectives and expected outcomes, not experimentally verified results.

## Technologies and Tools

The following technologies are candidates for the implementation, subject to the final architecture and development environment:

- **Programming language:** Python
- **Image processing:** OpenCV
- **Numerical computing:** NumPy
- **Data analysis:** Pandas
- **Deep learning:** PyTorch or TensorFlow
- **Model evaluation:** Scikit-learn
- **Visualization:** Matplotlib
- **Version control:** Git and GitHub

The final tools and library versions will be documented after they are selected and used in the implementation.

## Repository Structure

The repository is intended to follow a modular structure as the project develops.

```text
marine-vegetation-discrimination/
├── README.md
├── .gitignore
├── requirements.txt
├── configs/
├── data/
│   └── README.md
├── notebooks/
├── src/
│   ├── preprocessing/
│   ├── enhancement/
│   ├── detection/
│   ├── segmentation/
│   ├── models/
│   ├── classification/
│   └── evaluation/
├── tests/
├── results/
│   └── README.md
└── docs/
```

This is a proposed structure. Directories and files will be added as the corresponding components are implemented.

### Directory Guidelines

- `configs/` — Configuration files and experiment settings.
- `data/` — Dataset organization instructions; large datasets may be stored separately.
- `notebooks/` — Exploratory data analysis and experimental notebooks.
- `src/` — Source code for the image processing and model pipeline.
- `tests/` — Tests for implemented components.
- `results/` — Evaluation outputs, plots, and experiment summaries.
- `docs/` — Research documentation and technical notes.

## Dataset and Data Management

The final dataset source, species categories, image count, and train-validation-test split will be documented after dataset selection and verification.

Dataset preparation should account for class balance, image quality, annotation quality, and the availability of species-level labels.

Dataset images and annotations must be shared only when their applicable licences and permissions allow redistribution. Where redistribution is not permitted, provide instructions for obtaining the data from its original source.

## Installation and Usage

The installation and execution instructions will be added after the source code, dependencies, and model architecture have been implemented.

The intended usage workflow is:

1. Prepare the required dataset and annotations.
2. Configure the preprocessing and image-enhancement pipeline.
3. Run detection and segmentation where implemented.
4. Train or load the selected classification model.
5. Perform inference on test images.
6. Evaluate predictions and confidence scores.
7. Review the results and document limitations.

No working installation or inference command is claimed until the corresponding code is available.

## Research Significance and Sustainable Development Goals

This research aligns with the following Sustainable Development Goals:

- **SDG 14 — Life Below Water:** Supports research into marine biodiversity protection and more selective identification of invasive vegetation.
- **SDG 9 — Industry, Innovation and Infrastructure:** Applies computer vision and deep learning to a marine environmental challenge.
- **SDG 13 — Climate Action:** Contributes to broader environmental sustainability research through improved marine ecosystem monitoring.

The proposed system is intended as a decision-support and research foundation. Its real-world ecological benefits will depend on model validation, field testing, and appropriate human oversight.

## Limitations and Future Work

Potential limitations include insufficient labelled images, variation between marine environments, severe underwater image degradation, class imbalance, and difficulty distinguishing closely related species.

Future work may investigate:

- Larger and more diverse underwater vegetation datasets.
- Improved underwater image restoration.
- More effective attention and metric-learning architectures.
- Better confidence calibration and uncertainty estimation.
- Testing across different visibility conditions and species pairs.
- Optimization for resource-constrained underwater devices.
- Integration with remotely operated vehicles (ROVs) or robotic removal systems.

Actual feasibility and performance will need to be established through experimentation and field validation.

## References

1. Gu, Z. et al. *Underwater Computational Imaging: A Survey*. Intelligent Marine Technology and Systems, 2023.
2. Drews-Jr, P. L. et al. *Underwater Image Segmentation Using Deep Learning Techniques*. Journal of the Brazilian Computer Society, 2021.
3. Islam, M. J., Xia, Y., and Sattar, J. *Fast Underwater Image Enhancement for Improved Visual Perception*. IEEE Robotics and Automation Letters, 2020.
4. Goodfellow, I., Bengio, Y., and Courville, A. *Deep Learning*. MIT Press.
5. Szeliski, R. *Computer Vision: Algorithms and Applications*. Springer.

Full bibliographic details and publication identifiers will be verified before the final research submission.

## Project Information

- **Project title:** Fine-Grained Discrimination of Invasive and Native Marine Vegetation Using a Hybrid Deep Learning Model for Selective Underwater Plant Removal
- **Programme:** B.Tech Artificial Intelligence and Data Science
- **Institution:** Saveetha Engineering College, Chennai, Tamil Nadu, India
- **Project type:** Academic mini-project and research study
- **Team number:** 160
- **Project status:** In progress
- **Faculty guide:** Dr. R. Augustian Isaac, Professor, Department of AIML

---

**Disclaimer:** This repository documents an academic research project. The proposed methodology, expected outcomes, and future applications do not imply that a complete system has been implemented, validated, or deployed. Experimental results will be added when supported by actual testing.
