# Methodology

The work is organised in six milestones. Each milestone froze its artefacts (manifests, checkpoints, result files)
before the next began so that later experiments could not silently change earlier results.

## M1 - Data preparation and integrity audit (ECU-MSS-2)

- Four classes: Amphibolis, Background, Halophila, Posidonia; 4,161 training and 1,040 test images.
- **Exact duplicates:** SHA-256 over all 5,201 images found 92 cross-split duplicate records. 32 test images duplicated
  training/validation images and were removed, plus 6 within-test duplicates: **clean test set = 1,002 images**.
- **Near duplicates:** perceptual hashing gave 137 candidate train/validation pairs, all confirmed by SIFT matching and
  manual inspection. They were merged into 132 perceptual groups, and the split was rebuilt with
  `StratifiedGroupKFold` (seed 42): **3,290 train / 824 validation**.
- Image-quality statistics (sharpness, contrast, brightness, saturation) were compared across splits with
  Mann-Whitney tests and FDR correction, revealing a train/test distribution shift.

## M2 - Baseline CNN

ImageNet-pretrained ResNet-18, final layer replaced by 4 outputs (11,178,564 parameters). Adam (lr 1e-4), batch 32,
up to 10 epochs, early stopping (patience 3), mixed precision, seed 42, no augmentation. Best epoch 3.

**CLAHE experiment:** CLAHE (clip limit 2.0 and 1.0, 8x8 tiles) on the L channel of LAB images did not help
(Table in [results.md](results.md)).

## M3 - Localisation and explainability

An audit of all eight ECU-MSS-2 archives found only images (no masks or boxes), so supervised segmentation was not
possible. Grad-CAM on `layer4[-1]` was analysed on 60 validation images. Maps are only moderately concentrated
(top-20% pixel energy 0.34-0.36), so Grad-CAM is treated as an explanation, **not** a segmentation mask.

## M4 - Native vs invasive baseline with a sealed test set (IMO dataset)

- Six verified species from the Galician coast, mapped to Native / Invasive.
- Whole UAV flights/orthomosaics are kept together. **Flights 1 and 6 (422 images)** form the sealed independent test
  set, never used for training, tuning or checkpoint selection.
- Development data (2,777 images) split by orthomosaic into 1,528 train / 1,249 validation images.
- Binary ResNet-18, weighted cross-entropy (native 0.5422, invasive 6.4202), Adam (lr 1e-4, wd 1e-4), 10 epochs;
  best checkpoint (epoch 2) locked before the test set was evaluated once.

## M5 - Hybrid ResNet-18 + CBAM + metric learning

- **Backbone:** ImageNet ResNet-18 up to `layer4` (512 channels).
- **CBAM:** channel attention (shared MLP, reduction 16) then spatial attention (7x7 conv).
- **Head:** global average pool -> Linear 512-512 -> ReLU -> Dropout 0.3 -> Linear 512-256 -> L2 normalisation ->
  Linear 256-6. 11,605,448 parameters.
- **Loss:** `CE + 0.5 * batch-hard triplet (margin 0.3) + 0.1 * SupCon (T = 0.07)`.
- **Sampling:** species-balanced batches (4 images x 6 species = 24), 98 batches/epoch.
- **Optimiser:** AdamW (lr 1e-4, wd 1e-4), ReduceLROnPlateau, 20 epochs, Tesla T4. Best epoch 16.
- **Split:** orthomosaic-grouped, 2,345 train / 432 validation. The M4 test set was never accessed.
- **Prototype bank:** mean normalised embedding per species; cosine similarity at inference.

## M6 - Decision support

A conservative decision engine (`src/marine_veg/decision.py`):

| Condition | Output |
|---|---|
| Native prediction | PROVISIONAL PROTECT RECOMMENDATION |
| Invasive prediction | POTENTIAL REMOVAL CANDIDATE, HIGH review priority |
| Probability < 0.795 | HIGH review priority (exploratory threshold, not calibrated) |
| Unsupported / unclassified | HUMAN REVIEW |
| **Always** | Human verification mandatory; automatic removal never authorised |

A Gradio interface shows the original image, Grad-CAM heat-map and overlay, class probabilities, prototype similarities
and the decision record.
