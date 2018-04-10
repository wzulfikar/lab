# docs: https://www.tensorflow.org/api_docs/python/tf/placeholder

import tensorflow as tf

print("- creating placeholder for 2 columns data with any number of rows")
placeholder = tf.placeholder(tf.float32, shape=[None, 2])

print("- creating computation `c` with placeholder")
c = placeholder

print("- creating tensorflow session")
s = tf.Session()

print("- running computation `c` with values for placeholder")
print("  result #1:", s.run(c, feed_dict={placeholder: [[1, 3]]}))
print("  result #2:", s.run(c, feed_dict={placeholder: [[5, 1], [2, 4]]}))

# this will fail because placeholder data is invalid.
# expected 2 columns but got 1 column only.
# change the args to 2 columns (ie. `[[3, 2]]`)
# and it will work.
try:
    print(s.run(c, feed_dict={placeholder: [[], []]}))
except ValueError as e:
    print("  result #3 (invalid):", e)

try:
    print(s.run(c, feed_dict={placeholder: [[2, 4, 1]]}))
except ValueError as e:
    print("  result #4 (invalid):", e)
