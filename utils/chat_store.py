# Shared module-level message store.
# Lives here so both pages/3_Chat.py and utils/auth.py can reach it
# without circular imports.
_MSG_STORE: dict = {}


def clear_user(user_id: str) -> None:
    _MSG_STORE.pop(user_id, None)
