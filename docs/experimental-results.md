# Experimental results

## Keep experiment partitions separate

Results below belong to different datasets, tasks and partitions. They must not be merged into a single performance claim.

| Experiment | Dataset / partition | Metric | Value |
|---|---|---|---:|
| M2 ResNet18 | ECU-MSS-2 validation (824) | Accuracy | 99.51% |
| M2 ResNet18 | ECU-MSS-2 clean test (1,002) | Accuracy | 86.73% |
| M4 binary ResNet18 | IMO independent test (422) | Accuracy | 86.02% |
| M4 binary ResNet18 | IMO independent test (422) | Balanced accuracy | 86.57% |
| M4 binary ResNet18 | IMO independent test (422) | Macro F1 | 0.86 |
| M5 hybrid six-species | IMO validation (432) | Species accuracy | 86.81% |
| M5 hybrid six-species | IMO validation (432) | Species macro F1 | 72.03% |
| M5 hybrid six-species | IMO validation (432) | Ecological accuracy | 90.74% |
| M5 hybrid six-species | IMO validation (432) | Ecological macro F1 | 84.35% |

## Interpretation

- M2's high validation accuracy and lower clean-test accuracy indicate a generalization gap.
- M4's independent test result belongs only to the binary experiment.
- M5 figures are validation metrics, not independent-test metrics.
- M5 train/validation sets have disjoint orthomosaic groups but share flights; unseen-flight/location generalization has not been demonstrated.
- M5 validation contains no Asparagopsis armata examples.
- Softmax probability and prototype similarity are not calibrated confidence.
- Grad-CAM is an exploratory explanation map, not segmentation.
