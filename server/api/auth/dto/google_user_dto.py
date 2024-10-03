from typing import TypedDict


class GoogleUserDTO(TypedDict):
    id: str
    email: str
    verified_email: bool
    name: str
    given_name: str
    family_name: str
    picture: str
