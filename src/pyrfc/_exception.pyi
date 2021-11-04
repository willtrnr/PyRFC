# pylint: disable=all

from __future__ import annotations

class RFCError(Exception):
    """Exception base class

    Indicates that there was an error in the Python connector.
    """

    ...

class RFCLibError(RFCError):
    """RFC library error

    Base class for exceptions raised by the local underlying C connector (sapnwrfc.c).
    """

    code2txt = ...
    def __init__(
        self,
        message=...,
        code=...,
        key=...,
        msg_class=...,
        msg_type=...,
        msg_number=...,
        msg_v1=...,
        msg_v2=...,
        msg_v3=...,
        msg_v4=...,
    ) -> None: ...
    def __str__(self) -> str: ...

class ABAPApplicationError(RFCLibError):
    """ABAP application error

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    ABAP_APPLICATION_FAILURE.
    """

    ...

class ABAPRuntimeError(RFCLibError):
    """ABAP runtime error

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    ABAP_RUNTIME_FAILURE.
    """

    ...

class LogonError(RFCLibError):
    """Logon error

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    LOGON_FAILURE.
    """

    def __init__(
        self,
        message=...,
        code=...,
        key=...,
        msg_class=...,
        msg_type=...,
        msg_number=...,
        msg_v1=...,
        msg_v2=...,
        msg_v3=...,
        msg_v4=...,
    ) -> None: ...

class CommunicationError(RFCLibError):
    """Communication error

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    COMMUNICATION_FAILURE.
    """

    ...

class ExternalRuntimeError(RFCLibError):
    """External runtime error

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    EXTERNAL_RUNTIME_FAILURE.
    """

    ...

class ExternalApplicationError(RFCLibError):
    """External application error

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    EXTERNAL_APPLICATION_FAILURE.
    """

    ...

class ExternalAuthorizationError(RFCLibError):
    """External authorization error

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    EXTERNAL_AUTHORIZATION_FAILURE.
    """

    ...

class RFCTypeError(RFCLibError):
    """Type concersion error

    This exception is raised when invalid data type detected in RFC input (fill) conversion
    and the error object has an RFC_ERROR_GROUP value of
    RFC_TYPE_ERROR
    """

    ...
