"""
docstring
"""

import os
import json
import base64
import pathlib
import configparser

import boto3
from botocore.exceptions import ClientError


def get_default_region() -> str:
    config_file_path = pathlib.Path.home() / ".aws" / "config"
    if os.path.isfile(config_file_path):
        config = configparser.ConfigParser()
        config.read(config_file_path)
        return config["default"]["region"]
    else:
        region = "us-west-1"
        return region


class AwsSecretMgmt:
    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client(service_name="secretsmanager", region_name=get_default_region())

    def get_secret(self, secret_name):
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "DecryptionFailureException":
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InternalServiceErrorException":
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response["Error"]["Code"] == "ResourceNotFoundException":
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS key.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
                return json.loads(secret)
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response["SecretBinary"])

    def get_secrets_list(self):
        return self.client.list_secrets()

    def create_secret(self, secret_string, secret_name, description="string description"):
        try:
            response = self.client.create_secret(
                Name=secret_name,
                Description=description,
                SecretString=secret_string,
            )
            return response
        except ClientError as e:
            return e


aws = AwsSecretMgmt()
