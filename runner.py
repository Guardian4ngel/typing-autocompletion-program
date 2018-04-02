import sys
from sys import stdin, stderr, stdout
import parameters as para
import functions as f
sep = chr(31)

def predict_review(trie):
    review_typed = ''
    while True:
        next_chars = stdin.readline().rstrip('\r\n')
        if len(next_chars) == 0: # the grader will pass a blank line when done typing this review.
            return
        review_typed += next_chars
        ### BEGIN CHANGES HERE
        preds=f.predict(review_typed,trie)
        #print(next_chars,file=stderr)
        #print(preds,file=stderr)
        #### END USER CHANGES HERE 
        try:
            print('{}{}{}{}{}'.format(preds[0], sep, preds[1], sep, preds[2]))
            stdout.flush()
        except Exception:
            print(' {} {} '.format(sep, sep)) # in the event that anything weird happens, pass three blank predictions
            stdout.flush()

trie=f.train(para.training_sample_size,para.review)

while True:
    try:
        print('Predicting review.', file=stderr)
        metadata = stdin.readline().rstrip('\r\n').split(',')
        product_id, user_id, unix_date, rating = metadata
        ### TODO: you may wish to modify arguments to predict_review.
        predict_review(trie)
    except EOFError:
        sys.exit(0)
    except Exception as e:
        print(e, file=stderr)
        sys.exit(1)
