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
    branches. The build tools and the hardened_malloc fork follow `main`.
- Pinned to exact commits:
  - Fairphone, CodeLinaro and linux-msm projects
  - DiamaneOS's unmodified mirror of hardware/google/pixel for libperfmgr
  - DiamaneOS's fork of LineageOS's hardware/lineage/interfaces for the power HAL
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

## Source dependencies

- Adopt the Qualcomm supplicant command backend before the FP6 device change
  that selects `lib_driver_cmd_qcwcn`.
- The Power HAL revision is pinned to the implementation that honors
  `vendor.powerhal.adpf_task_profiles`. Keep that behavior when updating the pin.

## Updating to a new GrapheneOS release

Verify GrapheneOS's signed release tag and rebase the DiamaneOS commits onto
it. `default.xml` takes GrapheneOS's new file and keeps the include line.
Then rebase the DiamaneOS forks onto the new release, and build.

## Licence

DiamaneOS's changes are under Apache-2.0 ([LICENSE](LICENSE)). The upstream
manifest keeps its own notices (COPPERHEAD-NOTICE).
