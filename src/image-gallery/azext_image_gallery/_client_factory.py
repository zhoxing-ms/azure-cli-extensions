# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def _compute_client_factory(cli_ctx, **kwargs):
    from azure.cli.core.profiles import ResourceType
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_COMPUTE,
                                   subscription_id=kwargs.get('subscription_id'),
                                   aux_subscriptions=kwargs.get('aux_subscriptions'))


def cf_galleries(cli_ctx, _):
    return _compute_client_factory(cli_ctx).galleries


def cf_gallery_images(cli_ctx, _):
    return _compute_client_factory(cli_ctx).gallery_images


def cf_gallery_image_version(cli_ctx, _):
    return _compute_client_factory(cli_ctx).gallery_image_versions


def cf_community_gallery(cli_ctx, *_):
    return _compute_client_factory(cli_ctx).community_galleries


def cf_community_gallery_image(cli_ctx, *_):
    return _compute_client_factory(cli_ctx).community_gallery_images


def cf_community_gallery_image_version(cli_ctx, *_):
    return _compute_client_factory(cli_ctx).community_gallery_image_versions


def cf_community_gallery_sharing_profile(cli_ctx, *_):
    return _compute_client_factory(cli_ctx).gallery_sharing_profile
