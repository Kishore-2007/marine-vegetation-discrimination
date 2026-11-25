# Limitations and threats to validity

- **Data domain.** ECU-MSS-2 is seagrass/substrate imagery and IMO is intertidal macroalgae imagery (UAV and in-situ).
  Neither is a validated underwater invasive-species dataset, so real underwater performance is unproven.
- **Validation-only hybrid results.** M5 has not been evaluated on the sealed M4 independent test set. M4 and M5 were
  measured on different splits and must not be compared directly.
- **Region-specific labels.** Status is valid only for Galicia, Spain. `Codium spp.` is mapped to Native at genus level
  and may include invasive members elsewhere.
- **Class imbalance.** *Asparagopsis armata* has 22 training images and none in the M5 validation set.
- **Uncalibrated confidence.** Softmax probability and prototype similarity are over-confident on wrong predictions;
  the 0.795 threshold is exploratory.
- **No segmentation.** No masks were available; Grad-CAM is an explanation, not a segmentation.
- **Not implemented from the original proposal:** YOLO / Mask R-CNN baselines, learned image enhancement,
  segmentation-based localisation. CLAHE was tested and did not help.
- **No physical deployment.** No robotics, real-time inference or field validation.

**Safety statement:** model output is advisory only. Expert verification is required for every prediction and no
automatic plant removal is authorised.
