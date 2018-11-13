

class PascalRule(object):		
	def __init__(self, file_inp):
		self.file = file_inp # used for file placeholder
		self.pof = 0 # used for defining position

	def accept(self, inp):
		if inp == self.file[self.pof].lower() : 
			self.pof += 1 # read next char
		else : 
			raise ValueError("can't accept grammar!")
	# for the sake of the beauty of the code~
	def accept_sequence(self, sequence):
		for seq in list(sequence):
			self.accept(seq)

	def first(self):
		self.program_name()
		self.accept(" ")
		self.program_content()
		self.accept(".")

	# part 1 of the BnF : 
	def program_name(self):
		if (self.file[self.pof].lower() == 'p') and (self.file[3].lower() == 'g') :
			self.accept_sequence("program")
			self.accept(" ")
			self.identifier()
			self.accept(";")
			print "clear~"

	def identifier(self): # temporary --> method should be according to the rule of alphanumeric
		while(self.file[self.pof] != " " and self.file[self.pof] != ";"):
			self.pof += 1

	def program_content(self): # still place holder
		if self.file[self.pof].lower() == 'b':
			self.accept_sequence("begin")
			
			self.accept_sequence("end")

	# part 2 of the BnF : 

	# part 3 of the BnF : 

		