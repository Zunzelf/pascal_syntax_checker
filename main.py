import os
from rule.pascal_bnf_exp import PascalRule
# core module
class SyntaxChecker(object):

	def check(self, file, filename = ""):
		# print(file)
		self.file = list(file); # list per line into list per char
		rule = PascalRule(self.file)
		result = rule.first()
		msg = ""
		if result[0] :
			msg = "no error detected"
		else:
			msg = "%s(%d,%d) error : %s"%(filename, result[2], result[1], result[3])
		return (msg, result)

# util modules
ln = []
def load_file(path) :
	res = ""	
	with open(path, "r") as lines :
		for line in lines :
			res += ""+line
			ln.append(line.replace("\n", ""))
		res += " $" # indicate eof
	return res.replace("\n", "@").replace("\t", "") # a bit prepro for removing newline and tab

import argparse
if __name__ == '__main__':
	# usage example : 
	# python main.py -c -p "sample_syntax.pas"
	parser = argparse.ArgumentParser()
	parser.add_argument("--path", "-p")
	parser.add_argument("--check", "-c", action = "store_true")
	args = parser.parse_args()
	if args.check:
			if args.path:
					path = args.path
	else :
		path = "sample_syntax.pas"
	sample = load_file(path)
	print "==============CODE================="
	for line in ln:
		print line
	print "=============RESULT================"
	sc = SyntaxChecker()
	res = sc.check(sample, os.path.basename(path))
	if (res[1][0] == False):
		print "> %s"%ln[res[1][2]-1]
	print (res[0])
	print "==============END=================="