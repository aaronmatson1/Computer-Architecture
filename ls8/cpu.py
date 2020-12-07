"""CPU functionality."""

import sys
import os.path

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110 

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

         # Setup Branch Table
        self.branchtable = {}
        self.branchtable[HLT] = self.execute_HLT
        self.branchtable[LDI] = self.execute_LDI
        self.branchtable[PRN] = self.execute_PRN
        self.branchtable[MUL] = self.execute_MUL
        self.branchtable[PUSH] = self.execute_PUSH
        self.branchtable[POP] = self.execute_POP

        # Property wrapper for stack pointers
        @property
        def sp(self):
            return self.reg[7]

        @sp.setter
        def sp(self, a):
            self.reg[7] = a & 0xFF

        def instruction_size(self):
            return ((self.ir >> 6) & 0b11) + 1

        def instruction_sets_pc(self):
            return ((self.ir >> 4) & 0b0001) == 1


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
    

    def load(self, file_name):
        """Load a program into memory."""

        address = 0


        file_path = os.path.join(os.path.dirname(__file__), file_name)
        try:
            with open(file_path) as f:
                for line in f:
                    num = line.split("#")[0].strip() #10000010
                    try:
                        instruction = int(num, 2)
                        self.ram[address] = instructionaddress += 1
                        address += 1
                    except:
                        continue

        except:
            print(f'Could not find file named: {file_name}')
            sys.exit(1)


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

        #Run loop

    def run(self):
        """Run the CPU."""
        # running = True

        # while running:
        #     #fetch the next instruction

        while not self.halted:
            self.ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if not self.instruction_sets_pc():
                self.pc += self.instruction_size()

            self.execute_instruction(operand_a, operand_b)

        def execute_instruction(self, operand_a, operand_b):
            if self.ir in self.branchtable:
                self.branchtable[self.ir](operand_a, operand_b)
            else:
            print(f"Error: Could not execute intsruction: {self.ir}")
            sys.exit(1)

            #Define operations to be loaded in the branch table

            def execute_HLT(self.operand_a, operand_b):
                self.reg[operand_a] = operand_b

            def execute_PRN(self, operand_a, operand_b):
                print(self.reg[operand_a])

            def execute_MUL(self, operand_a, operand_b):
                self.reg[operand_a] *= self.reg[operand_b]

            def execute_PUSH(self, operand_a, operand_b):
                self.sp -= 1
                value_in_register = self.reg[operand_a]
                self.ram[self.sp] = value_in_register

            def execute_POP(self, operand_a, operand_b):
                top_most_value_in_stack = self.ram[self.sp]
                self.reg[operand_a] = top_most_value_in_stack
                self.sp += 1

