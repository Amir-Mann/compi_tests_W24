import os
import argparse
import random


DIGITS = [str(d) for d in range(0, 10)]
LETTERS = [chr(c) for c in range(ord("a"), ord("z") + 1)] + [chr(c) for c in range(ord("A"), ord("Z") + 1)]
WHITE_SPACES = [" ", "\t", "\n", "\r"]
SAVED_WORDS = ["void", "int", "byte", "b", "bool", "and", "or", "not", "true", "false", "return", "if", "else", "while", "break", "continue"]
OPS_AND_SYMBOLS = [";", "(", ")", "{", "}", "=","==","!=","<",">","<=",">=", "+", "-", "*", "/"]
INTS = [str(random.randint(0, 13) ** random.randint(1, 15)) for i in range(1000)] + ["0" + str(random.randint(0, 11)) + "0"]
IDS = ["".join([random.choice(LETTERS)] + 
               [random.choice(LETTERS + DIGITS) 
                for j in range(0, random.randint(0, 4) ** random.randint(1, 3))])
        for i in range(1000)]
CHOOSE_TWICE = lambda list_of_lists: random.choice(random.choice(list_of_lists))


def safe_makedir(path):
    if os.path.isdir(path) or path == "":
        return

    parent_dir = os.path.split(path)[0]
    safe_makedir(parent_dir)
    os.mkdir(path)

def rand_upper(aa):
    return random.choice([aa[0], aa[0].upper()]) + random.choice([aa[1], aa[1].upper()])

def generate_sting(with_new_lines):
    string = '"'
    escapes = ["\\t", "\\\\", "\\\"", "\\\\", "\\\""]
    if with_new_lines:
        escapes += ["\\r", "\\n"]
    for i in range(0, random.randint(0, 40)):
        string += CHOOSE_TWICE([
            escapes,
            escapes,
            ["\\x" + rand_upper(hex(i)[2:].zfill(2)) for i in range(0, 128)],
            [chr(c) for c in range(0x20, 0x22)] + [chr(c) for c in range(0x23, 0x5C)] + [chr(c) for c in range(0x5D, 0x7F)],
            [" ", "\t"],
            LETTERS + DIGITS
        ])
    string += '"'
    return string

def main():
    parser = argparse.ArgumentParser(description="Script for generating test cases.")
    parser.add_argument("amount", type=int, nargs='?', default=50, 
                        help="Specifies the number of test cases to generate. Default is 50.")
    parser.add_argument("--start", type=int, default=1, 
                        help="Sets the starting number for test case generation. Useful for continuing from a previous set. Default is 1.")
    parser.add_argument("--allow_errors", action='store_true', default=False, 
                        help="NOT IMPLEMENTED! Allows the generation of test cases with intentional errors. Useful for testing error handling. Default is False.")
    parser.add_argument("--test_strings", action='store_true', default=False, 
                        help="Includes string-based test cases. Default is False.")
    parser.add_argument("--test_numbers", action='store_true', default=False, 
                        help="Includes number-based test cases. Default is False.")
    parser.add_argument("--test_comments", action='store_true', default=False, 
                        help="NOT IMPLEMENTED! Includes test cases with comments for testing comment handling. Default is False.")
    parser.add_argument("--tests_dir", type=str, default="tests", 
                        help="Specifies the directory where test cases will be stored. Default directory is 'tests'.")
    parser.add_argument("--reference_code", type=str, default="", 
                        help="Reference code ('./hw.out' file) to use to generate output files. Default not would generate outputs.")
    parser.add_argument("--maximal_test_length", type=int, default=1000, 
                        help="Maximal amount of tokens in a test")


    args = parser.parse_args()
    

    test_possible_tokens = [WHITE_SPACES, WHITE_SPACES, WHITE_SPACES, WHITE_SPACES,
        SAVED_WORDS,
        OPS_AND_SYMBOLS,
        IDS, IDS
    ]
    if args.test_strings:
        test_possible_tokens.append(INTS)
    safe_makedir(args.tests_dir)
    next_precentile_to_print = 0
    for test_num in range(args.start, args.start + args.amount):
        if test_num / args.amount > next_precentile_to_print:
            print(f"finshed {test_num} out of {args.amount} tests.")
            next_precentile_to_print += 0.1
        test_in = ""
        for token in range(0, random.randint(1, args.maximal_test_length)):
            if args.test_strings and random.random() < 0.5:
                test_in += generate_sting(token > args.maximal_test_length / 4)
                continue
            if args.test_comments and random.random() < 0.1:
                test_in += "//"
                continue
            test_in += CHOOSE_TWICE(test_possible_tokens)
        test_in_path = os.path.join(args.tests_dir, f"test{test_num}.in")
        with open(test_in_path, "w") as test_in_file:
            test_in_file.write(test_in)

        if args.reference_code != "":
            test_out_path = os.path.join(args.tests_dir, f"test{test_num}.out")
            os.system(f'{args.reference_code} < {test_in_path} > {test_out_path}')





if __name__ == '__main__':
    main()