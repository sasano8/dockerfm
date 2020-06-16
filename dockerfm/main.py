import os
import typer
import click

from dockerfm import config
from dockerfm import show
from dockerfm import generate

app = typer.Typer()
app.add_typer(config.app, name="config")
app.add_typer(show.app, name="show")

DIR_BLOCK_WORDS = [":", "_"]


# resilient_parsing: dockerfm.tomlが存在する場合、対話形式のプロンプトを無視する。値はNoneとなる。
@app.command(
    context_settings={
        "resilient_parsing": os.path.exists(config.get_dockerfm_toml_path())
    }
)
def init(
    user_name: str = typer.Option(prompt=True, default="yourname",),
    project_name: str = typer.Option(prompt=True, default="sample"),
    dockerfm_dir: str = typer.Option(prompt=True, default="./dockerfm/"),
    create_template: bool = typer.Option(
        prompt="Create template dockerfm directories?", default=False
    ),
):
    """generate dockerfm.toml and dockerfm directory in the current diretory."""
    config_dic = config.get_default_config_dic(
        username=user_name, projectname=project_name, dockerfm_dir=dockerfm_dir,
    )

    config.generate(
        config_dic=config_dic, create_template=create_template,
    )


@app.command()
def validate():
    """Validate a dockerfm.toml in the current directory and validate dockerfm directory."""
    config.load()

    from itertools import chain

    is_all_ok = True

    for dir_name in chain(show.get_compose_dirs(), show.get_dockerfile_dirs()):
        basename = os.path.basename(dir_name)

        is_validate_ok = True
        msg = ""

        for char in DIR_BLOCK_WORDS:
            if char in basename:
                is_validate_ok = False
                msg = "Can't use '{}'".format(char)
                break

        if is_validate_ok:
            typer.echo("[OK]{}".format(dir_name))

        else:
            is_all_ok = False
            typer.echo("[NG]{} => {}".format(dir_name, msg))

    if is_all_ok == False:
        raise click.ClickException("Exists validation error.")

    # for image in images:
    #     if ":" in image:
    #         raise ValueError(":はyamlで誤作動を起こすから禁止:{}".format(image))
    #
    #     if "_" in image:
    #         raise ValueError("_はセパレータとして予約したいから禁止:{}".format(image))


@app.command()
def ci(ci_provider="circleci"):
    """Generate .circleci/config.yml"""
    config_dic = config.load()

    PROJECTNAME = config_dic["tool"]["dockerfm"]["project"]
    USERNAME = config_dic["tool"]["dockerfm"]["user"]

    generate.output_config_yml(PROJECTNAME, USERNAME)


if __name__ == "__main__":
    app()
