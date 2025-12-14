import json


class ValueWrapper:
    def __init__(self, value):
        self.value = value


def uncapitalize(s: str) -> str:
    return s[:1].lower() + s[1:]


def load_json() -> dict:
    with open("chords.json", "r") as file:
        data = json.load(file)
    return data


def _printable_ascii_only_list(input: list[int]) -> bool:
    for val in input:
        if (val < 32 and val != 0) or val >= 127:
            return False
    return True


# returns none if not printable str
def _to_str(input: list[int]) -> str | None:

    output = ""
    for val in input:
        # charachorder uses zeros for padding
        if val == 0:
            continue

        if val < 32 or val >= 127:
            return None
        output += chr(val)
    return output


def ascii_only(data: dict) -> dict[frozenset[str], str]:
    # format: key combinations are stored as a list of integers, with 0 to fix there length I think atleast for the input part
    # these are stored in a list with two elements the trigger followed by the output
    # these are then all stored in the list of chords
    chords: list[list[list[int]]] = data["chords"]
    out: dict[str, str] = {}
    for pair in chords:
        trig = _to_str(pair[0])
        if not trig:
            continue

        output = _to_str(pair[1])
        if not output:
            continue
        out[frozenset(trig.lower())] = uncapitalize(output)
    return out


def longest_number_of_words(input: list[str]):
    max_length = 0
    for text in input:
        text = text.strip()
        max_length = max(max_length, text.count(' '))
    return max_length
