# DiamaneOS source manifest

Source manifests and revision-pinning tools for DiamaneOS.

## Contents and status

- [default.xml](default.xml): imported GrapheneOS project definitions with an
  include for the DiamaneOS delta.
- [diamaneos.xml](diamaneos.xml): generated revision overrides and the project
  remote definition.
- [Source observations](upstream-pins-2026-09-10.json): the observed upstream
  manifest commit and project revisions used by the generator.
- [freeze.py](freeze.py): generates the delta and checks the effective revision
  table and checkout-path uniqueness.

This is source-integration preparation. Source observations and manifest checks
do not establish release-signature verification, a working FP6 port or a
qualified OS release.

The dated files in this repository are a preserved source-integration snapshot,
not the active builder checkout or a current FP6 product manifest. The current
selected GrapheneOS release, signer identity and canonical project map are
bound separately by `diamaneos-tools/config/build-environment.json`. Refresh
this repository from a reviewed upstream manifest before using it as a build
input; do not infer currentness from its default branch.

The snapshot is reproducible on any host with Python 3 and no Android checkout:

```sh
python3 freeze.py --check
python3 freeze.py --self-test
```

`python3 freeze.py` regenerates `diamaneos.xml` from the byte-preserved
`default.xml` and dated observation file. A new snapshot must use a new dated
observation file and update the generator deliberately rather than overwriting
the provenance of this one.

Upstream names, URLs and project identifiers identify the sources being used.
The current manifests use GrapheneOS sources; DiamaneOS is not affiliated with
or endorsed by the GrapheneOS project.
Retain their attribution; DiamaneOS product branding must be integrated before
distributing modified OS images, as described in the
[GrapheneOS branding guidance](https://grapheneos.org/faq#trademarks).

## Licence

Original DiamaneOS code, documentation and manifest additions are licensed
under [Apache-2.0](LICENSE). Imported project definitions and fetched source
trees retain their upstream terms. See [NOTICE](NOTICE) and
[upstream licensing and provenance](UPSTREAM-LICENSING.md), including the
unresolved licence identification for the pinned upstream `default.xml`.
