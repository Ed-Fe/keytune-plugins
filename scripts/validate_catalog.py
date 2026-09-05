"""Validate packages with KeyTune's installer without loading plugin code."""

import argparse
import importlib
import json
from pathlib import Path
import re
import sys
import tempfile
import types

import jsonschema


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keytune', type=Path, required=True)
    parser.add_argument('--catalog', type=Path, default=Path('catalog.json'))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    document = json.loads(args.catalog.read_text(encoding='utf-8'))
    schema = json.loads((root / 'catalog.schema.json').read_text(encoding='utf-8'))
    jsonschema.Draft202012Validator(schema).validate(document)

    # Load only the dependency-free validation modules, bypassing GUI/service
    # imports in package initializers. Never import an installed plugin.
    source = args.keytune.resolve() / 'src' / 'player'
    for name, path in [('player', source), ('player.plugins', source / 'plugins')]:
        package = types.ModuleType(name)
        package.__path__ = [str(path)]
        sys.modules[name] = package
    marketplace = importlib.import_module('player.plugins.marketplace')
    installer = importlib.import_module('player.plugins.installer')
    constants = importlib.import_module('player.constants')
    api = importlib.import_module('player.plugins.api')
    entries = marketplace.parse_catalog(json.dumps(document))

    def version(value):
        return tuple(map(int, re.match(r'^(\d+)\.(\d+)\.(\d+)', value).groups()))

    with tempfile.TemporaryDirectory(prefix='keytune-catalog-') as temporary:
        directory = Path(temporary)
        for entry in entries:
            archive = directory / (entry.id + '.ktplugin')
            installer.download_package(entry.download_url, archive)
            manifest = installer.install_archive(
                archive, directory / 'plugins', expected_sha256=entry.sha256,
                expected_plugin_id=entry.id, expected_version=entry.version,
            )
            if manifest.api_version.split('.')[0] != api.API_VERSION.split('.')[0]:
                raise ValueError(f'{entry.id}: API incompatível')
            if version(manifest.minimum_keytune_version) > version(constants.APP_VERSION):
                raise ValueError(f'{entry.id}: requer KeyTune mais recente')
            if manifest.name != entry.name or manifest.author != entry.author:
                raise ValueError(f'{entry.id}: nome/autor divergem do manifesto')
            print(f'OK: {entry.id} {entry.version}')
    print(f'Catálogo válido: {len(entries)} plugin(s).')


if __name__ == '__main__':
    main()
