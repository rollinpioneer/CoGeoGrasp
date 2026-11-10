"""Summarize a scene-results CSV in the format of Supplementary Data S1."""

import argparse
import csv
import sys
from collections import defaultdict
from statistics import fmean


CONDITION_FIELDS = ("comparison", "detector", "method", "collision_voxel_mm", "critic_ensembles")
SPLITS = ("Seen", "Similar", "Novel")


def summarize(rows):
    by_condition = defaultdict(dict)
    for row in rows:
        condition = tuple(row[field] for field in CONDITION_FIELDS)
        scene_id = int(row["scene_id"])
        scenes = by_condition[condition]
        if scene_id in scenes:
            raise ValueError(f"Duplicate scene {scene_id} for condition {condition}.")
        split = row["object_split"]
        if split not in SPLITS:
            raise ValueError(f"Unknown object split {split!r} for scene {scene_id}.")
        ap, top1 = float(row["ap_percent"]), float(row["top1_percent"])
        if not (0 <= ap <= 100 and 0 <= top1 <= 100):
            raise ValueError(f"Scene {scene_id} has a percentage outside [0, 100].")
        scenes[scene_id] = (split, ap, top1)

    for condition, scenes in by_condition.items():
        for split in ("All", *SPLITS):
            scores = [(ap, top1) for label, ap, top1 in scenes.values()
                      if split == "All" or label == split]
            if scores:
                ap_scores, top1_scores = zip(*scores)
                yield (*condition, split, len(scores), fmean(ap_scores), fmean(top1_scores))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scene_csv", help="Path to scene_results.csv")
    args = parser.parse_args()
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow((*CONDITION_FIELDS, "object_split", "n_scenes", "ap_percent", "top1_percent"))
    with open(args.scene_csv, encoding="utf-8-sig", newline="") as source:
        for *group, ap, top1 in summarize(csv.DictReader(source)):
            writer.writerow((*group, f"{ap:.2f}", f"{top1:.2f}"))
