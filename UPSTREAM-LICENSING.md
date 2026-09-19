# Manifest licensing and provenance

The root [Apache-2.0 licence](LICENSE) covers original DiamaneOS contributions:
the project documentation, `freeze.py`, the generated DiamaneOS revision
overrides and the project-authored pin observations. It does not relicense the
upstream project definitions in `default.xml` or the source trees they fetch.

## Imported project definitions

`default.xml` comes from GrapheneOS `platform_manifest` revision
`75ae9fb65fa78389ea4a4d5f21aa1ba4be88e287`. The local modification adds
`<include name="diamaneos.xml"/>`; the upstream definitions remain preserved.
The upstream generated-file notice identifies `adevtool` as the generator.

- [Pinned upstream file](https://github.com/GrapheneOS/platform_manifest/blob/75ae9fb65fa78389ea4a4d5f21aa1ba4be88e287/default.xml)
- [Pinned upstream tree](https://github.com/GrapheneOS/platform_manifest/tree/75ae9fb65fa78389ea4a4d5f21aa1ba4be88e287)
- [Preserved upstream notice](third_party/grapheneos-platform-manifest/COPPERHEAD-NOTICE)

At that revision, the upstream tree contains `COPPERHEAD-NOTICE`,
`GLOBAL-PREUPLOAD.cfg`, `config.yml` and `default.xml`. It contains no explicit
licence file, and `default.xml` has no licence header or SPDX identifier.
GrapheneOS's [general licensing explanation](https://grapheneos.org/faq#copyright-and-licensing)
describes inherited upstream licences and MIT licensing for standalone
projects; it does not supply an explicit licence declaration for this pinned
manifest file. Its exact licence identification therefore remains unresolved.
The DiamaneOS Apache-2.0 declaration must not be read as resolving that gap.

The preserved upstream notice has SHA-256
`c8ccc0c4e5f3f6ccda46d448f75d359a3fd7c152e1b029c0ecd901f624f708c3`.
It is upstream's statement, retained as source provenance without modification.

## Projects fetched through the manifests

Every fetched project retains its own applicable licences and notices. A
manifest entry or revision pin does not place that project's code under this
repository's licence. Preserve the actual per-file SPDX identifiers, licence
texts, copyright and attribution notices when importing or changing code.
