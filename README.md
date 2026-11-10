# CoGeoGrasp

*Contact-Geometry-Guided Pose Re-selection for Six-Degree-of-Freedom Grasp Detection with Limited Annotations*

[`pose_selection.py`](pose_selection.py) implements the pose-replacement threshold.

## Evaluation tools

| Script | Input | Output |
| --- | --- | --- |
| [`graspnet_metrics.py`](tools/graspnet_metrics.py) | A NumPy precision array from the GraspNet evaluator, with 50 rank cutoffs and six friction levels as its last two axes | AP and Top-1 success at a friction coefficient of 0.4, both in percent |
| [`summarize_scenes.py`](tools/summarize_scenes.py) | A `scene_results.csv` file in the format of Supplementary Data S1 | Mean AP and Top-1 for each evaluation condition, overall and for the Seen, Similar and Novel splits |

```sh
python tools/graspnet_metrics.py precision.npy
python tools/summarize_scenes.py scene_results.csv
```

The first script requires NumPy and accepts precision values from 0 to 1. The second uses the Python standard library and gives each scene equal weight.

Additional code will be released here after it has been organized.
