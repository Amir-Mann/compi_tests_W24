import re
import os
import argparse
import random
import string

RULES = {
    "@Prog": [
        "@Stas\n"
    ],
    "@Stas": [
        "@Stat\n",
        "@Stas@Stat\n",
        "@Stas@Stat//$COMENT\n"
    ],
    "@Stat": [
        "{\n@Stas\n}",
        "@Type $ID____;",
        "@Type $ID____ = @Exp_;",
        "$ID____ = @Exp_;",
        "@Call;",
        "return;",
        "if ( @Exp_ )\n@Stat",
        "if ( @Exp_ )\n@Stat\nelse\n@Stat",
        "while ( @Exp_ )\n@Stat",
        "break;",
        "continue;"
    ],
    "@Call": [
        "$ID____(@Exp_)"
    ],
    "@Type": [
        "int",
        "byte",
        "bool"
    ],
    "@Exp_": [
        "( @Exp_ )",
        "@Exp_ + @Exp_",
        "@Exp_ - @Exp_",
        "@Exp_ * @Exp_",
        "@Exp_ / @Exp_",
        "$ID____",
        "@Call",
        "$NUM___",
        "$NUM___ b",
        "$STRING",
        "true",
        "false",
        "$ID____",
        "$NUM___",
        "$NUM___ b",
        "$STRING",
        "true",
        "false",
        "not @Exp_",
        "@Exp_ and @Exp_",
        "@Exp_ or @Exp_",
        "@Exp_ $RELOP_ @Exp_",
        "( @Type ) @Exp_"
    ]
}




def safe_makedir(path):
    if os.path.isdir(path) or path == "":
        return

    parent_dir = os.path.split(path)[0]
    safe_makedir(parent_dir)
    os.mkdir(path)


def random_id():
    return random.choice(list("xyzaij") + ["".join([random.choice(string.ascii_letters)] + random.choices(string.ascii_letters+string.digits, k = random.randint(1, 10)))])


def random_num():
    return random.choice(list(map(str, range(10))) + [str(random.randint(2, 13) ** random.randint(3, 15))])


def random_string():
    return '"' + random.choice([
        "you're",
        "a wizard",
        "harry",
        "".join([random.choice(list("abcdefgh ") + ["\\r", "\\n", "\\t", "\\\"", "\\\\"])])
    ]) + '"'


def random_relop():
    return random.choice(["==", "!=", "<", ">", "<=", ">="])


def random_comment():
    return "Your " + random.choice([
            "code", "sex life", "github", "mama", "partner", "food", "grammer", "laptop", "pp"
        ]) + " " + random.choice([
            "is un readable.", "is none existent.", "makes recruters start smoking", "so FAT when she jumps into the ocean the ocean jumps out.",
            "hates the way you call functions.", "is the only thing more ASHCENAZY then you.", "should go back to first grade.", "looks like a piazza box.",
            "is smaller then required to pass these tests."
        ]) + random.choice([" <3", " ^^", " uwu", " mother fucker...", "..", " :)", " :(", " bitch."])


RANDOM_REPLACEMENT = {
    "$ID____": random_id,
    "$NUM___": random_num,
    "$STRING": random_string,
    "$RELOP_": random_relop,
    "$COMENT": random_comment
}


def main():
    parser = argparse.ArgumentParser(description="Script for generating test cases.")
    parser.add_argument("amount", type=int, nargs='?', default=50, 
                        help="Specifies the number of test cases to generate. Default is 50.")
    parser.add_argument("--start", type=int, default=1, 
                        help="Sets the starting number for test case generation. Useful for continuing from a previous set. Default is 1.")
    parser.add_argument("--allow_errors", action='store_true', default=False, 
                        help="Allows the generation of test cases with intentional errors. Useful for testing error handling. Default is False.")
    parser.add_argument("--tests_dir", type=str, default="tests", 
                        help="Specifies the directory where test cases will be stored. Default directory is 'tests'.")
    parser.add_argument("--reference_code", type=str, default="", 
                        help="Reference code ('./hw.out' file) to use to generate output files. Default would not generate outputs.")
    parser.add_argument("--max_test_length", type=int, default=1000, 
                        help="Maximal rule derivations before not allowing any recursive ones")
    parser.add_argument("--min_test_length", type=int, default=10, 
                        help="Minimum amount of statements in test")
    parser.add_argument("--dont_generate", action='store_true', default=False, 
                        help="Skips the whole generateion process and only creates new .out files.")

    args = parser.parse_args()
    

    safe_makedir(args.tests_dir)
    next_precentile_to_print = 0
    for test_num in range(args.start, args.start + args.amount):
        if (test_num - args.start) / args.amount > next_precentile_to_print:
            print(f"finshed test {test_num} for {test_num - args.start} out of {args.amount} tests.")
            next_precentile_to_print += 0.1
        test_in = ""
        if args.dont_generate:
            pass
        elif args.allow_errors:
            raise NotImplementedError("allow errors not implemnted")
        else:
            test_in = RULES["@Prog"][0] * args.min_test_length
            count_vars = args.min_test_length
            derivation_num = 0
            while count_vars > 0:
                var_to_derive_num = random.randint(0, count_vars - 1)
                var_to_derive_index = -1
                for i in range(var_to_derive_num + 1):
                    var_to_derive_index = test_in.find("@", var_to_derive_index + 1)
                var_to_derive = test_in[var_to_derive_index:var_to_derive_index+5]
                replacement = random.choice(RULES[var_to_derive])
                while derivation_num > args.max_test_length and var_to_derive in replacement :
                    replacement = random.choice(RULES[var_to_derive])
                test_in = test_in[:var_to_derive_index] + replacement + test_in[var_to_derive_index+5:]

                count_vars = len(re.findall("@", test_in))
                derivation_num += 1

            count_needs_choosing = len(re.findall(r"\$", test_in))
            while count_needs_choosing:
                i = test_in.find("$")
                test_in = test_in[:i] + RANDOM_REPLACEMENT[test_in[i: i + 7]]() + test_in[i+7:]

                count_needs_choosing -= 1
        
        test_in_path = os.path.join(args.tests_dir, f"test{test_num}.in")
        if not args.dont_generate:
            with open(test_in_path, "w") as test_in_file:
                test_in_file.write(test_in)

        if args.reference_code != "":
            test_out_path = os.path.join(args.tests_dir, f"test{test_num}.out")
            os.system(f'{args.reference_code} < {test_in_path} > {test_out_path}')



if __name__ == '__main__':
    main()