import dataclasses
import textwrap

import colorama
import prettytable

import defs


@dataclasses.dataclass
class License:
    title: str
    spdx_id: str
    description: str
    permissions: list[str]
    conditions: list[str]
    limitations: list[str]
    content: str

    def wrap_description(self) -> str:
        return "\n".join(textwrap.wrap(self.description))

    def pretty_table(self) -> prettytable.PrettyTable:
        table = prettytable.PrettyTable()
        table.set_style(prettytable.PLAIN_COLUMNS)
        rows: int = max(
            len(self.permissions), len(self.conditions), len(self.limitations)
        )
        permissions = self.colorful_permissions() + [""] * (
            rows - len(self.permissions)
        )
        conditions = self.colorful_conditions() + [""] * (rows - len(self.conditions))
        limitations = self.colorful_limitations() + [""] * (
            rows - len(self.limitations)
        )
        table.add_column(
            fieldname=License.colorful_title_permissions(),
            column=permissions,
            align="l",
        )
        table.add_column(
            fieldname=License.colorful_title_conditions(),
            column=conditions,
            align="l",
        )
        table.add_column(
            fieldname=License.colorful_title_limitations(),
            column=limitations,
            align="l",
        )
        return table

    def need(self, key: defs.PlaceHolderType) -> bool:
        place_holders: list[str] = defs.PLACE_HOLDERS[key]
        for place_holder in place_holders:
            if place_holder in self.content:
                return True
        return False

    def needs(self) -> list[defs.PlaceHolderType]:
        return list(filter(self.need, defs.PLACE_HOLDERS.keys()))

    def fill(self, info: dict[defs.PlaceHolderType]) -> str:
        content: str = self.content
        for key, value in info.items():
            place_holders: list[str] = defs.PLACE_HOLDERS[key]
            for place_holder in place_holders:
                content: str = content.replace(place_holder, value)
        return content

    def colorful_title_permissions() -> str:
        return License._colorful_str(
            string="permissions", style=colorama.Fore.GREEN + colorama.Style.BRIGHT
        )

    def colorful_title_conditions() -> str:
        return License._colorful_str(
            string="conditions", style=colorama.Fore.BLUE + colorama.Style.BRIGHT
        )

    def colorful_title_limitations() -> str:
        return License._colorful_str(
            string="limitations", style=colorama.Fore.RED + colorama.Style.BRIGHT
        )

    def colorful_permissions(self) -> list[str]:
        return License._colorful_list(self.permissions, colorama.Fore.GREEN)

    def colorful_conditions(self) -> list[str]:
        return License._colorful_list(self.conditions, colorama.Fore.BLUE)

    def colorful_limitations(self) -> list[str]:
        return License._colorful_list(self.limitations, colorama.Fore.RED)

    def _colorful_list(string_list: list[str], style: str) -> list[str]:
        return [
            License._colorful_str(string="- " + string.replace("-", " "), style=style)
            for string in string_list
        ]

    def _colorful_str(string: str, style: str) -> str:
        if string:
            return style + string.title() + colorama.Style.RESET_ALL
        else:
            return string
