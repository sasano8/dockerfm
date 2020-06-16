import os
import sys
from typer.testing import CliRunner
import pytest
from dockerfm import main
from dockerfm import config

runner = CliRunner()


def test_init():
    current = os.getcwd()
    input_arr = ["sasano8", "basic", "./dockerfm/", "False"]
    input_value = "\n".join(input_arr)

    result = runner.invoke(
        # main.app, ["init", "--no-create-template"], input=input_value
        main.app,
        ["init", "--no-create-template"],
        input=input_value,
    )
    assert result.exit_code == 0
    assert os.path.exists("dockerfm.toml")
    assert os.path.exists("dockerfm")

    # すでに初期化済みの場合
    result = runner.invoke(
        main.app, ["init", "--no-create-template"], input=input_value
    )
    assert result.exit_code != 0
    assert "Already exists dockerfm.toml" in result.stdout

    # dockerfm.tomlは存在しないがdockerfm directoryが存在する場合
    os.unlink("dockerfm.toml")
    assert os.path.exists("dockerfm.toml") == False
    assert os.path.exists("dockerfm")
    result = runner.invoke(
        main.app, ["init", "--no-create-template"], input=input_value
    )
    assert result.exit_code != 0
    assert "Already exists dockerfm directory" in result.stdout

    # 雛形作成テスト
    import shutil

    shutil.rmtree("dockerfm")
    assert os.path.exists("dockerfm.toml") == False
    assert os.path.exists("dockerfm") == False

    input_arr = ["sasano8", "basic", "./dockerfm/", "True"]
    input_value = "\n".join(input_arr)

    result = runner.invoke(main.app, ["init", "--create-template"], input=input_value)
    assert result.exit_code == 0
    assert os.path.exists("dockerfm.toml")
    assert os.path.exists("dockerfm/base/alpine")
    assert os.path.exists("dockerfm/compose/alpine1")
    assert os.path.exists("dockerfm/compose/alpine2")


def test_validate():
    current = os.getcwd()
    config.generate_sample()  # 検証用の雛形を作成する

    result = runner.invoke(main.app, ["validate"])
    assert result.exit_code == 0

    # 禁止文字の確認
    os.mkdir("dockerfm/base/:")
    result = runner.invoke(main.app, ["validate"])
    assert result.exit_code != 0
    assert "Exists validation error" in result.stdout
    os.rmdir("dockerfm/base/:")

    # 禁止文字の確認
    os.mkdir("dockerfm/base/_")
    result = runner.invoke(main.app, ["validate"])
    assert result.exit_code != 0
    assert "Exists validation error" in result.stdout
    os.rmdir("dockerfm/base/_")

    # dockerfm.tomlの確認
    with open("dockerfm.toml", "w") as f:
        f.write("aaaa")

    result = runner.invoke(main.app, ["validate"])
    assert result.exit_code != 0


def test_ci():
    current = os.getcwd()

    result = runner.invoke(main.app, ["ci"])
    assert result.exit_code != 0

    config.generate_sample()  # 検証用の雛形を作成する

    result = runner.invoke(main.app, ["ci"])
    assert result.exit_code == 0
