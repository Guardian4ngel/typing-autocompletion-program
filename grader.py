import pandas as pd
import subprocess
import sys
from sys import stderr
import parameters as para

holdout_data = [lines.strip() for lines in open(para.test_file, 'r',encoding="utf8")]
sep = chr(31)

invocations = 1
# Usage: python grader.py python -u runner.py
process = subprocess.Popen(sys.argv[1:], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
for i in range(para.test_size):
    review = holdout_data[i].lower()
    j = 1
    # Type the first character and start hunting for predictions
    process.stdin.write(bytes('{}\n'.format(review[0]), 'utf8'))
    process.stdin.flush()
    stdoutdata = process.stdout.readline().decode('utf8').rstrip('\r\n')
    while True:
        next_chars = 1
        try:
            review_typed, review_to_type = (review[:j], review[j:])
            pred1, pred2, pred3 = sorted(stdoutdata.lower().split(sep), key=len, reverse=True)
            if review_to_type.startswith(pred1) and pred1 != '':
                next_chars = len(pred1)
            elif review_to_type.startswith(pred2) and pred2 != '':
                next_chars = len(pred2)
            elif review_to_type.startswith(pred3) and pred3 != '':
                next_chars = len(pred3)
            else:
                next_chars = 1
        except IndexError as e:
            next_chars = 1

        if j + next_chars >= len(review):
            process.stdin.write(bytes('\n', 'utf8'))
            process.stdin.flush()
            break # the review has been completely typed
        process.stdin.write(bytes('{}\n'.format(review[j:j + next_chars]), 'utf8'))
        process.stdin.flush()
        stdoutdata = process.stdout.readline().decode('utf8').rstrip('\r\n')
        j += next_chars
        invocations += 1


process.terminate()
print('Terminated in {} invocations of predict.'.format(invocations))
