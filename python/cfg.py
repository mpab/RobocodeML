import pathlib

data_root = "../data/"

observations_root = data_root + "observations/"
observations = "observations.csv"

features_root = data_root + "features/"
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
    "enemy_collisions",
    "wall_collisions",
    "shell_hits",
    "shell_wounds",
    "shell_intercepts"
]

# convention: feature_target
# convention: feature_target_target
features_classes = [
    "pure_pure",
    "pure_classified",
    "pure_boolean",
    "pure_boolean_classified",
    "scaled_pure",
    "scaled_classified",
    "scaled_boolean",
    "scaled_boolean_classified"
]

classification_compatible = [
    "pure_classified",
    "pure_boolean_classified",
    "scaled_classified",
    "scaled_boolean_classified"
]


def ensure_path(path):
    pathlib_path = pathlib.Path(path)
    pathlib_path.mkdir(parents=True, exist_ok=True)
    return pathlib_path


def ensure_fp(path, filename):
    pathlib_path = ensure_path(path)
    fp = pathlib_path / filename
    return str(fp)
