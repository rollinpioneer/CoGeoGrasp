"""Read a GraspNet precision array and report AP and Top-1 as percentages."""

import argparse

import numpy as np


def graspnet_metrics(precision):
    """Average precision over ranks and friction levels, and Top-1 at friction 0.4."""
    precision = np.asarray(precision)
    if precision.shape[-2:] != (50, 6) or precision.size == 0:
        raise ValueError("Expected a nonempty precision array ending in (50, 6).")
    if not np.all((precision >= 0) & (precision <= 1)):
        raise ValueError("Precision values must be fractions between 0 and 1.")

    ap = precision.mean(dtype=np.float64)
    # The evaluator orders friction levels as 0.2, 0.4, 0.6, 0.8, 1.0, 1.2.
    top1 = precision[..., 0, 1].mean(dtype=np.float64)
    return 100 * ap, 100 * top1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("precision_file", help="GraspNet evaluator output saved as a .npy array")
    args = parser.parse_args()
    ap, top1 = graspnet_metrics(np.load(args.precision_file, allow_pickle=False))
    print(f"AP = {ap:.2f}%")
    print(f"Top-1 (friction 0.4) = {top1:.2f}%")
