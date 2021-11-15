# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint:disable=too-many-lines


def process_gallery_image_version_namespace(cmd, namespace):
    TargetRegion, EncryptionImages, OSDiskImageEncryption, DataDiskImageEncryption, OSDiskImageSecurityProfile, \
    SecurityProfileType = cmd.get_models('TargetRegion', 'EncryptionImages', 'OSDiskImageEncryption',
                                         'DataDiskImageEncryption', 'OSDiskImageSecurityProfile', 'SecurityProfileType')
    storage_account_types_list = [item.lower() for item in ['Standard_LRS', 'Standard_ZRS', 'Premium_LRS']]
    storage_account_types_str = ", ".join(storage_account_types_list)

    from azure.cli.core.azclierror import ArgumentUsageError, InvalidArgumentValueError

    if namespace.target_regions:
        if hasattr(namespace, 'target_region_encryption') and namespace.target_region_encryption:
            if len(namespace.target_regions) != len(namespace.target_region_encryption):
                raise InvalidArgumentValueError(
                    'usage error: Length of --target-region-encryption should be as same as length of target regions')

        if hasattr(namespace, 'target_region_cvm_encryption') and namespace.target_region_cvm_encryption:
            if len(namespace.target_regions) != len(namespace.target_region_cvm_encryption):
                raise InvalidArgumentValueError(
                    'usage error: Length of --target_region_cvm_encryption should be as same as '
                    'length of target regions')

        regions_info = []
        for i, t in enumerate(namespace.target_regions):
            parts = t.split('=', 2)
            replica_count = None
            storage_account_type = None

            # Region specified, but also replica count or storage account type
            if len(parts) == 2:
                try:
                    replica_count = int(parts[1])
                except ValueError:
                    storage_account_type = parts[1]
                    if parts[1].lower() not in storage_account_types_list:
                        raise ArgumentUsageError(
                            "usage error: {} is an invalid target region argument. "
                            "The second part is neither an integer replica count or a valid storage account type. "
                            "Storage account types must be one of {}.".format(t, storage_account_types_str))

            # Region specified, but also replica count and storage account type
            elif len(parts) == 3:
                try:
                    replica_count = int(parts[1])   # raises ValueError if this is not a replica count, try other order.
                    storage_account_type = parts[2]
                    if storage_account_type not in storage_account_types_list:
                        raise ArgumentUsageError(
                            "usage error: {} is an invalid target region argument. "
                            "The third part is not a valid storage account type. "
                            "Storage account types must be one of {}.".format(t, storage_account_types_str))
                except ValueError:
                    raise ArgumentUsageError(
                        "usage error: {} is an invalid target region argument. "
                        "The second part must be a valid integer replica count.".format(t))

            # Parse target region encryption, example: ['des1,0,des2,1,des3', 'null', 'des4']
            encryption = None
            if hasattr(namespace, 'target_region_encryption') and namespace.target_region_encryption:
                terms = namespace.target_region_encryption[i].split(',')

                # OS disk
                os_disk_image = terms[0]
                if os_disk_image == 'null':
                    os_disk_image = None
                else:
                    des_id = _disk_encryption_set_format(cmd, namespace, os_disk_image)

                    security_profile = None
                    if hasattr(namespace, 'target_region_cvm_encryption') and namespace.target_region_cvm_encryption:
                        cvm_terms = namespace.target_region_cvm_encryption[i].split(',')
                        if not cvm_terms or len(cvm_terms) != 2:
                            raise ArgumentUsageError(
                                "usage error: {} is an invalid target region cvm encryption. "
                                "Both os_cvm_encryption_type and os_cvm_des parameters are required.".format(cvm_terms))

                        storage_profile_types = [profile_type.value for profile_type in SecurityProfileType]
                        storage_profile_types_str = ", ".join(storage_profile_types)
                        if cvm_terms[0] not in storage_profile_types:
                            raise ArgumentUsageError(
                                "usage error: {} is an invalid os_cvm_encryption_type. "
                                "The valid values for os_cvm_encryption_type are {}".format(
                                    cvm_terms, storage_profile_types_str))

                        cvm_des_id = _disk_encryption_set_format(cmd, namespace, cvm_terms[1])
                        security_profile = OSDiskImageSecurityProfile(type=cvm_terms[0],
                                                                      secure_v_mdisk_encryption_set_id=cvm_des_id)

                    os_disk_image = OSDiskImageEncryption(disk_encryption_set_id=des_id,
                                                          security_profile=security_profile)
                # Data disk
                if len(terms) > 1:
                    data_disk_images = terms[1:]
                    data_disk_images_len = len(data_disk_images)
                    if data_disk_images_len % 2 != 0:
                        raise ArgumentUsageError(
                            'usage error: LUN and disk encryption set for data disk should appear in pair in '
                            '--target-region-encryption. Example: osdes,0,datades0,1,datades1')
                    data_disk_image_encryption_list = []
                    for j in range(int(data_disk_images_len / 2)):
                        lun = data_disk_images[j * 2]
                        des_id = data_disk_images[j * 2 + 1]
                        des_id = _disk_encryption_set_format(cmd, namespace, des_id)
                        data_disk_image_encryption_list.append(DataDiskImageEncryption(
                            lun=lun, disk_encryption_set_id=des_id))
                    data_disk_images = data_disk_image_encryption_list
                else:
                    data_disk_images = None
                encryption = EncryptionImages(os_disk_image=os_disk_image, data_disk_images=data_disk_images)

            # At least the region is specified
            if len(parts) >= 1:
                regions_info.append(TargetRegion(name=parts[0], regional_replica_count=replica_count,
                                                 storage_account_type=storage_account_type,
                                                 encryption=encryption))

        namespace.target_regions = regions_info


def _disk_encryption_set_format(cmd, namespace, name):
    """
    Transform name to ID. If it's already a valid ID, do nothing.
    :param name: string
    :return: ID
    """
    from msrestazure.tools import resource_id, is_valid_resource_id
    from azure.cli.core.commands.client_factory import get_subscription_id
    if name is not None and not is_valid_resource_id(name):
        name = resource_id(
            subscription=get_subscription_id(cmd.cli_ctx), resource_group=namespace.resource_group_name,
            namespace='Microsoft.Compute', type='diskEncryptionSets', name=name)
    return name
