# 本パッケージについて
pypiへpythonパッケージを公開するためのサンプルプロジェクトです。
以下の手順に従い、パッケージを公開することができます。

また、将来的にpoetry-dynamic-versioningが提供する機能（gitのtagを利用した動的なバージョン発行）が、
poetryに取り込まれた場合、poetry-dynamic-versioningは不要となります。


# 前提環境
- [x] pip
- [x] setuptools
- [x] poetry
- [x] poetry-dynamic-versioning

# 公開までの手順

## プロジェクトフォルダ作成
``` shell
# test用pypiの登録
poetry config repositories.testpypi https://test.pypi.org/legacy/

# プロジェクトフォルダ作成
poetry new sample_project
```

## pyproject.tomlの編集
pyproject.tomlに以下を追加する。

``` toml
[tool.poetry-dynamic-versioning]
enable = true
style = "pep440"
```


## パッケージのテスト
``` shell
pytest -v --cov
```

## pypIへパッケージをアップロード

``` shell
# 現在のコミットにタグを付与する(pypiへは重複したバージョンはpushできない)
git tag -a v0.0.0

# test用pypiへパッケージをアップロード
poetry publish --build -u $PYPI_USER -p $PYPI_PASSWORD -r testpypi

```


