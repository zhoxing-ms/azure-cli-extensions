# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements

from knack.arguments import CLIArgumentType
from azure.cli.core.commands.parameters import get_location_type, tags_type, get_enum_type, get_three_state_flag


def load_arguments(self, _):

    public_gallery_name_type = CLIArgumentType(help='The public name of community gallery.', id_part='child_name_1')

    gallery_image_name_type = CLIArgumentType(
        options_list=['--gallery-image-definition', '-i'],
        help='The name of the community gallery image definition from which the image versions are to be listed.',
        id_part='child_name_2'
    )

    gallery_image_name_version_type = CLIArgumentType(
        options_list=['--gallery-image-version', '-e'],
        help='The name of the gallery image version to be created. Needs to follow semantic version name pattern: '
             'The allowed characters are digit and period. Digits must be within the range of a 32-bit integer. '
             'Format: <MajorVersion>.<MinorVersion>.<Patch>', id_part='child_name_3'
    )

    marker_type = CLIArgumentType(
        help='A string value that identifies the portion of the list of containers to be '
             'returned with the next listing operation. The operation returns the NextMarker value within '
             'the response body if the listing operation did not return all containers remaining to be listed '
             'with the current page. If specified, this generator will begin returning results from the point '
             'where the previous generator stopped.')

    with self.argument_context('sig show-community') as c:
        c.argument('location', arg_type=get_location_type(self.cli_ctx), id_part='name')
        c.argument('public_gallery_name', public_gallery_name_type)

    with self.argument_context('sig image-definition show-community') as c:
        c.argument('location', arg_type=get_location_type(self.cli_ctx), id_part='name')
        c.argument('public_gallery_name', public_gallery_name_type)
        c.argument('gallery_image_name', gallery_image_name_type)

    with self.argument_context('sig image-definition list-community') as c:
        c.argument('location', arg_type=get_location_type(self.cli_ctx), id_part='name')
        c.argument('public_gallery_name', public_gallery_name_type)
        c.argument('marker', arg_type=marker_type)
        c.argument('show_next_marker', action='store_true', help='Show nextMarker in result when specified.')

    with self.argument_context('sig image-version show-community') as c:
        c.argument('location', arg_type=get_location_type(self.cli_ctx), id_part='name')
        c.argument('public_gallery_name', public_gallery_name_type)
        c.argument('gallery_image_name', gallery_image_name_type)
        c.argument('gallery_image_version_name', gallery_image_name_version_type)

    with self.argument_context('sig image-version list-community') as c:
        c.argument('location', arg_type=get_location_type(self.cli_ctx), id_part='name')
        c.argument('public_gallery_name', public_gallery_name_type)
        c.argument('gallery_image_name', gallery_image_name_type)
        c.argument('marker', arg_type=marker_type)
        c.argument('show_next_marker', action='store_true', help='Show nextMarker in result when specified.')

    with self.argument_context('sig') as c:
        c.argument('gallery_name', options_list=['--gallery-name', '-r'], help='gallery name')
        c.argument('gallery_image_name', options_list=['--gallery-image-definition', '-i'], help='gallery image definition')
        c.argument('gallery_image_version', options_list=['--gallery-image-version', '-e'], help='gallery image version')
        c.argument('tags', tags_type)

    with self.argument_context('sig create') as c:
        c.argument('description', help='the description of the gallery')
        c.argument('permissions', arg_type=get_enum_type(['Private', 'Groups', 'Community']),
                   arg_group='Sharing Profile', is_experimental=True,
                   help='This property allows you to specify the permission of sharing gallery.')
        c.argument('soft_delete', arg_type=get_three_state_flag(), is_preview=True,
                   help='Enable soft-deletion for resources in this gallery, '
                        'allowing them to be recovered within retention time.')
        c.argument('publisher_uri', help='Community gallery publisher uri.')
        c.argument('publisher_contact', options_list=['--publisher-email'], help='Community gallery publisher contact email.')
        c.argument('eula', help='Community gallery publisher eula.')
        c.argument('public_name_prefix', help='Community gallery public name prefix.')

    with self.argument_context('sig share enable-community') as c:
        c.argument('gallery_name', type=str, help='The name of the Shared Image Gallery.', id_part='name')
        c.argument('subscription_ids', nargs='+', help='A list of subscription ids to share the gallery.')
        c.argument('tenant_ids', nargs='+', help='A list of tenant ids to share the gallery.')
        c.argument('op_type', default='EnableCommunity', deprecate_info=c.deprecate(hide=True),
                   help='distinguish add operation and remove operation')

    ReplicationMode, SecurityProfileType = self.get_models('ReplicationMode', 'SecurityProfileType')
    from ._validators import process_gallery_image_version_namespace
    with self.argument_context('sig image-version create') as c:
        c.argument('gallery_image_version', options_list=['--gallery-image-version', '-e'],
                   help='Gallery image version in semantic version pattern. The allowed characters are digit and period. Digits must be within the range of a 32-bit integer, e.g. `<MajorVersion>.<MinorVersion>.<Patch>`')
        c.argument('description', help='the description of the gallery image version')
        c.argument('managed_image', help='image name(if in the same resource group) or resource id')
        c.argument('os_snapshot', help='Name or ID of OS disk snapshot')
        c.argument('data_snapshots', nargs='+', help='Names or IDs (space-delimited) of data disk snapshots')
        c.argument('data_snapshot_luns', nargs='+', help='Logical unit numbers (space-delimited) of data disk snapshots')
        c.argument('exclude_from_latest', arg_type=get_three_state_flag(), help='The flag means that if it is set to true, people deploying VMs with version omitted will not use this version.')
        c.argument('version', help='image version')
        c.argument('end_of_life_date', help="the end of life date, e.g. '2020-12-31'")
        c.argument('storage_account_type', help="The default storage account type to be used per region. To set regional storage account types, use --target-regions",
                   arg_type=get_enum_type(["Standard_LRS", "Standard_ZRS", "Premium_LRS"]), min_api='2019-03-01')
        c.argument('target_region_encryption', nargs='+',
                   help='Space-separated list of customer managed keys for encrypting the OS and data disks in the gallery artifact for each region. Format for each region: `<os_des>,<lun1>,<lun1_des>,<lun2>,<lun2_des>`. Use "null" as a placeholder.')
        c.argument('os_vhd_uri', help='Source VHD URI of OS disk')
        c.argument('os_vhd_storage_account', help='Name or ID of storage account of source VHD URI of OS disk')
        c.argument('data_vhds_uris', nargs='+', help='Source VHD URIs (space-delimited) of data disks')
        c.argument('data_vhds_luns', nargs='+', help='Logical unit numbers (space-delimited) of source VHD URIs of data disks')
        c.argument('data_vhds_storage_accounts', options_list=['--data-vhds-storage-accounts', '--data-vhds-sa'], nargs='+', help='Names or IDs (space-delimited) of storage accounts of source VHD URIs of data disks')
        c.argument('replication_mode', min_api='2021-07-01', arg_type=get_enum_type(ReplicationMode), help='Optional parameter which specifies the mode to be used for replication. This property is not updatable.')
        c.argument('target_regions', nargs='*', validator=process_gallery_image_version_namespace,
                   help='Space-separated list of regions and their replica counts. Use `<region>[=<replica count>][=<storage account type>]` to optionally set the replica count and/or storage account type for each region. '
                        'If a replica count is not specified, the default replica count will be used. If a storage account type is not specified, the default storage account type will be used')
        c.argument('replica_count', help='The default number of replicas to be created per region. To set regional replication counts, use --target-regions', type=int)
        c.argument('target_region_cvm_encryption', nargs='+',
                   help='Space-separated list of customer managed key for Confidential VM encrypting the OS disk in the gallery artifact for each region. '
                        'Format for each region: `<os_cvm_encryption_type>,<os_cvm_des>`. The valid values for os_cvm_encryption_type are {} '.format(', '.join([profile_type.value for profile_type in SecurityProfileType])))
