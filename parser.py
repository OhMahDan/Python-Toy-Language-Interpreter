from lexer import Lexer
from ast_nodes import Num, Var, BinOp, UnaryOp, Assign

class Parser:
	def __init__(self, lexer):
		self.lexer = lexer
		self.current_token = self.lexer.get_next_token()

	def program(self):
		statements = []
		while self.current_token.type != 'EOF':
			statements.append(self.assignment())
		return statements

	def factor(self):
		token = self.current_token

		if token.type == 'PLUS':
			self.eat('PLUS')
			return UnaryOp(token, self.factor())
		
		elif token.type == 'MINUS':
			self.eat('MINUS')
			return UnaryOp(token, self.factor())
		
		elif token.type == 'NUMBER':
			self.eat('NUMBER')
			return Num(token)
		
		elif token.type == 'IDENTIFIER':
			self.eat('IDENTIFIER')
			return Var(token)
		
		elif token.type == 'LPAREN':
			self.eat('LPAREN')
			node = self.expr()
			self.eat('RPAREN')
			return node
	
		else:
			self.error("NUMBER, IDENTIFIER, +, -, or '('")
	
	def term(self):
		node = self.factor()

		while self.current_token.type == 'MULTIPLY':
			token = self.current_token
			self.eat('MULTIPLY')
			right = self.factor()
			node = BinOp(left=node, op=token, right=right)
		
		return node
	
	def expr(self):
		node = self.term()

		while self.current_token.type == 'PLUS' or self.current_token.type == 'MINUS':
			token = self.current_token
			self.eat(token.type)
			right = self.term()
			node = BinOp(left=node, op=token, right=right)
		
		return node
	
	def assignment(self):
		letVal = False

		if self.current_token.type == 'LET':
			self.eat('LET')
			letVal = True
		
		varNode = Var(self.current_token)
		self.eat('IDENTIFIER')
		self.eat('ASSIGN')
		exprNode = self.expr()
		self.eat('SEMICOLON')
		return Assign(left=varNode, right=exprNode, is_let=letVal)

	def error(self, expected_type):
		raise Exception(f"Syntax Error: Expected {expected_type}, got {self.current_token.type}")
	
	def eat(self, token_type):
		if self.current_token.type == token_type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error(token_type)