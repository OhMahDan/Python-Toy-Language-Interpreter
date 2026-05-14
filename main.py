from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_interpreter(text):
	lexer = Lexer(text)
	parser = Parser(lexer)
	interpreter = Interpreter(parser)

	try:
		interpreter.interpret()
	except Exception as e:
		print(e)

if __name__ == '__main__':
	text = """
	let x = 1;
	y = 2;
	z = ---(x+y)*(x+-y);
	"""
	run_interpreter(text)
	



