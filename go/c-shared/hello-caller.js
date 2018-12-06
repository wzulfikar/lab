var ffi = require("ffi");

const hello = ffi.Library("./hello.so", {
  // function Hello returns string ("string")
  // and receives no arguments (`[]`)
  Hello: ["string", []],
});

console.log(hello.Hello());
