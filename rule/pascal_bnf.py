import sys
class PascalRule(object):		
	def __init__(self, file_inp):
		self.file = file_inp # used for file placeholder
		self.pof = 0 # used for defining position
		self.letterList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		self.numberList = ['0','1','2','3','4','5','6','7','8','9']
		self.sign = ['-','+']
		self.symbol = ['+','-','*','=','<','>','(',')','.',',',';',':','"','{','}']
		self.relational = ['<','>','='] #belum dipake sih, rencana buat type dan var. 

	def accept(self, inp):
		if inp.lower() == self.file[self.pof].lower() : 
			self.pof += 1 # read next char
		else : 
			# raise ValueError("can't accept grammar! value= "+inp+", char: "+self.file[self.pof].lower()+", pointer position: "+str(self.pof)+"\n ")
			raise ValueError("can't accept grammar! '"+inp+"' expected, '"+self.file[self.pof]+"' found. position: "+str(self.pof))

			
	# for the sake of the beauty of the code~
	def accept_sequence(self, sequence):
		for seq in list(sequence):
			self.accept(seq)

	def first(self):
		print("for checking position purpose: ")
		print(self.file)
		self.skip_space()
		self.program_name()
		self.skip_space()
		self.program_content()
		self.accept('.')

	# part 1 of the BnF : 
	def program_name(self):
		if (self.file[self.pof].lower() == 'p') and (self.file[self.pof+3].lower() == 'g') :
			self.accept_sequence("program")
			self.accept(" ")
			self.identifier()
			self.accept(";")

	# rule 7
	def constant_definition_part(self):
		if(self.file[self.pof].lower() == 'c') and (self.file[self.pof+2].lower()=='n') and (self.file[self.pof+3].lower() == 's'):
			self.accept_sequence("const")
			self.skip_space()
			self.constant_definition()
			self.accept(";")
			self.skip_space()
			while(not self.is_command()):
				self.constant_definition()
				self.accept(";")
				self.skip_space()

	#for ignoring space
	def skip_space(self):
		while(self.file[self.pof] == " "):
			self.accept(" ")

	#check something 
	def check(self,cmd):
		tmp_pof = self.pof
		for x in list(cmd):
			if self.file[tmp_pof].lower() != x:
				return False
			tmp_pof += 1
		return True

	# 
	def is_command(self):
		# begin
		if self.check("begin"):
			return True
        # var
		elif self.check("var"):
			return True
        # type
		elif self.check("type"):
			return True
        # const
		elif self.check("const"):
			return True
        # procedure
		elif self.check("procedure"):
			return True
        # function
		elif self.check("function"):
			return True
		else:
			return False
	
	# rule 8
	def constant_definition(self):
		self.skip_space()
		self.identifier()
		self.skip_space()
		self.accept("=")
		self.skip_space()
		self.constant()


	# rule 9
	def constant(self):
		# for number
		if self.file[self.pof] in self.numberList:
			self.number()
			self.numbers()
			# for real number
			if(self.file[self.pof] == '.'):
				self.accept('.')
				self.numbers()
				# real number with e constant
				if(self.file[self.pof].lower() == 'e'):
					self.accept('e')
					if(self.file[self.pof] in self.sign):
						self.accept(self.file[self.pof])
						self.numbers()
					elif (self.file[self.pof] in self.numberList):
						self.numbers()
		# for signed number
		elif self.file[self.pof] in self.sign:
			self.accept(self.file[self.pof])
			self.number()
			# for real number
			if(self.file[self.pof] == '.'):
				self.accept('.')
				self.number()
		# for string or char
		elif self.file[self.pof] == '"' or self.file[self.pof] == "'":
			self.string()
	
	# variable declaration part 
	def variable_declaration_part(self):
		if(self.file[self.pof].lower() == 'v' and self.file[self.pof+1].lower() == 'a' and self.file[self.pof+2].lower() == 'r'):
			self.accept_sequence("var")
			self.skip_space()
			self.variable_declaration()
			self.skip_space()
			self.accept(";")
			self.skip_space()
			while(not self.is_command()):
				self.variable_declaration()
				self.accept(";")
				self.skip_space()
			# note: belum repeat

	# variable declaration
	def variable_declaration(self):
		self.skip_space()
		self.identifier()
		self.skip_space()
		if self.file[self.pof] == ',':
			while(self.file[self.pof] != ':'):
				# simple repeat is okay
				self.accept(',')
				self.skip_space()
				self.identifier()
				self.skip_space()
		self.accept(':')
		# bagian teza
		self.skip_space()
		self.identifier()

	# procedure and functoin declaration part
	def proc_func_declare_part(self):
		self.pro_func_declare()

	# proc and func declaration
	def pro_func_declare(self):
		if(self.file[self.pof].lower() == 'p' and self.file[self.pof+1].lower() == 'r' and self.file[self.pof+3].lower() == 'c' ):
			# bagian teza
			self.procedure_declaration()
			self.skip_space()
			self.accept(';')
		elif self.file[self.pof].lower() == 'f' and self.file[self.pof+1].lower() == 'u' and self.file[self.pof+2].lower() == 'n' and self.file[self.pof+3].lower() == 'c':
			self.function_declaration()
			self.skip_space()
			self.accept(';')

	# procedure heading
	def procedure_heading(self):
		self.accept_sequence("procedure")
		self.identifier()
		if(self.file[self.pof] == '('):
			self.accept('(')
			# ini di cek tolong repeatnya
			self.formal_parameter_section()
			if(self.file[self.pof] == ';'):
				while(self.file[self.pof] != ')'):
					self.accept(';')
					self.skip_space()
					self.formal_parameter_section()
			# harusnya ada repeat disini
			self.accept(')')
		self.accept(';')
	
	# formal parameter section
	def formal_parameter_section(self):
		if(self.file[self.pof].lower() == 'v' and self.file[self.pof+1].lower() == 'a' and self.file[self.pof+2].lower() == 'r'):
			self.accept_sequence('var')
		# di dokumentasi tulisannya parameter grup, tapi struktur = variable declaration
		self.skip_space()
		self.variable_declaration()

	# function
	def function_declaration(self):
		self.function_heading()
		self.skip_space()
		self.program_content()
	
	# function heading
	def function_heading(self):
		self.skip_space()
		self.accept_sequence("function")
		self.skip_space()
		self.identifier()
		self.skip_space()
		if(self.file[self.pof] == '('):
			self.accept('(')
			# ini di cek tolong repeatnya
			self.formal_parameter_section()
			if(self.file[self.pof] == ';'):
				while(self.file[self.pof] != ')'):
					self.accept(';')
					self.skip_space()
					self.formal_parameter_section()
			# harusnya ada repeat disini
			self.accept(')')
		self.accept(':')
		self.identifier()
		self.accept(';')

	# procedure ext statement
	def variable_or_proc_statement(self):
		if self.check(":="):
			self.accept_sequence(":=")
			self.skip_space()
			self.expression
		elif self.file[self.pof] == '(':
			self.accept('(')
			self.skip_space()
			self.actual_parameter()
			self.skip_space()
			if self.file[self.pof] == ',':
				self.accept(',')
				self.skip_space()
				while(self.file[self.pof] != ')'):
					self.actual_parameter()
					self.accept(',')
					self.skip_space()
			self.accept(')')

	# actual parameter
	def actual_parameter(self):
		self.expression()

	# expression
	def expression(self):
		self.simple_expression()
		self.skip_space()
		if self.file[self.pof] in self.relational or self.check("in"):
			self.relational_operator()
			self.skip_space()
			self.simple_expression()
			self.skip_space()

	# relational opr
	def relational_operator(self):
		if self.file[self.pof] == '=':
			self.accept('=')
		elif self.file[self.pof] == '<':
			self.accept('<')
			if self.file[self.pof] == '>' or self.file[self.pof] == '=':
				self.rel_opr_ext()
		elif self.file[self.pof] == '>':
			self.accept('>')
			if self.file[self.pof] == '=':
				self.accept('=')
		elif self.check("in"):
			self.accept_sequence("in")

	# rel opr ext
	def rel_opr_ext(self):
		if self.file[self.pof] == '=':
			self.accept('=')
		elif self.file[self.pof] == '>':
			self.accept('>')

	# simple expression
	def simple_expression(self):
		if self.file[self.pof] in self.sign:
			self.accept(self.file[self.pof])
		elif self.check("or"):
			self.accept_sequence("or") 
		self.term()

	# term
	def term(self):
		self.factor()
		self.skip_space()
		if self.file[self.pof] == '*' or self.file[self.pof] == '/' or self.check("div") or self.check("mod") or self.check("and"):
			self.multiply_operator()
			self.skip_space()
			self.factor()

	# factor
	def factor(self):
		if self.file[self.pof] in self.letterList:
			self.identifier()
			self.skip_space()
			if self.file[self.pof] == '(':
				self.function_designator()
		elif self.file[self.pof] in self.numberList:
			self.unsigned_number()
		elif self.file[self.pof] =='(':
			self.accept('(')
			self.skip_space()
			self.expression()
			self.skip_space()
			self.accept(')')
		elif self.file[self.pof] == '[':
			self.set()
		elif self.check("not"):
			self.accept_sequence("not")
			self.skip_space()
			self.factor()

	#function designator 
	def function_designator(self):
		self.accept('(')
		self.skip_space()
		self.actual_parameter()
		self.skip_space()
		if self.file[self.pof] == ',':
			self.accept(',')
			self.skip_space()
			while self.file[self.pof] != ')':
				self.actual_parameter()
		self.accept(')')

	# set
	def set(self):
		self.accept('[')
		self.skip_space()
		self.element_list()
		self.skip_space()
		self.accept(']')
	
	# unsigned constant
	def unsigned_constant(self):
		if self.file[self.pof] == "'" or self.file[self.pof] == '"':
			self.string()
		else:
			self.unsigned_number()

	# unsigned number
	def unsigned_number(self):
		self.number()
		self.numbers()
	
	# element list
	def element_list(self):
		self.element()
		self.skip_space()
		if self.file[self.pof] == ',':
			self.accept(',')
			self.skip_space()
			self.element()
			while self.file[self.pof] != ']':
				self.accept(',')
				self.skip_space()
				self.element()
	
	# element
	def element(self):
		self.identifier()
		if self.accept(".."):
			self.accept_sequence("..")
			self.identifier


	# multiply operator
	def multiply_operator(self):
		if self.file[self.pof] == '*':
			self.accept('*')
		elif self.file[self.pof] == '/':
			self.accept('/')
		elif self.check("div"):
			self.accept_sequence("div")
		elif self.check("mod"):
			self.accept_sequence("mod")
		elif self.check("and"):
			self.accept_sequence("and")
	
	# for statement
	def for_statement(self):
		self.accept_sequence("for")
		self.skip_space()
		self.identifier()
		self.skip_space()
		self.accept_sequence(":=")
		self.skip_space()
		self.expression()
		self.skip_space()
		self.to_or_downto()
		self.skip_space()
		self.accept_sequence("do")
		self.skip_space()
		self.statement()

	# to or downto
	def to_or_downto(self):
		if self.check("to"):
			self.accept_sequence("to")
			self.skip_space()
			self.expression()
		elif self.check("downto"):
			self.accept_sequence("downto")
			self.skip_space()
			self.expression()
	
	# with statement
	def with_statement(self):
		self.accept_sequence("with")
		self.skip_space()
		self.record_variable_list()
		self.skip_space()
		if self.file[self.pof] == ',':
			self.accept(',')
			self.skip_space()
			self.record_variable
			self.skip_space()
			while (not self.check("do")):
				self.accept(',')
				self.skip_space()
				self.record_variable
				self.skip_space()
		self.accept_sequence("do")
		self.skip_space()
		self.statement()
					
	def program_content(self): # still place holder
		self.skip_space()
		self.constant_definition_part()
		self.skip_space()
		# check eror
		# sys.exit()
		self.variable_declaration_part()
		self.skip_space()
		self.proc_func_declare_part()
		self.skip_space()
		if self.file[self.pof].lower() == 'b' and self.file[self.pof+2].lower() == 'g' and self.file[self.pof+4].lower() == 'n':
			self.accept_sequence("begin")
			# for ignore space
			self.skip_space()
			self.accept_sequence("end")

	# for letter
	def letter(self):
		if (self.file[self.pof].lower() in self.letterList):
			self.accept(self.file[self.pof])
		else:
			raise ValueError("cant accept grammar")

	# for number
	def number(self):
		if (self.file[self.pof] in self.numberList):
			self.accept(self.file[self.pof])
			if(self.file[self.pof] in self.numberList):
				self.number()

	# for multiple number
	def numbers(self):
		while (self.file[self.pof] in self.numberList):
			self.accept(self.file[self.pof])

		# for identifier, naming purpose
	def identifier(self): 
		self.letter()
		while (self.file[self.pof] != " " and self.file[self.pof] != ";" and self.file[self.pof] in self.letterList or self.file[self.pof] in self.numberList or self.file[self.pof] == '_'):
			self.letter_or_number()

	# for string (accept anything in between petik)
	def string(self):
		if(self.file[self.pof] == '"' or self.file[self.pof] == "'"):
			petik = self.file[self.pof]
			self.accept(petik)
			while(self.file[self.pof] != petik):
				self.accept(self.file[self.pof])
			self.accept(petik)

	# for letter or number
	def letter_or_number(self):
		if (self.file[self.pof].lower() in self.letterList):
			self.letter()
		elif (self.file[self.pof] in self.numberList):
			self.number()
		else:
			raise ValueError("cant accept grammar")

		