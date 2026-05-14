class AST:
	pass

class Num(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value

class Var(AST):
	def __init__(self, token):
		self.token = token
		self.value = token.value

class BinOp(AST):
	def __init__(self, left, op, right):
		self.left = left
		self.token = self.op = op
		self.right = right

class UnaryOp(AST):
	def __init__(self, op, expr):
		self.token = self.op = op
		self.expr = expr

class Assign(AST):
	def __init__(self, left, right, is_let=False):
		self.left = left
		self.right = right
		self.is_let = is_let
