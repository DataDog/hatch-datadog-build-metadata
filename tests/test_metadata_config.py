# SPDX-FileCopyrightText: 2023-present Datadog, Inc. <dev@datadoghq.com>
#
# SPDX-License-Identifier: MIT
import pytest

from hatch_datadog_build_metadata.metadata_hook import DatadogBuildMetadataHook


class TestURLs:
    def test_correct(self, new_project_basic):
        config = {'urls': {'foo': 'url'}}
        metadata_hook = DatadogBuildMetadataHook(new_project_basic, config)

        assert metadata_hook.config_urls == metadata_hook.config_urls == {'foo': 'url'}

    def test_not_table(self, new_project_basic):
        config = {'urls': 9000}
        metadata_hook = DatadogBuildMetadataHook(new_project_basic, config)

        with pytest.raises(TypeError, match='option `urls` must be a table'):
            _ = metadata_hook.config_urls

    def test_url_not_string(self, new_project_basic):
        config = {'urls': {'foo': 9000}}
        metadata_hook = DatadogBuildMetadataHook(new_project_basic, config)

        with pytest.raises(TypeError, match='URL `foo` in option `urls` must be a string'):
            _ = metadata_hook.config_urls
