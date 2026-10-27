#!/usr/bin/env python3
"""Build the public project registry from published project-site metadata."""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ORG = os.environ.get("GITHUB_ORG", "cogrob-tuni")
TOKEN = os.environ.get("GITHUB_TOKEN")
OUTPUT = "data/projects.json"
REQUIRED_FIELDS = ("schemaVersion", "published", "title", "description", "authors", "url")
OPTIONAL_FIELDS = ("repository", "image", "year", "order")


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
    except HTTPError as error:
        print(f"Skipped {repository}: metadata unavailable (HTTP {error.code})", file=sys.stderr)
        return None
    except URLError:
        print(f"Skipped {repository}: metadata unavailable (network error)", file=sys.stderr)
        return None


def validation_reason(metadata):
    if not metadata:
        return "missing metadata"
    if metadata.get("schemaVersion") != 1:
        return "unsupported schemaVersion"
    if metadata.get("published") is not True:
        return "published is not true"
    if not all(metadata.get(field) for field in REQUIRED_FIELDS[2:]):
        return "missing required fields"
    if not isinstance(metadata["authors"], list):
        return "authors is not a list"
    if any(field not in REQUIRED_FIELDS + OPTIONAL_FIELDS for field in metadata):
        return "unknown fields"
    if any(not isinstance(author, str) or not author.strip() for author in metadata["authors"]):
        return "authors contains an invalid value"
    if any(
        field in metadata and metadata[field] is not None
        and not isinstance(metadata[field], str)
        for field in ("repository", "image")
    ):
        return "repository or image is not a string"
    if "year" in metadata and metadata["year"] is not None and (
        not isinstance(metadata["year"], int) or isinstance(metadata["year"], bool)
    ):
        return "year is not an integer"
    if "order" in metadata and metadata["order"] is not None and (
        not isinstance(metadata["order"], int) or isinstance(metadata["order"], bool)
    ):
        return "order is not an integer"
    return None


def valid_project(metadata):
    return validation_reason(metadata) is None


def main():
    repositories = fetch_json(
        f"https://api.github.com/orgs/{ORG}/repos?per_page=100&type=public"
    )
    projects = []
    skipped = {}
    for repository in repositories:
        metadata = fetch_metadata(repository["name"])
        if valid_project(metadata):
            projects.append(metadata)
            print(f"Included {repository['name']}", file=sys.stderr)
        else:
            reason = validation_reason(metadata) or "unknown"
            skipped[reason] = skipped.get(reason, 0) + 1
            if metadata:
                print(f"Skipped {repository['name']}: {reason}", file=sys.stderr)

    projects.sort(key=lambda project: (project.get("order", 1000), project["title"].lower()))
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as output:
        json.dump(projects, output, indent=2)
        output.write("\n")
    print(f"Published projects: {len(projects)}", file=sys.stderr)
    if skipped:
        summary = ", ".join(f"{reason}={count}" for reason, count in sorted(skipped.items()))
        print(f"Skipped repositories: {summary}", file=sys.stderr)


if __name__ == "__main__":
    main()
