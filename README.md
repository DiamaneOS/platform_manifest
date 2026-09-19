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
