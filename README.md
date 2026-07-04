# PLC Communication using Manual Modbus ASCII

A Python project that communicates with a PLC using the **Modbus ASCII protocol** over a serial connection. Instead of relying on Modbus libraries, this project manually constructs Modbus ASCII frames, calculates the LRC checksum, transmits requests, and validates PLC responses.

## Features

* Manual implementation of the Modbus ASCII protocol
* LRC (Longitudinal Redundancy Check) checksum calculation
* Serial communication using PySerial
* Build and transmit Modbus ASCII frames
* Parse and validate PLC responses
* Automatic LRC verification
* Read and write PLC registers using Function Code `06`
* Well-documented and easy to modify for other Modbus commands

## Technologies Used

* Python 3
* PySerial
* Modbus ASCII Protocol

## Project Structure

```text
PLC-Communication-Manual-Modbus-ASCII/
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── images/
    └── example_output.png
```

## Requirements

Install the required dependency:

```bash
pip install pyserial
```

or

```bash
pip install -r requirements.txt
```

## Hardware Requirements

* PLC supporting the Modbus ASCII protocol
* USB-to-Serial (RS-232 / RS-485) converter (if required)
* Python 3

## Serial Configuration

The example uses the following serial settings:

| Parameter | Value    |
| --------- | -------- |
| Baud Rate | 9600     |
| Data Bits | 7        |
| Parity    | Even     |
| Stop Bits | 1        |
| Timeout   | 1 second |

Modify these settings according to your PLC configuration.

## Usage

Run the program:

```bash
python main.py
```

Example:

```python
send_data(register_address='0800', data_value='0000')
```

The program will:

1. Build the Modbus ASCII frame.
2. Calculate the LRC checksum.
3. Send the frame through the serial port.
4. Wait for the PLC response.
5. Verify the returned LRC checksum.
6. Decode and display the received data.

## Example Output

```text
Connected to COM8

:010608000000F1

Received: :010608000000F1

Data is complete and correct

Device Address : 01
Function Code  : 06
Register       : 0800
Value          : 0000
```

## How It Works

The project manually implements the Modbus ASCII communication process:

1. Build the data frame.
2. Calculate the LRC checksum.
3. Convert hexadecimal characters into ASCII bytes.
4. Send the message through the serial port.
5. Receive the PLC response.
6. Validate the received LRC checksum.
7. Extract the device address, function code, register address, and data value.

## Supported Function

Currently implemented:

* Function Code **06** — Preset Single Register

The project can be extended to support additional Modbus function codes such as:

* Function Code 01 — Read Coils
* Function Code 02 — Read Discrete Inputs
* Function Code 03 — Read Holding Registers
* Function Code 04 — Read Input Registers
* Function Code 05 — Write Single Coil
* Function Code 15 — Write Multiple Coils
* Function Code 16 — Write Multiple Registers

## Future Improvements

* Support additional Modbus function codes
* Automatic serial port detection
* Better exception handling
* Communication timeout recovery
* CRC implementation for Modbus RTU
* Graphical User Interface (GUI)
* Logging communication to a file

## Related Project

This repository demonstrates a manual implementation of the Modbus ASCII protocol.

A second version using the **PyModbus** library is also available:

**PLC Communication – PyModbus**

https://github.com/Matin-python/PLC-Communication-PyModbus

## License

This project is licensed under the MIT License.

## Author

**Mohammad Reza Bakhshandeh**

Electrical Engineering (Electronics) Graduate

Interested in Industrial Automation, Embedded Systems, PLC Programming, Python Development, Computer Vision, Machine Learning, and Artificial Intelligence.
