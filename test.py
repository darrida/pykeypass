import click
from click.testing import CliRunner


@click.command()
@click.option('--name', prompt='Your name', help='The person to greet.')
@click.option('--count', default=1, help='Number of greetings.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)


def test_hello_world():

    runner = CliRunner()
    result = runner.invoke(hello, ['--name', 'Peter'])
    assert result.exit_code == 0
    assert result.output == 'Hello Peter!\n'

    result = runner.invoke(hello, [], input='Peter\n')
    assert result.exit_code == 0
    assert result.output == 'Your name: Peter\nHello Peter!\n'

# test_hello_world()