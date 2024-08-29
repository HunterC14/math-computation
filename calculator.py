#!/usr/bin/env python3
def simplify(number: int | float):
	if int(number) == number:
		number = int(number)
	return number

def convert_string_into_tokens(string: str):
	tokens = []
	for index in range(0,len(string)):
		tokens.append(string[index])
	new_tokens = []
	for index in range(0,len(tokens)):
		if tokens[index] in ["0","1","2","3","4","5","6","7","8","9"]:
			if len(new_tokens) == 0 or type(new_tokens[-1]) is not int:
				new_tokens.append(int(tokens[index]))
			else:
				new_tokens[-1] = new_tokens[-1] * 10
				new_tokens[-1] = new_tokens[-1] + int(tokens[index])
		else:
			new_tokens.append(tokens[index])
	return new_tokens

def calculate_tokens(tokens: list[str]):
	answer = tokens[0]
	for index in range(1,len(tokens),2):
		operation = tokens[index]
		operand = tokens[index+1]
		if operation == "+":
			answer = answer + operand
		elif operation == "-":
			answer = answer - operand
		elif operation in ("x", "*"):
			answer = answer * operand
		elif operation in ("÷", "/"):
			answer = answer / operand
		elif operation == "^":
			answer = answer ** operand
		elif operation == "%":
			answer = answer % operand
		else:
			raise SystemExit("Unknown operation.")
	return simplify(answer)

def calculate_expression(expression: str):
	return calculate_tokens(convert_string_into_tokens(expression))

def run_calculator():
	print("Allowed operations: +, -, x, ÷ (or /), ^, % (modulo).\nThis calculator does not do order of operations.")
	to_calculate = input("Type an expression to calculate. Expression: ")
	answer = calculate_expression(to_calculate)
	print(f"Answer: {answer}")

if __name__ == "__main__":
	run_calculator()