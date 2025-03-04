files=$(ip netns delete teste)
files=$(ip netns add teste)
if [ $? != 0 ]; then
  echo "Netns teste já criado."
else
  ip netns add teste
  ip netns exec teste ip link set dev lo up
  ip link add veth-hpg0 type veth peer name veth-npg0
  ip link set veth-npg0 netns teste
  ip netns exec teste ip link set dev veth-npg0 up
  ip netns exec teste ip link set veth-npg0 promisc on
  ip link set dev veth-hpg0 up
  ip link set veth-hpg0 promisc on
  ip addr add 10.1.1.100/24 dev veth-hpg0
  ip netns exec teste route add -host 10.1.1.100 dev veth-npg0
  ip netns exec teste ip addr add 10.1.2.100/24 dev veth-npg0
  route add -host 10.1.2.100 dev veth-hpg0
fi