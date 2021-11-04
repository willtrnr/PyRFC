# pylint: disable=all

from __future__ import annotations

from . import _pyrfc as pyrfc
from ._exception import (
    ABAPApplicationError as ABAPApplicationError,
    ABAPRuntimeError as ABAPRuntimeError,
    CommunicationError as CommunicationError,
    ExternalApplicationError as ExternalApplicationError,
    ExternalAuthorizationError as ExternalAuthorizationError,
    ExternalRuntimeError as ExternalRuntimeError,
    LogonError as LogonError,
    RFCError as RFCError,
    RFCLibError as RFCLibError,
)
from ._pyrfc import (
    __VERSION__ as __VERSION__,
    Connection as Connection,
    ConnectionParameters as ConnectionParameters,
    FunctionDescription as FunctionDescription,
    TypeDescription as TypeDescription,
)
