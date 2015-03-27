from __future__ import print_function
import sys
import os
import tempfile
import subprocess
import shlex

class Test(object):

    def __init__(self, name=None, email=None):
        self.tests = dict()
        self.marks_for_questions = dict()
        self.test_marks = dict()
        self.name = name
        self.email = email

    def register(self, name, email):
        if not '@' in email:
            return('Usage: register("Real Name", "email@somewhere.ac.za")')
        self.name = name
        self.email = email
        return("Thank you " + self.name)

    def add_test(self, question, test, marks):
        self.tests[question] = test
        self.marks_for_questions[question] = marks

    def run_test(self, question, func):
        if question not in self.tests:
            print("Unknown test", question)
        else:
            try:
                self.tests[question](func)
                marks = self.marks_for_questions[question]
            except AssertionError:
                print("Incorrect")
                self.test_marks[question] = 0
            else:
                print("Correct")
                self.test_marks[question] = marks

    def total_marks(self):
        total = 0
        for question in self.test_marks:
            total += self.test_marks[question]
        return total

    def max_marks(self):
        total = 0
        for question, mark in self.marks_for_questions.items():
            total += mark
        return total

def test_multiply(func):
    multiply = func
    assert multiply(1,1) == 1
    assert multiply(2,2) == 4
    assert multiply(4,0) == 0

def test_product_of(func):
    product_of = func
    assert product_of([1,2]) == 2
    assert product_of([2,2,2]) == 8
    assert product_of([-1,-1]) == 1

def test_mol_weight(func):
    mol_weight = func
    assert int(mol_weight('GATACCA')) == 2089
    assert int(mol_weight('C')) == 227
    assert int(mol_weight('')) == -61

def test_longest_line(func):
    longest_line = func
    assert longest_line('sample.txt') == 'GGCTGATTGAGCTAACCGCAAAACCGCCTTAGGCCTGATACGTTGCGTGGTGGCGTGTC\n'

def test_deduplicate(func):
    deduplicate = func
    data = """        COL1A1
            MED12
            IREB2
            GDF9
            RXRG
            CBFB
            IREB2
            TUBB
    """    
    data_file = tempfile.NamedTemporaryFile(delete=False)
    data_file.write(data)
    data_file.close()
    expected = ['CBFB', 'COL1A1', 'GDF9', 'IREB2', 'MED12', 'RXRG', 'TUBB']
    try:
        assert expected == sorted(deduplicate(data_file.name))
    except AssertionError:
        # cleanup
        os.remove(data_file.name)
        # re-raise the exception
        raise

def run_count_name(filename, protein_name):
    cmd_str = 'bin/count_name.py {} {}'.format(filename, protein_name)
    cmd = shlex.split(cmd_str)
    output_file = tempfile.NamedTemporaryFile(delete=False)
    return_code = subprocess.call(cmd, stdout=output_file, stderr=output_file)
    output_file.close()
    if return_code != 0:
        os.remove(output_file.name)
        return None
    else:
        input_file = open(output_file.name)
        line = input_file.readline()
        fields = line.rstrip().split()
        count = int(fields[1])
        return count

def test_count_name(func):
    try:
        assert run_count_name('names.txt', 'IREB2') == 3
        assert run_count_name('names.txt', 'RXRG') == 6
    except OSError as e:
        raise AssertionError("Test failed: {}".format(e.strerror))

python_test = Test()
python_test.add_test(1, test_multiply, 2)
python_test.add_test(2, test_product_of, 3)
python_test.add_test(3, test_mol_weight, 5)
python_test.add_test(4, test_longest_line, 5)
python_test.add_test(5, test_deduplicate, 6)
python_test.add_test(6, test_count_name, 4)