class RegisterMachineInterpreter:
    registers = {}

    def set(self, registers):
        r1, r2 = registers.split(' ')
        if r2.isnumeric():
            data = int(r2)
        else:
            data = int(self.registers[r2], 2)
        self.registers[r1] = ''
        for i in range(8):
            self.registers[r1] = str(data % 2) + self.registers[r1]
            data = data >> 1
        print(self.registers[r1])

    def execute(self, command: str):
        operator = command[0]
        if command[0] == '&':
            self.set(command[2:])

    def interpret(self, code):
        keep_going = True
        command = 0
        while keep_going:
            self.execute(code[command])
