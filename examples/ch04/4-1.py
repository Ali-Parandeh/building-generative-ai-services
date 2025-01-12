from datetime import datetime


def timestamp_to_isostring(date: int) -> str:
    return datetime.fromtimestamp(date).isoformat()


print(timestamp_to_isostring(1736680773))
# 2025-01-12T11:19:52.876758

print(timestamp_to_isostring("27 Jan 2025 14:48:00"))
# error: Argument 1 to "timestamp_to_isostring" has incompatible type "str";
# expected "int" [arg-type]
