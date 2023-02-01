class RegisterMachineInterpreter:
    registers: dict[str: str] = {}

    def execute(self, command: str):
        pass

    def interpret(self, code):
        keep_going: bool = True
        command: int = 0
        while keep_going:
            self.execute(list[command])
