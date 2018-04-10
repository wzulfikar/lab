import tensorflow as tf

a = tf.constant([
    [1., 2.],
    [3., 1.]])
b = tf.constant([
    [True, False],
    [False, False],
    [True, True]])
c = tf.constant([
    [1, 3, 11, 41]])
d = tf.constant([
    [1., 2., 4., 2.],
    [1., 2., 1., 5.]])
e = tf.constant(3)

print("- showing shapes of valid Tensors:")
print("  shape of `a`:", a.dtype, a.shape)
print("  shape of `b`:", b.dtype, b.shape)
print("  shape of `c`:", c.dtype, c.shape)
print("  shape of `d`:", d.dtype, d.shape)
print("  shape of `e`:", d.dtype, e.shape)
print()

print("- showing shapes of invalid Tensors:")
try:
    f = tf.constant([
        [1., ],
        [1.0, 2.],
        [1.0, 2.]])
except ValueError as e:
    print("  - shape of `f` is invalid:\n   ", e)

try:
    g = tf.constant([
        [1., None]])
except TypeError as e:
    print("  - shape of `g` is invalid:\n   ", e)

try:
    h = tf.constant([
        [1.],
        [1.0, 2.]])
except ValueError as e:
    print("  - shape of `h` is invalid:\n   ", e)
