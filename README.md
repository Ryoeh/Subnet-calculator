# NetCalc — IPv4 Subnet Calculator

NetCalc is a command-line networking tool written in Python.
It provides IPv4 subnet calculations, FLSM subnet splitting,
and VLSM subnet allocation through a simple interactive interface.

The project uses Python's standard library and requires no
external dependencies.

## Features

### IPv4 Subnet Calculator
- Network address calculation
- Broadcast address calculation
- Subnet mask and wildcard mask
- CIDR notation
- Total address count
- Usable host count
- First and last usable host
- Binary representation of network information
- Support for /31 and /32 networks

### FLSM Subnet Splitter
- Divide an IPv4 network into equal-sized subnets
- Automatically calculate the required CIDR prefix
- Display network and broadcast addresses
- Display subnet masks and usable host ranges
- Round up to the next power-of-two subnet count

### VLSM Subnet Allocator
- Allocate subnets based on host requirements
- Automatically sort requests by size
- Calculate the smallest suitable subnet for each requirement
- Align network addresses to valid subnet boundaries
- Detect insufficient address space
- Display allocated network information

### Input Validation
- IPv4 address validation
- Invalid subnet handling
- Invalid host requirement handling
- Insufficient address space detection

## Requirements

- Python 3.9 or newer
- No external Python packages required

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/NetCalc.git
```

Navigate into the project directory:

```bash
cd NetCalc
```

## Usage

Run the application:

```bash
python main.py
```

The interactive menu provides three main tools:

1. IPv4 Subnet Calculator
2. FLSM Subnet Splitter
3. VLSM Subnet Allocator

## Examples

### 1. IPv4 Subnet Calculator

Input:

```text
192.168.1.0/24
```

Example output:

```text
Network Address:   192.168.1.0
Broadcast Address: 192.168.1.255
Subnet Mask:       255.255.255.0
Wildcard Mask:     0.0.0.255
CIDR Notation:     /24
Total Addresses:   256
Usable Hosts:      254
First Host:        192.168.1.1
Last Host:         192.168.1.254
```

### 2. FLSM Subnet Splitter

Input:

```text
Parent network: 192.168.1.0/24
Number of subnets: 4
```

Result:

| Subnet | Network | CIDR |
|---|---|---|
| 1 | 192.168.1.0 | /26 |
| 2 | 192.168.1.64 | /26 |
| 3 | 192.168.1.128 | /26 |
| 4 | 192.168.1.192 | /26 |

### 3. VLSM Subnet Allocator

Parent network:

```text
192.168.1.0/24
```

Requirements:

| Department | Required Hosts |
|---|---:|
| Servers | 100 |
| Office | 50 |
| Guests | 20 |

Example allocation:

| Department | Network | CIDR | Usable Hosts |
|---|---|---|---:|
| Servers | 192.168.1.0 | /25 | 126 |
| Office | 192.168.1.128 | /26 | 62 |
| Guests | 192.168.1.192 | /27 | 30 |

The largest subnet is allocated first to improve address-space utilization.

## Running Tests

NetCalc uses Python's built-in `unittest` framework.

Run all tests with:

```bash
python -m unittest -v
```

The test suite covers:

- Binary conversion
- IPv4 host calculations
- /31 and /32 handling
- FLSM subnet splitting
- VLSM allocation
- Invalid input handling
- Insufficient address space

## Technical Notes

- The project uses Python's `ipaddress` module for IPv4 network operations.
- Traditional LAN subnet allocations reserve network and broadcast addresses.
- /31 networks are handled according to point-to-point IPv4 conventions.
- /32 networks represent a single IPv4 address.
- VLSM allocations use conventional LAN subnet sizes, with /30 as the minimum.
- FLSM generates the smallest power-of-two number of equal-sized subnets
  that satisfies the requested count. It may therefore generate more
  subnets than requested.

## Project Structure

```text
NetCalc/
│
├── main.py
├── test_netcalc.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Technologies

- Python
- IPv4 Networking
- CIDR
- Subnetting
- FLSM
- VLSM
- Binary Representation
- Unit Testing

## License

This project is licensed under the **Ryoeh Proprietary License v1.2**.

All rights not expressly granted by the license are reserved. Viewing the source code does not grant permission to reuse, modify, reproduce, or redistribute it.

For the complete license terms, see the [Ryoeh Proprietary License v1.2](https://github.com/Ryoeh/Ryoeh-License/blob/main/versions/RYOEH-PROPRIETARY-LICENSE-v1.2.txt).

For permission requests, please open an [Issue](https://github.com/Ryoeh/Ryoeh-License/issues).
