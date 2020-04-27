# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=too-many-statements

from azure.cli.core.commands.parameters import (
    tags_type,
    resource_group_name_type,
    get_location_type
)
from azure.cli.core.commands.validators import get_default_location_from_resource_group
from ._validators import validate_workspace_resource_id
from knack.arguments import CLIArgumentType

solution_name = CLIArgumentType(options_list=['--name', '-n'], help='Name of the log-analytics solution.')


def load_arguments(self, _):

    with self.argument_context('monitor log-analytics solution create') as c:
        c.argument('solution_name', solution_name)
        c.argument('location', arg_type=get_location_type(self.cli_ctx),
                   validator=get_default_location_from_resource_group)
        c.argument('tags', tags_type)
        c.argument('plan_name', help='Name of the plan for solution. For Microsoft published solution it should be in the format of solutionType(workspaceName). '
                                     'SolutionType part is case sensitive. For third party solution, it can be anything.')
        c.argument('plan_publisher', help='Publisher name of the plan for solution. For gallery solution, it is Microsoft.')
        c.argument('plan_product', help='Product name of the plan for solution. '
                                        'For Microsoft published gallery solution it should be in the format of OMSGallery/<solutionType>. This is case sensitive.')
        c.argument('workspace_resource_id', options_list=['--workspace-resource-id', '-w'],
                   validator=validate_workspace_resource_id,
                   help='The resource ID of the log analytics workspace with which the solution will be linked.')
        c.argument('workspace_name', options_list=['--workspace-name'],
                   help='The name of the log analytics workspace with which the solution will be linked.')

    with self.argument_context('monitor log-analytics solution update') as c:
        c.argument('solution_name', solution_name)
        c.argument('tags', tags_type)

    with self.argument_context('monitor log-analytics solution delete') as c:
        c.argument('solution_name', solution_name)

    with self.argument_context('monitor log-analytics solution show') as c:
        c.argument('solution_name', solution_name)
