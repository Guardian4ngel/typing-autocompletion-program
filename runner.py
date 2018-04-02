import sys
from sys import stdin, stderr, stdout
import parameters as para
import functions as f
sep = chr(31)

def predict_review(trie):
    review_typed = ''
    while True:
        next_chars = stdin.readline().rstrip('\r\n')
        if len(next_chars) == 0:
            return
        review_typed += next_chars
        preds=f.predict(review_typed,trie)
        try:
            print('{}{}{}{}{}'.format(preds[0], sep, preds[1], sep, preds[2]))
            stdout.flush()
        except Exception:
            print(' {} {} '.format(sep, sep)) # in the event that anything weird happens, pass three blank predictions
            stdout.flush()

trie=f.train(para.training_sample_size,para.training_file)

while True:
    try:
        print('Predicting review.', file=stderr)
        predict_review(trie)
    except EOFError:
        sys.exit(0)
    except Exception as e:
        print(e, file=stderr)
        sys.exit(1)
