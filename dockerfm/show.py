# coding:utf-8

import os
import typer
import click

app = typer.Typer(help="show Dockerfile.yml and dockercompose.yml")


@app.command()
def compose():
    for item in get_compose_names():
        click.echo(f"{item}")


@app.command()
def dockerfile():
    for item in get_dockerfile_names():
        click.echo(f"{item}")


def get_directories(target_dir_path):
    """指定したdirectoryに存在するdirectoryを返す"""
    filenames = os.listdir(target_dir_path)
    filepaths = map(lambda name: os.path.join(target_dir_path, name), filenames)
    directories = filter(lambda filepath: os.path.isdir(filepath), filepaths)

    for dirpath in directories:
        yield dirpath


def get_compose_dirs():
    from dockerfm import config

    path_dockerfm_dir = config.get_dockerfm_dir()

    return get_directories(path_dockerfm_dir)


def get_compose_names():
    return map(lambda compose_dir: os.path.basename(compose_dir), get_compose_dirs())


def get_compose_files():
    return map(
        lambda compose_dir: os.path.join(compose_dir, "dockercompose.yml"),
        get_compose_dirs(),
    )


def get_dockerfile_dirs():
    for path_compose_dirs in get_compose_dirs():
        for path_dockerfile_dir in get_directories(path_compose_dirs):
            yield path_dockerfile_dir


def get_dockerfile_names():
    return map(
        lambda dockerfile_dir: os.path.basename(dockerfile_dir), get_dockerfile_dirs()
    )


def get_dockerfile_files():
    return map(
        lambda dockerfile_dir: os.path.join(dockerfile_dir, "Dockerfile"),
        get_dockerfile_dirs(),
    )


def get_dockerfilereadme_files():
    return map(
        lambda dockerfile_dir: os.path.join(dockerfile_dir, "README.md"),
        get_dockerfile_dirs(),
    )
