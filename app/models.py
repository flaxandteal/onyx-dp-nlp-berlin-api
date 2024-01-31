from dataclasses import dataclass, asdict
from berlin import Location
from typing import Optional

@dataclass
class LocationModel:
    id: str
    key: str
    encoding: str
    words: list[str]
    names: list[str]
    codes: list[str]
    subdiv: Optional[list[str]]
    state: list[str]

    @classmethod
    def from_location(cls, loc: Location, db):
        state_str: str = loc.get_state_code()
        subdiv_str: Optional[str] = loc.get_subdiv_code()
        subdiv: Optional[list[str]]
        if subdiv_str:
            subdiv = [subdiv_str, db.get_subdiv_key(state_str, subdiv_str)]
        else:
            subdiv = None
        state: list[str] = [state_str, db.get_state_key(state_str)]

        return cls(
            key=loc.key,
            encoding=loc.encoding,
            id=loc.id,
            words=loc.words,
            names=loc.get_names(),
            codes=loc.get_codes(),
            subdiv=subdiv,
            state=state
        )

    def to_json(self):
        return asdict(self)
