files=$(ip netns delete NFVPrime)
files=$(ip netns add NFVPrime)
if [ $? != 0 ]; then
  echo "Netns NFVPrime já criado."
else
  ip netns add NFVPrime
  ip netns exec NFVPrime ip link set dev lo up
  ip link add veth-hpg0 type veth peer name veth-npg0
  ip link set veth-npg0 netns NFVPrime
  ip netns exec NFVPrime ip link set dev veth-npg0 up
  ip netns exec NFVPrime ip link set veth-npg0 promisc on
  ip link set dev veth-hpg0 up
  ip link set veth-hpg0 promisc on
  ip addr add 10.1.1.100/24 dev veth-hpg0
  ip netns exec NFVPrime route add -host 10.1.1.100 dev veth-npg0
  ip netns exec NFVPrime ip addr add 10.1.2.100/24 dev veth-npg0
  route add -host 10.1.2.100 dev veth-hpg0
  echo "Criou NFVPrime"
fi