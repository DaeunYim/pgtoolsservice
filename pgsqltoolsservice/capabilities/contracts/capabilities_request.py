# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from typing import List

from pgsqltoolsservice.hosting import IncomingMessageConfiguration
import pgsqltoolsservice.utils as utils


class CapabilitiesRequestParams:
    @classmethod
    def from_dict(cls, dictionary: dict):
        return utils.deserialize_from_dict(cls, dictionary)

    def __init__(self):
        self.host_name = None
        self.host_version = None


class CategoryValue(object):
    """Defines a category value for a connection option"""

    def __init__(self, display_name: str = None, name: str = None):
        self.display_name: str = display_name
        self.name: str = name


class ConnectionOption(object):
    """Defines a connection provider option"""

    VALUE_TYPE_STRING = 'string'
    VALUE_TYPE_MULTI_STRING = 'multistring'
    VALUE_TYPE_PASSWORD = 'password'
    VALUE_TYPE_NUMBER = 'number'
    VALUE_TYPE_CATEGORY = 'category'
    VALUE_TYPE_BOOLEAN = 'boolean'

    SPECIAL_VALUE_SERVER_NAME = 'serverName'
    SPECIAL_VALUE_DATABASE_NAME = 'databaseName'
    SPECIAL_VALUE_AUTH_TYPE = 'authType'
    SPECIAL_VALUE_USER_NAME = 'userName'
    SPECIAL_VALUE_PASSWORD_NAME = 'password'
    SPECIAL_VALUE_APP_NAME = 'appName'

    def __init__(
            self,
            name: str = None,
            display_name: str = None,
            description: str = None,
            group_name: str = None,
            value_type: str = None,
            default_value: str = None,
            category_values: List[CategoryValue] = None,
            special_value_type: str = None,
            is_identity: bool = False,
            is_required: bool = False):
        self.name: str = name
        self.display_name: str = display_name
        self.description: str = description
        self.group_name: str = group_name
        self.value_type: str = value_type
        self.default_value: str = default_value
        self.category_values: List[CategoryValue] = category_values
        self.special_value_type: str = special_value_type
        self.is_identity: bool = is_identity
        self.is_required: bool = is_required


class ConnectionProviderOptions:
    """Defines the connection provider options that the DMP server implements"""

    def __init__(self, options):
        self.options: List[ConnectionOption] = options or None


class DMPServerCapabilities:
    """Defines the DMP server capabilities"""

    def __init__(self):
        self.protocol_version: str = None
        self.provider_name: str = None
        self.provider_display_name: str = None
        self.connection_provider: ConnectionProviderOptions = None


class CapabilitiesResult(object):
    """Defines the capabilities result contract"""

    def __init__(self):
        self.capabilities: DMPServerCapabilities


CAPABILITIES_REQUEST = IncomingMessageConfiguration('capabilities/list', CapabilitiesRequestParams)
