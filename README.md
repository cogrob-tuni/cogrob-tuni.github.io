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

For a project to appear, its public repository must have a `website` branch containing valid `website/site.json` metadata.

To trigger an update manually:

1. Open this repository on GitHub.
2. Select **Actions**.
3. Select **Deploy landing page**.
4. Click **Run workflow**.
5. Select the `main` branch.
6. Click **Run workflow** again.
