# adapted from
# https://github.com/aymericdamien/TensorFlow-Examples/

from __future__ import absolute_import, division, print_function

import numpy as np
import tensorflow as tf
import tensorflow.contrib.eager as tfe

# eager execution, a define-by-run interface for tensorflow
#  to execute operations immediately (wihout tf session).
print("- enabling Eager execution..")
tfe.enable_eager_execution()
print("  done ✔")
print()

print("- defining constant tensors:")
a = tf.constant(2)
b = tf.constant(3)
print("  a = {}, b = {}".format(a, b))
print()

print("- running operations without tf.Session:")
print("  [ADD] a + b =", a + b)
print("  [MUL] a * b =", a * b)
print()

print("- creating Tensors and NumpyArray variables (for mixing operations):")
a = tf.constant([[6., 1.], [1., 0.]], dtype=tf.float32)
b = np.array([[4., 0.], [5., 1.]], dtype=np.float32)
print("  Tensor     `a`: [{} {}]".format(a[0], a[1]))
print("  NumpyArray `b`: [{} {}]".format(b[0], b[1]))
print()

add = a + b
print("- addition of Tensor & NumpyArray  (a + b):")
print("  [{} {}]".format(add[0], add[1]))
print()

mul = tf.matmul(a, b)
print("- multiplication (dot product) of Tensor `a` & NumpyArray `b`:")
print("  a * b = [{} {}]".format(mul[0], mul[1]))
print("""
  calculation steps:
    [a]      *    [b]                                    [ab]
  +------+     +------+
  | 6, 1 |     | 4, 0 |  →  6*4 + (1*5), 6*0 + (1*1)  → 29,  1
  | 1, 0 |     | 5, 1 |  →  1*4 + (0*5), 0*0 + (0*1)  →  4,  0
  +------+     +------+
""")
