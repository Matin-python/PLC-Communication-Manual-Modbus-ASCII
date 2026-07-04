import serial
import time

sr = serial.Serial(port="COM8",
                   baudrate= 9600,
                   bytesize= 7,
                   parity= 'E',
                   stopbits= 1,
                   timeout= 1
                   )

print(f"Connected to {sr.name}")

def calculate_lrc(data: str) -> str:
    """
    Calculate the Modbus ASCII LRC checksum.

    Parameters
    ----------
    data : str
        Hexadecimal data without STX or CR/LF.

    Returns
    -------
    str
        Two-character hexadecimal LRC checksum.
    """
    checksum = 0
    for i in range (0, len(data), 2):
        checksum += int(data[i:i+2], 16)


    # Calculate LRC (8-bit two's complement)
    checksum = checksum & 0xFF         # Ensure 8-bit
    checksum = (checksum ^ 0xFF) + 0X01
    lrc_checksum = format(checksum, '02X')

    return lrc_checksum

def send_data(
        STX: str = "3A",                  # Start word (STX): ‘: ’ (3AH) 
        device_address: str = "01",
        function_code: str = "06",
        register_address: str = "",
        data_value: str = "",
        END: str = "0D0A"                # Fix the END as END Hi = CR (0DH)(\r), END Lo = LF (0AH)(\n)
        ):
    """
    Build a Modbus ASCII frame, calculate the LRC checksum,
    transmit the message over the serial port, and process
    the PLC response.
    """
    
    data = device_address + function_code + register_address + data_value
    if len(data) % 2 != 0:
        raise ValueError("Hex string must have an even number of characters")

    # Calculate LRC (8-bit two's complement)
    lrc_checksum = calculate_lrc(data)

    message = device_address + function_code + register_address + data_value + lrc_checksum
    # Convert each character to its ASCII value, then to hex, and join them
    result = ''.join(format(ord(c), '02x') for c in message)
    print(STX + result + END)
    message_bytes = bytes.fromhex(STX + result + END)

    print(message_bytes)

    sr.write(message_bytes)
    # sr.write(STX + result + END).encode('utf-8')
            
    # Small delay to ensure data is sent
    time.sleep(0.1)

    if sr.in_waiting > 0:
        response = sr.readline().decode('utf-8').strip()
        print(f"Received: {response}")
        get_data(response)

    else:
        print("No response received.")
 



def get_data(input_string):
    """
    Parse and validate a Modbus ASCII response frame.
    Verify the LRC checksum and extract the returned fields.
    """
    input_string = input_string.strip()

    data_string = None
    FRAME_LENGTH = 14               # Number of data transmitter send =16 - 2(we have 2 header)

    start_string = ":"
    if input_string[0] == start_string:
        data_string = input_string[len(start_string): (len(start_string) + FRAME_LENGTH)]
    else:
        data_string = None


    # Input_String completely get. Now, we should check the checksum to be sure the data is correct
    if data_string is not None:
        if len(input_string[len(start_string):]) >= FRAME_LENGTH:

            # Calculate LRC 
            lrc_checksum = calculate_lrc(data_string[:-2])

            if lrc_checksum == data_string[-2:]:
                print("Data is complete and correct")
                device = data_string[0:2]
                function = data_string[2:4]
                memory_address = data_string[4:8]
                value = data_string[8:12]
                print(device)
                print(function)
                print(memory_address)
                print(value)


        elif len(input_string[len(start_string):]) < FRAME_LENGTH:
            print("The data you send has problem.")


if __name__ == "__main__":
    send_data(register_address='0800', data_value='0000')    
    # send_date(register_address='17D0', data_value='0005')    

    sr.close()
