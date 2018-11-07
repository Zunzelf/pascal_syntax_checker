import os

# core module
class SyntaxChecker(object):
	pof = "" # used for defining position
	file = "" # used for file placeholder

	def accept(self, inp):
		if True : 
			pass
		else : 
			raise ValueError("can't accept grammar!")
	def check(self, file):
		pass

# util modules
def load_file(path) :
	res = ""	
	with open(path, "r") as lines :
		for line in lines :
			res += ""+line
		res += " $" # indicate eof
	return res.replace("\n", " ").replace("\t", "") # a bit prepro for removing newline and tab

if __name__ == '__main__':
	# load sample file
	sample_path = os.path.join(os.getcwd(), "sample_syntax.pas")
	sample = load_file(sample_path)
	sc = SyntaxChecker()
	print sc.check(sample)
	print sc.accept(sample)