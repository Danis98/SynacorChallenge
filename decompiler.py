import sys

OP_HALT = 0
OP_SET = 1
OP_PUSH = 2
OP_POP = 3
OP_EQ = 4
OP_GT = 5
OP_JMP = 6
OP_JT = 7
OP_JF = 8
OP_ADD = 9
OP_MULT = 10
OP_MOD = 11
OP_AND = 12
OP_OR = 13
OP_NOT = 14
OP_RMEM = 15
OP_WMEM = 16
OP_CALL = 17
OP_RET = 18
OP_OUT = 19
OP_IN = 20
OP_NOP = 21

op_memo = {
    OP_HALT: "halt",
    OP_SET: "set",
    OP_PUSH: "push",
    OP_POP: "pop",
    OP_EQ: "eq",
    OP_GT: "gt",
    OP_JMP: "jmp",
    OP_JT: "jt",
    OP_JF: "jf",
    OP_ADD: "add",
    OP_MULT: "mult",
    OP_MOD: "mod",
    OP_AND: "and",
    OP_OR: "or",
    OP_NOT: "not",
    OP_RMEM: "rmem",
    OP_WMEM: "wmem",
    OP_CALL: "call",
    OP_RET: "ret",
    OP_OUT: "out",
    OP_IN: "in",
    OP_NOP: "nop"
}

# Load program
program_hex = map(ord, open('challenge.bin').read())
mem = [0 for i in xrange(0, len(program_hex)/2)]
for i in xrange(0, len(program_hex), 2):
    mem[i/2] = program_hex[i] | program_hex[i+1]<<8

for op in op_memo:
    print "0x%02x  %s" % (op, op_memo[op])
print "------------"

out_file = open('challenge.sasm', 'w')

def get_memo(num):
    if num < 2**15:
        return "0x%04x" % num
    elif num - 2**15 <8:
        return "reg%d" % (num-2**15+1)
    else:
        # print "INVALID NUMBER %d" % num
        quit()

def get_ascii(num):
    if num < 256:
        if num == ord('\n'):
            return '\\n'
        elif num == ord('\t'):
            return '\\t'
        return "%c" % chr(num)
    elif num < 2**15:
        return "0x%04x" % num
    elif num - 2**15 <8:
        return "reg%d" % (num-2**15+1)
    else:
        # print "INVALID NUMBER %d" % num
        quit()

# Decompile instructions
instr_ptr = 0
while instr_ptr >= 0 and instr_ptr < len(mem):
    op = mem[instr_ptr]
    if op == OP_HALT:
        out_file.write("0x%04x: %s\n" % (instr_ptr, op_memo[op]))
        # print "0x%04x: %s\n" % (instr_ptr, op_memo[op])
        instr_ptr += 1
    elif op == OP_SET:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        out_file.write("0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b))
        # print "0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b)
        instr_ptr += 3
    elif op == OP_PUSH:
        a = get_memo(mem[instr_ptr+1])
        out_file.write("0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a))
        # print "0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a)
        instr_ptr += 2
    elif op == OP_POP:
        a = get_memo(mem[instr_ptr+1])
        out_file.write("0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a))
        # print "0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a)
        instr_ptr += 2
    elif op == OP_EQ:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        c = get_memo(mem[instr_ptr+3])
        out_file.write("0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c))
        # print "0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c)
        instr_ptr += 4
    elif op == OP_GT:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        c = get_memo(mem[instr_ptr+3])
        out_file.write("0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c))
        # print "0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c)
        instr_ptr += 4
    elif op == OP_JMP:
        a = get_memo(mem[instr_ptr+1])
        out_file.write("0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a))
        # print "0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a)
        instr_ptr += 2
    elif op == OP_JT:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        out_file.write("0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b))
        # print "0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b)
        instr_ptr += 3
    elif op == OP_JF:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        out_file.write("0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b))
        # print "0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b)
        instr_ptr += 3
    elif op == OP_ADD:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        c = get_memo(mem[instr_ptr+3])
        out_file.write("0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c))
        # print "0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c)
        instr_ptr += 4
    elif op == OP_MULT:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        c = get_memo(mem[instr_ptr+3])
        out_file.write("0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c))
        # print "0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c)
        instr_ptr += 4
    elif op == OP_MOD:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        c = get_memo(mem[instr_ptr+3])
        out_file.write("0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c))
        # print "0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c)
        instr_ptr += 4
    elif op == OP_AND:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        c = get_memo(mem[instr_ptr+3])
        out_file.write("0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c))
        # print "0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c)
        instr_ptr += 4
    elif op == OP_OR:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        c = get_memo(mem[instr_ptr+3])
        out_file.write("0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c))
        # print "0x%04x: %s %s %s %s\n" % (instr_ptr, op_memo[op], a, b, c)
        instr_ptr += 4
    elif op == OP_NOT:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        out_file.write("0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b))
        # print "0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b)
        instr_ptr += 3
    elif op == OP_RMEM:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        out_file.write("0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b))
        # print "0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b)
        instr_ptr += 3
    elif op == OP_WMEM:
        a = get_memo(mem[instr_ptr+1])
        b = get_memo(mem[instr_ptr+2])
        out_file.write("0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b))
        # print "0x%04x: %s %s %s\n" % (instr_ptr, op_memo[op], a, b)
        instr_ptr += 3
    elif op == OP_CALL:
        a = get_memo(mem[instr_ptr+1])
        out_file.write("0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a))
        # print "0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a)
        instr_ptr += 2
    elif op == OP_RET:
        out_file.write("0x%04x: %s\n" % (instr_ptr, op_memo[op]))
        # print "0x%04x: %s\n" % (instr_ptr, op_memo[op])
        instr_ptr += 1
    elif op == OP_OUT:
        a = get_ascii(mem[instr_ptr+1])
        out_file.write("0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a))
        # print "0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a)
        instr_ptr += 2
    elif op == OP_IN:
        a = get_memo(mem[instr_ptr+1])
        out_file.write("0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a))
        # print "0x%04x: %s %s\n" % (instr_ptr, op_memo[op], a)
        instr_ptr += 2
    elif op == OP_NOP:
        out_file.write("0x%04x: %s\n" % (instr_ptr, op_memo[op]))
        # print "0x%04x: %s\n" % (instr_ptr, op_memo[op])
        instr_ptr += 1
    else:
        out_file.write("0x%04x: db 0x%04x\n" % (instr_ptr, mem[instr_ptr]))
        # print "0x%04x: db 0x%04x\n" % (instr_ptr, mem[instr_ptr])
        instr_ptr += 1
# print "Decompiled successfully"
