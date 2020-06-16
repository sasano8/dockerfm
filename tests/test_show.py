import os
import pytest
from typer.testing import CliRunner
from dockerfm import main
from dockerfm import show
from dockerfm import config

runner = CliRunner()


def test_compose():
    current = os.getcwd()
    config.generate_sample()  # 検証用の雛形を作成する

    result = runner.invoke(main.app, ["show", "compose"])
    items = result.stdout.splitlines()
    items = sorted(items)

    assert items[0] == "base"
    assert items[1] == "compose"


def test_dockerfile():
    current = os.getcwd()
    config.generate_sample()  # 検証用の雛形を作成する

    result = runner.invoke(main.app, ["show", "dockerfile"])
    items = result.stdout.splitlines()
    items = sorted(items)
    assert items[0] == "alpine"
    assert items[1] == "alpine1"
    assert items[2] == "alpine2"


def test_get_compose_files():
    current = os.getcwd()
    config.generate_sample()  # 検証用の雛形を作成する

    files = list(show.get_compose_files())
    files = sorted(files)

    assert files[0] == os.path.join(current, "dockerfm/base/dockercompose.yml")
    assert files[1] == os.path.join(current, "dockerfm/compose/dockercompose.yml")


def test_get_dockerfile_files():
    current = os.getcwd()
    config.generate_sample()  # 検証用の雛形を作成する

    files = list(show.get_dockerfile_files())
    files = sorted(files)

    assert files[0] == os.path.join(current, "dockerfm/base/alpine/Dockerfile")
    assert files[1] == os.path.join(current, "dockerfm/compose/alpine1/Dockerfile")
    assert files[2] == os.path.join(current, "dockerfm/compose/alpine2/Dockerfile")


def test_get_dockerfilereadme_files():
    current = os.getcwd()
    config.generate_sample()  # 検証用の雛形を作成する

    files = list(show.get_dockerfilereadme_files())
    files = sorted(files)

    assert files[0] == os.path.join(current, "dockerfm/base/alpine/README.md")
    assert files[1] == os.path.join(current, "dockerfm/compose/alpine1/README.md")
    assert files[2] == os.path.join(current, "dockerfm/compose/alpine2/README.md")
