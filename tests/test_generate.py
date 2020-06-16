import os
import pytest
from typer.testing import CliRunner
from dockerfm import main
from dockerfm import generate
from dockerfm import config

runner = CliRunner()


def test_represent_odict():
    assert True


def test_construct_odict():
    assert True


def test_output_config_yml():
    current = os.getcwd()
    config.generate_sample()  # 検証用の雛形を作成する

    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_expected_file = os.path.join(current_dir, "expected", "config.yml")
    path_actual_file = ".circleci/config.yml"

    generate.output_config_yml("testproject", "testman")
    assert os.path.exists(path_actual_file)

    # 答えが変わった場合は、想定結果を置き換える）
    # import shutil
    # src = path_actual_file
    # dest = path_expected_file
    # shutil.copyfile(src, dest)

    actual_file = None
    expected_file = None

    with open(path_actual_file, "r") as f:
        actual_file = f.read()

    with open(path_expected_file, "r") as f:
        expected_file = f.read()

    # difflibを活用したかったが、エラーが綺麗に出力できなかったので自作でdiffする
    # import difflib

    actual_file = actual_file.splitlines()
    expected_file = expected_file.splitlines()

    for i in range(max(len(actual_file), len(expected_file))):
        assert actual_file[i] == expected_file[i]


def test_define_step():
    assert True


def test_define_workflow():
    assert True
