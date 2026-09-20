# DiamaneOS manifest overlay

This repository contains the Android `repo` local-manifest overlay for
DiamaneOS. The base source tree comes directly from an authenticated GrapheneOS
release tag; this repository does not copy or repin the upstream manifest.

The selected release, manifest commit and resolved project-map digest are
recorded in the corresponding immutable build environment in
[`diamaneos-tools`](https://codeberg.org/DiamaneOS/diamaneos-tools/src/branch/main/config/build-environment.json).

[`diamaneos.xml`](diamaneos.xml) currently declares the DiamaneOS remote but no
projects. Add entries only when a DiamaneOS repository or reviewed upstream
fork is actually integrated. Every project revision must be an exact commit.

## Use

Initialize the source tree from the release declared by the selected build
environment, then install the overlay before syncing:

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

The build procedure verifies the signed release, the resolved project map and
the exact overlay revision. Adding the first project or changing an existing
entry creates a new build-environment identity and requires a new source sync
and affected qualification.

DiamaneOS is based on GrapheneOS source and is not affiliated with or endorsed
by the GrapheneOS project. Follow the
[GrapheneOS branding guidance](https://grapheneos.org/faq#trademarks) when
integrating product identity.

The original files in this repository are licensed under Apache-2.0. Projects
fetched by `repo` retain their own licences, copyright notices and attribution
requirements.
