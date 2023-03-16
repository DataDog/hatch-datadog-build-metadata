# SPDX-FileCopyrightText: 2023-present Datadog, Inc. <dev@datadoghq.com>
#
# SPDX-License-Identifier: MIT
from hatchling.plugin import hookimpl

from hatch_datadog_build_metadata.metadata_hook import DatadogBuildMetadataHook


@hookimpl
def hatch_register_metadata_hook():
    return DatadogBuildMetadataHook
