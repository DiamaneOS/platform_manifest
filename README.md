# DiamaneOS manifest

The `repo` manifest for DiamaneOS on the Fairphone 6: GrapheneOS's manifest with
DiamaneOS's changes on top.

- GrapheneOS and AOSP projects stay at the exact revisions of one GrapheneOS
  release.
  - The `grapheneos` remote in `default.xml` names its tag.
  - The signed tag is verified when it is merged here.
- DiamaneOS forks and projects follow their `android17` branches; the build
  tools follow `main`.
- Pinned to exact commits:
  - Fairphone, CodeLinaro and linux-msm projects;
  - DiamaneOS's unmodified mirrors of LineageOS's power HAL projects;
  - AOSP's nos host libraries, which GrapheneOS leaves out.
- Kernels for other devices are left out.
- It also brings in the published FP6 kernel prebuilts
  (`device/fairphone/FP6-kernel`) and the build tools (`tools/diamaneos`).

## Get the source

```sh
repo init -u https://github.com/DiamaneOS/platform_manifest.git -b android17
repo sync -c -j8
```

Build with the tools in `tools/diamaneos`; see their
[BUILDING.md](https://github.com/DiamaneOS/diamaneos-tools/blob/main/docs/BUILDING.md).
Each build records the exact revision of every project (`repo manifest -r`).

## Updating to a new GrapheneOS release

Verify GrapheneOS's signed release tag, merge it into `android17`, rebase the
DiamaneOS forks onto the new release, and build.

## Licence

Apache-2.0 for DiamaneOS's changes; see [LICENSE](LICENSE). The upstream manifest
keeps its own notices (COPPERHEAD-NOTICE).
