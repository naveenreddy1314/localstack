# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)
from localstack.utils.strings import short_uid


class LambdaLayerVersionProperties(TypedDict):
    Content: Optional[Content]
    CompatibleArchitectures: Optional[list[str]]
    CompatibleRuntimes: Optional[list[str]]
    Description: Optional[str]
    Id: Optional[str]
    LayerName: Optional[str]
    LicenseInfo: Optional[str]


class Content(TypedDict):
    S3Bucket: Optional[str]
    S3Key: Optional[str]
    S3ObjectVersion: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class LambdaLayerVersionProvider(ResourceProvider[LambdaLayerVersionProperties]):
    TYPE = "AWS::Lambda::LayerVersion"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[LambdaLayerVersionProperties],
    ) -> ProgressEvent[LambdaLayerVersionProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - Content

        Create-only properties:
          - /properties/CompatibleRuntimes
          - /properties/LicenseInfo
          - /properties/CompatibleArchitectures
          - /properties/LayerName
          - /properties/Description
          - /properties/Content

        Read-only properties:
          - /properties/Id



        """
        model = request.desired_state
        lambda_client = request.aws_client_factory.lambda_
        if not model.get("LayerName"):
            model["LayerName"] = f"layer-{short_uid()}"
        response = lambda_client.publish_layer_version(**model)
        model["Id"] = response["LayerVersionArn"]

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[LambdaLayerVersionProperties],
    ) -> ProgressEvent[LambdaLayerVersionProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[LambdaLayerVersionProperties],
    ) -> ProgressEvent[LambdaLayerVersionProperties]:
        """
        Delete a resource


        """
        model = request.desired_state
        lambda_client = request.aws_client_factory.lambda_
        version = int(model["Id"].split(":")[-1])

        lambda_client.delete_layer_version(LayerName=model["LayerName"], VersionNumber=version)
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[LambdaLayerVersionProperties],
    ) -> ProgressEvent[LambdaLayerVersionProperties]:
        """
        Update a resource


        """
        raise NotImplementedError
