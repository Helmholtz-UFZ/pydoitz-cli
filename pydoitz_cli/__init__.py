import pydoitz
import click
import sys
from pydoitz_cli.application import Application
from pydoitz_cli.cmdb.category import category
from pydoitz import cache as _cache


@click.group(
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True
)
@click.pass_context
@click.option(
    "--host",
    "-H",
    metavar="<host>",
    help="Name of the iDoit Host to connect to.",
)
@click.option(
    "--user",
    "-u",
    metavar="<user>",
    help="Username for the API",
)
@click.option(
    "--password",
    "-p",
    metavar="<password>",
    help="Password for the API",
)
@click.option(
    "--key",
    "-k",
    metavar="<key>",
    help="API-Key",
)
@click.option(
    "--verbose",
    "-v",
    metavar="<verbose>",
    help="Logging verbosity",
    count=True,
)
def cli(ctx, host, user, password, key, verbose):
    app = Application(host, user, password, key)
    ctx.obj = app
    ctx.verbose = verbose


@cli.group(no_args_is_help=True)
@click.pass_context
def cmdb(ctx):
    pass


cmdb.add_command(category)


@cli.command()
@click.pass_context
def cache(ctx):
    _cache.init(ctx.obj.api)


def main(args=sys.argv):
    cli(obj={})
