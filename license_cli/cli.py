import datetime
import os.path
import re

import git.config
import questionary

from license import License
import local


def main():
    licenses: dict[str, License] = local.get_all()
    spdx_id: str = ask_license(licenses=licenses)
    license: License = licenses[spdx_id]
    print(license.wrap_description())
    print(license.pretty_table())
    needs = license.needs()
    info: dict[str, str] = dict()
    if "year" in needs:
        info["year"] = ask_year()
    if "name" in needs:
        info["name"] = ask_name()
    content: str = license.fill(info=info)
    if not content.endswith("\n"):
        content += "\n"
    print(content)
    write: bool = True
    if os.path.exists(path="LICENSE"):
        write: bool = ask_confirm(message="Are you sure to overwrite LICENSE?")
    if write:
        with open(file="LICENSE", mode="w") as file:
            file.write(content)
            success("LICENSE generated successfully")


def ask_license(licenses: dict[str, License]) -> str:
    def validate(input: str) -> bool:
        return input in licenses.keys()

    return questionary.autocomplete(
        message="Choose a license",
        choices=list(licenses.keys()),
        default="MIT",
        meta_information=_make_meta_info(licenses=licenses),
        validate=validate,
    ).ask()


def ask_year() -> str:
    default_year: str = str(datetime.datetime.now().year)
    return questionary.text(
        message="Year",
        default=default_year,
        validate=_validate_year,
    ).ask()


def ask_name() -> str:
    default_name: str
    try:
        git_config = git.config.GitConfigParser(
            file_or_files=git.config.get_config_path(config_level="global")
        )
        default_name: str = git_config.get_value(section="user", option="name")
    except:
        default_name: str = ""
    return questionary.text(
        message="Name", default=default_name, validate=_validate_name
    ).ask()


def ask_confirm(message: str) -> bool:
    return questionary.confirm(message=message).ask()


def success(message: str) -> None:
    questionary.print(text=message, style="fg:ansibrightgreen")


def _make_meta_info(licenses: dict[str, License]) -> dict[str, str]:
    meta_info: dict[str, str] = dict()
    for key, value in licenses.items():
        meta_info[key] = value.title
    return meta_info


def _validate_year(input: str) -> bool:
    try:
        return bool(re.fullmatch(pattern=r"^[12]\d{3}$", string=input))
    except:
        return False


def _validate_name(input: str) -> bool:
    return bool(input)
