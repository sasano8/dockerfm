import os
import pytest
from typer.testing import CliRunner
from dockerfm import main
from dockerfm import config

runner = CliRunner()


def test_list():
    current = os.getcwd()
    config.generate_sample()

    result = runner.invoke(main.app, ["config", "list"])
    items = result.stdout.splitlines()
    items = sorted(items)

    assert items[0] == "dockerfm_dir = ./dockerfm/"
    assert items[1] == "project = sample"
    assert items[2] == "user = yourname"

    assert len(items) == 3


def test_load():
    current = os.getcwd()

    with pytest.raises(Exception, match="Not exists dockerfm.toml") as e:
        config.load()
