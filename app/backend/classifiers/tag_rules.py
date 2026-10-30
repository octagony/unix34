import re
from typing import List, Dict

TAG_RULES: Dict[str, List[str]] = {
    "nixos": [
        r"\bnixos\b",
        r"\bnix\s+os\b",
    ],
    "ubuntu": [
        r"\bubuntu\b",
        r"\bkubuntu\b",
        r"\bxubuntu\b",
        r"\blubuntu\b",
    ],
    "mangowm": [
        r"\bmango\b",
        r"\bmangowm\b",
        r"\bmango\s*wm\b",
    ],
    "arch": [
        r"\barch\s+linux\b",
        r"\barchlinux\b",
        r"\barch\b",
    ],
    "fedora": [
        r"\bfedora\b",
        r"\bfedora\s+linux\b",
    ],
    "debian": [
        r"\bdebian\b",
    ],
    "kde": [
        r"\bkde\b",
        r"\bplasma\b",
    ],
    "gnome": [
        r"\bgnome\b",
    ],
    "hyprland": [
        r"\bhyprland\b",
        r"\bhypr\b",
        r"\bhyprwm\b",
    ],
    "sway": [
        r"\bsway\b",
        r"\bswaywm\b",
    ],
    "i3": [
        r"\bi3\b",
        r"\bi3wm\b",
        r"\bi3\s+wm\b",
    ],
    "wayland": [
        r"\bwayland\b",
    ],
    "cosmic": [
        r"\bcosmic\b",
    ],
    "openbox": [
        r"\bopenbox\b",
    ],
    "сinnamon": [
         r"\bcinnamon\b",
    ],
    "bspwm": [
        r"\bbspwm\b",
    ],
    "dwm": [
        r"\bdwm\b",
    ],
    "niri": [
        r"\bniri\b",
    ],
    "OC": [
        r"\boc\b",
        r"\bsystem\b",
    ],
}

COMPILED_RULES = {
    slug: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for slug, patterns in TAG_RULES.items()
}

def classify_post(title: str, body: str, flair: str) -> List[str]:
    search_text = f"{title} {body} {flair}".lower()
    
    matched_tags = []
    
    for slug, patterns in COMPILED_RULES.items():
        for pattern in patterns:
            if pattern.search(search_text):
                matched_tags.append(slug)
                break
                
    return matched_tags