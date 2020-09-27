# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import TYPE_CHECKING
import warnings

from azure.core.exceptions import HttpResponseError, ResourceExistsError, ResourceNotFoundError, map_error
from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import HttpRequest, HttpResponse
from azure.mgmt.core.exceptions import ARMErrorFormat

from .. import models

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, Callable, Dict, Generic, Iterable, Optional, TypeVar, Union

    T = TypeVar('T')
    ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

class MaintenanceConfigurationOperations(object):
    """MaintenanceConfigurationOperations operations.

    You should not instantiate this class directly. Instead, you should create a Client instance that
    instantiates it for you and attaches it as an attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~maintenance_client.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer):
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    def get(
        self,
        resource_group_name,  # type: str
        resource_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.MaintenanceConfiguration"
        """Get Configuration record.

        Get Configuration record.

        :param resource_group_name: Resource Group Name.
        :type resource_group_name: str
        :param resource_name: Resource Identifier.
        :type resource_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MaintenanceConfiguration, or the result of cls(response)
        :rtype: ~maintenance_client.models.MaintenanceConfiguration
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.MaintenanceConfiguration"]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2020-07-01-preview"

        # Construct URL
        url = self.get.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'resourceName': self._serialize.url("resource_name", resource_name, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = 'application/json'

        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.MaintenanceError, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('MaintenanceConfiguration', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    get.metadata = {'url': '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Maintenance/maintenanceConfigurations/{resourceName}'}  # type: ignore

    def create_or_update(
        self,
        resource_group_name,  # type: str
        resource_name,  # type: str
        location=None,  # type: Optional[str]
        tags=None,  # type: Optional[Dict[str, str]]
        namespace=None,  # type: Optional[str]
        extension_properties=None,  # type: Optional[Dict[str, str]]
        maintenance_scope=None,  # type: Optional[Union[str, "models.MaintenanceScope"]]
        visibility=None,  # type: Optional[Union[str, "models.Visibility"]]
        start_date_time=None,  # type: Optional[str]
        expiration_date_time=None,  # type: Optional[str]
        duration=None,  # type: Optional[str]
        time_zone=None,  # type: Optional[str]
        recur_every=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.MaintenanceConfiguration"
        """Create or Update configuration record.

        Create or Update configuration record.

        :param resource_group_name: Resource Group Name.
        :type resource_group_name: str
        :param resource_name: Resource Identifier.
        :type resource_name: str
        :param location: Gets or sets location of the resource.
        :type location: str
        :param tags: Gets or sets tags of the resource.
        :type tags: dict[str, str]
        :param namespace: Gets or sets namespace of the resource.
        :type namespace: str
        :param extension_properties: Gets or sets extensionProperties of the maintenanceConfiguration.
        :type extension_properties: dict[str, str]
        :param maintenance_scope: Gets or sets maintenanceScope of the configuration.
        :type maintenance_scope: str or ~maintenance_client.models.MaintenanceScope
        :param visibility: Gets or sets the visibility of the configuration.
        :type visibility: str or ~maintenance_client.models.Visibility
        :param start_date_time: Effective start date of the maintenance window in YYYY-MM-DD hh:mm
         format. The start date can be set to either the current date or future date. The window will be
         created in the time zone provided and adjusted to daylight savings according to that time zone.
        :type start_date_time: str
        :param expiration_date_time: Effective expiration date of the maintenance window in YYYY-MM-DD
         hh:mm format. The window will be created in the time zone provided and adjusted to daylight
         savings according to that time zone. Expiration date must be set to a future date. If not
         provided, it will be set to the maximum datetime 9999-12-31 23:59:59.
        :type expiration_date_time: str
        :param duration: Duration of the maintenance window in HH:mm format. If not provided, default
         value will be used based on maintenance scope provided. Example: 05:00.
        :type duration: str
        :param time_zone: Name of the timezone. List of timezones can be obtained by executing
         [System.TimeZoneInfo]::GetSystemTimeZones() in PowerShell. Example: Pacific Standard Time, UTC,
         W. Europe Standard Time, Korea Standard Time, Cen. Australia Standard Time.
        :type time_zone: str
        :param recur_every: Rate at which a Maintenance window is expected to recur. The rate can be
         expressed as daily, weekly, or monthly schedules. Daily schedule are formatted as recurEvery:
         [Frequency as integer]['Day(s)']. If no frequency is provided, the default frequency is 1.
         Daily schedule examples are recurEvery: Day, recurEvery: 3Days.  Weekly schedule are formatted
         as recurEvery: [Frequency as integer]['Week(s)'] [Optional comma separated list of weekdays
         Monday-Sunday]. Weekly schedule examples are recurEvery: 3Weeks, recurEvery: Week
         Saturday,Sunday. Monthly schedules are formatted as [Frequency as integer]['Month(s)'] [Comma
         separated list of month days] or [Frequency as integer]['Month(s)'] [Week of Month (First,
         Second, Third, Fourth, Last)] [Weekday Monday-Sunday]. Monthly schedule examples are
         recurEvery: Month, recurEvery: 2Months, recurEvery: Month day23,day24, recurEvery: Month Last
         Sunday, recurEvery: Month Fourth Monday.
        :type recur_every: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MaintenanceConfiguration, or the result of cls(response)
        :rtype: ~maintenance_client.models.MaintenanceConfiguration
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.MaintenanceConfiguration"]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))

        _configuration = models.MaintenanceConfiguration(location=location, tags=tags, namespace=namespace, extension_properties=extension_properties, maintenance_scope=maintenance_scope, visibility=visibility, start_date_time=start_date_time, expiration_date_time=expiration_date_time, duration=duration, time_zone=time_zone, recur_every=recur_every)
        api_version = "2020-07-01-preview"
        content_type = kwargs.pop("content_type", "application/json")

        # Construct URL
        url = self.create_or_update.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'resourceName': self._serialize.url("resource_name", resource_name, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = 'application/json'

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(_configuration, 'MaintenanceConfiguration')
        body_content_kwargs['content'] = body_content
        request = self._client.put(url, query_parameters, header_parameters, **body_content_kwargs)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.MaintenanceError, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('MaintenanceConfiguration', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    create_or_update.metadata = {'url': '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Maintenance/maintenanceConfigurations/{resourceName}'}  # type: ignore

    def delete(
        self,
        resource_group_name,  # type: str
        resource_name,  # type: str
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.MaintenanceConfiguration"
        """Delete Configuration record.

        Delete Configuration record.

        :param resource_group_name: Resource Group Name.
        :type resource_group_name: str
        :param resource_name: Resource Identifier.
        :type resource_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MaintenanceConfiguration, or the result of cls(response)
        :rtype: ~maintenance_client.models.MaintenanceConfiguration
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.MaintenanceConfiguration"]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2020-07-01-preview"

        # Construct URL
        url = self.delete.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'resourceName': self._serialize.url("resource_name", resource_name, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Accept'] = 'application/json'

        request = self._client.delete(url, query_parameters, header_parameters)
        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.MaintenanceError, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('MaintenanceConfiguration', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    delete.metadata = {'url': '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Maintenance/maintenanceConfigurations/{resourceName}'}  # type: ignore

    def update(
        self,
        resource_group_name,  # type: str
        resource_name,  # type: str
        location=None,  # type: Optional[str]
        tags=None,  # type: Optional[Dict[str, str]]
        namespace=None,  # type: Optional[str]
        extension_properties=None,  # type: Optional[Dict[str, str]]
        maintenance_scope=None,  # type: Optional[Union[str, "models.MaintenanceScope"]]
        visibility=None,  # type: Optional[Union[str, "models.Visibility"]]
        start_date_time=None,  # type: Optional[str]
        expiration_date_time=None,  # type: Optional[str]
        duration=None,  # type: Optional[str]
        time_zone=None,  # type: Optional[str]
        recur_every=None,  # type: Optional[str]
        **kwargs  # type: Any
    ):
        # type: (...) -> "models.MaintenanceConfiguration"
        """Patch configuration record.

        Patch configuration record.

        :param resource_group_name: Resource Group Name.
        :type resource_group_name: str
        :param resource_name: Resource Identifier.
        :type resource_name: str
        :param location: Gets or sets location of the resource.
        :type location: str
        :param tags: Gets or sets tags of the resource.
        :type tags: dict[str, str]
        :param namespace: Gets or sets namespace of the resource.
        :type namespace: str
        :param extension_properties: Gets or sets extensionProperties of the maintenanceConfiguration.
        :type extension_properties: dict[str, str]
        :param maintenance_scope: Gets or sets maintenanceScope of the configuration.
        :type maintenance_scope: str or ~maintenance_client.models.MaintenanceScope
        :param visibility: Gets or sets the visibility of the configuration.
        :type visibility: str or ~maintenance_client.models.Visibility
        :param start_date_time: Effective start date of the maintenance window in YYYY-MM-DD hh:mm
         format. The start date can be set to either the current date or future date. The window will be
         created in the time zone provided and adjusted to daylight savings according to that time zone.
        :type start_date_time: str
        :param expiration_date_time: Effective expiration date of the maintenance window in YYYY-MM-DD
         hh:mm format. The window will be created in the time zone provided and adjusted to daylight
         savings according to that time zone. Expiration date must be set to a future date. If not
         provided, it will be set to the maximum datetime 9999-12-31 23:59:59.
        :type expiration_date_time: str
        :param duration: Duration of the maintenance window in HH:mm format. If not provided, default
         value will be used based on maintenance scope provided. Example: 05:00.
        :type duration: str
        :param time_zone: Name of the timezone. List of timezones can be obtained by executing
         [System.TimeZoneInfo]::GetSystemTimeZones() in PowerShell. Example: Pacific Standard Time, UTC,
         W. Europe Standard Time, Korea Standard Time, Cen. Australia Standard Time.
        :type time_zone: str
        :param recur_every: Rate at which a Maintenance window is expected to recur. The rate can be
         expressed as daily, weekly, or monthly schedules. Daily schedule are formatted as recurEvery:
         [Frequency as integer]['Day(s)']. If no frequency is provided, the default frequency is 1.
         Daily schedule examples are recurEvery: Day, recurEvery: 3Days.  Weekly schedule are formatted
         as recurEvery: [Frequency as integer]['Week(s)'] [Optional comma separated list of weekdays
         Monday-Sunday]. Weekly schedule examples are recurEvery: 3Weeks, recurEvery: Week
         Saturday,Sunday. Monthly schedules are formatted as [Frequency as integer]['Month(s)'] [Comma
         separated list of month days] or [Frequency as integer]['Month(s)'] [Week of Month (First,
         Second, Third, Fourth, Last)] [Weekday Monday-Sunday]. Monthly schedule examples are
         recurEvery: Month, recurEvery: 2Months, recurEvery: Month day23,day24, recurEvery: Month Last
         Sunday, recurEvery: Month Fourth Monday.
        :type recur_every: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: MaintenanceConfiguration, or the result of cls(response)
        :rtype: ~maintenance_client.models.MaintenanceConfiguration
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.MaintenanceConfiguration"]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))

        _configuration = models.MaintenanceConfiguration(location=location, tags=tags, namespace=namespace, extension_properties=extension_properties, maintenance_scope=maintenance_scope, visibility=visibility, start_date_time=start_date_time, expiration_date_time=expiration_date_time, duration=duration, time_zone=time_zone, recur_every=recur_every)
        api_version = "2020-07-01-preview"
        content_type = kwargs.pop("content_type", "application/json")

        # Construct URL
        url = self.update.metadata['url']  # type: ignore
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'resourceName': self._serialize.url("resource_name", resource_name, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters = {}  # type: Dict[str, Any]
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters = {}  # type: Dict[str, Any]
        header_parameters['Content-Type'] = self._serialize.header("content_type", content_type, 'str')
        header_parameters['Accept'] = 'application/json'

        body_content_kwargs = {}  # type: Dict[str, Any]
        body_content = self._serialize.body(_configuration, 'MaintenanceConfiguration')
        body_content_kwargs['content'] = body_content
        request = self._client.patch(url, query_parameters, header_parameters, **body_content_kwargs)

        pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize(models.MaintenanceError, response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize('MaintenanceConfiguration', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized
    update.metadata = {'url': '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Maintenance/maintenanceConfigurations/{resourceName}'}  # type: ignore

    def list(
        self,
        **kwargs  # type: Any
    ):
        # type: (...) -> Iterable["models.ListMaintenanceConfigurationsResult"]
        """Get Configuration records within a subscription.

        Get Configuration records within a subscription.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either ListMaintenanceConfigurationsResult or the result of cls(response)
        :rtype: ~azure.core.paging.ItemPaged[~maintenance_client.models.ListMaintenanceConfigurationsResult]
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        cls = kwargs.pop('cls', None)  # type: ClsType["models.ListMaintenanceConfigurationsResult"]
        error_map = {404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop('error_map', {}))
        api_version = "2020-07-01-preview"

        def prepare_request(next_link=None):
            # Construct headers
            header_parameters = {}  # type: Dict[str, Any]
            header_parameters['Accept'] = 'application/json'

            if not next_link:
                # Construct URL
                url = self.list.metadata['url']  # type: ignore
                path_format_arguments = {
                    'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
                }
                url = self._client.format_url(url, **path_format_arguments)
                # Construct parameters
                query_parameters = {}  # type: Dict[str, Any]
                query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

                request = self._client.get(url, query_parameters, header_parameters)
            else:
                url = next_link
                query_parameters = {}  # type: Dict[str, Any]
                request = self._client.get(url, query_parameters, header_parameters)
            return request

        def extract_data(pipeline_response):
            deserialized = self._deserialize('ListMaintenanceConfigurationsResult', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return None, iter(list_of_elem)

        def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                error = self._deserialize(models.MaintenanceError, response)
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return ItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': '/subscriptions/{subscriptionId}/providers/Microsoft.Maintenance/maintenanceConfigurations'}  # type: ignore
