import pathlib
import typing

BASE_URL: str = "https://api.github.com"
OWNER: str = "github"
REPO: str = "choosealicense.com"
PATH: str = "_licenses"
API_URL: str = f"{BASE_URL}/repos/{OWNER}/{REPO}/contents/{PATH}"

LOCAL_DB: str = pathlib.Path.home() / ".cache" / "licenses.json"


class RepoItem(typing.TypedDict):
    download_url: str


PlaceHolderType = typing.Literal["year", "name"]
PLACE_HOLDERS: dict[PlaceHolderType, list[str]] = {
    "year": ["[year]"],
    "name": ["[fullname]", "[name]"],
}
