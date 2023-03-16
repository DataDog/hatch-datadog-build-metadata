# SPDX-FileCopyrightText: 2023-present Datadog, Inc. <dev@datadoghq.com>
#
# SPDX-License-Identifier: MIT
import subprocess
from functools import lru_cache
from urllib.parse import urlsplit


@lru_cache(maxsize=None)
def get_commit_hash(root: str):
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode('utf-8').strip()


@lru_cache(maxsize=None)
def get_remote_url(root: str):
    return subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], cwd=root).decode('utf-8').strip()


def get_http_url(root: str):
    remote_url = get_remote_url(root)

    http_url = parse_http_url(remote_url)
    if http_url.endswith('.git'):
        http_url = http_url[:-4]

    return http_url


def parse_http_url(http_url: str) -> str:
    url = urlsplit(http_url)

    if not (url.scheme or url.netloc):
        # git@foo.bar.baz/path/repo.git
        if '@' in url.path:
            _, _, path = url.path.partition('@')
            return parse_http_url(path)
        # foo.bar.baz/path/repo.git
        else:
            return f'https://{url.path}'
    elif url.scheme and not url.netloc:
        # foo.bar.baz:6789:path/repo.git
        if ':' in url.path:
            port, _, path = url.path.partition(':')
            return f'https://{url.scheme}:{port}/{path}'
        # foo.bar.baz:path/repo.git
        else:
            return f'https://{url.scheme}/{url.path}'
    else:
        scheme = url.scheme
        if not scheme.startswith('http'):
            scheme = 'https'

        netloc = url.netloc
        path = url.path

        # git+ssh://git@foo.bar.baz/path/repo.git
        if '@' in netloc:
            _, _, netloc = netloc.partition('@')
            return parse_http_url(f'{scheme}://{netloc}{path}')

        netloc, *extra_parts = netloc.split(':')
        # git+ssh://git@foo.bar.baz:path/repo.git
        if extra_parts:
            if extra_parts[0].isdigit():
                netloc = f'{netloc}:{extra_parts.pop(0)}'

            if extra_parts:
                path = f'/{"/".join(extra_parts)}{path}'

        return f'{scheme}://{netloc}{path}'
