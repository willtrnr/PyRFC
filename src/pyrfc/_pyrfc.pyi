# pylint: disable=all

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence, TypedDict

__VERSION__: str

ConnectionParameters = Mapping[str, Any]

class Connection:
    @property
    def version(self) -> Mapping[str, Any]: ...
    @property
    def options(self) -> Mapping[str, Any]: ...
    def __init__(self, config: Mapping[str, Any] = ..., **params: Any) -> None: ...
    def __enter__(self) -> Connection: ...
    def __exit__(self, type, value, traceback) -> None: ...
    def __del__(self) -> None: ...
    def is_open(self) -> bool: ...
    def open(self) -> None: ...
    def reopen(self) -> None: ...
    def close(self) -> None: ...
    def ping(self) -> None: ...
    def reset_server_context(self) -> None: ...
    def get_connection_attributes(self) -> Mapping[str, Any]: ...
    def get_function_description(self, func_name: str) -> FunctionDescription: ...
    def call(
        self, func_name: str, options: Mapping[str, Any] = ..., **params: Any
    ) -> Mapping[str, Any]: ...
    def type_desc_get(self, type_name: str) -> TypeDescription: ...
    def type_desc_remove(self, sysid: str, type_name: str) -> int: ...
    def func_desc_remove(self, sysid: str, func_name: str) -> int: ...
    def free(self) -> None: ...

class TypeField(TypedDict):
    name: str
    field_type: str
    nuc_length: int
    nuc_offset: int
    uc_length: int
    uc_offset: int
    decimals: int
    type_description: Optional[TypeDescription]

class TypeDescription:
    name: str
    nuc_length: int
    uc_length: int
    fields: Sequence[TypeField]
    def __init__(self, name: str, nuc_length: int, uc_length: int) -> None: ...
    def add_field(
        self,
        name: str,
        field_type: str,
        nuc_length: int,
        uc_length: int,
        nuc_offset: int,
        uc_offset: int,
        decimals: int = ...,
        type_description: Optional[TypeDescription] = ...,
    ) -> None: ...

class FunctionParameter(TypedDict):
    name: str
    parameter_type: str
    direction: str
    nuc_length: int
    uc_length: int
    decimals: int
    default_value: str
    parameter_text: str
    optional: bool
    type_description: Optional[TypeDescription]

class FunctionDescription:
    name: str
    parameters: Sequence[FunctionParameter]
    def __init__(self, name: str) -> None: ...
    def add_parameter(
        self,
        name: str,
        parameter_type: str,
        direction: str,
        nuc_length: int,
        uc_length: int,
        decimals: int = ...,
        default_value: str = "",
        parameter_text: str = ...,
        optional: bool = ...,
        type_description: Optional[TypeDescription] = ...,
    ) -> None: ...
