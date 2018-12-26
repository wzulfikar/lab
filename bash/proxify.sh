proxify() {
  if [ -z "$1" ]
  then
    echo "proxify - export env vars for proxy"
    echo "usage: proxify <proxy server>|off"
    echo "example: proxify 192.168.0.101:8080"
    return
  fi

  proxyserver="$1"
  if [ "$proxyserver" = "off" ]
  then
    proxyserver=""
    echo "proxy vars cleared"
  else
    echo "proxy vars set to $1"
  fi

  export http_proxy="$proxyserver"
  export https_proxy="$proxyserver"

  export HTTP_PROXY="$proxyserver"
  export HTTPS_PROXY="$proxyserver"
}
