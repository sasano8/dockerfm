# coding:utf-8

import logging
import os
import sys
import json
import urllib.request
import urllib.error
import urllib.parse

log = logging.getLogger()
log.setLevel(logging.INFO)
sh = logging.StreamHandler()
log.addHandler(sh)


def login(username, password):
    data = {"username": username, "password": password}

    data = json.dumps(data).encode()

    req = urllib.request.Request(
        url="https://hub.docker.com/v2/users/login/",
        method="POST",
        data=data,
        headers={"Content-Type": "application/json"},
    )

    response = None

    try:
        req = urllib.request.urlopen(req)
        response = json.load(req)
        req.close()

    except Exception as e:
        raise

    return response


# def push_readme(username, password, repository, token, readme_local_path):
def push_readme(token, readme_text, imagename):
    # type hintを設けるとpythonのバージョンに
    # TODO: quay.io  Harbor2
    data = {"full_description": readme_text}

    databyte = json.dumps(data).encode()

    url = "https://hub.docker.com/v2/repositories/{}/".format(imagename)
    req = urllib.request.Request(url=url, method="PATCH",)

    req.add_header("Authorization", "JWT " + token)
    req.add_header("Content-Type", "application/json")
    req.add_header("Content-Length", len(databyte))

    response = None

    log.info("request: {}".format(url))
    try:
        req = urllib.request.urlopen(req, databyte)
        response = json.load(req)
        req.close()

    except Exception as e:
        raise

    return response


# __name__ == "__main"
if __name__ == "__main__":
    username = os.environ["DOCKERHUB_USERNAME"]
    password = os.environ["DOCKERHUB_PASS"]

    imagename = sys.argv[1]
    path_readme = sys.argv[2]

    log.info("try to login to dockerhub.")
    try:
        response = login(username, password)
    except urllib.error.HTTPError as e:
        log.critical(e.reason)
        log.critical(str(e))
        raise

    token = response["token"]

    readme_text = None

    log.info("try to open specified readme file.")
    f = open(path_readme, "r")
    readme_text = f.read()
    f.close()

    log.debug("request http patach update readme")
    try:
        response = push_readme(token, readme_text, imagename)
    except urllib.error.HTTPError as e:
        log.critical(e.reason)
        log.critical(str(e))
        raise

    log.info(response)
