import sys
class PascalRule(object):
    def __init__(self, file_inp):
        self.file = self.all_lowercase(file_inp) # used for file placeholder
        self.pof = 0 # used for defining position
        self.letterList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.numberList = ['0','1','2','3','4','5','6','7','8','9']
        self.sign = ['-','+']
        self.symbol = ['+','-','*','=','<','>','(',')','.',',',';',':','"','{','}']
        self.relational = ['<','>','='] #belum dipake sih, rencana buat type dan var. 
        self.typeReserved = ['integer','real','string','boolean'] #belum dipake sih, rencana buat type dan var.
        (self.col, self.line) = (1, 1)
        self.newline = "@" 
    ## utility functions
    def accept(self, inp):
        if inp == self.file[self.pof] : 
            self.col += 1
            self.pof += 1 # read next char
        else : 
            self.msg = "'"+inp+"' expected, '"+self.file[self.pof]+"' found"
            raise ValueError()      
    # for the sake of the beauty of the code~
    def accept_sequence(self, sequence):
        try:
            for seq in list(sequence):
                self.accept(seq)
        except ValueError: 
            self.msg = "'%s' expected, '%s' found"%(sequence, self.file[self.pof])
            raise ValueError()  
    def check(self, cmd):
        tmp_pof = self.pof
        for x in list(cmd):
            if self.file[tmp_pof] != x:
                return False
            tmp_pof += 1
        return True
    # becoz pascal isn't case sensitive *wink*
    def all_lowercase(self, file):
        return [x.lower() for x in file]
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
        while(self.file[self.pof] == " " or self.file[self.pof] == self.newline):
            # self.col += 1
            if self.file[self.pof] == self.newline:
                self.line += 1
                self.col = 1
            self.accept(self.file[self.pof])
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
            if self.file[p] == ":" and self.file[p+1] != "=":
                return True
        else :
            return False

    ## rules
    # rule 1
    def first(self):
        try :
            self.skip_space()
            self.program_name()
            self.skip_space()
            self.program_content()
            self.skip_space()
            self.accept(".")
        except ValueError:
            return [False, self.col, self.line, self.msg]
        return [True, self.col, self.line, "no error"]
    # rule 2
    def program_name(self):
        if (self.check("program")) :
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
            self.variable_declaration_part()
            self.skip_space()
            self.pro_func_declare()
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
        if(self.check("const")):
            self.accept_sequence("const")
            self.skip_space()
            self.constant_definition()
            self.skip_space()
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
            if(self.file[self.pof] == '.' and not self.check("..")):
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
        
    # rule 10 -- perbaikan untuk bil real
    def unsigned_number(self):
        self.number()
        if self.file[self.pof] == '.':
            self.real_number_ext()
    # rule 11 <belum ada>    
    def real_number_ext(self):
        if self.file[self.pof] == '.':
            self.accept('.')
            self.number()
            # real number with e constant
            if(self.file[self.pof].lower() == 'e'):
                self.accept('e')
                self.scale_factor()
    # rule 12 <belum ada>   
    def scale_factor(self):
        if self.file[self.pof] in self.sign:
            self.accept(self.file[self.pof])
            self.number()
        else:
            self.number()  
    # rule 13
    def string(self):
        if(self.file[self.pof] == '"' or self.file[self.pof] == "'"):
            petik = self.file[self.pof]
            self.accept(petik)
            while(self.file[self.pof] != petik):
                self.accept(self.file[self.pof])
            self.accept(petik)  
    # rule 15
    def type_definition_part(self):
        if self.check("type"):
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
        if self.check('array') or self.check('set of') or self.check('file of') or self.check('record') or self.check('packed'):
            self.structured_file()
        elif self.file[self.pof].lower() in self.letterList:
            self.identifier()
        else :
            self.simple_type()
    # rule 18 - teza_rev
    def simple_type(self):
        # const .. const
        if self.file[self.pof].lower() in self.numberList or self.file[self.pof].lower() in self.sign or self.file[self.pof].lower() in ["'", '"']:
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
        self.constant()
        self.skip_space()
        self.accept_sequence("..")
        self.skip_space()
        self.constant()
    # rule 21
    def structured_file(self):
        if self.check('array') or self.check('packed'):
            self.array_type()
        elif self.check('set of'):
            self.set_type()
        elif self.check('file of'):
            self.file_type()
        else:
            self.record_type()
    # rule 22
    def array_type(self):
        if self.check('packed'):
            self.accept_sequence("packed")
            self.skip_space()
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
    # rule 23, 24
    def record_type(self):
        self.accept_sequence("record")
        self.skip_space()
        self.field_list()
        self.skip_space()
        self.accept_sequence("end")
    # rule 25
    def field_list(self):
        self.fixed_part()
    # rule 26
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
    # rule 27
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
                self.constant()
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
    # rule 33 ?????
    def variable_declaration_part(self):
        if(self.check("var")):
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
    # rule 34
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
        self.skip_space()
        self.type()
    # rule 35
    def proc_func_declare_part(self):
        self.pro_func_declare()
    # rule 36
    def pro_func_declare(self):
        while (self.check("procedure") or self.check("function")):
            if(self.check("procedure")):
                self.procedure_declaration()
                self.skip_space()
                self.accept(';')
            elif self.check("function"):
                self.function_declaration()
                self.skip_space()
                self.accept(';')
            self.skip_space()
    # rule 37 <belum ada>
    def procedure_declaration(self):
        self.procedure_heading()
        self.skip_space()
        self.program_content()
    # rule 38
    def procedure_heading(self):
        self.accept_sequence("procedure")
        self.skip_space()
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
    # rule 39, 40
    def formal_parameter_section(self):
        if(self.check("var")):
            self.accept_sequence('var')
        # di dokumentasi tulisannya parameter grup, tapi struktur = variable declaration
        self.skip_space()
        self.variable_declaration()
    # rule 41
    def function_declaration(self):
        self.function_heading()
        self.skip_space()
        self.program_content()
    # rule 42
    def function_heading(self):
        self.accept_sequence("function")
        self.skip_space()
        self.identifier()
        self.skip_space()
        if(self.file[self.pof] == '('):
            self.accept('(')
            self.skip_space()
            # ini di cek tolong repeatnya
            self.formal_parameter_section()
            self.skip_space()
            if(self.file[self.pof] == ';'):
                while(self.file[self.pof] != ')'):
                    self.accept(';')
                    self.skip_space()
                    self.formal_parameter_section()
            # harusnya ada repeat disini
            self.accept(')')
        self.accept(':')
        self.skip_space()
        self.identifier()
        self.skip_space()
        self.accept(';')
    # rule 43
    def statement_part(self):
        if (not self.check('begin')) :
            self.msg = "can't accept grammar! 'begin' expected"
            raise ValueError()
        self.compound_statement()
    # rule 44
    def statement(self):
        if self.is_label():
            self.label()
            self.skip_space()
            self.accept(":")
            self.skip_space()
            self.unlabelled_statement()
        else :
            self.unlabelled_statement()
    # rule 45, 65
    def unlabelled_statement(self):
        ## misal ada structured statement
        if self.check("begin"):
            self.compound_statement()
        elif self.check("if") or self.check("case"):
            self.conditional_statement()
        elif self.check("repeat ") or self.check("while ") or self.check("for "):
            self.repetitive_statement()
        elif self.check("with"):
            self.with_statement()
        else:
            self.simple_statement()
    # rule 46
    def simple_statement(self):
        if self.check("goto"):
            self.go_to_statement()
        else:
            self.identifier()
            self.skip_space()
            self.variable_or_proc_statement()
    # rule 47
    def variable_or_proc_statement(self):
        if self.check(":="):
            self.accept_sequence(":=")
            self.skip_space()
            self.expression()
        elif self.file[self.pof] == '(':
            self.accept('(')
            self.skip_space()
            self.actual_parameter()
            self.skip_space()
            if self.file[self.pof] == ',':
                while(self.file[self.pof] != ')'):
                    self.accept(',')
                    self.skip_space()
                    self.actual_parameter()
                    self.skip_space()
            self.accept(')')
    # rule 48
    def actual_parameter(self):
            self.expression()
    # rule 49
    def go_to_statement(self):
        self.accept_sequence("goto")
        self.skip_space()
        self.label()
    
# ------------------------------------------------------------------------------------------------------------------------      
    # rule 50 new
    def expression(self):
        # kalau dia adalah factor = turunan dari math expression
        if self.file[self.pof] in self.sign or self.file[self.pof] == '(' or self.file[self.pof] == '[' or self.file[self.pof] in self.letterList or self.file[self.pof] in self.numberList or self.check("not"):
            self.math_expression()
            self.skip_space()
            if self.file[self.pof] in self.relational:
                self.comparing_expression()
        # kalau dia boolean identifier
        elif self.check("true") or self.check("false"):
            self.boolean_expression()
            self.skip_space()
        elif self.file[self.pof] == '"' or self.file[self.pof] == "'":
            self.string()
            self.skip_space()
            if self.file[self.pof] == '+':
                self.accept('+')
                self.skip_space()
                self.string()
                self.skip_space()
                while(self.file[self.pof] == '+'):
                    self.accept('+')
                    self.skip_space()
                    self.string
                    self.skip_space()
    # rule 51 new
    def math_expression(self):
        self.simple_expression()
        self.skip_space()
        # kalau ada math operator
        if self.file[self.pof] in self.sign or self.file[self.pof] == '/' or self.file[self.pof] == '*' or self.check("div") or self.check("mod") or self.check("and") or self.check("or") or self.check("xor") or self.check("shl") or self.check("shr"):
            self.math_operator()
            self.skip_space()
            self.simple_expression()
            self.skip_space()
            # selama ada math operator
            while self.file[self.pof] in self.sign or self.file[self.pof] == '/' or self.file[self.pof] == '*' or self.check("div") or self.check("mod") or self.check("and") or self.check("or") or self.check("xor") or self.check("shl") or self.check("shr"):
                self.math_operator()
                self.skip_space()
                self.simple_expression()
                self.skip_space()
    # rule 52 new
    def math_operator(self):
        if self.file[self.pof] in self.sign or self.file[self.pof] == '/' or self.file[self.pof] == '*':
            self.accept(self.file[self.pof])
        elif self.check("div"):
            self.accept_sequence("div")
        elif self.check("mod"):
            self.accept_sequence("mod")
        elif self.check("or") or self.check("and") or self.check("xor"):
            self.boolean_operator()
        elif self.check("shl"):
            self.accept_sequence("shl")
        elif self.check("shr"):
            self.accept_sequence("shr")
    # rule 53 new  = plus, ga kepake
    # rule 54 new
    def comparing_expression(self):
        self.comparing_operator()
        self.skip_space()
        # kalau ada first dari math expression = simple expression = factor
        if self.file[self.pof] in self.sign or self.file[self.pof] == '(' or self.file[self.pof] == '[' or self.file[self.pof] in self.letterList or self.file[self.pof] in self.numberList or self.check("not"):
            self.math_expression()
            self.skip_space()
    #  rule 55 new
    def comparing_operator(self):
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
    # rule 56 new
    def rel_opr_ext(self):
        if self.file[self.pof] == '=':
            self.accept('=')
        elif self.file[self.pof] == '>':
            self.accept('>')
    # rule 57 new
    def boolean_expression(self):
        self.boolean_identifier()
        self.skip_space()
        self.boolean_operator()
        self.skip_space()
        self.boolean_identifier()
        self.skip_space()
        if self.check("and") or self.check("or") or self.check("xor"):
            self.boolean_operator()
            self.skip_space()
            self.identifier()
            self.skip_space()
            while self.check("and") or self.check("or") or self.check("xor"):
                self.boolean_operator()
                self.skip_space()
                self.identifier()
                self.skip_space()
    # rule 58 new
    def boolean_identifier(self):
        if self.check("true"):
            self.accept_sequence("true")
        elif self.check("false"):
            self.accept_sequence("false")
    # rule 59 new
    def boolean_operator(self):
        if self.check("and"):
            self.accept_sequence("and")
        elif self.check("or"):
            self.accept_sequence("or")
        elif self.check("xor"):
            self.accept_sequence("xor")
    # rule 60 new
    def simple_expression(self):
        if self.file[self.pof] in self.sign:
            self.accept(self.file[self.pof])
            self.skip_space()
            self.factor()
        else:
            self.factor()
        self.skip_space()
    # rule 61 new 
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
        elif self.check("not") or self.check("not"):
            self.accept_sequence("not")
            self.skip_space()
            self.factor()
        self.skip_space()
    # rule 62 new
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
    # rule 63 new
    def set(self):
        self.accept('[')
        self.skip_space()
        self.element_list()
        self.skip_space()
        self.accept(']')    
    # rule 64 new
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
        self.skip_space()
    # rule 65 new
    def element(self):
        self.identifier()
        if self.accept(".."):
            self.accept_sequence("..")
            self.identifier
        self.skip_space()
    # rule 66 new, strucuted statement, digabung sama rule 45.
# ---------------------------------------------------------------------------------------------------------------------------
    # these are experimental functions
    def conditions(self):
        self.condition()
        self.skip_space()
        while self.check("or") or self.check("and") or self.check("xor") :
            self.condition()
            self.skip_space()

    def condition(self):
        wrapper = False
        if self.check("(") :
            self.accept("(")
            self.skip_space()
            wrapper = True
        if self.check("not ") or self.check("not("):
            self.accept_sequence("not")
            self.skip_space()
        if self.check("true") or self.check("false"):
            self.boolean_expression()
        else :
            # kalau dia adalah factor = turunan dari math expression
            if self.file[self.pof] in self.sign or self.file[self.pof] == '(' or self.file[self.pof] == '[' or self.file[self.pof] in self.letterList or self.file[self.pof] in self.numberList or self.check("not"):
                self.math_expression()
                self.skip_space()
                if self.file[self.pof] in self.relational:
                    self.comparing_expression()
        self.skip_space()
        if wrapper:
            self.accept(")")
        
# ---------------------------------------------------------------------------------------------------------------------------
    # rule 66
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
    # rule 67
    def conditional_statement(self):
        if self.check("if"):
            self.if_statement()
        elif self.check("case"):
            self.case_statement()
    # rule 68 exp
    def if_statement(self):
        self.accept_sequence("if")
        self.skip_space()
        self.conditions() # will be changed
        self.skip_space()
        self.accept_sequence("then")
        self.skip_space()
        self.statement()
        self.skip_space()
        while self.check("else") :
            self.accept_sequence("else")
            self.skip_space()
            self.statement()
    # rule 69
    def case_statement(self):
        self.accept_sequence("case")
        self.skip_space()
        self.expression()
        self.skip_space()
        self.accept_sequence("of")
        self.skip_space()
        while(not self.check("end")):
            self.case_list_element()
            self.skip_space()
        self.accept_sequence("end")
    # rule 70
    def case_list_element(self):
        self.case_label_list()
        self.skip_space()
        self.accept(":")
        self.skip_space()
        self.statement()
        self.skip_space()
        self.accept(";")
    # rule 71
    def repetitive_statement(self):
        if self.check("while"):
            self.while_statement()
        elif self.check("repeat"):
            self.repeat_statement()
        elif self.check("for"):
            self.for_statement()
    # rule 72 exp
    def while_statement(self):
        self.accept_sequence("while")
        self.skip_space()
        self.conditions() # will be changed
        self.skip_space()
        self.accept_sequence("do")
        self.skip_space()
        self.statement()
    # rule 73 exp
    def repeat_statement(self):
        self.accept_sequence("repeat")
        self.skip_space()
        while(not self.check("until")):
            self.statement()
            self.skip_space()
            self.accept(";")
            self.skip_space()
        self.accept_sequence("until")
        self.skip_space()
        self.conditions()  # will be changed 
    # rule 74
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
    # rule 75
    def to_or_downto(self):
        if self.check("to"):
            self.accept_sequence("to")
            self.skip_space()
            self.expression()
        elif self.check("downto"):
            self.accept_sequence("downto")
            self.skip_space()
            self.expression()
    # rule 76
    def with_statement(self):
        self.accept_sequence("with")
        self.skip_space()
        self.identifier()
        self.skip_space()
        if self.file[self.pof] == ',':
            self.accept(',')
            self.skip_space()
            self.identifier()
            self.skip_space()
            while (not self.check("do")):
                self.accept(',')
                self.skip_space()
                self.identifier()
                self.skip_space()
        self.accept_sequence("do")
        self.skip_space()
        self.statement()
    # rule 77
    def identifier(self): 
        self.letter()
        while(self.file[self.pof] in self.letterList or self.file[self.pof] in self.numberList or self.file[self.pof] == "_"):
            if self.file[self.pof] == "_":
                self.accept("_")
            self.letter_or_number()
    # rule 78
    def letter_or_number(self):
        if(self.file[self.pof] in self.letterList):
            self.letter()
        elif(self.file[self.pof] in self.numberList):
            self.number()
        else :
            self.msg = "can't accept grammar!"
            raise ValueError()
    # rule 79
    def letter(self):
        if (self.file[self.pof].lower() in self.letterList):
            self.accept(self.file[self.pof])
        else :
            self.msg = "can't accept grammar! %s not a letter" %self.file[self.pof] 
            raise ValueError()
    # rule 80
    def number(self):
        if (self.file[self.pof] in self.numberList):
            while (self.file[self.pof] in self.numberList):
                self.accept(self.file[self.pof])
        else :
            self.msg = "can't accept grammar! %s not a number" %self.file[self.pof] 
            raise ValueError()