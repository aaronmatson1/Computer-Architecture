"""CPU functionality."""

import sys
import os.path

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #256-byte RAM. Each element is 1 byte and can only store intergers 0-255

        #RO-R7: 8-bit general purpose registers, R5 = interrupt mask (IM),
        # R6 = interrupt status (IS), R7 = stack pointer (SP)
        self.reg = [0]*8

        #internal Registers
        self.pc = 0 #Program Counter. Address of the currently executing instruction
        self.ir = 0 #Instruction Register: COntains a copy of the currently executing instruction
        self.mar = 0 # Memoray Address Register: Holds the memory address we're reading or writing
        self.mdr = 0 #Memory Data Register: hold the value to write or the value to just read
        self.fl = 0 # Flag Register: Holds the current flags status
        self.halted = False

        # Initialize the Stack Pointer
        # SP points at the value at the op of the stack (most recently pushed), or at address F4 if the stack is empty
        self.reg[7] = 0xF4 # 244 # int('F4', 16)

        # Property wrapper for stack pointers
        @property
        def sp(self):
            return self.reg[7]

        @sp.setter
        def sp(self, a):
            self.reg[7] = a & 0xFF


    def ram_read(self, mar):
        if mar >= 0 and mar < len(self.ram):
            return self.ram[mar]
        else:
            print(f"Error: Attempted to read from memory address: {mar}, which is outside of the memory bounds.")
            return -1

    def ram_write(self, mar, mdr):
        if mar >= 0 and mar < len(self.ram):
            self.ram[mar] = mdr & 0xFF
        else:
            print(f"Error: Attempted to write to memory address: {mar}, which is outside of the memory bounds.")
    

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # running = True

        # while running:
        #     #fetch the next instruction

        while not self.halted:
            self.ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # #Now, decode the instruction
            # binary_ir = bin(self.ir)[2:].zfill(8)
            # operand_count = int(binary_ir[2],2)
            # is_ALU_operation = binary_ir[2] =='1'
            # instruction_does_set_pc = binary_ir[3] == '1'
            # instruction_id = int(binary_ir[4:], 2)

            # #Increment the program counter
            # self.pc += (1+ operand_count)

            # #execute instruction
            # if self.ir == int('0000001', 2): #HLT
            #     running = False
            # elif self.ir == int('1000010', 2): #LDI
            #     self.reg[operand_a] = operand_b
            # elif self.ir == int('01000111',2): #PRN
            #     print(self.reg[operand_a))
            # else:
            #     print(f'Error: Could not execute instruction: {bin(self.ir)[2:].zfill(8)}')
            #     sys.exit(1)
            self.execute_instruction(operand_a, operand_b)

        def execute_instruction(self, operand_a, operand_b):
            if self.ir == HLT:
                self.halted = True
                self.pc += 1

            elif self.ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 2

            elif self.ir == PRN:
                print(self.eg[operand_a])
                self.pc += 2

            elif self.ir == MUL:
                self.reg[operand_a] *- self.reg[operand_b]
                self.pc += 3

            else:
                print(f'Error: Could not execute instruction: {bin(self.ir)[2:].zfill(8)}')
                sys.exit(1)

