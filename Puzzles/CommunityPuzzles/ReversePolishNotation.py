import sys

n = int(input())
stack = []


def pop_two():
    right = stack.pop()
    left = stack.pop()
    return left, right


for instruction in input().split():
    try:
        if instruction == "ADD":
            stack.append(sum(pop_two()))
        elif instruction == "SUB":
            left, right = pop_two()
            stack.append(left - right)
        elif instruction == "MUL":
            left, right = pop_two()
            stack.append(left * right)
        elif instruction == "DIV":
            left, right = pop_two()
            stack.append(left // right)
        elif instruction == "MOD":
            left, right = pop_two()
            stack.append(left % right)
        elif instruction == "POP":
            stack.pop()
        elif instruction == "DUP":
            stack.append(stack[-1])
        elif instruction == "SWP":
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif instruction == "ROL":
            stack.pop()
            stack[-3], stack[-2], stack[-1] = stack[-2], stack[-1], stack[-3]
        else:
            stack.append(int(instruction))
    except Exception:
        stack.append("ERROR")
        break
print(" ".join(map(str, stack)))