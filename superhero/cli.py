import click
import logging
from .supervisor import Supervisor


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    import superhero
    click.echo('Current version is: ' + superhero.__version__)
    ctx.exit()


@click.group(context_settings=dict(obj={}))
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Print out current version.')
@click.option('--log-level', '-l',
              type=click.Choice(['debug', 'info', 'warning', 'error']),
              help='Choose a logger level',
              default='info')
def cli(log_level):
    if log_level == 'debug':
        fmt = '%(asctime)s [%(levelname)s] %(module)s: %(message)s'
    else:
        fmt = '%(asctime)s [%(levelname)s]: %(message)s'
    logging.basicConfig(level=log_level.upper(), format=fmt)


@cli.command()
def hello():
    """Hello world."""
    click.echo('Hello world!')


@cli.command()
@click.option('--daemon', is_flag=True, help='Run in daemon mode.')
def serve(daemon):
    """Start to server."""
    if daemon:
        raise NotImplementedError('Daemon mode is not implemented')
    app = Supervisor()
    app.loop()
