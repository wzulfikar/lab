require 'ffi'

module Hello
  extend FFI::Library
  ffi_lib './hello.so'

  # function Hello receives no argument (`[]`)
  # and returns string (`:string`)
  attach_function :Hello, [], :string
end

print Hello.Hello()
