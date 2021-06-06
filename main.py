import re
from dataclasses import dataclass
import pyperclip

@dataclass
class Headline:
    level: str
    headline: str
    anchor: str = ""


r_headline = re.compile(r"(#+ )(.*)")
r_sub = re.compile(r"[^A-Za-z0-9- ]")

def read_file(path) -> list:
    with open(path, "r") as f:
        data = f.readlines()
    return data


def parse_data(data: list[str]) -> list:
    headlines = []
    for line in data:
        if match:=re.match(r_headline, line):
            level = match.group(1).strip()
            headline = match.group(2)
            anchor = create_anchor(headline)
            headlines.append(
                Headline(level, headline, anchor)
            )
    return headlines


def create_anchor(headline: str):
    """
    It downcases the string
    remove anything that is not a letter, number, space or hyphen(see the source for how Unicode is handled)
    changes any space to a hyphen.
    If that is not unique, add "-1", "-2", "-3", ... to make it unique
    """
    anchor = re.sub(r_sub, "", headline.lower()).replace(" ", "-")
    return anchor


def build_toc(headlines: list[Headline]) -> list[str]:
    toc = []
    for h in headlines:
        if len(h.level) <= 1:
            continue
        else:
            indentation = ((len(h.level) - 2) * 2)
            r = indentation * " " + "- [" + h.headline + "]" + "(#" + h.anchor + ")"
            toc.append(r)
    return toc

if __name__ == "__main__":
    data = read_file("./test.md")
    headlines = parse_data(data)
    toc = build_toc(headlines)
    pyperclip.copy("\n".join(toc))
