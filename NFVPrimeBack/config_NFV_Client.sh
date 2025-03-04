files=$(ip netns delete NFV-client)
files=$(ip netns add NFV-client)
if [ $? != 0 ]; then
  echo "Netns NFV-client já criado."
else
  ip netns exec NFV-client ip link set dev lo up
  ip link add veth-ch0 type veth peer name veth-cn0
  ip link set veth-cn0 netns NFV-client
  ip netns exec NFV-client ip link set dev veth-cn0 up
  ip netns exec NFV-client ip link set veth-cn0 promisc on
  ip link set dev veth-ch0 up
  ip link set veth-ch0 promisc on
  ip link set dev veth-ch0 address 16:1a:a7:f2:ac:36
  ip addr add 10.2.1.100/24 dev veth-ch0
  ip netns exec NFV-client route add -host 10.2.1.100 dev veth-cn0
  ip netns exec NFV-client ip link set dev veth-cn0 address 16:1a:a7:f2:ac:37
  ip netns exec NFV-client ip addr add 10.2.2.100/24 dev veth-cn0
  route add -host 10.2.2.100 dev veth-ch0
  ip netns exec NFV-client route add default gw 10.2.2.100 veth-cn0
  echo "Criou NFV-Client"
fi