# KeyTune plugins

Public community catalog for the KeyTune 2 marketplace. The player reads `catalog.json` from the `main` branch.

## Install

In KeyTune's plugin manager, choose **Open marketplace**, select a plugin, and review its details and permissions before confirming. You can also download a `.ktplugin` release asset and install it through the manager.

Plugins are Python code with access to your computer. Install only plugins from authors you trust. A separate process isolates ordinary failures but is not a security sandbox.

## Contribute

1. Create a plugin following the developer guide: [English](https://github.com/Ed-Fe/KeyTune/blob/main/docs/plugins.en.md), [Português](https://github.com/Ed-Fe/KeyTune/blob/main/docs/plugins.md), or [Español](https://github.com/Ed-Fe/KeyTune/blob/main/docs/plugins.es.md).
2. Publish the `.ktplugin` package in a public release of your repository.
3. Calculate the final file's SHA-256; in PowerShell: `Get-FileHash file.ktplugin -Algorithm SHA256`.
4. Open a pull request adding or updating an entry in `catalog.json`: ID, name, version, description, author, homepage, HTTPS package URL, lowercase SHA-256, and `verified: false`.
5. Wait for automated validation and maintainer review.

Publish a new version whenever a package changes. Do not replace already cataloged assets. Each ID appears once in the catalog, pointing to the currently distributed version.

The `verified` field is reserved for maintainers after human review of provenance; it does not guarantee security. Automation checks the schema, unique IDs, download, checksum, ZIP paths, manifest, entrypoint, and compatibility with the reference KeyTune version. It does not execute the plugin.

## Maintenance

The workflow pins KeyTune's code to a reviewed commit. Update that reference when the supported contract changes. Workflow and validator changes also require maintainer review.

To validate locally, install `jsonschema` and run `python scripts/validate_catalog.py --keytune ../Media-Player`. This downloads packages and installs them only in temporary directories, without activation.
