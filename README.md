# DiamaneOS manifest overlay

This repository contains the Android `repo` local-manifest overlay for
DiamaneOS. The base source tree comes directly from an authenticated GrapheneOS
release tag; this repository does not copy or repin the upstream manifest.

The selected release, manifest commit and resolved project-map digest are
recorded in the corresponding immutable build environment in
[`diamaneos-tools`](https://codeberg.org/DiamaneOS/diamaneos-tools/src/branch/main/config/build-environment.json).

[`diamaneos.xml`](diamaneos.xml) pins the Fairphone 6 device configuration and
shared DiamaneOS product configuration. Every revision is an exact commit.
These are initial integration sources: generated hardware inputs and native
product-graph validation remain required before building usable images.
The independently built kernel workspace is not overlaid onto Android source.

## Use

Environment v4 authenticates and syncs upstream directly; it does not install
this overlay. A new environment must bind the overlay revision, content digest
and composed project map before using these projects. The source-layout verifier requires that explicit composition declaration;
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

The current build procedure verifies the signed release and upstream resolved
project map. The first consuming environment must additionally bind the exact
overlay revision and digest and validate the composed project map. Adding the
first project or changing an existing entry creates a new build-environment identity and requires a new source sync
and affected qualification.

DiamaneOS is based on GrapheneOS source and is not affiliated with or endorsed
by the GrapheneOS project. Follow the
[GrapheneOS branding guidance](https://grapheneos.org/faq#trademarks) when
integrating product identity.

The original files in this repository are licensed under Apache-2.0. Projects
fetched by `repo` retain their own licences, copyright notices and attribution
requirements.

The FP6 composition also pins Fairphone's published boot-control HAL and its
GPT/UFS recovery extension at exact revisions. They are source inputs, with
native dependency, hardening and device behavior validation still pending.
No generic boot-control substitution is declared by this overlay.
