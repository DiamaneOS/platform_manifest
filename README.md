# DiamaneOS manifest

The `repo` manifest for DiamaneOS: GrapheneOS's manifest with DiamaneOS's
projects on top.

- `default.xml` is GrapheneOS's manifest of one release, unchanged apart from
  one line at its end that includes `diamaneos.xml`.
  - GrapheneOS and AOSP projects stay at the exact revisions of that release.
  - GrapheneOS's signed tag is verified before the manifest takes it.
- `diamaneos.xml` holds what DiamaneOS changes:
  - `remove-project` lines for the GrapheneOS and AOSP projects DiamaneOS
    replaces with its forks, and for the kernels of other devices
  - the DiamaneOS forks and projects, which follow their `android17`
    branches. The build tools follow `main`.
- Pinned to exact commits:
  - Fairphone, CodeLinaro and linux-msm projects
  - DiamaneOS's unmodified mirrors of LineageOS's power HAL projects
  - AOSP's nos host libraries, which GrapheneOS leaves out
- It also brings in the published kernel prebuilts
  (`device/fairphone/FP6-kernel`) and the build tools (`tools/diamaneos`).

## Get the source

```sh
repo init -u https://github.com/DiamaneOS/platform_manifest.git -b android17
repo sync -c -j8
```

Build with the tools in `tools/diamaneos`, as their
[BUILDING.md](https://github.com/DiamaneOS/diamaneos-tools/blob/main/docs/BUILDING.md)
describes.
Each build records the exact revision of every project (`repo manifest -r`).

## Updating to a new GrapheneOS release

Verify GrapheneOS's signed release tag and rebase the DiamaneOS commits onto
it. `default.xml` takes GrapheneOS's new file and keeps the include line.
Then rebase the DiamaneOS forks onto the new release, and build.

## Licence

DiamaneOS's changes are under Apache-2.0 ([LICENSE](LICENSE)). The upstream
manifest keeps its own notices (COPPERHEAD-NOTICE).
