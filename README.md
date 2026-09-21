# DiamaneOS manifest overlay

This repository contains the Android `repo` local-manifest overlay for
DiamaneOS. The base source tree comes directly from an authenticated GrapheneOS
release tag; this repository does not copy or repin the upstream manifest.

The selected release, manifest commit and resolved project-map digest are
recorded in the corresponding immutable build environment in
[`diamaneos-tools`](https://github.com/DiamaneOS/diamaneos-tools/blob/main/config/build-environment.json).

[`diamaneos.xml`](diamaneos.xml) tracks the Fairphone 6 device configuration and
shared DiamaneOS product configuration on `android17`, inherited from the
DiamaneOS remote. Fairphone projects remain pinned to exact upstream commits.
Native product-graph, selected HAL and enforcing USER policy checks have passed
for the development composition. Generated vendor and kernel inputs remain
required; compilation does not establish image or device compatibility.
The independently built kernel workspace is not overlaid onto Android source.

## Use

The FP6 build environment in `config/build-environment-fp6.json` in the tools
repository binds this overlay, its content digest and the composed project map.
The source-layout verifier requires that explicit composition declaration;
upstream-only environments continue to reject local manifests.
The following is the repo composition step, not an accepted build recipe:

```sh
repo init \
  -u https://github.com/GrapheneOS/platform_manifest.git \
  -b "refs/tags/$GRAPHENEOS_RELEASE"

install -d -m 0755 .repo/local_manifests
install -m 0644 "$OVERLAY_ROOT/diamaneos.xml" \
  .repo/local_manifests/diamaneos.xml

repo sync
repo manifest -r -o resolved-manifest.xml
```

The build procedure verifies the signed release, upstream resolved project map
and exact overlay composition. Changing a project entry or advancing a resolved
owned branch creates a new build-environment identity and requires source sync
and affected qualification.

DiamaneOS is based on GrapheneOS source and is not affiliated with or endorsed
by the GrapheneOS project. Follow the
[GrapheneOS branding guidance](https://grapheneos.org/faq#trademarks) when
integrating product identity.

The original files in this repository are licensed under Apache-2.0. Projects
fetched by `repo` retain their own licences, copyright notices and attribution
requirements.

The FP6 composition includes the source boot-control HAL and GPT/UFS recovery
extension. Owned branches inherit `android17`; the build environment freezes
their exact revisions. Normal/recovery compilation, CFI and matched UFS header
layout checks pass. Runtime slot switching still needs device verification.
No generic boot-control substitution is declared by this overlay.

## Hosting and branches

GitHub's DiamaneOS organization is the authoritative host. Use `android17`
as this repository's default branch; owned Android projects inherit that branch
from the DiamaneOS remote.
There is no parallel `main` manifest. Future Android lines receive their own
branches and immutable release tags identify accepted snapshots. Branch names
are development entry points. Resolve them with `repo manifest -r` and record
the exact project commits in a new build environment before qualification.
A later branch advance cannot silently change an existing build identity.
Release tags retain a manifest with exact project revisions. Kernel workspaces
use their relevant kernel branch independently of this Android overlay.

Repository remotes and the GitHub default branch must be configured separately
from changing this overlay. Preserve signed history and independent Git backups.
