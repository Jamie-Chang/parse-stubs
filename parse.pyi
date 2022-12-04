from datetime import tzinfo
from typing import Any, Callable, Generic, Iterator, Literal
from typing import Match as _Match
from typing import TypeAlias, TypeVar, overload

TypeCoverter: TypeAlias = Callable[[str], Any]
ExtraTypes: TypeAlias = dict[str, TypeCoverter]

class TooManyFields(ValueError): ...
class RepeatedNameError(ValueError): ...

class FixedTzOffset(tzinfo):
    def __init__(self, offset, name): ...

class Parser:
    def __init__(
        self,
        format: str,
        extra_types: ExtraTypes | None = None,
        case_sensitive: bool = False,
    ): ...
    named_fields: list[str]
    fixed_fields: list[str]
    def evaluate_result(self, m: _Match) -> Result: ...
    @overload
    def parse(
        self, string: str, evaluate_result: Literal[True] = True
    ) -> "Result" | None: ...
    @overload
    def parse(self, string: str, evaluate_result: Literal[False]) -> "Match" | None: ...
    @overload
    def search(
        self, string: str, pos: int, endpos: int | None, evaluate_result: Literal[False]
    ) -> "Match" | None: ...
    @overload
    def search(
        self,
        string: str,
        pos: int = 0,
        endpos: int | None = None,
        *,
        evaluate_result: Literal[False],
    ) -> "Match" | None: ...
    @overload
    def search(
        self,
        string: str,
        pos: int = 0,
        endpos: int | None = None,
        evaluate_result: Literal[True] = True,
    ) -> "Result" | None: ...
    @overload
    def findall(
        self,
        string: str,
        pos: int = 0,
        endpos: int | None = None,
        extra_types: ExtraTypes | None = None,
    ) -> "ResultIterator[Result]": ...
    @overload
    def findall(
        self,
        string: str,
        pos: int = 0,
        endpos: int | None = None,
        extra_types: ExtraTypes | None = None,
        evaluate_result: Literal[True] = True,
    ) -> "ResultIterator[Result]": ...
    @overload
    def findall(
        self,
        string: str,
        pos: int = 0,
        endpos: int | None = None,
        extra_types: ExtraTypes | None = None,
        *,
        evaluate_result: Literal[False],
    ) -> "ResultIterator[Match]": ...
    @overload
    def findall(
        self,
        string: str,
        pos: int,
        endpos: int | None,
        extra_types: ExtraTypes | None,
        evaluate_result: Literal[False],
    ) -> "ResultIterator[Result]": ...

class Result:
    fixed: tuple
    named: dict[str, Any]
    spans: dict[str, tuple[int, int]]
    def __init__(
        self,
        fixed: tuple,
        named: dict[str, Any],
        spans: dict[str, tuple[int, int]] | None,
    ) -> None: ...
    def __getitem__(self, item: str | int | slice) -> Any: ...
    def __contains__(self, name: str) -> bool: ...

class Match:
    parser: Parser
    match: _Match
    def __init__(self, parser: Parser, match: _Match): ...
    def evaluate_result(self) -> Result: ...

T = TypeVar("T", Result, Match)

class ResultIterator(Generic[T]):
    def __next__(self) -> T: ...
    def __iter__(self) -> Iterator[T]: ...

# @overload
# def parse(
#     format: str, string: str, *, case_sensitive: bool = False
# ) -> "Result" | None: ...
@overload
def parse(
    format: str,
    string: str,
    extra_types: ExtraTypes | None = None,
    evaluate_result: Literal[True] = True,
    case_sensitive: bool = False,
) -> "Result" | None: ...
@overload
def parse(
    format: str,
    string: str,
    extra_types: ExtraTypes | None,
    evaluate_result: Literal[False],
    case_sensitive: bool = False,
) -> "Match" | None: ...
@overload
def parse(
    format: str,
    string: str,
    extra_types: ExtraTypes | None = None,
    *,
    evaluate_result: Literal[False],
    case_sensitive: bool = False,
) -> "Match" | None: ...
@overload
def search(
    format: str,
    string: str,
    pos: int,
    endpos: int | None,
    extra_types: ExtraTypes | None,
    evaluate_result: Literal[False],
    case_sensitive: bool = False,
) -> "Match" | None: ...
@overload
def search(
    format: str,
    string: str,
    pos: int = 0,
    endpos: int | None = None,
    extra_types: ExtraTypes | None = None,
    *,
    evaluate_result: Literal[False],
    case_sensitive: bool = False,
) -> "Match" | None: ...
@overload
def search(
    format: str,
    string: str,
    pos: int = 0,
    endpos: int | None = None,
    extra_types: ExtraTypes | None = None,
    evaluate_result: Literal[True] = True,
    case_sensitive: bool = False,
) -> "Result" | None: ...
@overload
def findall(
    format: str,
    string: str,
    pos: int = 0,
    endpos: int | None = None,
    extra_types: ExtraTypes | None = None,
    *,
    case_sensitive: bool = False,
) -> "ResultIterator[Result]": ...
@overload
def findall(
    format: str,
    string: str,
    pos: int = 0,
    endpos: int | None = None,
    extra_types: ExtraTypes | None = None,
    evaluate_result: Literal[True] = True,
    case_sensitive: bool = False,
) -> "ResultIterator[Result]": ...
@overload
def findall(
    format: str,
    string: str,
    pos: int = 0,
    endpos: int | None = None,
    extra_types: ExtraTypes | None = None,
    *,
    evaluate_result: Literal[False],
    case_sensitive: bool = False,
) -> "ResultIterator[Match]": ...
@overload
def findall(
    format: str,
    string: str,
    pos: int,
    endpos: int | None,
    extra_types: ExtraTypes | None,
    evaluate_result: Literal[False],
    case_sensitive: bool = False,
) -> "ResultIterator[Match]": ...
def compile(
    format: str,
    extra_types: ExtraTypes | None = None,
    case_sensitive: bool = False,
) -> Parser: ...

T_CALLABLE = TypeVar("T_CALLABLE", bound=Callable)

def with_pattern(
    pattern: str, regex_group_count: int | None = None
) -> Callable[[T_CALLABLE], T_CALLABLE]: ...
def extract_format(format: str, extra_types: ExtraTypes) -> dict[str, Any]: ...
