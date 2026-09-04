"""기관 manifest를 GUI에서 사용할 탭 모델로 변환한다."""

from __future__ import annotations

from dataclasses import dataclass

from .registry import 기관등록부


@dataclass(frozen=True)
class 기관기능:
    id: str
    name: str
    handler: str
    legacy_method: str | None
    parameters: tuple[str, ...]
    ui_ready: bool
    status: str


@dataclass(frozen=True)
class 기관탭:
    id: str
    name: str
    functions: tuple[기관기능, ...]


def 기관탭목록(등록부: 기관등록부) -> tuple[기관탭, ...]:
    결과 = []
    for 기관 in 등록부.전체기관().values():
        기능 = tuple(
            기관기능(
                id=항목["id"],
                name=항목["name"],
                handler=항목["handler"],
                legacy_method=항목.get("legacy_method"),
                parameters=tuple(항목.get("parameters", ())),
                ui_ready=항목.get("ui_ready", True),
                status=항목.get("status", "source"),
            )
            for 항목 in 기관.functions
        )
        결과.append(기관탭(id=기관.id, name=기관.name, functions=기능))
    return tuple(결과)
