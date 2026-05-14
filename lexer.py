class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value
	
	def __repr__(self):
		return f"token({self.type}, {repr(self.value)})"

class Lexer:
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.current_char = self.text[self.pos] if self.text else None
	
	def advance(self):
		self.pos += 1
		if self.pos >= len(self.text):
			self.current_char = None
		else:
			self.current_char = self.text[self.pos]
	
	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()
	
	def get_next_token(self):
		while self.current_char is not None:
			if self.current_char.isspace():
				self.skip_whitespace()
				continue
			if self.current_char == '+':
				self.advance()
				return Token('PLUS', '+')
			if self.current_char == '-':
				self.advance()
				return Token('MINUS', '-')
			if self.current_char == '*':
				self.advance()
				return Token('MULTIPLY', '*')
			if self.current_char == '(':
				self.advance()
				return Token('LPAREN', '(')
			if self.current_char == ')':
				self.advance()
				return Token('RPAREN', ')')
			if self.current_char == '=':
				self.advance()
				return Token('ASSIGN', '=')
			if self.current_char == ';':
				self.advance()
				return Token('SEMICOLON', ';')
			if self.current_char.isalpha() or self.current_char == '_':
				return self._id()
			if self.current_char.isdigit():
				return self.number()
			raise Exception(f"Lexer Error: Invalid character '{self.current_char}'")
		return Token('EOF', None)
	
	def number(self):
		if self.current_char == '0':
			self.advance()
			if self.current_char is not None and self.current_char.isdigit():
				raise Exception("Lexer Error: Leading zero.")
			return Token('NUMBER', 0)
		numStr = ""
		while self.current_char is not None and self.current_char.isdigit():
			numStr += self.current_char
			self.advance()
		return Token('NUMBER', int(numStr))
	
	def _id(self):
		currentStr = ""
		while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
			currentStr += self.current_char
			self.advance()
		if currentStr == "let":
			return Token('LET', 'let')
		return Token('IDENTIFIER', currentStr)