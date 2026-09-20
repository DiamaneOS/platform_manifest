# DiamaneOS manifest overlay

This repository contains the small Android `repo` local-manifest overlay owned
by DiamaneOS. It does not copy, fork or repin the upstream platform manifest.

The base source tree is selected from an authenticated GrapheneOS release tag.
The authoritative tag, tag object, peeled manifest commit and resolved project
map belong to the corresponding immutable build-environment record in
[`diamaneos-tools`](https://codeberg.org/DiamaneOS/diamaneos-tools/src/branch/main/config/build-environment.json).
Changing any of those inputs creates a new environment identity; this overlay
must not provide a second value for them.

## Contents

- [diamaneos.xml](diamaneos.xml) is the local-manifest overlay. It contains
  only repositories, forks, removals or overrides actually owned by a current
  DiamaneOS integration. It is intentionally empty of projects today.
- [validate.py](validate.py) checks the overlay policy and can verify that a
  resolved checkout contains only immutable project revisions and unique
  checkout paths.

There is deliberately no copied upstream `default.xml`, generated list of
upstream revision overrides or observed branch-head inventory here. A signed
GrapheneOS release already defines the upstream project set. Repeating that
set in this repository would create a second pin authority and make updates
harder to audit.

## Use with a selected release

Initialize the source checkout from the release declared by the selected
build-environment record, verify that release as required by the build
procedure, and then install the overlay as a local manifest before syncing:

```sh
repo init \
  -u https://github.com/GrapheneOS/platform_manifest.git \
  -b "refs/tags/$GRAPHENEOS_RELEASE"

install -d -m 0755 .repo/local_manifests
install -m 0644 "$OVERLAY_ROOT/diamaneos.xml" \
  .repo/local_manifests/diamaneos.xml

repo sync
repo manifest -r -o resolved-manifest.xml
python3 "$OVERLAY_ROOT/validate.py" \
  --resolved resolved-manifest.xml
```

`GRAPHENEOS_RELEASE` is the reviewed release tag from the build-environment
record. `OVERLAY_ROOT` is this repository checkout. The complete build
procedure additionally verifies the signed tag, the `repo` implementation and
the expected resolved project-map digest; copying this example alone is not a
substitute for those checks.

The currently accepted environment has no DiamaneOS overlay projects, so its
existing qualified checkout remains unchanged. Adding the first project or
override will create a new build-environment identity and require a new source
sync and affected qualification.

## Adding a DiamaneOS repository or fork

Add an entry only when the repository exists and its integration is ready:

1. Add a `<project>` for a new repository, or a reviewed
   `<remove-project>`/replacement `<project>` pair for an upstream fork.
2. Use the `diamaneos` remote and an exact 40-character commit revision.
   Branch names, moving tags and placeholder repositories are rejected.
3. Preserve the upstream path and attribution when replacing a project.
4. Record applicable source licences, notices, downstream changes and the
   removal/rebase condition in the owning component records.
5. Run the checks below, resolve the full manifest with `repo manifest -r`,
   bind its digest into a new build environment and qualify that environment.

Do not add upstream projects merely to repeat their GrapheneOS revisions. Do
not create empty repositories to match a planned architecture.

## Checks

The local checks require only Python 3:

```sh
python3 validate.py --check
python3 -m unittest discover -s tests
```

After a source sync, also validate the immutable resolved output:

```sh
python3 validate.py --resolved /path/to/resolved-manifest.xml
```

## Upstream identity

DiamaneOS is based on GrapheneOS source and is not affiliated with or endorsed
by the GrapheneOS project. Follow the
[GrapheneOS branding guidance](https://grapheneos.org/faq#trademarks) when
integrating product identity.

Every fetched source project retains its own applicable licences, copyright
notices and attribution requirements. This repository's Apache-2.0 licence
covers only the original overlay, validation code and documentation stored
here.
