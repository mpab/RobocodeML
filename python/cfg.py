import pathlib


data_root = "../data/"
analysis_root = data_root + "trained_models_analysis/"
features_root = data_root + "features/"
model_root = data_root + "trained_models/"

observations_root = data_root + "observations/"
observations = "observations.csv"

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

feature_classes = ["raw", "scaled", "rounded"]


def ensure_path(path):
    pathlib_path = pathlib.Path(path)
    pathlib_path.mkdir(parents=True, exist_ok=True)
    return pathlib_path


def ensure_fp(path, filename):
    pathlib_path = ensure_path(path)
    fp = pathlib_path / filename
    return fp
