# Limitations and safety

## Dataset scope

- ECU-MSS-2 contains four image classes and does not provide invasive/native labels or segmentation masks.
- IMO Dataset imagery is intertidal macroalgae imagery, including UAV/in-situ acquisition. It is not a validated underwater robotic-removal dataset.
- The ecological status mapping used here is specific to Galicia, Spain. Status may differ by region and requires local expert validation.
- The original Caulerpa taxifolia/native Caulerpa pair was not available in the selected IMO data.

## Model and evaluation limits

- M4 is an initial binary ecological classification experiment, not a validated removal system.
- M4's independent test set was evaluated once and sealed; it must not be reused for M5/M6 training, validation, model selection, threshold calibration or further testing.
- M5 validation results do not establish independent-test performance.
- M5 train/validation orthomosaic groups are disjoint, but flights overlap.
- No calibrated confidence estimate is implemented. Softmax scores and cosine similarity values are not calibrated probabilities of correctness.
- The six-class closed-set classifier cannot reliably recognize unknown or unsupported species.
- Grad-CAM highlights influential regions but does not provide segmentation masks or precise removal boundaries.

## Human oversight

- Every prediction requires human verification.
- An invasive prediction is only a potential removal candidate, not permission to remove a plant.
- Expert ecological approval is required before any intervention.
- Automatic removal is disabled. No robot control or physical removal has been implemented or validated.
- The 0.795 threshold is exploratory and was assessed on the same validation data; it must not be described as a validated safety threshold.
