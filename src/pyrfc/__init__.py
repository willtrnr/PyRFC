# SPDX-FileCopyrightText: 2013 SAP SE Srdjan Boskovic <srdjan.boskovic@sap.com>
#
# SPDX-License-Identifier: Apache-2.0

# import from internal modules that they could be directly imported from
# the pyrfc package

# Set DLL path, due to https://docs.python.org/3.8/whatsnew/3.8.html#bpo-36085-whatsnew
import os

if os.name == "nt":
    try:
        os.add_dll_directory(os.path.join(os.environ["SAPNWRFC_HOME"], "lib"))
    except Exception:
        pass

from ._exception import (
    ABAPApplicationError,
    ABAPRuntimeError,
    CommunicationError,
    ExternalApplicationError,
    ExternalAuthorizationError,
    ExternalRuntimeError,
    LogonError,
    RFCError,
    RFCLibError,
)
from .pyrfc import (
    __VERSION__,
    Connection,
    ConnectionParameters,
    FunctionDescription,
    Server,
    Throughput,
    TypeDescription,
    get_nwrfclib_version,
)

__author__ = """"Srdjan Boskovic"""
__email__ = "srdjan.boskovic@sap.com"
__version__ = __VERSION__
