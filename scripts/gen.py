#! /usr/bin/env python3

import requests
import yaml
from collections import defaultdict
import os
import pathlib

def wow_banner():
    return \
r"""
   /\\\\\\\\\ ·····················································································
  /\\\//////// ····················································································
  \//\\\ ··························································································
   \////\\\        /\\\\\\\\   /\\/\\\\\\\     /\\\\\\\\\   /\\\\\\\\\     /\\\\\\\\\\\\\ ·········
───── \////\\\ ── /\\\/////\\\ \/\\\/////\\\  /\\\////// ─ /\\\/////\\\ ─ /\\\/////////\\\ ────────
─────────── \////\\\  /\\\\\\\\\\\ \//\\\\\\\\/\\\/\\\ ────── \//\\\\\\\\/\\\ \/\\\ ───── \/\\\ ───
─────────────── \////\\\ \//\\/////// ─ \///////\// \//\\\ ────── \///////\// ─ \//\\\ ──── /\\\ ──
─────────────────── \////\\\\\ ───────────────────── \///\\\ ───── /\\\/\\\\\\ ── \///\\\\\\\\\/ ──
                       \/////                          \/////      \///\\\\\\       \///////// ····
                                                                       \///// ·····················
"""

def wow_linguist_langs():
    with open('languages.yml', 'r') as f:
        return yaml.safe_load(f)

def wow_anchor_link(language, aliases):
    header = f"{language} · {', '.join(aliases)}"
    a = header.lower().replace(" · ", "--").replace(", ", "-").replace(" ", "-")
    return a

def wow_letter_nav(current_letter):
    abc = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    parts = []
    parts.append("[/ back](../)")

    for l in abc:
        if l == current_letter:
            parts.append(f" {l} ")
        else:
            parts.append(f"[{l}](../{l})")

    return " · ".join(parts)


def wow_letter_readme(l, lang_dict):
    l_dir = pathlib.Path("Languages") / l
    l_dir.mkdir(parents=True, exist_ok=True)

    with open(l_dir / "README.md", "w") as f:
        f.write(f"{wow_letter_nav(l)}\n\n")
        for lang, aliases in sorted(lang_dict.items()):
            alias_str = ", ".join(aliases)
            f.write(f"##### {lang} · `{alias_str}`\n")
            f.write(f"```{aliases[0]}\n")
            f.write(wow_banner())
            f.write("\n```\n\n")

def wow_main_readme(az):
    pathlib.Path("Languages").mkdir(exist_ok=True)
    with open("Languages/README.md", "w") as f:
        f.write("[/ back](../)\n\n")
        f.write("## Languages\n\n")

        for letter in sorted(az.keys()):
            f.write(f"- [{letter}](./{letter})\n")
            for lang, aliases in sorted(az[letter].items()):
                anchor = wow_anchor_link(lang, aliases)
                f.write(f"    - [{lang}](./{letter}/README.md#{anchor})\n")

def wow_parse_languages():
    lang_data = wow_linguist_langs()
    az = defaultdict(dict)

    for lang, props in lang_data.items():
        aliases = props.get('aliases', [])
        if not aliases:
            continue

        first_l = lang[0].upper()
        az[first_l][lang] = aliases

    pathlib.Path("Languages").mkdir(exist_ok=True)
    wow_main_readme(az)
    for l in az:
        wow_letter_readme(l, az[l])

if __name__ == "__main__":
    try:
        wow_parse_languages()
    except Exception as e:
        print(f"An error occurred: {e}")
