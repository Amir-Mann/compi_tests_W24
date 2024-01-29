## Tests failing survay
If you fail a test, you can fill this survay:

https://docs.google.com/forms/d/e/1FAIpQLSfhSETdznSglj7sJN3sLbz4zBocgYPbdEQe27xGnK4PXr_oKQ/viewform?usp=sf_link

The use is that problem with the tests themselves might be discuvered this way.

If you know the issue causing the failure on this test and line you can publish it on the form.

If you fail a test and someone published the cause you would be able to see it.



## Running the tests

Use python3.6 or above



running examples: 
Note that all examples assume you are running from the runner.py directory.

run all tests and abort on first fail:

`python3 runner.py ../compy_hw1/hw1.out`

run all tests and continue when failing:

`python3 runner.py ../compy_hw1/hw1.out --dont_abort`

run tests 1, 2 and 3:

`python3 runner.py ../compy_hw1/hw1.out --test_num 1 2 3`

remove all .res files from the tests dir:

`python3 runner.py ../compy_hw1/hw1.out --clean`

run all tests from assignment 2 (not implemented):

`python3 runner.py ../compy_hw2/hw2.out --hw_num 2`



## Tests structure:

tests 0 - 49: simple tests without strings, comments or expected errors.

tests 50 - 99: tests with mainly strings

tests 100 - 109: tests with strings and comments

tests 110 - 999: tests for errors and their edge cases
