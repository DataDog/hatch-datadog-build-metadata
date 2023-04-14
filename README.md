# hatch-datadog-build-metadata

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/DataDog/hatch-datadog-build-metadata/actions/workflows/test.yml/badge.svg)](https://github.com/DataDog/hatch-datadog-build-metadata/actions/workflows/test.yml) [![CD - Build](https://github.com/DataDog/hatch-datadog-build-metadata/actions/workflows/build.yml/badge.svg)](https://github.com/DataDog/hatch-datadog-build-metadata/actions/workflows/build.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/hatch-datadog-build-metadata.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/hatch-datadog-build-metadata/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-datadog-build-metadata.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/hatch-datadog-build-metadata/) |
| Meta | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/ambv/black) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) |

-----

This provides a plugin for [Hatch](https://github.com/pypa/hatch) that injects metadata from your preferred version control system like Git.

**Table of Contents**

- [Global dependency](#global-dependency)
- [Metadata hook](#metadata-hook)
  - [Metadata hook options](#metadata-hook-options)
    - [URLs](#urls)
  - [Example](#example)
- [License](#license)

## Global dependency

Ensure `hatch-datadog-build-metadata` is defined within the `build-system.requires` field in your `pyproject.toml` file.

```toml
[build-system]
requires = ["hatchling", "hatch-datadog-build-metadata"]
build-backend = "hatchling.build"
```

## Metadata hook

**Note:** only Git is supported

The [metadata hook plugin](https://hatch.pypa.io/latest/plugins/metadata-hook/reference/) name is `datadog-build-metadata`.

- ***pyproject.toml***

    ```toml
    [tool.hatch.metadata.hooks.datadog-build-metadata]
    ```

### Metadata hook options

#### URLs

The `urls` option is equivalent to [`project.urls`](https://hatch.pypa.io/latest/config/metadata/#urls) except that each URL supports [context formatting](https://hatch.pypa.io/latest/config/context/) with the following fields:

- `commit_hash` - the latest commit hash
- `remote_url` - the raw remote URL as stored in VCS config
- `remote_http_url` - the `remote_url` converted to an HTTP(S) URL

Be sure to add `urls` to [`project.dynamic`](https://hatch.pypa.io/latest/config/metadata/#dynamic):

- ***pyproject.toml***

    ```toml
    [project]
    dynamic = [
      "urls",
    ]
    ```

By default, the following URLs are set:

- `source_code_link` -> `{remote_http_url}#{commit_hash}`

### Example

The following example assumes that the code is hosted by GitHub.

- ***pyproject.toml***

    ```toml
    [tool.hatch.metadata.hooks.datadog-build-metadata]
    Homepage = "https://www.example.com"
    source_archive = "{remote_http_url}/archive/{commit_hash}.tar.gz"
    ```

- ***hatch.toml***

    ```toml
    [metadata.hooks.datadog-build-metadata]
    Homepage = "https://www.example.com"
    source_archive = "{remote_http_url}/archive/{commit_hash}.tar.gz"
    ```

## License

`hatch-datadog-build-metadata` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
