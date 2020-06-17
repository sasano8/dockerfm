import os
import typer
import yaml
from collections import OrderedDict

from dockerfm import config
from dockerfm import show


app = typer.Typer()

# yaml出力時にOrderedDictに対応させるコード
def represent_odict(dumper, instance):
    return dumper.represent_mapping("tag:yaml.org,2002:map", instance.items())


def construct_odict(loader, node):
    raise Exception()
    return OrderedDict(loader.construct_pairs(node))


yaml.add_representer(OrderedDict, represent_odict)
yaml.add_constructor("tag:yaml.org,2002:map", construct_odict)


def output_config_yml(PROJECTNAME: str, USERNAME: str):

    from dockerfm import main

    # dockerfm.tomlが存在とディレクトリにブロックリストワードが含まれていないか精査する
    main.validate()
    PATH_CONFIG_ROOT = os.path.dirname(config.get_dockerfm_toml_path())
    CI_PATH = os.path.abspath(PATH_CONFIG_ROOT + "/.circleci/config.yml")

    config_dic = OrderedDict()
    config_dic["version"] = 2
    config_dic["jobs"] = OrderedDict()

    for path_compose_file in show.get_compose_files():
        path_compose_dir = os.path.dirname(path_compose_file)
        compose_name = os.path.basename(path_compose_dir)

        for path_dockerfile_dir in show.get_directories(path_compose_dir):
            base_name = os.path.basename(path_dockerfile_dir)
            image_name = (
                USERNAME + "/" + PROJECTNAME + "_" + compose_name + "_" + base_name
            )

            path_dockerfile_dir = path_dockerfile_dir.replace(PATH_CONFIG_ROOT, ".")

            define_step(
                config_dic=config_dic,
                base_name=base_name,
                image_name=image_name,
                tag="latest",
                path_dockerfile_dir=path_dockerfile_dir,
                path_dockerfm_dir=config.get_dockerfm_dir(),
            )

    define_workflow(config_dic)

    os.makedirs(os.path.dirname(CI_PATH))
    with open(CI_PATH, "w") as f:
        # default_flow_style:出力形式が変わる。5.3からFalseが標準になり、5.3未満と互換性を維持するために指定する。
        yaml.dump(config_dic, f, default_flow_style=False)


def define_step(
    config_dic: OrderedDict,
    base_name: str,
    image_name: str,
    path_dockerfm_dir: str,
    path_dockerfile_dir: str,
    tag: str = "latest",
):

    jobname = "dockerfm-build-" + image_name
    config_dic["jobs"][jobname] = OrderedDict()
    # od['jobs'][jobname]['docker'] = [{'image': CI_IMAGE_CIRCLECI}]
    # od['jobs'][jobname]['machine'] = {'docker_layer_caching': True}
    # od['jobs'][jobname]['machine'] = True
    config_dic["jobs"][jobname]["docker"] = [{"image": "circleci/python:3.6.4"}]
    steps = []
    config_dic["jobs"][jobname]["steps"] = steps
    steps.append("checkout")

    # machineでない場合は、以下のコマンドを実行しないとdockerを利用できない
    if not "machine" in config_dic["jobs"][jobname]:
        steps.append("setup_remote_docker")

    build = f"docker build -t {image_name}:{tag} {path_dockerfile_dir}"
    login = f'echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin'
    push_image = f"docker push {image_name}:{tag}"
    path_pushreadme = os.path.normpath(os.path.join(path_dockerfm_dir, "pushreadme.py"))
    path_pushreadme = os.path.relpath(path_pushreadme)
    push_readme = (
        f"python {path_pushreadme} {image_name} {path_dockerfile_dir}/README.md"
    )
    steps.append({"run": build})
    steps.append({"run": login})
    steps.append({"run": push_image})
    steps.append({"run": push_readme})


def define_workflow(config_dic: OrderedDict):
    config_dic["workflows"] = OrderedDict()
    config_dic["workflows"]["version"] = 2
    config_dic["workflows"]["build_and_test"] = OrderedDict()
    config_dic["workflows"]["build_and_test"]["jobs"] = []

    for jobname in config_dic["jobs"].keys():
        config_dic["workflows"]["build_and_test"]["jobs"].append(jobname)
