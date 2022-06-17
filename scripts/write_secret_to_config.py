'''
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

# aws = AwsSecretMgmt()
# secret_name = "test/test_secret"
# secret = aws.get_secret(secret_name)

# secret_name = 'test/test_secret_2'
# secret_string = json.dumps(secret)
# aws.create_secret(secret_string,secret_name)

## write aws secrets to local
'''

from .aws import AwsSecretMgmt

aws_secret = AwsSecretMgmt()

def write_secret_to_local_config(project_name):
    config = ConfigHandler(project_name)
    secrets_prefix = "projects/dev"
    secret = aws_secret.get_secret(os.path.join(secrets_prefix, project_name))
    config.write_config_file_from_dict(config_dict=secret)
    return config.print_configs()

for project_name in projects:
    write_secret_to_local_config(project_name)

    
