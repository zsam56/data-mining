import math
import csv
import HW_05_Samuelson_Zachary_Classifier as classifier

"""
HW05B
Zachary Samuelson
3/2017

This program will create a decision tree
program
"""

VALIDATE = False

TRAINING_FILE = "HW_05BB_DecTree_Training__v200.csv"
TESTING_FILE = "HW_05B_DecTree_Testing___v200.csv"
VALIDATION_FILE = "HW_05B_DecTree_validation_data___v200.csv"
DEC_TREE_OUTPUT = "HW_05_Samuelson_Zachary_MyClassifications.txt"

DECISION_TREE_PROGRAM = "HW_05_Samuelson_Zachary_Classifier.py"

output = open(DECISION_TREE_PROGRAM, "w")

attr1_index = 0
attr2_index = 1
attr3_index = 2
attr4_index = 3
class_index = 4

# convert the csv file to our list
with open(TRAINING_FILE, 'r') as f:
    reader = csv.reader(f)
    data_list = list(reader)

# remove the headers from the list
del data_list[0]

# organize the data into columns
attr1 = []
attr2 = []
attr3 = []
attr4 = []
classList = []
for attr in data_list:
    attr1.append(attr[0])
    attr2.append(attr[1])
    attr3.append(attr[2])
    attr4.append(attr[3])
    classList.append(attr[4])

#this will be a list of tuples with the
#best attribute of each node and it's corresponding threshold
attr_threshold_list = []

def main():

    generate_decision_tree(data_list)
    print(attr_threshold_list)
    output.write("import csv\n")
    output.write("\"\"\"Decision Tree Program\"\"\"\n")
    # write the prologue
    emit_prologue()
    # write the actual tree
    emit_body(attr_threshold_list, 1)
    # write the epilogue
    emit_epilogue()
    output.close()
    #run the classifier
    classifier.main()
    if (VALIDATE):
        validate_testing()

"""
This function with validate the output file
against the
"""
def validate_testing():
    with open(TRAINING_FILE, 'r') as f:
        reader = csv.reader(f)
        test_data = list(reader)

    del test_data[0]
    dec_tree_output = open(DEC_TREE_OUTPUT, "r")
    lines = dec_tree_output.readlines()
    correct = 0
    index = 0
    print(lines)
    for row in test_data:
        if (int(row[class_index]) == int(lines[index].strip())):
            correct += 1
        index += 1
    print("CORRECT: " + str(correct))
    print("Correction percentage: " + str(correct/len(lines)))


"""
Create the body (tree itself)
"""
def emit_body(params, tabs):
    tabs = 2
    index = 0
    for leaf in params:
        if leaf[0] != -1:
            print_if(leaf, tabs)
            tabs += 1
        else:
            if (index != (len(params)-1)):
                print_return(leaf, tabs)
                if (index+1 != (len(params)-1)):
                    print_else(tabs - 1)
            else:
                print_else(2)
                print_return(leaf, 3)

        index += 1

"""
Print an if statement
"""
def print_if(leaf, tabs):
    output.write("\t" * tabs + "if (float(item[" + str(leaf[0]) + "]) <= " + str(leaf[1]) + "):\n")

"""
Print an else statement
"""
def print_else(tabs):
    output.write("\t" * tabs + "else: \n")

"""
Print a return statement
"""
def print_return(leaf, tabs):
    output.write("\t" * tabs + "output.write( str(" + str(leaf[1]) + ")+\"\\n\")"+ "\n")

"""
Generate the decision tree
"""
def generate_decision_tree(branch):

    #stopping criteria
    num_one = 0.0
    num_zero = 0.0
    #check to see if 95% of my data already
    #belongs to one class
    for row in branch:
        if (int(row[class_index]) == 1):
            num_one += 1
        else:
            num_zero += 1

    #stopping critieria:
    #if 95% belongs to one class, stop
    if ((num_one/(len(branch)*1.0) >= .95) |
            (num_zero/(len(branch)*1.0) >= .95)):
        #stop
        print("Node found: \n")
        # I'm adding (-1, num_choice) to my attr_threshold list so that
        # I know when I've reached a node when going back through it
        # num_choice is the choice to be made at that node
        if (num_zero > num_one):
            num_choice = 0
        else:
            num_choice = 1
        attr_threshold_list.append((-1, num_choice))
        return branch

    attr_list = [attr1, attr2, attr3, attr4]

    print("\n\nSplit\n")
    best_attr_index = 0
    best_attr = []
    best_entropy = 1
    best_threshold = 0
    index = 0
    #find the attribute with the best split
    for attr in attr_list:
        for threshold in attr:
            # get the table for this threshold split
            truth_table = calculate_truth_table(branch, index, threshold)
            # calculate the weighted entropy of this split
            entropy = calculate_entropy(truth_table)
            if (entropy < best_entropy):
                best_entropy = entropy
                best_threshold = threshold
                best_attr_index = index
                best_attr = attr
        index += 1

    split1 = []
    split2 = []
    #create the new lists based on the best threshold
    for row in branch:
        if (row[best_attr_index] <= best_threshold):
            split1.append(row)
        else:
            split2.append(row)

    print("Best attribute index: " + str(best_attr_index))
    print("Best threshold: " + str(best_threshold))
    print("Best entropy: " + str(best_entropy))

    attr_threshold_list.append((best_attr_index, best_threshold))

    #Recursively call
    print("Left Branch\n")
    generate_decision_tree(split1)

    print("Right Branch\n")
    generate_decision_tree(split2)

"""
Creates the prologue for the decision tree program
"""
def emit_prologue():
    output.write("\ndef main():\n")
    # write the code for reading in the input file
    output.write("\t# convert the csv file to our list\n" +
                     "\twith open('" + VALIDATION_FILE + "', 'r') as f:\n" +
                     "\t\treader = csv.reader(f)\n" +
                     "\t\tdata_list = list(reader)\n" +
                     "\tdel data_list[0]\n\n" +
                     "\toutput = open(\"HW_05_Samuelson_Zachary_MyClassifications.txt\", \"w\")\n")

    output.write("\tfor item in data_list:\n")

"""
Creates the epilogue for the decision tree program
"""
def emit_epilogue():
    output.write("\toutput.close()")
    output.write("main()")

def calculate_entropy():
    return

"""
Create a truth table
for a given attribute
"""
def calculate_truth_table(branch, attr_index, threshold):
    # set up "table" variables
    true_greater = 0.0
    true_less = 0.0
    false_less = 0.0
    false_greater = 0.0
    index = 0
    for entry in branch:
        if (entry[attr_index] <= threshold) & (int(entry[class_index]) == 1):
            true_less += 1
        elif (entry[attr_index] <= threshold) & (int(entry[class_index]) == 0):
            false_less += 1
        elif (entry[attr_index] > threshold) & (int(entry[class_index]) == 0):
            false_greater += 1
        else:
            true_greater += 1

        index += 1


    table = [false_less, false_greater,
             true_less, true_greater]

    # table set up as follows:
    # {!class & less} |{!class & greater}
    # {class & less}  |{class & greater}

    return table

"""
calculate the entropy of
a table of values
"""
def calculate_entropy(table):
    # table set up as follows:
    # {!attribute & !stopped}|{attribute & !stopped}
    # {!attribute & stopped  |{attribute & stopped}
    total = table[0] + table[1] + table[2] + table[3]

    #calculate attribute = NO
    if ((table[0] + table[2]) == 0):
        num1 = 0
        num2 = 0
    else:
        less_zero = table[0]/(table[0]+table[2])
        if (less_zero == 0):
            num1 = 0
        else:
            num1 = (-1 * (less_zero * (math.log(less_zero, 2))))

        less_one = table[2]/(table[0]+table[2])
        if (less_one == 0):
            num2 = 0
        else:
            num2 = (-1 * (less_one*(math.log(less_one, 2))))

    less = num1 + num2

    #calculate attribute = YES
    if ((table[1]+table[3] == 0)):
        num1 = 0
        num2 = 0
    else:
        greater_zero = table[1] / (table[1] + table[3])
        if (greater_zero == 0):
            num1 = 0
        else:
            num1 = (-1 * (greater_zero * (math.log(greater_zero, 2))))

        greater_one = table[3] / (table[1] + table[3])
        if (greater_one == 0):
            num2 = 0
        else:
            num2 = (-1 * (greater_one * (math.log(greater_one, 2))))

    greater = num1 + num2

    #calculate weighted entropy
    weighted_entropy = (((table[0] + table[2]) / total) * less) + \
                       (((table[1] + table[3]) / total) * greater)

    return weighted_entropy


main()
