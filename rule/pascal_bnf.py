class PascalRule(object):		
	def __init__(self, file_inp):
		self.file = file_inp # used for file placeholder
		self.pof = 0 # used for defining position
		self.letter = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		self.number = ['0','1','2','3','4','5','6','7','8','9']
		self.sign = ['-','+']
		self.symbol = ['+','-','*','=','<','>','(',')','.',',',';',':','"','{','}']
		self.typeReserved = ['integer','real','string','boolean']

	def accept(self, inp):
		if inp == self.file[self.pof].lower() : 
			self.pof += 1 # read next char
		else : 
			raise ValueError("can't accept grammar! value= "+inp+", char: "+self.file[self.pof].lower()+", pointer position: "+str(self.pof)+"\n ")
			# raise ValueError("can't accept grammar!")

			
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
			self.accept(" ")
			self.constant_definition()
			self.accept(";")

	# rule 8
	def skip_space(self):
		while(self.file[self.pof] == " "):
			self.accept(" ")

	# rule 9
	def constant_definition(self):
		self.constantVar()
		self.skip_space()
		self.accept("=")
		self.skip_space()
		self.constant()

	# rule 10
	def constant(self):
		# for number
		if self.file[self.pof] in self.number:
			while(self.file[self.pof] in self.number):
				self.accept(self.file[self.pof])
			# for real number
			if(self.file[self.pof] == '.'):
				self.accept('.')
				while(self.file[self.pof] in self.number):
					self.accept(self.file[self.pof])
				# real number with e constant
				if(self.file[self.pof].lower() == 'e'):
					self.accept('e')
					if(self.file[self.pof] in self.sign):
						self.accept(self.file[self.pof])
						while(self.file[self.pof] in self.number):
							self.accept(self.file[self.pof])
					elif (self.file[self.pof] in self.number):
						while(self.file[self.pof] in self.number):
							self.accept(self.file[self.pof])
		# for signed number
		elif self.file[self.pof] in self.sign:
			self.pof += 1
			while(self.file[self.pof] in self.number):
				self.accept(self.file[self.pof])
			# for real number
			if(self.file[self.pof] == '.'):
				self.accept('.')
				while(self.file[self.pof] in self.number):
					self.accept(self.file[self.pof])
		# for string or char
		elif self.file[self.pof] == '"' or self.file[self.pof] == "'":
			petik = self.file[self.pof]
			self.accept(petik)
			while(self.file[self.pof] != petik):
				self.accept(self.file[self.pof])
			self.accept(petik)

	#for variabel in constant, var, type, and so on 
	def constantVar(self):
		while(self.file[self.pof] != " " and self.file[self.pof] != ";" and self.file[self.pof] not in self.symbol):
			self.pof += 1

	def identifier(self): # temporary --> method should be according to the rule of alphanumeric
		while(self.file[self.pof] != " " and self.file[self.pof] != ";"):
			self.pof += 1

	def program_content(self): # still place holder
		self.constant_definition_part()
		# print("Now here: "+str(self.pof))
		if self.file[self.pof].lower() == 'b' and self.file[self.pof+1].lower() == 'e' and self.file[self.pof+2].lower() == 'g' and self.file[self.pof+3].lower() == 'i' and self.file[self.pof+4].lower() == 'n':
			self.accept_sequence("begin")
			# for ignore space
			self.skip_space()
			self.accept_sequence("end.")

	# part 2 of the BnF : 

	# part 3 of the BnF : 

		