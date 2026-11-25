"""Conservative decision engine (M6).

Human verification is ALWAYS mandatory and automatic removal is NEVER authorised.
The 0.795 threshold is exploratory (derived from validation data, not calibrated).
"""

REVIEW_THRESHOLD = 0.795

# Region-specific mapping: Galicia, Spain (conservative, genus-level for Codium).
SPECIES_STATUS = {
    "Asparagopsis armata": "Invasive",
    "Sargassum muticum": "Invasive",
    "Bifurcaria bifurcata": "Native",
    "Codium spp.": "Native",
    "Ericaria selaginoides": "Native",
    "Saccorhiza polyschides": "Native",
}


def decision_engine(predicted_species, class_probabilities, threshold=REVIEW_THRESHOLD):
    status = SPECIES_STATUS.get(predicted_species)
    probability = float(class_probabilities[predicted_species])

    if probability < threshold:
        review_priority = "HIGH"
        review_reason = ("Prediction falls below the exploratory "
                         "validation-derived review threshold.")
    else:
        review_priority = "NORMAL"
        review_reason = ("Prediction meets the exploratory threshold, "
                         "but human verification remains mandatory.")

    if status is None:
        recommendation, review_priority = "UNSUPPORTED SPECIES - HUMAN REVIEW", "HIGH"
    elif status == "Native":
        recommendation = "PROVISIONAL PROTECT RECOMMENDATION"
    elif status == "Invasive":
        recommendation, review_priority = "POTENTIAL REMOVAL CANDIDATE", "HIGH"
    else:
        recommendation, review_priority = "UNCLASSIFIED - HUMAN REVIEW", "HIGH"

    return {
        "predicted_species": predicted_species,
        "predicted_ecological_status": status,
        "ecological_mapping_region": "Galicia, Spain",
        "softmax_probability": probability,
        "probability_threshold": threshold,
        "threshold_type": "Exploratory, not calibrated",
        "recommendation": recommendation,
        "review_priority": review_priority,
        "review_reason": review_reason,
        "human_verification": "MANDATORY",
        "expert_approval_required": True,
        "automatic_removal_authorized": False,
        "segmentation_mask_available": False,
    }
