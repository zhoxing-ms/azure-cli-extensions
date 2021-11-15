# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
# pylint: disable=too-many-statements
# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=unused-argument

from knack.log import get_logger
from azure.cli.core.azclierror import ArgumentUsageError, RequiredArgumentMissingError
from azure.cli.core.profiles import ResourceType
from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.cli.core.util import sdk_no_wait
from ._client_factory import _compute_client_factory

logger = get_logger(__name__)


def sig_community_image_definition_list(client, location, public_gallery_name, marker=None, show_next_marker=None):
    generator = client.list(location=location, public_gallery_name=public_gallery_name)
    return get_page_result(generator, marker, show_next_marker)


def sig_community_image_version_list(client, location, public_gallery_name, gallery_image_name, marker=None,
                                     show_next_marker=None):
    generator = client.list(location=location, public_gallery_name=public_gallery_name,
                            gallery_image_name=gallery_image_name)
    return get_page_result(generator, marker, show_next_marker)


def get_page_result(generator, marker, show_next_marker=None):
    pages = generator.by_page(continuation_token=marker)  # ContainerPropertiesPaged
    result = list_generator(pages=pages)

    if show_next_marker:
        next_marker = {"nextMarker": pages.continuation_token}
        result.append(next_marker)
    else:
        if pages.continuation_token:
            logger.warning('Next Marker:')
            logger.warning(pages.continuation_token)

    return result


# The REST service takes 50 items as a page by default
def list_generator(pages, num_results=50):
    result = []

    # get first page items
    page = list(next(pages))
    result += page

    while True:
        if not pages.continuation_token:
            break

        # handle num results
        if num_results is not None:
            if num_results == len(result):
                break

        page = list(next(pages))
        result += page

    return result


def create_image_gallery(cmd, resource_group_name, gallery_name, description=None,
                         location=None, no_wait=False, tags=None, permissions=None, soft_delete=None,
                         publisher_uri=None, publisher_contact=None, eula=None, public_name_prefix=None):
    Gallery = cmd.get_models('Gallery')
    location = location or _get_resource_group_location(cmd.cli_ctx, resource_group_name)
    gallery = Gallery(description=description, location=location, tags=(tags or {}))
    if soft_delete is not None:
        gallery.soft_delete_policy = {'is_soft_delete_enabled': soft_delete}
    client = _compute_client_factory(cmd.cli_ctx)
    if permissions:
        SharingProfile = cmd.get_models('SharingProfile')
        gallery.sharing_profile = SharingProfile(permissions=permissions)
        if permissions == 'Community':
            if publisher_uri is None or publisher_contact is None or eula is None or public_name_prefix is None:
                raise RequiredArgumentMissingError('If you want to share to the community, '
                                                   'you need to fill in all the following parameters:'
                                                   ' --publisher-uri, --publisher-email, --eula, --public-name-prefix.')

            CommunityGalleryInfo = cmd.get_models('CommunityGalleryInfo')
            gallery.sharing_profile.community_gallery_info = CommunityGalleryInfo(publisher_uri=publisher_uri,
                                                                                  publisher_contact=publisher_contact,
                                                                                  eula=eula,
                                                                                  public_name_prefix=public_name_prefix)
    return sdk_no_wait(no_wait, client.galleries.begin_create_or_update, resource_group_name, gallery_name, gallery)


def sig_share_update(cmd, client, resource_group_name, gallery_name, subscription_ids=None, tenant_ids=None,
                     op_type=None):
    SharingProfileGroup, SharingUpdate, SharingProfileGroupTypes = cmd.get_models(
        'SharingProfileGroup', 'SharingUpdate', 'SharingProfileGroupTypes')
    if op_type != 'EnableCommunity':
        if subscription_ids is None and tenant_ids is None:
            raise RequiredArgumentMissingError('At least one of subscription ids or tenant ids must be provided')
    groups = []
    if subscription_ids:
        groups.append(SharingProfileGroup(type=SharingProfileGroupTypes.SUBSCRIPTIONS, ids=subscription_ids))
    if tenant_ids:
        groups.append(SharingProfileGroup(type=SharingProfileGroupTypes.AAD_TENANTS, ids=tenant_ids))
    sharing_update = SharingUpdate(operation_type=op_type, groups=groups)
    return client.begin_update(resource_group_name=resource_group_name,
                               gallery_name=gallery_name,
                               sharing_update=sharing_update)


def create_image_version(cmd, resource_group_name, gallery_name, gallery_image_name, gallery_image_version,
                         location=None, target_regions=None, storage_account_type=None,
                         end_of_life_date=None, exclude_from_latest=None, replica_count=None, tags=None,
                         os_snapshot=None, data_snapshots=None, managed_image=None, data_snapshot_luns=None,
                         target_region_encryption=None, os_vhd_uri=None, os_vhd_storage_account=None,
                         data_vhds_uris=None, data_vhds_luns=None, data_vhds_storage_accounts=None,
                         replication_mode=None, target_region_cvm_encryption=None):

    from msrestazure.tools import resource_id, is_valid_resource_id
    from azure.cli.core.commands.client_factory import get_subscription_id

    ImageVersionPublishingProfile, GalleryArtifactSource, ManagedArtifact, ImageVersion, TargetRegion = cmd.get_models(
        'GalleryImageVersionPublishingProfile', 'GalleryArtifactSource', 'ManagedArtifact', 'GalleryImageVersion',
        'TargetRegion')
    aux_subscriptions = _get_image_version_aux_subscription(managed_image, os_snapshot, data_snapshots)

    from ._client_factory import _compute_client_factory
    client = _compute_client_factory(cmd.cli_ctx, aux_subscriptions=aux_subscriptions)

    location = location or _get_resource_group_location(cmd.cli_ctx, resource_group_name)
    end_of_life_date = fix_gallery_image_date_info(end_of_life_date)
    if managed_image and not is_valid_resource_id(managed_image):
        managed_image = resource_id(subscription=get_subscription_id(cmd.cli_ctx), resource_group=resource_group_name,
                                    namespace='Microsoft.Compute', type='images', name=managed_image)
    if os_snapshot and not is_valid_resource_id(os_snapshot):
        os_snapshot = resource_id(subscription=get_subscription_id(cmd.cli_ctx), resource_group=resource_group_name,
                                  namespace='Microsoft.Compute', type='snapshots', name=os_snapshot)
    if data_snapshots:
        for i, s in enumerate(data_snapshots):
            if not is_valid_resource_id(data_snapshots[i]):
                data_snapshots[i] = resource_id(
                    subscription=get_subscription_id(cmd.cli_ctx), resource_group=resource_group_name,
                    namespace='Microsoft.Compute', type='snapshots', name=s)
    source = GalleryArtifactSource(managed_image=ManagedArtifact(id=managed_image))
    profile = ImageVersionPublishingProfile(exclude_from_latest=exclude_from_latest,
                                            end_of_life_date=end_of_life_date,
                                            target_regions=target_regions or [TargetRegion(name=location)],
                                            source=source, replica_count=replica_count,
                                            storage_account_type=storage_account_type)
    if replication_mode is not None:
        profile.replication_mode = replication_mode
    if cmd.supported_api_version(min_api='2019-07-01'):
        if managed_image is None and os_snapshot is None and os_vhd_uri is None:
            raise RequiredArgumentMissingError('usage error: Please provide --managed-image or --os-snapshot or --vhd')
        GalleryImageVersionStorageProfile = cmd.get_models('GalleryImageVersionStorageProfile')
        GalleryArtifactVersionSource = cmd.get_models('GalleryArtifactVersionSource')
        GalleryOSDiskImage = cmd.get_models('GalleryOSDiskImage')
        GalleryDataDiskImage = cmd.get_models('GalleryDataDiskImage')
        source = os_disk_image = data_disk_images = None
        if managed_image is not None:
            source = GalleryArtifactVersionSource(id=managed_image)
        if os_snapshot is not None:
            os_disk_image = GalleryOSDiskImage(source=GalleryArtifactVersionSource(id=os_snapshot))
        if data_snapshot_luns and not data_snapshots:
            raise ArgumentUsageError('usage error: --data-snapshot-luns must be used together with --data-snapshots')
        if data_snapshots:
            if data_snapshot_luns and len(data_snapshots) != len(data_snapshot_luns):
                raise ArgumentUsageError('usage error: Length of --data-snapshots and --data-snapshot-luns should be equal.')
            if not data_snapshot_luns:
                data_snapshot_luns = list(range(len(data_snapshots)))
            data_disk_images = []
            for i, s in enumerate(data_snapshots):
                data_disk_images.append(GalleryDataDiskImage(source=GalleryArtifactVersionSource(id=s),
                                                             lun=data_snapshot_luns[i]))
        # from vhd, only support os image now
        if cmd.supported_api_version(min_api='2020-09-30'):
            # OS disk
            if os_vhd_uri and os_vhd_storage_account is None or os_vhd_uri is None and os_vhd_storage_account:
                raise ArgumentUsageError('--os-vhd-uri and --os-vhd-storage-account should be used together.')
            if os_vhd_uri and os_vhd_storage_account:
                if not is_valid_resource_id(os_vhd_storage_account):
                    os_vhd_storage_account = resource_id(
                        subscription=get_subscription_id(cmd.cli_ctx), resource_group=resource_group_name,
                        namespace='Microsoft.Storage', type='storageAccounts', name=os_vhd_storage_account)
                os_disk_image = GalleryOSDiskImage(source=GalleryArtifactVersionSource(
                    id=os_vhd_storage_account, uri=os_vhd_uri))

            # Data disks
            if data_vhds_uris and data_vhds_storage_accounts is None or \
                    data_vhds_uris is None and data_vhds_storage_accounts:
                raise ArgumentUsageError('--data-vhds-uris and --data-vhds-storage-accounts should be used together.')
            if data_vhds_luns and data_vhds_uris is None:
                raise ArgumentUsageError('--data-vhds-luns must be used together with --data-vhds-uris')
            if data_vhds_uris:
                # Generate LUNs
                if data_vhds_luns is None:
                    # 0, 1, 2, ...
                    data_vhds_luns = list(range(len(data_vhds_uris)))
                # Check length
                len_data_vhds_uris = len(data_vhds_uris)
                len_data_vhds_luns = len(data_vhds_luns)
                len_data_vhds_storage_accounts = len(data_vhds_storage_accounts)
                if len_data_vhds_uris != len_data_vhds_luns or len_data_vhds_uris != len_data_vhds_storage_accounts:
                    raise ArgumentUsageError(
                        'Length of --data-vhds-uris, --data-vhds-luns, --data-vhds-storage-accounts must be same.')
                # Generate full storage account ID
                for i, storage_account in enumerate(data_vhds_storage_accounts):
                    if not is_valid_resource_id(storage_account):
                        data_vhds_storage_accounts[i] = resource_id(
                            subscription=get_subscription_id(cmd.cli_ctx), resource_group=resource_group_name,
                            namespace='Microsoft.Storage', type='storageAccounts', name=storage_account)
                if data_disk_images is None:
                    data_disk_images = []
                for uri, lun, account in zip(data_vhds_uris, data_vhds_luns, data_vhds_storage_accounts):
                    data_disk_images.append(GalleryDataDiskImage(
                        source=GalleryArtifactVersionSource(id=account, uri=uri), lun=lun))

        storage_profile = GalleryImageVersionStorageProfile(source=source, os_disk_image=os_disk_image,
                                                            data_disk_images=data_disk_images)
        image_version = ImageVersion(publishing_profile=profile, location=location, tags=(tags or {}),
                                     storage_profile=storage_profile)
    else:
        if managed_image is None:
            raise RequiredArgumentMissingError('usage error: Please provide --managed-image')
        image_version = ImageVersion(publishing_profile=profile, location=location, tags=(tags or {}))

    return client.gallery_image_versions.begin_create_or_update(
        resource_group_name=resource_group_name,
        gallery_name=gallery_name,
        gallery_image_name=gallery_image_name,
        gallery_image_version_name=gallery_image_version,
        gallery_image_version=image_version
    )


def _get_resource_group_location(cli_ctx, resource_group_name):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azure.cli.core.profiles import ResourceType

    client = get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES)
    # pylint: disable=no-member
    return client.resource_groups.get(resource_group_name).location


def _parse_aux_subscriptions(resource_id):
    from msrestazure.tools import is_valid_resource_id, parse_resource_id
    if is_valid_resource_id(resource_id):
        res = parse_resource_id(resource_id)
        return [res['subscription']]
    return None


def _add_aux_subscription(aux_subscriptions, resource_id):
    if resource_id:
        aux_subs = _parse_aux_subscriptions(resource_id)
        if aux_subs and aux_subs[0] not in aux_subscriptions:
            aux_subscriptions.extend(aux_subs)


def _get_image_version_aux_subscription(managed_image, os_snapshot, data_snapshots):
    aux_subscriptions = []
    _add_aux_subscription(aux_subscriptions, managed_image)
    _add_aux_subscription(aux_subscriptions, os_snapshot)
    if data_snapshots:
        for data_snapshot in data_snapshots:
            _add_aux_subscription(aux_subscriptions, data_snapshot)
    return aux_subscriptions if aux_subscriptions else None


def fix_gallery_image_date_info(date_info):
    # here we add needed time, if only date is provided, so the setting can be accepted by servie end
    if date_info and 't' not in date_info.lower():
        date_info += 'T12:59:59Z'
    return date_info

