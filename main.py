import os
from rule.pascal_bnf import PascalRule
# core module
class SyntaxChecker(object):

	def check(self, file):
		# print(file)
		self.file = list(file); # list per line into list per char
		rule = PascalRule(self.file)
		
		return rule.first()

# util modules
def load_file(path) :
	res = ""	
	with open(path, "r") as lines :
		for line in lines :
			res += ""+line
		res += " $" # indicate eof
	return res.replace("\n", "@").replace("\t", "") # a bit prepro for removing newline and tab

if __name__ == '__main__':
	# load sample file
	sample_path = os.path.join(os.getcwd(), "sample_syntax.pas")
	sample = load_file(sample_path)
	sc = SyntaxChecker()
	print (sc.check(sample))