

import re
import os
import sys
import argparse


def get_test_num(test_path):
    return int(re.findall(r"\d+", test_path)[-1])


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    parser = argparse.ArgumentParser(description="Runs all test cases for a spesific hw assignment.")
    parser.add_argument("path_to_code", type=str,
                        help="The path to the code to run, for example '../hw1/hw1.out'.")
    parser.add_argument("--hw_num", type=int, default=1, nargs='?' ,
                        help="Which assignment is it. default is 1")
    parser.add_argument("--test_num", type=int, default=None, nargs='+',
                        help="Test number(s) to run, if not spesified will run all available tests")
    parser.add_argument("--path_to_save_results", type=str, default=None,
                        help="The path to save result files of your code, default is in the tests dir.")
    parser.add_argument("--dont_abort", action='store_true', default=False, 
                        help="If a test case fails continue to the next one. Default would abort.")
    parser.add_argument("--clean", action='store_true', default=False, 
                        help="Remove all .res files from path_to_save_results(or tests dir if uspesified) instead of testing.")    
    
    args = parser.parse_args()

    tests_dir = os.path.join(f"hw{args.hw_num}", "tests")
    if not os.path.isdir(tests_dir):
        raise(RuntimeError("tests dir doesnt exist, probably invalid --hw_num, see --help for information."))
    results_dir = args.path_to_save_results if args.path_to_save_results else tests_dir

    if args.clean:
        removed_files = 0
        for filename in os.listdir(results_dir):
            path = os.path.join(results_dir, filename)
            if filename[-4:] == ".res" and os.path.isfile(path):
                os.system(f"rm {path}")
                if not os.path.isfile(path):
                    removed_files += 1
        print(f"Removed {removed_files} .res files.")
        exit()

    files = os.listdir(tests_dir)
    in_paths = sorted([os.path.join(tests_dir, f) for f in files if f[-3:] == ".in"], 
                      key=get_test_num)
    failed_tests = 0
    passed_tests = 0
    for in_path in in_paths:
        test_num = get_test_num(in_path)
        if args.test_num and test_num not in args.test_num:
            continue
        print(f"Running test {test_num}.", end=" ")
        res_path = os.path.join(results_dir, f"test{test_num}.res")
        out_path = os.path.join(tests_dir,   f"test{test_num}.out")
        os.system(f"{args.path_to_code} < {in_path} > {res_path}")
        if not os.path.isfile(res_path):
            print(f"{bcolors.FAIL}Failed{bcolors.ENDC} to generate results file!")
            if not args.dont_abort:
                exit()
            failed_tests += 1
            continue
        with open(res_path, "r") as res_file, open(out_path, "r") as out_file:
            for i, (res_line, out_line) in enumerate(zip(res_file, out_file)):
                if res_line == out_line:
                    continue
                print(f"{bcolors.FAIL}Failed{bcolors.ENDC} do to diff in line {i}!")
                print(f" Your output is:\n{res_line}\n Expected output is:\n{out_line}")
                print(f"You can use this google forms to see how many have the same problem (report 'test={test_num}, line={i}''):")
                print("https://docs.google.com/forms/d/e/1FAIpQLSfhSETdznSglj7sJN3sLbz4zBocgYPbdEQe27xGnK4PXr_oKQ/viewform?usp=sf_link")
                if not args.dont_abort:
                    exit()
                failed_tests += 1
                break
            else:
                print(f"{bcolors.OKGREEN}Passed!{bcolors.ENDC}")
                passed_tests += 1
    message = ""
    if passed_tests:
        message += f"{bcolors.OKGREEN}Passed {passed_tests}{bcolors.ENDC} tests. "
    if failed_tests:
        message +=    f"{bcolors.FAIL}Failed {failed_tests}{bcolors.ENDC} tests. "

    print(message)

if __name__ == '__main__':
    main()