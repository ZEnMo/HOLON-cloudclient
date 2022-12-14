import os
import shutil
import sys
from pathlib import Path

import yaml

CONFIG_FOLDER = Path(__file__).parent.parent / "cloudclient" / "config"


def pprint(prompt):
    print("[HOLON-cloudclient]: " + prompt)


def create_folder(folder_location: str = None, get_api_key: bool = None) -> None:

    if folder_location is None:
        args = sys.argv[1:]
        if not ("-tf" in args or "--target-folder" in args):
            raise SystemExit(
                "Please provide the target folder using the [-tf | --target-folder] option to specify the relative location of the .cloudclient folder."
            )
        else:
            for i, arg in enumerate(args):
                if "-tf" in arg or "--target-folder" in arg:
                    try:
                        target_folder = args[i + 1]
                    except IndexError:
                        raise SystemError(
                            "Option [-tf | --target-folder] is supplied but no value is supplied!"
                        )
    abs_target = (Path().resolve().absolute() / target_folder).__str__()
    pprint(f"Initiating cloudclient... \t (at {abs_target})")

    # make folders
    BASE_PATH = Path(target_folder + "/.cloudclient")
    BASE_PATH.mkdir(exist_ok=True, parents=True)
    CONFIG_PATH = BASE_PATH / "config"
    CONFIG_PATH.mkdir(exist_ok=True, parents=True)
    (BASE_PATH / "input").mkdir(exist_ok=True, parents=True)
    (BASE_PATH / "ouput").mkdir(exist_ok=True, parents=True)

    # move files
    config_target = CONFIG_PATH / "config.yml"
    if not config_target.exists():
        shutil.copy2(
            CONFIG_FOLDER / "config.example.yml",
            config_target,
        )
    else:
        pprint("Config file already exists at provided location, skipping!")

    experiment_target = CONFIG_PATH / "experiments.yml"
    if not experiment_target.exists():
        shutil.copy2(
            CONFIG_FOLDER / "experiments.example.yml",
            experiment_target,
        )
    else:
        pprint("Experiment file already exists at provided location, skipping!")

    # add a pointer to the new top folder
    with open(CONFIG_FOLDER / ".cloudclient_location.yml", "w") as f:
        yaml.dump({"file_path": str(CONFIG_PATH.absolute())}, f)

    pprint("Done!")

    if get_api_key is None:
        if "--get-api-key" in args:
            update_config_yaml(CONFIG_PATH / "config.yml")
        else:
            pprint(
                "No api_key is supplied. Either add it to 'cloudclient/config/config.yml' or get it from OS by adding the [--get-api-key] to the options."
            )


def update_config_yaml(config_path: Path) -> None:

    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    config["anylogic_cloud"]["api_key"] = os.environ["AL_API_KEY"]

    with open(config_path, "w") as f:
        yaml.dump(config, f)
