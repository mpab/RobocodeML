import pathlib

trainer = 'sample.SpinBot'

data_root = "../data-" + trainer + "/"

observations_root = data_root + "observations/"

observations = "observations.csv"

features_root = data_root + "features/"
features_unscanned_root = data_root + "features_unscanned/"
features = "features.csv"

models_root = data_root + "models/"

csv_column_names = [
    "action",
    "x",
    "y",
    "heading",
    "enemy_distance",
    "enemy_bearing",
    "enemy_x",
    "enemy_y",
    "enemy_collisions",
    "wall_collisions",
    "shell_hits",
    "shell_wounds",
    "shell_intercepts"
]

onehot_targets = [
    "enemy_collisions",     # minimise
    "wall_collisions",      # minimise
    "shell_wounds",         # minimise
    "shell_intercepts",     # maximise
    "shell_hits"            # maximise
]

# convention: feature_target
# convention: feature_target_target
features_classes = [
    "pure_pure",
    "pure_boolean",
    "scaled_pure",
    "scaled_boolean",
]

features_filters = [
   ["xyhead_wc", ["action", "x", "y", "heading", "wall_collisions"]],
]

#classification_compatible = [
#    "pure_classified",
#    "pure_boolean_classified",
#    "scaled_classified",
#    "scaled_boolean_classified"
#]


def ensure_path(path):
    pathlib_path = pathlib.Path(path)
    pathlib_path.mkdir(parents=True, exist_ok=True)
    return pathlib_path


def ensure_fp(path, filename):
    pathlib_path = ensure_path(path)
    fp = pathlib_path / filename
    return str(fp)
