import json
import datetime

import click

from .aws import aws


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


def echo_dict(input_dict: dict):
    for key, val in input_dict.items():
        click.echo(f"{key[:18]+'..' if len(key)>17 else key}{(20-int(len(key)))*'.'}{val}")


@click.group()
@click.version_option()
def cli():
    "A simple CLI for managing secrets in AWS Secrets Manager"
    pass


@cli.command()
def ls():
    "list secrets in AWS Secrets Manager"
    resp = aws.get_secrets_list()
    for secret in resp.get("SecretList"):
        click.echo(f"\n-- {secret.get('Name')} --")
        echo_dict(input_dict)


# create
@cli.command()
@click.option("-s", "--secret-string", "secret_string", help="serialized json", required=True)
@click.option("-n", "--secret-name", "secret_name", required=True)
def create(secret_string, secret_name):
    "create new secret"
    aws.create(name=secret_name,secret_value=secret_string)


# read
@cli.command()
@click.option("-n", "--secret-name", "secret_name", required=True)
def read(secret_name):
    "read contents of secret, metadata and secret_string"
    resp = aws.describe(name=secret_name)
    echo_dict(resp)
    value = click.prompt("display secret string? [Y/n]", type=str)
    if value.lower() == "y":
        click.echo(aws.get_value())


# update
@cli.command()
@click.option("-s", "--secret-string", "secret_string", help="serialized json", required=True)
@click.option("-n", "--secret-name", "secret_name", required=True)
# @click.option("-d", "--description", "description", required=False, default="string description")
def update(secret_string, secret_name):  # , description):
    "change or add the contents of an existing secert"
    resp = aws.put_value(secret_value=secret_string, name=secret_name)
    click.echo(resp)


# delete
@cli.command()
@click.option("-n", "--secret-name", "secret_name", required=True)
def delete(secret_name):
    "remove or archive a secret from AWS Secret Manager"
    resp = aws.delete(name=secret_name, without_recovery=False)
    click.echo(resp)


cli.add_command(ls)
cli.add_command(create)
cli.add_command(read)
cli.add_command(update)
cli.add_command(delete)
# cli.add_command(search)
