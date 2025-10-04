from src.enums import condition


def encode(data: list[list[condition]]) -> list[list[int]]:
    return [[elem.value for elem in row] for row in data]
