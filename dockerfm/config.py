import typer
import click
import os

app = typer.Typer(help="load value from dockerfm.toml in the current directory.")


@app.command()
def list():
    """Enumrate key-value with dockerfm.toml."""
    config_dic = load()
    arr_config = config_dic["tool"]["dockerfm"]
    for key, value in arr_config.items():
        typer.echo(f"{key} = {value}")


def get_dockerfm_toml_path():
    cd = os.getcwd()
    path_dockerfm_toml = os.path.join(cd, "dockerfm.toml")
    return os.path.abspath(path_dockerfm_toml)


def get_dockerfm_dir():
    config_dic = load()

    cd = os.getcwd()
    tmp_path = config_dic["tool"]["dockerfm"]["dockerfm_dir"]
    path_dockerfm_dir = os.path.join(cd, tmp_path)
    return os.path.abspath(path_dockerfm_dir)


def get_default_config_dic(
    username: str = "yourname",
    projectname: str = "sample",
    dockerfm_dir: str = "./dockerfm/",
):

    return {
        "tool": {
            "dockerfm": {
                "dockerfm_dir": dockerfm_dir,
                "user": username,
                "project": projectname,
            },
        }
    }


def generate_sample():
    config_dic = get_default_config_dic()
    generate(config_dic, create_template=True)


def generate(config_dic, create_template: bool = False):
    import toml

    dockerfm_dir = config_dic["tool"]["dockerfm"]["dockerfm_dir"]
    cd = os.getcwd()
    path_dockerfm_toml = get_dockerfm_toml_path()
    path_dockerfm_dir = cd + "/" + dockerfm_dir

    if os.path.exists(path_dockerfm_toml):
        raise click.ClickException("Already exists dockerfm.toml in current directory.")

    if os.path.exists(path_dockerfm_dir):
        raise click.ClickException(
            "Already exists dockerfm directory in current directory."
        )

    if os.path.exists(os.path.join(path_dockerfm_dir, "pushreadme.py")):
        raise click.ClickException(
            "Already exists pushreadme.py in dockerfm directory."
        )

    with open(path_dockerfm_toml, mode="w") as f:
        os.makedirs(path_dockerfm_dir)
        from dockerfm.customscripts import pushreadme
        import shutil

        base_name = os.path.basename(pushreadme.__file__)
        shutil.copyfile(pushreadme.__file__, os.path.join(path_dockerfm_dir, base_name))

        if create_template:
            os.makedirs(path_dockerfm_dir + "/base/alpine")
            os.makedirs(path_dockerfm_dir + "/compose/alpine1")
            os.makedirs(path_dockerfm_dir + "/compose/alpine2")

        toml.dump(config_dic, f)


def load():
    import toml

    path_dockerfm_toml = get_dockerfm_toml_path()

    if not os.path.exists(path_dockerfm_toml):
        raise click.ClickException(
            "Not exists dockerfm.toml in the current directory. Please run [dockerfm init]"
        )

    f = open(path_dockerfm_toml)
    settings = toml.load(f)
    f.close()

    return settings
