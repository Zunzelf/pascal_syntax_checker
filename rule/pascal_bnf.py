import sys
class PascalRule(object):		
	def __init__(self, file_inp):
		self.file = file_inp # used for file placeholder
		self.pof = 0 # used for defining position
		self.letterList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		self.numberList = ['0','1','2','3','4','5','6','7','8','9']
		self.sign = ['-','+']
		self.symbol = ['+','-','*','=','<','>','(',')','.',',',';',':','"','{','}']
		self.typeReserved = ['integer','real','string','boolean'] #belum dipake sih, rencana buat type dan var. 

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
			# while(not self.cek(self.file[self.pof].lower(),self.file[self.pof+1].lower(),self.file[self.pof+2].lower(),self.file[self.pof+3].lower())):
			self.skip_space()
			self.constant_definition()
			self.accept(";")

	#for ignoring space
	def skip_space(self):
		while(self.file[self.pof] == " "):
			self.accept(" ")

	# ala-ala dikit cek reserved word (ternyata gagal)
	# def cek(self,char1,char2,char3,char4):
	# 	if char1 == 'f' and char2 == 'u' and char3 == 'n' and char4 == 'c':
	# 		return True
	# 	elif char1 == 'b' and char2 == 'e' and char3=='g' and char4 =='i':
	# 		return True
	# 	elif char1 =='t' and char2 == 'y' and char3 == 'p' and char4 =='e':
	# 		return True
	# 	elif char1 =='p' and char2 == 'r' and char3 == 'o' and char4 =='c':
	# 		return True
	# 	elif char1 =='v' and char2 == 'a' and char3 == 'r' and char4 ==' ':
	# 		return True
	# 	elif char1 =='l' and char2 == 'a' and char3 == 'b' and char4 =='e':
	# 		return True
	# 	else:
	# 		return False
	
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
			# for real number
			if(self.file[self.pof] == '.'):
				self.accept('.')
				self.number()
				# real number with e constant
				if(self.file[self.pof].lower() == 'e'):
					self.accept('e')
					if(self.file[self.pof] in self.sign):
						self.accept(self.file[self.pof])
						self.number()
					elif (self.file[self.pof] in self.numberList):
						self.number()
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
			self.variable_declaration()
			self.accept(";")
			# note: belum repeat

	# variable declaration
	def variable_declaration(self):
		self.skip_space()
		self.identifier()
		self.skip_space()
		if self.file[self.pof] == ',':
			while(self.file[self.pof] != ':'):
				# simple repeat is okay
				self.skip_space()
				self.accept(',')
				self.skip_space()
				self.identifier()
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
			self.procedure_declararation()
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
		elif self.file[self.pof].lower() == 'o' and self.file[self.pof].lower() == 'r':
			self.accept_sequence("or") 
		self.term()

	# multiply operator
	def multiply_operator(self):
		if self.file[self.pof] == '*':
			self.accept('*')
		elif self.file[self.pof] == '/':
			self.accept('/')
		elif self.file[self.pof].lower() == 'd' and self.file[self.pof+1].lower() == 'i' and self.file[self.pof+2] == 'v':
			self.accept_sequence('div')
		elif self.file[self.pof].lower() == 'm' and self.file[self.pof+1].lower() == 'o' and self.file[self.pof+2] == 'd':
			self.accept_sequence("mod")
		elif self.file[self.pof].lower() == 'a' and self.file[self.pof+1].lower() == 'n' and self.file[self.pof+2] == 'd':
			self.accept_sequence("and")

	# unsigned constant
	def unsigned_constant(self):
		if self.file[self.pof] == "'" or self.file[self.pof] == '"':
			self.string()
		else:
			self.number()

	# for identifier, naming purpose
	def identifier(self): 
		self.letter()
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
		if(self.file[self.pof] != " " and self.file[self.pof] != ";" and self.file[self.pof] in self.letterList or self.file[self.pof] in self.numberList or self.file[self.pof] == '_'):
			self.accept(self.file[self.pof])
			if(self.file[self.pof] != " " and self.file[self.pof] != ";" and self.file[self.pof] in self.letterList or self.file[self.pof] in self.numberList or self.file[self.pof] == '_'):
				self.letter_or_number()
	# for letter
	def letter(self):
		if (self.file[self.pof].lower() in self.letterList):
			self.accept(self.file[self.pof])
			if(self.file[self.pof].lower() in self.letterList):
				self.letter()
	# for number
	def number(self):
		if (self.file[self.pof] in self.numberList):
			self.accept(self.file[self.pof])
			if(self.file[self.pof] in self.numberList):
				self.number()

	def program_content(self): # still place holder
		self.skip_space()
		self.constant_definition_part()
		self.skip_space()
		self.variable_declaration_part()
		self.skip_space()
		self.proc_func_declare_part()
		self.skip_space()
		if self.file[self.pof].lower() == 'b' and self.file[self.pof+2].lower() == 'g' and self.file[self.pof+4].lower() == 'n':
			self.accept_sequence("begin")
			# for ignore space
			self.skip_space()
			self.accept_sequence("end")

	# part 2 of the BnF : 

	# part 3 of the BnF : 

		