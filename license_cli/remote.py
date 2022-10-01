import frontmatter
import requests
import tqdm.contrib.concurrent

from license import License
import defs


def fetch(download_url: str) -> License:
    raw: str = requests.get(url=download_url).content
    details: frontmatter.Post = frontmatter.loads(text=raw)
    license: License = License(
        title=details["title"],
        spdx_id=details["spdx-id"],
        description=details["description"],
        permissions=details["permissions"],
        conditions=details["conditions"],
        limitations=details["limitations"],
        content=details.content,
    )
    return license


def fetch_all() -> dict[str, License]:
    items: list[defs.RepoItem] = requests.get(url=defs.API_URL).json()
    licenses: list[License] = tqdm.contrib.concurrent.process_map(
        fetch, [item["download_url"] for item in items], desc="Fetching"
    )
    return dict(zip([license.spdx_id for license in licenses], licenses))
