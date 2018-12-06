import ctypes

lib = ctypes.cdll.LoadLibrary("./hello.so")

# in Python, Go's `*C.char` maps to `ctypes.c_char_p`
lib.Hello.restype = ctypes.c_char_p

print "%s" % lib.Hello()
