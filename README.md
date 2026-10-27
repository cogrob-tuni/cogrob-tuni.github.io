# Cognitive Robotics Group landing page

Public website for the Cognitive Robotics Group at Tampere University:

<https://cogrob-tuni.github.io/>

## Automatic project list

The deployment workflow scans public `cogrob-tuni` repositories for:

```text
website/website/site.json
```

Only metadata with `"published": true` is displayed. The workflow generates the project list during deployment; it does not commit generated files back to this repository.

The landing page updates automatically:

- When changes are pushed to `main`
- Daily at 03:17 UTC
- Manually from **Actions → Deploy landing page → Run workflow**

After adding or changing a project's `website/site.json`, run **Actions → Deploy landing page → Run workflow** to refresh the published project list immediately. The scheduled run is only daily.

For a project to appear, a public repository must host its website on a `website` branch containing valid `website/site.json` metadata. This hosting repository does not need to contain source code: it can be a publication-only repository. The optional `repository` field adds a **Source code** link; omit it when no code is available.

`schemaVersion` identifies the metadata format. The current format is version `1`. Projects using another version are ignored until the landing page supports that format.

Required fields:

```json
{
  "schemaVersion": 1,
  "published": true,
  "title": "Project title",
  "description": "Short description.",
  "authors": ["Author Name"],
  "url": "https://cogrob-tuni.github.io/repository-name/"
}
```

Optional fields include `repository`, `image`, `year`, and `order`.

To trigger an update manually:

1. Open this repository on GitHub.
2. Select **Actions**.
3. Select **Deploy landing page**.
4. Click **Run workflow**.
5. Select the `main` branch.
6. Click **Run workflow** again.
