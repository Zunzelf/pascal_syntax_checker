import os
from rule.pascal_bnf import PascalRule
# core module
class SyntaxChecker(object):

	def check(self, file, filename = ""):
		# print(file)
		self.file = list(file); # list per line into list per char
		rule = PascalRule(self.file)
		result = rule.first()
		if result[0] :
			return "no error detected"
		else:
			return "%s(%d,%d) error : %s"%(filename, result[2], result[1], result[3])

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
	print (sc.check(sample, os.path.basename(sample_path)))