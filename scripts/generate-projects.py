#!/usr/bin/env python3
"""Build the public project registry from published project-site metadata."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ORG = os.environ.get("GITHUB_ORG", "cogrob-tuni")
TOKEN = os.environ.get("GITHUB_TOKEN")
OUTPUT = "data/projects.json"


def fetch_json(url):
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def fetch_metadata(repository):
    url = f"https://raw.githubusercontent.com/{ORG}/{repository}/website/website/site.json"
    try:
        return fetch_json(url)
    except (HTTPError, URLError):
        return None


def valid_project(metadata):
    required = ("title", "description", "authors", "url", "repository")
    return (
        metadata
        and metadata.get("schemaVersion") == 1
        and metadata.get("published") is True
        and all(metadata.get(field) for field in required)
        and isinstance(metadata["authors"], list)
    )


def main():
    repositories = fetch_json(
        f"https://api.github.com/orgs/{ORG}/repos?per_page=100&type=public"
    )
    projects = []
    for repository in repositories:
        metadata = fetch_metadata(repository["name"])
        if valid_project(metadata):
            projects.append(metadata)

    projects.sort(key=lambda project: (project.get("order", 1000), project["title"].lower()))
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as output:
        json.dump(projects, output, indent=2)
        output.write("\n")


if __name__ == "__main__":
    main()
