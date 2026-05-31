#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import requests


LANGUAGE_ITEMS = {
    "TypeScript": {"label": "TypeScript", "slug": "typescript", "accent": "#3178C6"},
    "Python": {"label": "Python", "slug": "python", "accent": "#3776AB"},
    "JavaScript": {"label": "JavaScript", "slug": "javascript", "accent": "#F7DF1E"},
    "C++": {"label": "C++", "slug": "cplusplus", "accent": "#00599C"},
    "C": {"label": "C", "slug": "c", "accent": "#A8B9CC"},
    "Go": {"label": "Go", "slug": "go", "accent": "#00ADD8"},
    "Rust": {"label": "Rust", "slug": "rust", "accent": "#000000"},
    "Java": {"label": "Java", "slug": "openjdk", "accent": "#F89820"},
}

TOOL_RULES = [
    {
        "item": {"label": "Next.js", "slug": "nextdotjs", "accent": "#111111"},
        "patterns": ["next", "nextjs", "next.js"],
        "files": ["next.config.js", "next.config.mjs", "next.config.ts"],
        "deps": ["next"],
    },
    {
        "item": {"label": "React", "slug": "react", "accent": "#61DAFB"},
        "patterns": ["react"],
        "files": [],
        "deps": ["react"],
    },
    {
        "item": {"label": "Node.js", "slug": "nodedotjs", "accent": "#5FA04E"},
        "patterns": ["node", "nodejs", "node.js"],
        "files": ["package.json"],
        "deps": [],
    },
    {
        "item": {"label": "Tailwind CSS", "slug": "tailwindcss", "accent": "#06B6D4"},
        "patterns": ["tailwind"],
        "files": ["tailwind.config.js", "tailwind.config.ts", "tailwind.config.cjs"],
        "deps": ["tailwindcss"],
    },
    {
        "item": {"label": "Docker", "slug": "docker", "accent": "#2496ED"},
        "patterns": ["docker"],
        "files": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
        "deps": [],
    },
    {
        "item": {"label": "Vercel", "slug": "vercel", "accent": "#000000"},
        "patterns": ["vercel"],
        "files": ["vercel.json"],
        "deps": ["vercel"],
    },
    {
        "item": {"label": "GitHub", "slug": "github", "accent": "#24292F"},
        "patterns": ["github actions", "github-action", "github"],
        "files": [".github"],
        "deps": [],
    },
    {
        "item": {"label": "Splunk", "slug": "splunk", "accent": "#65A637"},
        "patterns": ["splunk", "spl"],
        "files": [],
        "deps": [],
    },
    {
        "item": {"label": "Midnight", "slug": None, "accent": "#0F172A", "short": "MN"},
        "patterns": ["midnight"],
        "files": [],
        "deps": [],
    },
    {
        "item": {"label": "MCP", "slug": None, "accent": "#8B5CF6", "short": "MC"},
        "patterns": ["mcp", "model context protocol"],
        "files": [],
        "deps": [],
    },
    {
        "item": {"label": "Compact", "slug": None, "accent": "#6D28D9", "short": "CP"},
        "patterns": ["compact"],
        "files": [],
        "deps": [],
    },
]

DATA_PATH = Path("data/stack_items.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build stack data from GitHub repos.")
    parser.add_argument("--user", default=os.getenv("GITHUB_REPOSITORY_OWNER", "prantikmedhi"))
    parser.add_argument("--output", default=str(DATA_PATH))
    parser.add_argument("--limit", type=int, default=14)
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def github_session() -> requests.Session:
    session = requests.Session()
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    session.headers.update(headers)
    return session


def paginate(session: requests.Session, url: str, params: dict[str, str | int] | None = None) -> list[dict]:
    results: list[dict] = []
    next_url = url
    next_params = params or {}

    while next_url:
        response = session.get(next_url, params=next_params, timeout=20)
        response.raise_for_status()
        results.extend(response.json())
        links = response.links
        next_url = links.get("next", {}).get("url")
        next_params = {}

    return results


def safe_get_json(session: requests.Session, url: str) -> dict | list | None:
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
    except requests.RequestException:
        return None
    return response.json()


def repo_text(repo: dict) -> str:
    parts = [
        repo.get("name") or "",
        repo.get("description") or "",
        " ".join(repo.get("topics") or []),
    ]
    return " ".join(parts).lower()


def fetch_root_names(session: requests.Session, repo: dict) -> set[str]:
    contents_url = f"https://api.github.com/repos/{repo['full_name']}/contents"
    payload = safe_get_json(session, contents_url)
    if not isinstance(payload, list):
        return set()
    return {entry.get("name", "") for entry in payload}


def fetch_package_dependencies(session: requests.Session, repo: dict) -> set[str]:
    package_url = f"https://api.github.com/repos/{repo['full_name']}/contents/package.json"
    payload = safe_get_json(session, package_url)
    if not isinstance(payload, dict) or payload.get("encoding") != "base64":
        return set()

    import base64

    try:
        content = base64.b64decode(payload["content"]).decode("utf-8")
        package_data = json.loads(content)
    except Exception:
        return set()

    deps = set()
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        deps.update((package_data.get(key) or {}).keys())
    return deps


def detect_languages(session: requests.Session, repos: list[dict]) -> list[dict[str, str | None]]:
    scores = defaultdict(int)
    for repo in repos:
        languages = safe_get_json(session, repo["languages_url"])
        if not isinstance(languages, dict):
            continue
        for language, bytes_used in languages.items():
            scores[language] += int(bytes_used)

    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    items = []
    for language, _ in ordered:
        mapped = LANGUAGE_ITEMS.get(language)
        if mapped and mapped not in items:
            items.append(mapped)
    return items


def detect_tools(session: requests.Session, repos: list[dict]) -> list[dict[str, str | None]]:
    matches: Counter[str] = Counter()
    label_to_item = {rule["item"]["label"]: rule["item"] for rule in TOOL_RULES}

    for repo in repos:
        text = repo_text(repo)
        root_names = fetch_root_names(session, repo)
        deps = fetch_package_dependencies(session, repo) if "package.json" in root_names else set()

        for rule in TOOL_RULES:
            label = rule["item"]["label"]
            if any(pattern in text for pattern in rule["patterns"]):
                matches[label] += 2
            if any(file_name in root_names for file_name in rule["files"]):
                matches[label] += 2
            if any(dep in deps for dep in rule["deps"]):
                matches[label] += 2

    ordered_labels = [label for label, _ in matches.most_common()]
    return [label_to_item[label] for label in ordered_labels]


def build_stack(session: requests.Session, user: str, limit: int) -> list[dict[str, str | None]]:
    repos = paginate(
        session,
        f"https://api.github.com/users/{user}/repos",
        {"per_page": 100, "sort": "updated"},
    )
    repos = [repo for repo in repos if not repo.get("fork")]

    detected = []
    seen = set()

    for item in detect_languages(session, repos) + detect_tools(session, repos):
        label = item["label"]
        if label in seen:
            continue
        seen.add(label)
        detected.append(item)
        if len(detected) >= limit:
            break

    return detected


def main() -> None:
    args = parse_args()
    session = github_session()
    stack_items = build_stack(session, args.user, args.limit)

    output_path = repo_root() / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(stack_items, indent=2) + "\n")
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
