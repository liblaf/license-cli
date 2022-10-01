import json

from license import License
import defs
import remote


def load_all() -> dict[str, License]:
    with open(file=defs.LOCAL_DB, mode="r") as file:
        licenses: dict[str] = json.load(fp=file)
        for key, value in licenses.items():
            licenses[key] = License(**value)
        return licenses


def dump_all() -> None:
    licenses: dict[str, License] = remote.fetch_all()
    with open(file=defs.LOCAL_DB, mode="w") as file:
        json.dump(obj=licenses, fp=file, default=lambda obj: obj.__dict__)


def get_all() -> dict[str, License]:
    try:
        return load_all()
    except:
        dump_all()
        return load_all()
