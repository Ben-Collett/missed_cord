class MyKeyEvent:
    def __init__(self, name: str, value: str):
        self.name: str = name
        self.value: int = int(value)


class TerminateEvent():
    pass


TERMINATE_EVENT = TerminateEvent()
