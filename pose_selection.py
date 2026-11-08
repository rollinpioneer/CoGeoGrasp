def should_replace(original_score, candidate_score, margin=0.05):
    """Return whether the candidate's predicted robustness gain exceeds the margin."""
    return candidate_score - original_score > margin
