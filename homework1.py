# Justin Choi (jc8mc)
# September 22nd 2017
# CS 4710: Artificial Intelligence
# Homework 1: Building a rule-based logic system similar to CLIPS

import re
import pyparsing as pp
from pyparsing import infixNotation, opAssoc, Keyword, Word, alphas

# use regex to see variables are acceptable characters
def check_var(input_var):
    regex = re.compile(r"[a-zA-Z_]+")
    result = regex.match(input_var)
    return result

# use regex to make sure that strings are in quotations for first teach
def check_quote_teach(quotes):
    regex = re.compile(r'"[^"]*"')
    result = regex.match(quotes)
    return result

def my_parse(givemeinput):
    identifier = pp.Regex("[a-zA-Z_]+")
    comparison_term = identifier
    condition = pp.Group(comparison_term)
    expr = pp.operatorPrecedence(condition, [
        ("!", 1, pp.opAssoc.RIGHT,),
        ("&", 2, pp.opAssoc.LEFT,),
        ("|", 2, pp.opAssoc.LEFT,),
    ])
    return expr.parseString(givemeinput)

def flatten(aList):
    new_list = []
    found_list = True
    while found_list:
        found_list = False
        for elem in aList:
            if isinstance(elem, list):
                for subelem in elem:
                    new_list.append(subelem)
                found_list = True
            else:
                new_list.append(elem)

        new_list, aList = aList, new_list
        new_list.clear()
    return aList

# data structure for storing variable definitions

# 1) a list for facts, trusted variables i.e True variables:
facts = []
fact_s = "S"
fact_v = "V"
facts.append(fact_s)
facts.append(fact_v)

# 2) a list for root variables:
root = []
# root variables:
root_s = 'S = "Sam likes Ice Cream"'
root_v = 'V = "Today is Sunday"'
root.append(root_s)
root.append(root_v)

# teach1 function
def root_insert(user_root_input):
    root_vars = toroot()
    all_vars = toall_vars()
    # Make sure variable name is not used twice
    if parse_command(user_root_input)[0] not in root_vars:
        if parse_command(user_root_input)[0] not in all_vars:
            root.append(user_root_input)
        else:
            print("Invalid Command. Variable name cannot be used twice.")
    else:
        print("Invalid Command. Variable name cannot be used twice.")

# teach1 helper function
# only returns the root variables, not the full expression
def toroot():
    root_vars = []
    for rootings in root:
        rootings = parse_command(rootings)[0]
        if rootings not in root:
            root_vars.append(rootings)
    return root_vars

# only returns the learned variables
def tolearned():
    learned_vars = []
    for learning in learned:
        only_learned_vars = parse_command(learning)[0]
        if only_learned_vars not in learned_vars:
            learned_vars.append(only_learned_vars)
    return learned_vars

# returns all of the currently used variable names
# checks for duplicate variable names since a variable name cannot be used twice
def toall_vars():
    learned_vars = tolearned()
    root_vars = toroot()
    all_vars = learned_vars + root_vars
    return all_vars

# ok they are in the root, however, are they in fact true?
# check to see if they are by using the second teach function

# teach2 function
# check if I want to make it a dictionary instead for root variables
# or should I divide them up?
def teach2_trustedfunction(your_input):
    received_input = parse_command(your_input)
    new_deparsed_toadd = deparse_command(received_input[1])
    quote_check = str(received_input[-1])
    if new_deparsed_toadd in learned:
        print("Invalid Command. Cannot set a learned variable to either boolean values")
    # setting a root variable to a true fact and putting them in a facts that can be used later
    elif (check_quote_teach(quote_check) == None):
        if (str(received_input[-1]) == 'true'):
            bool_value = True
            root_var_list = toroot()
            # first needs to be amongst the root_variables
            if new_deparsed_toadd in root_var_list:
                # check for duplicates
                if new_deparsed_toadd not in facts:
                    facts.append(new_deparsed_toadd)
            else:
                print("Invalid Command. No such root variable: " + new_deparsed_toadd + " that can be set to true")
        # setting a root variable that is true to false.
        # 1) if the user input's variable is in the facts (root variables with true values)
        # and user want it to be false, remove it from the facts
        # 2) if the user input's variable is not even in the facts, give ERROR
        elif (str(received_input[-1]) == 'false'):
            bool_value = False
            if new_deparsed_toadd in facts:
                facts.remove(new_deparsed_toadd)
            else:
                print("Invalid Command. No such True root variable that you can set to False")
        else:
            print("Invalid Command. This parameter can only take a boolean value: 'true' or 'false'.")
    else:
        print("Invalid Syntax for Second Teach Command; boolean values must not be in quotation marks")

# Parsing commands correctly
def parse_command(command_string):
    command_splitted = command_string.split()
    return command_splitted

# after parsing, deparse it so I can add it in the list of variables
def deparse_command(alist):
    getlist = alist
    list2string = ''
    i = 0
    while (i < len(getlist)):
        list2string += getlist[i] + " "
        i += 1
    return list2string[:(len(list2string) - 1)]

valid_logical_operator = ['!', '&', '|']

# List Command
def list_command():
    print("Root Variables: ")
    for root_vars in root:
        print("\t" + str(root_vars))
    print("")
    print("Learned Variables: ")
    for learn in learned:
        print("\t" + learn)
    print("")
    print("Facts: ")
    for fact in facts:
        print("\t" + fact)
    print("")
    print("Rules: ")
    for rule in rules:
        print("\t" + rule)

# 3) a list for learned variables:
learned = []
# learned variables:
learned_EAT = 'EAT = "Sam will eat ice cream"'
learned.append(learned_EAT)

def check4paranthesis(expr):
    regex = re.compile(r'\([^"]*\)')
    result = regex.match(expr)
    return result

# 4) a list for rules:
rules = []
#rule_sv = "S&V -> EAT"
#rules.append(rule_sv)

# Types of commands: "Teach", "Learn", "List", "Query", "Why"
commands = ["Teach", "Learn", "List", "Query", "Why"]

# for Learn command: forward chaining
# def forward_chaining():
#     for rule in rules:
#         # actual first part of rule you are looking for
#         rule_sep = parse_command(rule)[0]
#         # a potential fact from the rule that might be added
#         new_fact_toadd = parse_command(rule)[2]
#
#         # check for true or false for expr variables
#         my_list_of_lists = my_parse(rule_sep)
#         my_one_list = flatten(my_list_of_lists[0].asList())
#         # now get only the variables using regex and iterating through the list
#         every_var = toall_vars()
#         my_one_list_vars = []
#         for item in my_one_list:
#             if (check_var(item) != None):
#                 my_one_list_vars.append(item)
#
#         # # S, V
#         # for my_vars in my_one_list_vars:
#         #     # default value is False: when not in trusted_var; i.e when in root variable = False and when in learned
#         #     globals()[my_vars] = False
#         #     if my_vars in facts:
#         #         globals()[my_vars] = True
#
#         ## not that we have parsed the expr, evaluate it
#         # if the eval_func returns true, add the new_fact_toadd
#         retvalue = False
#         if all(x in my_one_list_vars for x in every_var):
#             retvalue = True
#
#         res = boolExpr.parseString(rule_sep, parseAll=True)[0]
#         if bool(res):
#             if retvalue == True:
#                 facts.append(new_fact_toadd)

def forward_chaining():
    facts_list = []
    for rule in rules:
        # actual rule you are looking for
        rule_sep = parse_command(rule)[0]
        # a potential fact from the rule that might be added
        new_fact_toadd = parse_command(rule)[2]

        # check for true or false for expr variables
        my_list_of_lists = my_parse(rule_sep)
        my_one_list = flatten(my_list_of_lists[0].asList())
        # now get only the variables using regex and iterating through the list
        my_one_list_vars = []
        for item in my_one_list:
            if (check_var(item) != None):
                my_one_list_vars.append(item)

        for my_vars in my_one_list_vars:
            # default value is False: when not in trusted_var; i.e when in root variable = False and when in learned
            globals()[my_vars] = False
            if my_vars in facts:
                globals()[my_vars] = True

        ## not that we have parsed the expr, evaluate it
        # if the eval_func returns true, add the new_fact_toadd
        res = boolExpr.parseString(rule_sep, parseAll=True)[0]
        if bool(res):
            if new_fact_toadd not in facts:
                facts_list.append(new_fact_toadd)
    return facts_list

def expr_only_var(rule_sep):
    my_list_of_lists = my_parse(rule_sep)
    my_one_list = flatten(my_list_of_lists[0].asList())
    # now get only the variables using regex and iterating through the list
    my_one_list_vars = []
    for item in my_one_list:
        if (check_var(item) != None):
            my_one_list_vars.append(item)
    return my_one_list_vars

def operator_only(rule_sep):
    my_list_of_lists = my_parse(rule_sep)
    my_one_list = flatten(my_list_of_lists[0].asList())
    # now get only the variables using regex and iterating through the list
    my_one_list_vars = []
    for item in my_one_list:
        if (check_var(item) == None):
            my_one_list_vars.append(item)
    return my_one_list_vars

def check_query1(query_expr):
    retval = 'false'
    # check for true or false for expr variables
    my_list_of_lists = my_parse(query_expr)
    my_one_list = flatten(my_list_of_lists[0].asList())
    # now get only the variables using regex and iterating through the list
    my_one_list_vars = []
    for item in my_one_list:
        if (check_var(item) != None):
            if item in facts:
                my_one_list_vars.append(item)

    ## not that we have parsed the expr, evaluate it
    # if the eval_func returns true, add the new_fact_toadd
    query_expr_dict = {}
    res = boolExpr.parseString(query_expr, parseAll=True)[0]
    for mytrue_vars in my_one_list_vars:
        query_expr_dict[globals()[mytrue_vars]] = 'true'

    if all(value == 'true' for value in query_expr_dict.values()):
        if bool(res):
            retval = 'true'

    if retval == 'true':
        print("true")
    else:
        print("false")

def backward_chaining_helper(inputme):
    # find rule R that match with H, the end result
    mylist = []
    for rule in rules:
        if inputme in parse_command(rule)[2]:
            mylist.append(rule)
    return mylist

#         if parse_command(rule)[2] == inputme:
#             stack.append(rule)

            # facts_combined = parse_command(rule)[0]
            # facts_combined = my_parse(facts_combined)
            # facts_list = flatten(facts_combined[0].asList())


    # if inputme in facts:
    #     print("True")
    # if len(mystack) == 0:
    #     print("False")
    # else:
        # myquery(

def backward_chaining(learned_b):
    # if learned is True
    retval = 'false'
    if learned_b in facts:
        for rule in rules:
            if parse_command(rule)[2] == learned_b:
                facts_combined = parse_command(rule)[0]
                facts_combined = my_parse(facts_combined)
                facts_list = flatten(facts_combined[0].asList())
                single_facts = []
                dict_check = {}
                for factings in facts_list:
                    if (check_var(factings) != None):
                        if factings in facts:
                            single_facts.append(factings)
                if len(single_facts) != 0:
                    for tiny in single_facts:
                        # default value is False: when not in trusted_var; i.e when in root variable = False and when in learned
                        dict_check[globals()[tiny]] = 'true'
                    # res = boolExpr.parseString(learned_b, parseAll=True)[0]
                    if learned_b in facts:
                        if all(value == 'true' for value in dict_check.values()):
                            retval = 'true'
    if retval == 'true':
        print("true")

def true_statement():
    mystr = "I KNOW"
    return mystr

def words(varyingvars, my):
    ret = []
    for i in range (0, len(varyingvars)):
        for k in range (0, len(my)):
            if varyingvars[i] == parse_command(my[k])[0]:
                ret.append(deparse_command(parse_command(my[k])[2:]))
    return ret

def concluding():
    mystr = "I THUS KNOW THAT"
    return mystr

def convert(alist):
    convert_list = []
    for item in alist:
        if item == '&':
            convert_list.append(' AND ')
        elif item == '|':
            convert_list.append(' OR ')
        elif item == '!':
            convert_list.append(' IT IS NOT TRUE')
        else:
            convert_list.append("BECAUSE ")
    return convert_list
# The code below is from simpleBool.py from the pyparsing library
# http://pyparsing.wikispaces.com/
# simpleBool.py
#
# Example of defining a boolean logic parser using
# the operatorGrammar helper method in pyparsing.
#
# In this example, parse actions associated with each
# operator expression will "compile" the expression
# into BoolXXX class instances, which can then
# later be evaluated for their boolean value.
#
# Copyright 2006, by Paul McGuire
# Updated 2013-Sep-14 - improved Python 2/3 cross-compatibility

class BoolOperand(object):
    def __init__(self, t):
        self.label = t[0]
        self.value = eval(t[0])

    def __bool__(self):
        return self.value

    def __str__(self):
        return self.label

    __repr__ = __str__
    __nonzero__ = __bool__

class BoolBinOp(object):
    def __init__(self, t):
        self.args = t[0][0::2]

    def __str__(self):
        sep = " %s " % self.reprsymbol
        return "(" + sep.join(map(str, self.args)) + ")"

    def __bool__(self):
        return self.evalop(bool(a) for a in self.args)

    __nonzero__ = __bool__
    __repr__ = __str__

class BoolAnd(BoolBinOp):
    reprsymbol = '&'
    evalop = all

class BoolOr(BoolBinOp):
    reprsymbol = '|'
    evalop = any

class BoolNot(object):
    def __init__(self, t):
        self.arg = t[0][1]

    def __bool__(self):
        v = bool(self.arg)
        return not v

    def __str__(self):
        return "~" + str(self.arg)

    __repr__ = __str__
    __nonzero__ = __bool__

TRUE = Keyword("True")
FALSE = Keyword("False")
boolOperand = TRUE | FALSE | Word(alphas, max=1)
boolOperand.setParseAction(BoolOperand)

# define expression, based on expression operand and
# list of operations in precedence order
boolExpr = infixNotation(boolOperand,
                         [
                             ("!", 1, opAssoc.RIGHT, BoolNot),
                             ("&", 2, opAssoc.LEFT, BoolAnd),
                             ("|", 2, opAssoc.LEFT, BoolOr),
                         ])



## Start of main, for testing and I/O purposes
if __name__ == "__main__":
    print("Welcome to Expert Systems Shell!")
    print("")
    print("To quit the program any time, please enter: 0")
    print("")
    while True:
        user_command = input("Type in a command: ")
        if user_command == '0':
            break
        else:
            # parses by each each space
            command_by_word = parse_command(user_command)
            # first verb / action command such as "Teach", "Learn", etc
            action_command = command_by_word[0]
            # print(command_by_word)
            if (action_command not in commands):
                print("Invalid Command")
            else:
                # Start of Teach Functions
                if action_command == 'Teach':
                    # both teach 1 and 2 have "=" sign
                    teach12cases = '='
                    # for teach 3:
                    var = '->'
                    # the length of a valid teach 1 and 2 is >= 4
                    if (len(command_by_word) >= 4):
                        if (teach12cases in command_by_word[3]) or (teach12cases in command_by_word[2]):
                            # teach 2 I/O and using teach1 function
                            if len(command_by_word) == 4:
                                # using regex to see if it is a valid variable according to the rules
                                if (check_var(command_by_word[1]) != None):
                                    # checked whether that variable exists first using toroot
                                    ### MUST CHECK that it is not modifying -L learned variables
                                    teach2_trustedfunction(user_command)
                                else:
                                    print("Invalid Variable Name, according to the naming convention of variables: 'Variable names can be any case-sensitive string containing the characters A-Z, a-z, and underscores. No other characters should appear in the variable'")
                            # teach 1 I/O and using teach2 function
                            elif (len(command_by_word) >= 5):
                                if (check_var(command_by_word[2]) != None):
                                    # check if quotations exist
                                    if (check_quote_teach(deparse_command(command_by_word[4:])) != None):
                                        new_deparsed_toadd = deparse_command(command_by_word[2:])
                                        if command_by_word[1] == '-L':
                                            # get all variables
                                            all_vars = toall_vars()
                                            # Make sure variable name is not used twice
                                            var_learn = tolearned()
                                            if command_by_word[2] not in var_learn:
                                                if command_by_word[2] not in all_vars:
                                                    learned.append(new_deparsed_toadd)
                                                else:
                                                    print("Invalid Command. Variable name cannot be used twice.")
                                            else:
                                                print("Invalid Command. Variable name cannot be used twice.")
                                        elif command_by_word[1] == '-R':
                                            # checks for duplicate variable names in root_insert()
                                            root_insert(new_deparsed_toadd)
                                        else:
                                            print("Invalid Command. Only the '-L' flag or '-R' flag can be used to mean learned variable and root variable, respectively")
                                else:
                                    print("Invalid Variable Name, according to the naming convention of variables: 'Variable names can be any case-sensitive string containing the characters A-Z, a-z, and underscores. No other characters should appear in the variable'")
                            else:
                                print("Invalid Command. Please check the guidelines for the Teaching Command.")
                        # teach 3 I/O and using teach3 function
                        else:
                            expr_to_check = command_by_word[1]
                            check_learned = command_by_word[3] # V
                            # conditions that must be met first to be a valid input for teach 3
                            # every words of the command visited to see if it is the right command
                            learned_vars_here = tolearned()
                            checking_then = command_by_word[2]
                            if (checking_then == var):
                                if check_learned not in learned_vars_here:
                                    print("Invalid Command. Variable not defined.")
                                else:
                                    # what we want to add
                                    rule_toadd = deparse_command(command_by_word[1:])
                                    list_of_lists = my_parse(expr_to_check)
                                    one_list = flatten(list_of_lists[0].asList())
                                    # now get only the variables using regex and iterating through the list
                                    one_list_vars = []
                                    for item in one_list:
                                        if (check_var(item) != None):
                                            one_list_vars.append(item)
                                    check_learned_vars = tolearned()
                                    check_root_vars = toroot()
                                    # allvar = toall_vars()
                                    # for x in one_list_vars:
                                    #     if x not in allvar:
                                    #         print("Invalid Command. Variables have not been defined ")
                                    for x in one_list_vars:
                                        if (x in check_learned_vars) or (x in check_root_vars):
                                            if check_learned in check_learned_vars:
                                                if rule_toadd not in rules:
                                                    rules.append(rule_toadd)
                                            else:
                                                print("Invalid Command: the <VAR> should be a learned variable")
                                        else:
                                            print("Invalid Command: a variable in the <EXP> is not a root or learned variable and <VAR> is not a learned variable")
                                # else:
                                        # check_learned_vars2 = tolearned()
                                        # check_root_vars2 = toroot()
                                        # if check_learned not in check_learned_vars2:
                                        #     if check_learned in check_root_vars2:
                                        #         print("Invalid Command: the <VAR> should be a learned variable")

                            else:
                                print("Invalid Logical Operator. For Third Teach Command you can only use the '->' operator")
                    else:
                        print("")
                        print("Invalid Command for Teach; You did not enter the correct amount of parameters / arguments")
                        print("There are three 'Teach' commands that you can apply: ")
                        print("1. Teach <ARG> <VAR> = <STRING>")
                        print("Example: Teach -R S = 'Sam likes ice cream'")
                        print("2. Teach <ROOT VAR> = <BOOL>")
                        print("Example: Teach S = true")
                        print("3. Teach <EXP> -> <VAR>")
                        print("Example: Teach S -> V")
                        print("")
                elif (user_command == "Learn"):
                    add_fact = forward_chaining()
                    if (len(add_fact) != 0):
                        for facts_of in add_fact:
                            facts.append(facts_of)
                elif (user_command == "List"):
                    list_command()
                elif (action_command == "Query"):
                    # get the parse and then get only the variables
                    # see them if they are in the facts

                    query_expr = command_by_word[1]
                    get = query_expr
                    var_in_query = expr_only_var(query_expr)
                    each_rule = []
                    # for ruling in rules:
                    #     each_rule.append(parse_command(ruling)[0])
                    myget = []
                    oldfacts = facts
                    for myvars in var_in_query:
                        if myvars not in facts:
                            list_rules = backward_chaining_helper(query_expr)
                            for rulings in list_rules:
                                # rules.append(rulings)
                                myget.append(rulings)
                                # from Learn
                                add_fact1 = forward_chaining()
                                if (len(add_fact1) != 0):
                                    for facts_of1 in add_fact1:
                                        if facts_of1 not in facts:
                                            facts.append(facts_of1)

                        else:
                            if myvars in facts:
                                globals()[myvars] = True
                            else:
                                globals()[myvars] = False
                                # first evaluate Query
                    count = 0
                    if (len(myget) == 0):
                        retvaling = False
                        for myvars in var_in_query:
                            if myvars not in oldfacts:
                                # if this was true, we added a fact
                                retvaling = True
                        if retvaling == True:
                            if var_in_query[0] not in facts:
                                print("false")
                            else:
                                print("Invalid Command")
                        else:
                            res = boolExpr.parseString(get, parseAll=True)[0]
                            if bool(res):
                                print("true")
                    elif len(myget) > 0:
                        i = 0
                        while (i < len(myget)):
                            for factinfo in facts:
                                globals()[factinfo] = True
                            res = boolExpr.parseString(parse_command(myget[i])[0], parseAll=True)[0]
                            if bool(res) == True:
                                count += 1
                            i += 1
                        if count == i:
                            print("true")
                    else:
                        res = boolExpr.parseString(get, parseAll=True)[0]
                        if bool(res):
                            print("true")

                elif (action_command == "Why"):

                    # from Query
                    query_expr = command_by_word[1]
                    #second_expr = command_by_word[3]
                    get = query_expr
                    var_in_query = expr_only_var(query_expr)
                    each_rule = []
                    # for ruling in rules:
                    #     each_rule.append(parse_command(ruling)[0])
                    # print(query_expr) : S&V
                    # print(var_in_query) : ['S', 'V']

                    myget = []
                    oldfacts = facts
                    for myvars in var_in_query:
                        if myvars not in facts:
                            list_rules = backward_chaining_helper(query_expr)
                            for rulings in list_rules:
                                # rules.append(rulings)
                                myget.append(rulings)
                                # from Learn
                                add_fact1 = forward_chaining()
                                if (len(add_fact1) != 0):
                                    for facts_of1 in add_fact1:
                                        if facts_of1 not in facts:
                                            facts.append(facts_of1)

                        else:
                            if myvars in facts:
                                globals()[myvars] = True
                            else:
                                globals()[myvars] = False
                                # first evaluate Query
                    count = 0
                    if (len(myget) == 0):
                        retvaling = False
                        for myvars in var_in_query:
                            if myvars not in oldfacts:
                                # if this was true, we added a fact
                                retvaling = True
                        if retvaling == True:
                            if var_in_query[0] not in facts:
                                print("false")
                            else:
                                print("Invalid Command")
                        else:
                            res = boolExpr.parseString(get, parseAll=True)[0]
                            if bool(res):
                                print("true")
                            else:
                                print("false")
                    elif len(myget) > 0:
                        i = 0
                        while (i < len(myget)):
                            for factinfo in facts:
                                globals()[factinfo] = True
                            res = boolExpr.parseString(parse_command(myget[i])[0], parseAll=True)[0]
                            if bool(res) == True:
                                count += 1
                            i += 1
                        if count == i:
                            print("true")
                        else:
                            print("false")
                    else:
                        res = boolExpr.parseString(get, parseAll=True)[0]
                        if bool(res):
                            print("true")
                        else:
                            print("false")



                    query_expr = command_by_word[1]
                    get = query_expr
                    var_in_query = expr_only_var(query_expr)
                    combined = root + learned
                    operations = operator_only(query_expr)
                    variables = expr_only_var(query_expr)

                    # print(query_expr)
                    # print(var_in_query)
                    # print(operations) ['&']
                    # print(variables) ['S', 'V']

                    # no rule case:
                    # rule_case = '->'
                    # if rule_case not in operations:
                        # nothing ex) single (Why (S))
                    total = '('
                    if len(operations) == 0:
                        know = words(variables, combined)
                        if (variables[0] in tolearned()) and (variables[0] not in rules):
                            for ruleing in rules:
                                if variables[0] in deparse_command(parse_command(ruleing)[2:]):
                                    from_logic = parse_command(ruleing[0])
                                else:
                                    print("Invalid Command")
                        else:
                            if variables[0] not in facts:
                                print("I KNOW IT IS NOT TRUE THAT " + str(know[0]))
                            else:
                                print(true_statement() + " THAT " + str(know[0]))
                    if ('&' in operations) or ('|' in operations) or ('!' in operations):
                        deduction = ''
                        more = []
                        know = words(variables, combined)
                        for knowing in know:
                            more.append(knowing)
                        opening = '('
                        closing = ')'
                        #combine_logic = ''
                        changed_operations = convert(operations)
                        for rule_part in rules:
                            if (query_expr in rule_part) and ('->' in rule_part):
                                total = "Because "
                                total += opening
                                deduction = deparse_command(parse_command(rule_part)[2:])
                            else:
                                total += opening
                        i = 0
                        j = 0
                        # for op in changed_operations:
                        while (i < len(more)):
                            total += more[i]
                            while (j < len(changed_operations)):
                                if changed_operations[i] == ' IT IS NOT TRUE':
                                    open_statement = true_statement() + changed_operations[i] + ' THAT '
                                    # total = open_statement + total
                                else:
                                    open_statement = true_statement() + " THAT "
                                    total = open_statement + total + changed_operations[j]
                                j += 1
                            i += 1
                        if len(deduction) == 0:
                            total += closing
                        else:
                            deduction_list = []
                            deduction_list.append(deduction)
                            deduction = words(deduction_list, learned)
                            print(deduction)
                            total += closing
                            total += true_statement()
                            total += ' THUS I KNOW THAT ' + deduction[0]
                        print(str(total))
                        # if ('&' in operations) or ('|' in operations) or ('!' in operations):
                        #     more = []
                        #     for vary in variables:
                        #         if vary in facts:
                        #             print(true_statement() + " " + words(vary, combined))
                        #             more.append(words(vary, combined))
                        #     opening = '('
                        #     closing = ')'
                        #     combine_logic = ''
                        #     changed_operations = convert(operations)
                        #     for valid in changed_operations:
                        #         combine_logic += str(valid)
                        #     total = opening
                        #     i = 0
                        #     j = 0
                        #     while (i < len(more)):
                        #         total += more[i]
                        #         while (j < len(changed_operations)):
                        #             total += changed_operations[j]
                        #             j += 1
                        #         i += 1
                        #     print(concluding() + " " + str(total) + ')')
                    # rule case:
                    # else:
                        # total = ''
                        # if ('&' in operations) or ('|' in operations) or ('!' in operations):
                        #     more = []
                        #     for vary in variables:
                        #         if vary in facts:
                        #             more.append(words(vary, combined))
                        #     opening = '('
                        #     closing = ')'
                        #     combine_logic = ''
                        #     changed_operations = convert(operations)
                        #     for valid in changed_operations:
                        #         if valid == "BECAUSE ":
                        #             total += valid
                        #             changed_operations.remove(valid)
                        #         else:
                        #             total += opening
                        #     i = 0
                        #     j = 0
                        #     while (i < len(more)):
                        #         total += more[i]
                        #         while (j < len(changed_operations)):
                        #             total += changed_operations[j]
                        #             j += 1
                        #         i += 1






