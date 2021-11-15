# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pylint: disable=line-too-long
from knack.help_files import helps  # pylint: disable=unused-import


helps['sig show-community'] = """
type: command
short-summary: Get a gallery that has been community (preview).
long-summary: Get a gallery that has been community (private preview feature, please contact community image gallery team by email sigpmdev@microsoft.com to register for preview if you're interested in using this feature).
examples:
  - name: Get a gallery that has been community in the given location.
    text: |
        az sig show-community --public-gallery-name publicGalleryName --location myLocation
"""

helps['sig image-definition show-community'] = """
type: command
short-summary: Get an image in a gallery community (preview).
long-summary: Get an image in a gallery community (private preview feature, please contact community image gallery team by email sigpmdev@microsoft.com to register for preview if you're interested in using this feature).
examples:
  - name: Get an image definition in a gallery community in the given location.
    text: |
        az sig image-definition show-community --public-gallery-name publicGalleryName \\
        --gallery-image-definition myGalleryImageName --location myLocation
"""

helps['sig image-definition list-community'] = """
type: command
short-summary: List VM Image definitions in a gallery community (preview).
long-summary: List VM Image definitions in a gallery community (private preview feature, please contact community image gallery team by email sigpmdev@microsoft.com to register for preview if you're interested in using this feature).
examples:
  - name: List an image definition in a gallery community.
    text: |
        az sig image-definition list-community --public-gallery-name publicGalleryName \\
        --location myLocation
"""

helps['sig image-version show-community'] = """
type: command
short-summary: Get an image version in a gallery community (preview).
long-summary: Get an image version in a gallery community (private preview feature, please contact community image gallery team by email sigpmdev@microsoft.com to register for preview if you're interested in using this feature).
examples:
  - name: Get an image version in a gallery community in the given location.
    text: |
        az sig image-version show-community --public-gallery-name publicGalleryName \\
        --gallery-image-definition MyImage --gallery-image-version 1.0.0 --location myLocation
"""

helps['sig image-version list-community'] = """
type: command
short-summary: List VM Image Versions in a gallery community (preview).
long-summary: List VM Image Versions in a gallery community (private preview feature, please contact community image gallery team by email sigpmdev@microsoft.com to register for preview if you're interested in using this feature).
examples:
  - name: List an image versions in a gallery community.
    text: |
        az sig image-version list-community --public-gallery-name publicGalleryName \\
        --gallery-image-definition MyImage --location myLocation
"""

helps['sig share enable-community'] = """
type: command
short-summary: Allow to share gallery to the community
examples:
  - name: Allow to share gallery to the community
    text: |
        az sig share enable-community --resource-group MyResourceGroup --gallery-name MyGallery
"""

helps['sig image-version create'] = """
type: command
short-summary: create a new image version
long-summary: this operation might take a long time depending on the replicate region number. Use "--no-wait" is advised.
examples:
  - name: Add a new image version from a virtual machine
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --managed-image /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/virtualMachines/MyVM
  - name: Add a new image version from a managed image
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --managed-image /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/images/MyManagedImage
  - name: Add a new image version from another image version
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --managed-image /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/galleries/MyGallery/images/MyImageDefinition/versions/1.0.0
  - name: Add a new image version from a managed disk
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --os-snapshot /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/disks/MyOSDisk
  - name: Add a new image version from a managed disk and add additional data disks
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --os-snapshot /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/disks/MyOSDisk \\
        --data-snapshots /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/disks/MyDataDisk \\
        --data-snapshot-luns 0
  - name: Add a new image version from a snapshot of an OS disk.
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --os-snapshot /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/snapshots/MyOsDiskSnapshot
  - name: Add a new image version from a snapshot of an OS disk and add additional snapshots as data disks
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --os-snapshot /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/snapshots/MyOsDiskSnapshot \\
        --data-snapshots /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/snapshots/MyDiskSnapshot \\
        --data-snapshot-luns 0
  - name: Add a new image version from a VHD of an OS disk.
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --os-vhd-storage-account /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Storage/storageAccounts/mystorageaccount \\
        --os-vhd-uri https://mystorageaccount.blob.core.windows.net/container/path_to_vhd_file
  - name: Add a new image version from a VHD of an OS disk and add additional VHDs as data disks
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --os-vhd-storage-account /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Storage/storageAccounts/mystorageaccount \\
        --os-vhd-uri https://mystorageaccount.blob.core.windows.net/container/path_to_vhd_file \\
        --data-vhds-sa /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Storage/storageAccounts/myotherstorageaccount \\
        --data-vhds-uris https://myotherstorageaccount.blob.core.windows.net/container/path_to_vhd_file \\
        --data-vhds-luns 0
  - name: You can combine snapshots, managed disks, and VHDs to create a new image version. Add a new image version using a VHD as the OS disk and a managed disk and a snapshot as data disks.
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --os-vhd-storage-account /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Storage/storageAccounts/mystorageaccount \\
        --os-vhd-uri https://mystorageaccount.blob.core.windows.net/container/path_to_vhd_file \\
        --data-snapshots /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/disks/MyDataDisk subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/snapshots/MyDiskSnapshot \\
        --data-snapshot-luns 0 1
  - name: Add a new image version and copy it to additional regions. The home location for the source of the image version must be included in the list of target regions. For each additional region, you can specify a different replica count and storage account type. Otherwise, the region will inherit from the global. The default replica count is 1 and the default storage account type is Standard LRS. In this example, eastus2 will have one replica stored on Standard ZRS storage, ukwest will have 3 replicas stored on Standard ZRS storage, southindia will have one replica stored on Standard LRS storage, and brazilsouth will have 2 replicas stored on Standard LRS storage.
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 --replica-count 1 \\
        --storage-account-type Standard_ZRS --managed-image image-name \\
        --target-regions eastus2 ukwest=3 southindia=standard_lrs \\
        brazilsouth=2=standard_lrs
  - name: Add a new image version with encryption using a disk encryption set. Encryption is applied to each disk that is a part of the image version.
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --managed-image /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/virtualMachines/MyVM \\
        --target-regions westus=2=standard eastus \\
        --target-region-encryption WestUSDiskEncryptionSet1,0,WestUSDiskEncryptionSet2 \\
        EastUSDiskEncryptionSet1,0,EastUSDiskEncryptionSet2
  - name: Add a new image version and don't wait on it. Later you can invoke "az sig image-version wait" command when ready to create a vm from the gallery image version
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --managed-image /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/virtualMachines/MyVM \\
        --no-wait
  - name: Add a new image version but remove it from consideration as latest version in its image definition
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --managed-image /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/virtualMachines/MyVM \\
        --exclude-from-latest true
  - name: Add a new image version and set its end-of-life date. The image version can still be used to create a virtual machine after its end-of-life date.
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --managed-image /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/virtualMachines/MyVM \\
        --end-of-life-date 2024-08-02T00:00:00+00:00
  - name: Add a new image version with encryption with disk encryption set and disk cvm encryption set. Encryption is applied to each disk that is a part of the image version.
    text: |
        az sig image-version create --resource-group MyResourceGroup \\
        --gallery-name MyGallery --gallery-image-definition MyImage \\
        --gallery-image-version 1.0.0 \\
        --managed-image /subscriptions/00000000-0000-0000-0000-00000000xxxx/resourceGroups/imageGroups/providers/Microsoft.Compute/virtualMachines/MyVM \\
        --target-regions westus=2=standard eastus \\
        --target-region-encryption WestUSDiskEncryptionSet1,0,WestUSDiskEncryptionSet2 EastUSDiskEncryptionSet1,0,EastUSDiskEncryptionSet2 \\
        --target-region-cvm-encryption EncryptedWithCmk,WestUSDiskCVMEncryptionSet1 EncryptedWithPmk,EastUSDiskCVMEncryptionSet1
"""
