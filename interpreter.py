from parser import Parser

class Interpreter:
	def __init__(self, parser):
		self.parser = parser
		self.GLOBAL_MEMORY = {}
		self.in_let_expr = False
	
	def visit(self, node):
		method_name = f'visit_{type(node).__name__}'
		visitor = getattr(self, method_name, self.generic_visit)
		return visitor(node)
	
	def generic_visit(self, node):
		raise Exception(f'No visit_{type(node).__name__} method defined')
	
	def visit_Num(self, node):
		return node.value
	
	def visit_BinOp(self, node):
		left_val = self.visit(node.left)
		right_val = self.visit(node.right)

		if node.op.type == 'PLUS':
			return left_val + right_val
		elif node.op.type == 'MULTIPLY':
			return left_val * right_val
		elif node.op.type == 'MINUS':
			return left_val - right_val
		
	def visit_UnaryOp(self, node):
		op = node.op.type
		if op == 'PLUS':
			return +self.visit(node.expr)
		elif op == 'MINUS':
			return -self.visit(node.expr)
		
	def visit_Assign(self, node):
		var_name = node.left.value
		if var_name in self.GLOBAL_MEMORY:
			if self.GLOBAL_MEMORY[var_name]['is_let']:
				raise Exception(f"Assignment Error: '{var_name}' is a 'let' variable.")
		self.in_let_expr = node.is_let
		result = self.visit(node.right)
		self.GLOBAL_MEMORY[var_name] = {'value': result, 'is_let': node.is_let}
		self.in_let_expr = False

	def visit_Var(self, node):
		var_name = node.value
		if var_name not in self.GLOBAL_MEMORY:
			raise Exception(f"Var Error: Uninitialized Variable '{var_name}'")
		data = self.GLOBAL_MEMORY[var_name]
		if self.in_let_expr and not data['is_let']:
			raise Exception(f"Var Error: 'let' expression contains normal variable '{var_name}'")
		return data['value']
	
	def interpret(self):
		tree = self.parser.program()
		for node in tree:
			self.visit(node)
		
		print("\n--- Final Memory State ---")
		for x, v in self.GLOBAL_MEMORY.items():
			print(f"{x}: {v['value']} (is_let={v['is_let']})")