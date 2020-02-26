# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.0.6225, generator: {generator})
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, Callable, Dict, Generic, Optional, TypeVar, Union
import warnings

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse, HttpRequest

from ... import models

T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class AssessmentsOperations:
    """AssessmentsOperations async operations.

    You should not instantiate directly this class, but create a Client instance that will create it for you and attach it as attribute.

    :ivar models: Alias to model classes used in this operation group.
    :type models: ~azure_migrate.models
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    """

    models = models

    def __init__(self, client, config, serializer, deserializer) -> None:
        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self._config = config

    def list_by_group(
        self,
        resource_group_name: str,
        project_name: str,
        group_name: str,
        **kwargs
    ) -> "models.AssessmentResultList":
        """Get all assessments created for the specified group.

    Returns a json array of objects of type 'assessment' as specified in Models section.

        Get all assessments created for the specified group.

        :param resource_group_name: Name of the Azure Resource Group that project is part of.
        :type resource_group_name: str
        :param project_name: Name of the Azure Migrate project.
        :type project_name: str
        :param group_name: Unique name of a group within a project.
        :type group_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: AssessmentResultList or the result of cls(response)
        :rtype: ~azure_migrate.models.AssessmentResultList
        :raises: ~azure_migrate.models.CloudErrorException:
        """
        cls: ClsType["models.AssessmentResultList"] = kwargs.pop('cls', None )
        error_map = kwargs.pop('error_map', {})
        api_version = "2018-02-02"

        def prepare_request(next_link=None):
            if not next_link:
                # Construct URL
                url = self.list_by_group.metadata['url']
                path_format_arguments = {
                    'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
                    'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
                    'projectName': self._serialize.url("project_name", project_name, 'str'),
                    'groupName': self._serialize.url("group_name", group_name, 'str'),
                }
                url = self._client.format_url(url, **path_format_arguments)
            else:
                url = next_link

            # Construct parameters
            query_parameters: Dict[str, Any] = {}
            query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

            # Construct headers
            header_parameters: Dict[str, Any] = {}
            if self._config.accept_language is not None:
                header_parameters['Accept-Language'] = self._serialize.header("self._config.accept_language", self._config.accept_language, 'str')
            header_parameters['Accept'] = 'application/json'

            # Construct and send request
            request = self._client.get(url, query_parameters, header_parameters)
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize('AssessmentResultList', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise models.CloudErrorException.from_response(response, self._deserialize)

            return pipeline_response

        return AsyncItemPaged(
            get_next, extract_data
        )
    list_by_group.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}/assessments'}

    def list_by_project(
        self,
        resource_group_name: str,
        project_name: str,
        **kwargs
    ) -> "models.AssessmentResultList":
        """Get all assessments created in the project.

    Returns a json array of objects of type 'assessment' as specified in Models section.

        Get all assessments created in the project.

        :param resource_group_name: Name of the Azure Resource Group that project is part of.
        :type resource_group_name: str
        :param project_name: Name of the Azure Migrate project.
        :type project_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: AssessmentResultList or the result of cls(response)
        :rtype: ~azure_migrate.models.AssessmentResultList
        :raises: ~azure_migrate.models.CloudErrorException:
        """
        cls: ClsType["models.AssessmentResultList"] = kwargs.pop('cls', None )
        error_map = kwargs.pop('error_map', {})
        api_version = "2018-02-02"

        def prepare_request(next_link=None):
            if not next_link:
                # Construct URL
                url = self.list_by_project.metadata['url']
                path_format_arguments = {
                    'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
                    'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
                    'projectName': self._serialize.url("project_name", project_name, 'str'),
                }
                url = self._client.format_url(url, **path_format_arguments)
            else:
                url = next_link

            # Construct parameters
            query_parameters: Dict[str, Any] = {}
            query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

            # Construct headers
            header_parameters: Dict[str, Any] = {}
            if self._config.accept_language is not None:
                header_parameters['Accept-Language'] = self._serialize.header("self._config.accept_language", self._config.accept_language, 'str')
            header_parameters['Accept'] = 'application/json'

            # Construct and send request
            request = self._client.get(url, query_parameters, header_parameters)
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize('AssessmentResultList', pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise models.CloudErrorException.from_response(response, self._deserialize)

            return pipeline_response

        return AsyncItemPaged(
            get_next, extract_data
        )
    list_by_project.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/assessments'}

    async def get(
        self,
        resource_group_name: str,
        project_name: str,
        group_name: str,
        assessment_name: str,
        **kwargs
    ) -> "models.Assessment":
        """Get an existing assessment with the specified name. Returns a json object of type 'assessment' as specified in Models section.

        Get an assessment.

        :param resource_group_name: Name of the Azure Resource Group that project is part of.
        :type resource_group_name: str
        :param project_name: Name of the Azure Migrate project.
        :type project_name: str
        :param group_name: Unique name of a group within a project.
        :type group_name: str
        :param assessment_name: Unique name of an assessment within a project.
        :type assessment_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Assessment or the result of cls(response)
        :rtype: ~azure_migrate.models.Assessment
        :raises: ~azure_migrate.models.CloudErrorException:
        """
        cls: ClsType["models.Assessment"] = kwargs.pop('cls', None )
        error_map = kwargs.pop('error_map', {})
        api_version = "2018-02-02"

        # Construct URL
        url = self.get.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'projectName': self._serialize.url("project_name", project_name, 'str'),
            'groupName': self._serialize.url("group_name", group_name, 'str'),
            'assessmentName': self._serialize.url("assessment_name", assessment_name, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters: Dict[str, Any] = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters: Dict[str, Any] = {}
        if self._config.accept_language is not None:
            header_parameters['Accept-Language'] = self._serialize.header("self._config.accept_language", self._config.accept_language, 'str')
        header_parameters['Accept'] = 'application/json'

        # Construct and send request
        request = self._client.get(url, query_parameters, header_parameters)
        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise models.CloudErrorException.from_response(response, self._deserialize)

        response_headers = {}
        response_headers['x-ms-request-id']=self._deserialize('str', response.headers.get('x-ms-request-id'))
        deserialized = self._deserialize('Assessment', pipeline_response)

        if cls:
          return cls(pipeline_response, deserialized, response_headers)

        return deserialized
    get.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}/assessments/{assessmentName}'}

    async def create(
        self,
        resource_group_name: str,
        project_name: str,
        group_name: str,
        assessment_name: str,
        azure_location: Union[str, "models.AzureLocation"],
        azure_offer_code: Union[str, "models.AzureOfferCode"],
        azure_pricing_tier: Union[str, "models.AzurePricingTier"],
        azure_storage_redundancy: Union[str, "models.AzureStorageRedundancy"],
        scaling_factor: float,
        percentile: Union[str, "models.Percentile"],
        time_range: Union[str, "models.TimeRange"],
        stage: Union[str, "models.AssessmentStage"],
        currency: Union[str, "models.Currency"],
        azure_hybrid_use_benefit: Union[str, "models.AzureHybridUseBenefit"],
        discount_percentage: float,
        sizing_criterion: Union[str, "models.AssessmentSizingCriterion"],
        e_tag: Optional[str] = None,
        **kwargs
    ) -> "models.Assessment":
        """Create a new assessment with the given name and the specified settings. Since name of an assessment in a project is a unique identifier, if an assessment with the name provided already exists, then the existing assessment is updated.

    Any PUT operation, resulting in either create or update on an assessment, will cause the assessment to go in a "InProgress" state. This will be indicated by the field 'computationState' on the Assessment object. During this time no other PUT operation will be allowed on that assessment object, nor will a Delete operation. Once the computation for the assessment is complete, the field 'computationState' will be updated to 'Ready', and then other PUT or DELETE operations can happen on the assessment.

    When assessment is under computation, any PUT will lead to a 400 - Bad Request error.

        Create or Update assessment.

        :param resource_group_name: Name of the Azure Resource Group that project is part of.
        :type resource_group_name: str
        :param project_name: Name of the Azure Migrate project.
        :type project_name: str
        :param group_name: Unique name of a group within a project.
        :type group_name: str
        :param assessment_name: Unique name of an assessment within a project.
        :type assessment_name: str
        :param azure_location: Target Azure location for which the machines should be assessed. These
         enums are the same as used by Compute API.
        :type azure_location: str or ~azure_migrate.models.AzureLocation
        :param azure_offer_code: Offer code according to which cost estimation is done.
        :type azure_offer_code: str or ~azure_migrate.models.AzureOfferCode
        :param azure_pricing_tier: Pricing tier for Size evaluation.
        :type azure_pricing_tier: str or ~azure_migrate.models.AzurePricingTier
        :param azure_storage_redundancy: Storage Redundancy type offered by Azure.
        :type azure_storage_redundancy: str or ~azure_migrate.models.AzureStorageRedundancy
        :param scaling_factor: Scaling factor used over utilization data to add a performance buffer
         for new machines to be created in Azure. Min Value = 1.0, Max value = 1.9, Default = 1.3.
        :type scaling_factor: float
        :param percentile: Percentile of performance data used to recommend Azure size.
        :type percentile: str or ~azure_migrate.models.Percentile
        :param time_range: Time range of performance data used to recommend a size.
        :type time_range: str or ~azure_migrate.models.TimeRange
        :param stage: User configurable setting that describes the status of the assessment.
        :type stage: str or ~azure_migrate.models.AssessmentStage
        :param currency: Currency to report prices in.
        :type currency: str or ~azure_migrate.models.Currency
        :param azure_hybrid_use_benefit: AHUB discount on windows virtual machines.
        :type azure_hybrid_use_benefit: str or ~azure_migrate.models.AzureHybridUseBenefit
        :param discount_percentage: Custom discount percentage to be applied on final costs. Can be in
         the range [0, 100].
        :type discount_percentage: float
        :param sizing_criterion: Assessment sizing criterion.
        :type sizing_criterion: str or ~azure_migrate.models.AssessmentSizingCriterion
        :param e_tag: For optimistic concurrency control.
        :type e_tag: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Assessment or Assessment or the result of cls(response)
        :rtype: ~azure_migrate.models.Assessment or ~azure_migrate.models.Assessment
        :raises: ~azure_migrate.models.CloudErrorException:
        """
        cls: ClsType["models.Assessment"] = kwargs.pop('cls', None )
        error_map = kwargs.pop('error_map', {})

        assessment = models.Assessment(e_tag=e_tag, azure_location=azure_location, azure_offer_code=azure_offer_code, azure_pricing_tier=azure_pricing_tier, azure_storage_redundancy=azure_storage_redundancy, scaling_factor=scaling_factor, percentile=percentile, time_range=time_range, stage=stage, currency=currency, azure_hybrid_use_benefit=azure_hybrid_use_benefit, discount_percentage=discount_percentage, sizing_criterion=sizing_criterion)
        api_version = "2018-02-02"

        # Construct URL
        url = self.create.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'projectName': self._serialize.url("project_name", project_name, 'str'),
            'groupName': self._serialize.url("group_name", group_name, 'str'),
            'assessmentName': self._serialize.url("assessment_name", assessment_name, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters: Dict[str, Any] = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters: Dict[str, Any] = {}
        if self._config.accept_language is not None:
            header_parameters['Accept-Language'] = self._serialize.header("self._config.accept_language", self._config.accept_language, 'str')
        header_parameters['Accept'] = 'application/json'
        header_parameters['Content-Type'] = 'application/json'

        # Construct body
        if assessment is not None:
            body_content = self._serialize.body(assessment, 'Assessment')
        else:
            body_content = None

        # Construct and send request
        request = self._client.put(url, query_parameters, header_parameters, body_content)
        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200, 201]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise models.CloudErrorException.from_response(response, self._deserialize)

        response_headers = {}
        deserialized = None
        if response.status_code == 200:
            response_headers['x-ms-request-id']=self._deserialize('str', response.headers.get('x-ms-request-id'))
            deserialized = self._deserialize('Assessment', pipeline_response)

        if response.status_code == 201:
            response_headers['x-ms-request-id']=self._deserialize('str', response.headers.get('x-ms-request-id'))
            deserialized = self._deserialize('Assessment', pipeline_response)

        if cls:
          return cls(pipeline_response, deserialized, response_headers)

        return deserialized
    create.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}/assessments/{assessmentName}'}

    async def delete(
        self,
        resource_group_name: str,
        project_name: str,
        group_name: str,
        assessment_name: str,
        **kwargs
    ) -> None:
        """Delete an assessment from the project. The machines remain in the assessment. Deleting a non-existent assessment results in a no-operation.

    When an assessment is under computation, as indicated by the 'computationState' field, it cannot be deleted. Any such attempt will return a 400 - Bad Request.

        Deletes an assessment from the project.

        :param resource_group_name: Name of the Azure Resource Group that project is part of.
        :type resource_group_name: str
        :param project_name: Name of the Azure Migrate project.
        :type project_name: str
        :param group_name: Unique name of a group within a project.
        :type group_name: str
        :param assessment_name: Unique name of an assessment within a project.
        :type assessment_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None or the result of cls(response)
        :rtype: None
        :raises: ~azure_migrate.models.CloudErrorException:
        """
        cls: ClsType[None] = kwargs.pop('cls', None )
        error_map = kwargs.pop('error_map', {})
        api_version = "2018-02-02"

        # Construct URL
        url = self.delete.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'projectName': self._serialize.url("project_name", project_name, 'str'),
            'groupName': self._serialize.url("group_name", group_name, 'str'),
            'assessmentName': self._serialize.url("assessment_name", assessment_name, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters: Dict[str, Any] = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters: Dict[str, Any] = {}
        if self._config.accept_language is not None:
            header_parameters['Accept-Language'] = self._serialize.header("self._config.accept_language", self._config.accept_language, 'str')

        # Construct and send request
        request = self._client.delete(url, query_parameters, header_parameters)
        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise models.CloudErrorException.from_response(response, self._deserialize)

        response_headers = {}
        response_headers['x-ms-request-id']=self._deserialize('str', response.headers.get('x-ms-request-id'))

        if cls:
          return cls(pipeline_response, None, response_headers)

    delete.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}/assessments/{assessmentName}'}

    async def get_report_download_url(
        self,
        resource_group_name: str,
        project_name: str,
        group_name: str,
        assessment_name: str,
        **kwargs
    ) -> "models.DownloadUrl":
        """Get the URL for downloading the assessment in a report format.

        Get download URL for the assessment report.

        :param resource_group_name: Name of the Azure Resource Group that project is part of.
        :type resource_group_name: str
        :param project_name: Name of the Azure Migrate project.
        :type project_name: str
        :param group_name: Unique name of a group within a project.
        :type group_name: str
        :param assessment_name: Unique name of an assessment within a project.
        :type assessment_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: DownloadUrl or the result of cls(response)
        :rtype: ~azure_migrate.models.DownloadUrl
        :raises: ~azure_migrate.models.CloudErrorException:
        """
        cls: ClsType["models.DownloadUrl"] = kwargs.pop('cls', None )
        error_map = kwargs.pop('error_map', {})
        api_version = "2018-02-02"

        # Construct URL
        url = self.get_report_download_url.metadata['url']
        path_format_arguments = {
            'subscriptionId': self._serialize.url("self._config.subscription_id", self._config.subscription_id, 'str'),
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str'),
            'projectName': self._serialize.url("project_name", project_name, 'str'),
            'groupName': self._serialize.url("group_name", group_name, 'str'),
            'assessmentName': self._serialize.url("assessment_name", assessment_name, 'str'),
        }
        url = self._client.format_url(url, **path_format_arguments)

        # Construct parameters
        query_parameters: Dict[str, Any] = {}
        query_parameters['api-version'] = self._serialize.query("api_version", api_version, 'str')

        # Construct headers
        header_parameters: Dict[str, Any] = {}
        if self._config.accept_language is not None:
            header_parameters['Accept-Language'] = self._serialize.header("self._config.accept_language", self._config.accept_language, 'str')
        header_parameters['Accept'] = 'application/json'

        # Construct and send request
        request = self._client.post(url, query_parameters, header_parameters)
        pipeline_response = await self._client._pipeline.run(request, stream=False, **kwargs)
        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise models.CloudErrorException.from_response(response, self._deserialize)

        response_headers = {}
        response_headers['x-ms-request-id']=self._deserialize('str', response.headers.get('x-ms-request-id'))
        deserialized = self._deserialize('DownloadUrl', pipeline_response)

        if cls:
          return cls(pipeline_response, deserialized, response_headers)

        return deserialized
    get_report_download_url.metadata = {'url': '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Migrate/projects/{projectName}/groups/{groupName}/assessments/{assessmentName}/downloadUrl'}
