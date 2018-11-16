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
    ## utility functions
    def accept(self, inp):
        if inp.lower() == self.file[self.pof].lower() : 
            self.pof += 1 # read next char
        else : 
            # raise ValueError("can't accept grammar! value= "+inp+", char: "+self.file[self.pof].lower()+", pointer position: "+str(self.pof)+"\n ")
            raise ValueError("can't accept grammar! '"+inp+"' expected, '"+self.file[self.pof]+"' found")
        
    # for the sake of the beauty of the code~
    def accept_sequence(self, sequence):
        for seq in list(sequence):
            self.accept(seq)

    def check(self, cmd):
        tmp_pof = self.pof
        for x in list(cmd):
            if self.file[tmp_pof] != x:
                return False
            tmp_pof += 1
        return True

    def is_command(self):
        # begin
        if self.check("begin") :
            return True
        # var
        elif self.check("var") :
            return True
        # type
        elif self.check("type") :
            return True
        # const
        elif self.check("const") :
            return True
        # procedure
        elif self.check("procedure") :
            return True
        # function
        elif self.check("function") :
            return True
        else :
            return False

    #for ignoring space
    def skip_space(self):
        while(self.file[self.pof] == " "):
            self.accept(" ")

    def is_label(self):
        p = self.pof
        x = 0
        if self.file[p] in self.letterList :
            x = 1
            while self.file[p] in self.letterList:
                p += 1
        elif self.file[p] in self.numberList :
            x = 1
            while self.file[p] in self.numberList:
                p += 1
        if x == 1 :
            while self.file[p] == " ":
                p += 1
            if self.file[p] == ":":
                return True
        else :
            return False

    # rule 1
    def first(self):
        # print("for checking position purpose: ")
        # print(self.file)
        self.skip_space()
        self.program_name()
        self.skip_space()
        self.program_content()
        self.skip_space()
        self.accept(".")
        return True

    # rule 2 
    def program_name(self):
        if (self.file[self.pof].lower() == 'p') and (self.file[self.pof+3].lower() == 'g') :
            self.accept_sequence("program")
            self.skip_space()
            self.identifier()
            self.skip_space()
            self.file_list()
            self.skip_space()
            self.accept(";")

    # rule 3
    def file_list(self):
        if self.file[self.pof].lower() == "(" :
            self.accept("(")
            self.skip_space()
            self.identifier()
            self.skip_space()
            while self.file[self.pof].lower() == "," :
                self.accept(",")
                self.skip_space()
                self.identifier()
                self.skip_space()
            self.accept(")")
    
    # rule 4
    def program_content(self): # still place holder
            self.label_declaration_part()
            self.skip_space()
            self.constant_definition_part()
            self.skip_space()
            self.type_definition_part()
            self.skip_space()
            self.statement_part()

    # rule 5
    def label_declaration_part(self):
        if self.file[self.pof].lower() == "l" and self.file[self.pof+2].lower() == "b" :
            self.accept_sequence("label")
            self.skip_space()
            self.identifier()
            if self.file[self.pof] != ";" :
                self.skip_space()
                while self.file[self.pof] == "," :
                    self.accept(",")
                    self.skip_space()
                    self.identifier()
                    self.skip_space()
            self.accept(";")

    # rule 6
    def label(self):
        if self.file[self.pof] in self.letterList :
            while self.file[self.pof] in self.letterList:
                self.accept(self.file[self.pof])
        elif self.file[self.pof] in self.numberList :
            while self.file[self.pof] in self.numberList:
                self.accept(self.file[self.pof])

    # rule 7
    def constant_definition_part(self):
        if(self.file[self.pof].lower() == 'c') and (self.file[self.pof+2].lower()=='n') and (self.file[self.pof+3].lower() == 's'):
            self.accept_sequence("const")
            self.accept(" ")
            self.constant_definition()
            self.accept(";")

    # rule 8
    def constant_definition(self):
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
    
    #rule 15
    def type_definition_part(self):
        if self.check("type"):
            print "type"
            self.accept_sequence("type")
            self.skip_space()
            self.type_definition()
            self.skip_space()
            self.accept(";")
            self.skip_space()
            while not self.is_command() :
                self.type_definition()
                self.accept(";")
                self.skip_space()
                if (self.file[self.pof] == "$") :
                    raise ValueError("can't accept grammar! 'begin' expected")
        if (self.file[self.pof] == "$") :
            raise ValueError("can't accept grammar! 'begin' expected")

        print "type succeed"

    # rule 16
    def type_definition(self):
        self.identifier()
        self.skip_space()
        self.accept("=")
        self.skip_space()
        self.type()
        self.skip_space()

    # rule 17
    def type(self):
        if self.check('array') or self.check('set of') or self.check('file of') or self.check('record') :
            self.structured_file()
        elif self.file[self.pof].lower() in self.letterList:
            self.identifier()
        else :
            self.simple_type()

    # rule 18
    def simple_type(self):
        # const .. const
        if self.file[self.pof].lower() in self.numberList or self.file[self.pof].lower() in self.sign:
            self.subrange_type()
        if self.file[self.pof] == "(":
            self.scalar_type()

    # rule 19
    def scalar_type(self):
        if self.file[self.pof].lower() == "(" :
            self.accept("(")
            self.skip_space()
            self.identifier()
            self.skip_space()
            while self.file[self.pof].lower() == "," :
                self.accept(",")
                self.skip_space()
                self.identifier()
                self.skip_space()
            self.accept(")")

    # rule 20
    def subrange_type(self):
        self.numbers()
        self.skip_space()
        self.accept_sequence("..")
        self.skip_space()
        self.numbers()

    # rule 21
    def structured_file(self):
        if self.check('array'):
            self.array_type()
        elif self.check('set of'):
            self.set_type()
        elif self.check('file of'):
            self.file_type()
        else:
            self.record_type()

    # rule 22
    def array_type(self):
        self.accept_sequence("array")
        self.skip_space()
        self.accept("[")
        self.skip_space()
        self.simple_type()
        self.skip_space()
        while self.file[self.pof].lower() == "," :
            self.accept(",")
            self.skip_space()
            self.simple_type()
            self.skip_space()
        self.accept("]")
        self.skip_space()
        self.accept_sequence("of")
        self.skip_space()
        self.type()

    # rule 23
    def record_type(self):
        self.accept_sequence("record")
        self.skip_space()
        self.field_list()
        self.skip_space()
        self.accept_sequence("end")

    # rule 24
    def field_list(self):
        self.fixed_part()

    # rule 25
    def fixed_part(self):
        self.record_section()
        self.skip_space()
        self.accept(";")
        self.skip_space()
        while (not self.check("end;")) and (not self.check("end ")):  
            self.record_section()
            self.skip_space()
            self.accept(";")
            self.skip_space()  

    # rule 26
    def record_section(self):
        self.identifier()
        self.skip_space()
        while (not self.check(":")):
            self.accept(",")
            self.skip_space()  
            self.identifier()
            self.skip_space()             
        self.accept(":")
        self.skip_space()
        self.type()

    # rule 28
    def tag_field(self):
        self.identifier()
        self.skip_space()
        self.accept(":")

    # rule 29
    def variant(self):
        self.case_label_list()
        self.skip_space()
        self.accept(":")
        self.skip_space()
        self.accept("(")
        self.skip_space()
        self.field_list()
        self.skip_space()
        self.accept(")")

    # rule 30
    def case_label_list(self):
        self.constant()
        self.skip_space()
        if(self.check(",")):
            while not self.check(":"):
                self.accept(",")
                self.skip_space()
                self.numbers()
                self.skip_space()

    # rule 31
    def set_type(self):
        self.accept_sequence("set of")
        self.skip_space()
        self.simple_type()

    # rule 32
    def file_type(self):
        self.accept_sequence("file of")
        self.skip_space()
        self.type()
    ####################
    # rule 44
    def statement_part(self):
        self.compound_statement()

    # rule 45
    def statement(self):
        if self.is_label():
            self.label()
            self.skip_space()
            self.accept(":")
            self.skip_space()
            self.unlabelled_statement()
        else :
            self.unlabelled_statement()

    # rule 46
    def unlabelled_statement(self):
        ##misal ada structured statement
        if self.check("begin"):
            self.compound_statement()
        elif self.check("if") or self.check("case"):
            self.conditional_statement()
        elif self.check("repeat ") or self.check("while ") or self.check("for "):
            self.repetitive_statement()
        elif self.check("with"):
            pass ############
        else:
            self.simple_statement()

    # rule 47
    def simple_statement(self):
        if self.check("goto"):
            self.go_to_statement()
        else:
            pass #################

    # rule 50
    def procedure_ext_statement(self):
        pass

    # rule 51
    def actual_parameter(self):
        pass

    # rule 52
    def go_to_statement(self):
        self.accept_sequence("goto")
        self.skip_space()
        self.label()
#######################################
    # rule 53
    def relational_operator(self):
        p = self.file[self.pof]
        if p == "=":
            self.accept("=")
        elif p == "<":
            self.accept("<")
            self.rel_opr_ext()
        elif p == ">":
            self.accept(">")
            if self.file[self.pof] == "=":
                self.accept("=")

    # rule 54
    def rel_opr_ext(self):
        p = self.file[self.pof]
        if p == "=":
            self.accept("=")
        elif p == ">":
            self.accept(">")
    ######################
    # rule 67
    def compound_statement(self):
        if self.check("begin"):
                self.accept_sequence("begin")
                self.skip_space()
                while(not self.check("end")):
                    self.statement()
                    self.skip_space()
                    self.accept(";")
                    self.skip_space()
                self.skip_space()
                self.accept_sequence("end")


    # rule 68
    def conditional_statement(self):
        pass

    # rule 69
    def if_statement(self):
        pass

    # rule 70
    def case_statement(self):
        pass

    # rule 71
    def case_list_element(self):
        pass

    # rule 72
    def repetitive_statement(self):
        pass

    # rule 73
    def while_statement(self):
        pass

    # rule 74
    def repeat_statement(self):
        pass
    ######################
    # rule 78
    def identifier(self): 
        print self.file[self.pof]
        self.letter()
        while(self.file[self.pof] in self.letterList or self.file[self.pof] in self.numberList):
            self.letter_or_number()

    # for string (accept anything in between petik)
    def string(self):
        if(self.file[self.pof] == '"' or self.file[self.pof] == "'"):
            petik = self.file[self.pof]
            self.accept(petik)
            while(self.file[self.pof] != petik):
                self.accept(self.file[self.pof])
            self.accept(petik)
    ########################
    # rule 79
    def letter_or_number(self):
        if(self.file[self.pof] in self.letterList):
            self.letter()
        elif(self.file[self.pof] in self.numberList):
            self.number()
        else :
            raise ValueError("can't accept grammar!")
    # rule 80
    def letter(self):
        if (self.file[self.pof].lower() in self.letterList):
            self.accept(self.file[self.pof])
        else :
            raise ValueError("can't accept grammar! not a letter")
    # rule 81
    def numbers(self):
        if (self.file[self.pof] in self.numberList):
            while (self.file[self.pof] in self.numberList):
                self.accept(self.file[self.pof])
    # rule 81
    def number(self):
        if (self.file[self.pof] in self.numberList):
            self.accept(self.file[self.pof])
        else :
            raise ValueError("can't accept grammar! not a number")
    ########################

import os
if __name__ == '__main__':
    # util modules
    def load_file(path) :
        res = ""    
        with open(path, "r") as lines :
            for line in lines :
                res += ""+line
            res += " $" # indicate eof
        return res.replace("\n", " ").replace("\t", "") # a bit prepro for removing newline and tab 


    sample_path = os.path.join(os.getcwd(), "sample_syntax.pas")
    sample = list(load_file(sample_path))
    rule = PascalRule(sample)
    print rule.first()
    # print rule.is_command()