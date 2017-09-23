import click


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
def cli():
    pass


@cli.command()
def hello():
    click.echo('Hello world!')
