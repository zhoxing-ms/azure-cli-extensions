# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.0.6225, generator: {generator})
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from typing import Any, Optional

from azure.core import AsyncPipelineClient
from msrest import Deserializer, Serializer

from ._configuration_async import AzureMigrateConfiguration
from .operations_async import LocationOperations
from .operations_async import AssessmentOptionsOperations
from .operations_async import ProjectsOperations
from .operations_async import MachinesOperations
from .operations_async import GroupsOperations
from .operations_async import AssessmentsOperations
from .operations_async import AssessedMachinesOperations
from .operations_async import Operations
from .. import models


class AzureMigrate(object):
    """Move your workloads to Azure.

    :ivar location: LocationOperations operations
    :vartype location: azure_migrate.aio.operations_async.LocationOperations
    :ivar assessment_options: AssessmentOptionsOperations operations
    :vartype assessment_options: azure_migrate.aio.operations_async.AssessmentOptionsOperations
    :ivar projects: ProjectsOperations operations
    :vartype projects: azure_migrate.aio.operations_async.ProjectsOperations
    :ivar machines: MachinesOperations operations
    :vartype machines: azure_migrate.aio.operations_async.MachinesOperations
    :ivar groups: GroupsOperations operations
    :vartype groups: azure_migrate.aio.operations_async.GroupsOperations
    :ivar assessments: AssessmentsOperations operations
    :vartype assessments: azure_migrate.aio.operations_async.AssessmentsOperations
    :ivar assessed_machines: AssessedMachinesOperations operations
    :vartype assessed_machines: azure_migrate.aio.operations_async.AssessedMachinesOperations
    :ivar operations: Operations operations
    :vartype operations: azure_migrate.aio.operations_async.Operations
    :param credential: Credential needed for the client to connect to Azure.
    :type credential: azure.core.credentials.TokenCredential
    :param subscription_id: Azure Subscription Id in which project was created.
    :type subscription_id: str
    :param accept_language: Standard request header. Used by service to respond to client in appropriate language.
    :type accept_language: str
    :param str base_url: Service URL
    """

    def __init__(
        self,
        credential: "TokenCredential",
        subscription_id: str,
        accept_language: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        if not base_url:
            base_url = 'https://management.azure.com'
        self._config = AzureMigrateConfiguration(credential, subscription_id, accept_language, **kwargs)
        self._client = AsyncPipelineClient(base_url=base_url, config=self._config, **kwargs)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.location = LocationOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.assessment_options = AssessmentOptionsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.projects = ProjectsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.machines = MachinesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.groups = GroupsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.assessments = AssessmentsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.assessed_machines = AssessedMachinesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.operations = Operations(
            self._client, self._config, self._serialize, self._deserialize)

    async def close(self) -> None:
        await self._client.close()

    async def __aenter__(self) -> "AzureMigrate":
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc_details) -> None:
        await self._client.__aexit__(*exc_details)
