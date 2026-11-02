import ipaddress


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def to_binary(ip):
    """Convert an IPv4 address into binary notation."""

    return ".".join(
        format(int(octet), "08b")
        for octet in str(ip).split(".")
    )


def get_host_info(network):
    """Return usable hosts, first host and last host."""

    if network.prefixlen == 32:
        return 1, network.network_address, network.network_address

    if network.prefixlen == 31:
        return 2, network.network_address, network.broadcast_address

    return (
        network.num_addresses - 2,
        network.network_address + 1,
        network.broadcast_address - 1
    )


# ============================================================
# IPV4 SUBNET CALCULATOR
# ============================================================

def calculate_subnet():

    print("\n" + "=" * 50)
    print("             IPV4 SUBNET CALCULATOR")
    print("=" * 50)

    try:
        user_input = input(
            "\nEnter an IPv4 network (e.g. 192.168.1.0/24): "
        )

        network = ipaddress.ip_network(user_input, strict=False)

        if network.version != 4:
            print("Error: Only IPv4 is supported.")
            return

        usable, first, last = get_host_info(network)

        print("\n--- NETWORK INFORMATION ---")

        print(f"Network Address:   {network.network_address}")
        print(f"Broadcast Address: {network.broadcast_address}")
        print(f"Subnet Mask:       {network.netmask}")
        print(f"Wildcard Mask:     {network.hostmask}")
        print(f"CIDR Notation:     /{network.prefixlen}")
        print(f"Total Addresses:   {network.num_addresses}")
        print(f"Usable Hosts:      {usable}")
        print(f"First Host:        {first}")
        print(f"Last Host:         {last}")

        print("\n--- BINARY REPRESENTATION ---")

        print(f"Network:   {to_binary(network.network_address)}")
        print(f"Mask:      {to_binary(network.netmask)}")
        print(f"Broadcast: {to_binary(network.broadcast_address)}")

    except ValueError as error:
        print(f"\nError: {error}")


# ============================================================
# FLSM SUBNET SPLITTER
# ============================================================

def split_network(network, subnet_count):
    """Divide an IPv4 network into equal-sized subnets."""

    if network.version != 4:
        raise ValueError("Only IPv4 networks are supported.")

    if subnet_count < 1:
        raise ValueError("Subnet count must be positive.")

    additional_bits = (subnet_count - 1).bit_length()
    new_prefix = network.prefixlen + additional_bits

    if new_prefix > 32:
        raise ValueError("Too many subnets requested.")

    return list(network.subnets(new_prefix=new_prefix))


def split_subnet():

    print("\n" + "=" * 50)
    print("               FLSM SUBNET SPLITTER")
    print("=" * 50)

    try:
        user_input = input("\nEnter parent network: ")
        network = ipaddress.ip_network(user_input, strict=False)

        subnet_count = int(input("How many subnets do you need? "))

        subnets = split_network(network, subnet_count)

        print(f"\n--- {len(subnets)} SUBNETS GENERATED ---")

        for index, subnet in enumerate(subnets, start=1):

            usable, first, last = get_host_info(subnet)

            print(f"\nSubnet #{index}")
            print(f"Network:   {subnet.network_address}")
            print(f"Broadcast: {subnet.broadcast_address}")
            print(f"CIDR:      /{subnet.prefixlen}")
            print(f"Mask:      {subnet.netmask}")
            print(f"Total IPs: {subnet.num_addresses}")
            print(f"Usable:    {usable}")
            print(f"Host range: {first} - {last}")

    except ValueError as error:
        print(f"\nError: {error}")


# ============================================================
# VLSM SUBNET ALLOCATOR
# ============================================================

def get_required_prefix(host_count):
    """Calculate the smallest conventional LAN subnet for a host count."""

    if host_count < 1:
        raise ValueError("Host count must be positive.")

    # Two additional addresses are reserved for network and broadcast.
    required_addresses = host_count + 2

    # Minimum block size is 4 addresses (a /30).
    block_size = max(
        4,
        1 << (required_addresses - 1).bit_length()
    )

    host_bits = block_size.bit_length() - 1

    return 32 - host_bits


def allocate_vlsm(network, requirements):
    """
    Allocate variable-sized IPv4 subnets.

    requirements format:
    [("Servers", 100), ("Office", 50), ("Guests", 20)]
    """

    if network.version != 4:
        raise ValueError("Only IPv4 networks are supported.")

    if not requirements:
        raise ValueError("At least one subnet is required.")

    for name, host_count in requirements:
        if not name.strip():
            raise ValueError("Subnet names cannot be empty.")

        if host_count < 1:
            raise ValueError("Host counts must be positive.")

    # Allocate the largest subnet first.
    sorted_requirements = sorted(
        requirements,
        key=lambda item: item[1],
        reverse=True
    )

    cursor = int(network.network_address)
    parent_end = int(network.broadcast_address)

    allocated_subnets = []

    for name, host_count in sorted_requirements:

        prefix = get_required_prefix(host_count)
        block_size = 1 << (32 - prefix)

        # Align the next network address to its block boundary.
        start = (
            (cursor + block_size - 1) // block_size
        ) * block_size

        end = start + block_size - 1

        if end > parent_end:
            raise ValueError(
                f"Not enough address space for subnet: {name}"
            )

        subnet = ipaddress.IPv4Network((start, prefix))

        allocated_subnets.append((name, subnet, host_count))

        cursor = end + 1

    return allocated_subnets


def vlsm_subnet():

    print("\n" + "=" * 50)
    print("                VLSM SUBNET ALLOCATOR")
    print("=" * 50)

    try:
        user_input = input("\nEnter parent network: ")
        network = ipaddress.ip_network(user_input, strict=False)

        requirements = []

        print("\nEnter subnet requirements.")
        print("Leave the name empty when finished.")

        while True:

            name = input("\nSubnet name: ").strip()

            if not name:
                break

            host_count = int(input("Required hosts: "))

            requirements.append((name, host_count))

        allocated = allocate_vlsm(network, requirements)

        print("\n--- VLSM ALLOCATION RESULTS ---")

        for index, (name, subnet, requested) in enumerate(
            allocated, start=1
        ):

            usable, first, last = get_host_info(subnet)

            print(f"\nSubnet #{index}: {name}")
            print(f"Network:        {subnet.network_address}")
            print(f"Broadcast:      {subnet.broadcast_address}")
            print(f"CIDR:           /{subnet.prefixlen}")
            print(f"Subnet Mask:    {subnet.netmask}")
            print(f"Requested Hosts: {requested}")
            print(f"Usable Hosts:   {usable}")
            print(f"First Host:     {first}")
            print(f"Last Host:      {last}")

    except ValueError as error:
        print(f"\nError: {error}")


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n" + "=" * 50)
        print("                     NETCALC")
        print("=" * 50)

        print("1. IPv4 Subnet Calculator")
        print("2. FLSM Subnet Splitter")
        print("3. VLSM Subnet Allocator")
        print("4. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            calculate_subnet()

        elif choice == "2":
            split_subnet()

        elif choice == "3":
            vlsm_subnet()

        elif choice == "4":
            print("\nExiting NetCalc. Goodbye!")
            break

        else:
            print("\nInvalid option. Please try again.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()