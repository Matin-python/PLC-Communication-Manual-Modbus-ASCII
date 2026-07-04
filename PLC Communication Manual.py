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

def send_data(
        STX = "3A",                  # Start word (STX): ‘: ’ (3AH) 
        Device_Adress = "01",
        Function_code = "06",
        Register_Adress = str,
        Data_Value = str,
        END = "0D0A"                # Fix the END as END Hi = CR (0DH)(\r), END Lo = LF (0AH)(\n)
        ):
    
    
    data = Device_Adress + Function_code + Register_Adress + Data_Value
    if len(data) % 2 != 0:
        raise ValueError("Hex string must have an even number of characters")

    checksum  = 0
    for i in range (0, len(data), 2):
        checksum  += int(data[i:i+2], 16)

    # Calculate LRC (8-bit two's complement)
    checksum  &= 0xFF         # Ensure 8-bit
    checksum  = (checksum  ^ 0xFF) + 0X01
    LRC_Checksum = format(checksum , '02X')

    s = Device_Adress + Function_code + Register_Adress + Data_Value + LRC_Checksum
    # Convert each character to its ASCII value, then to hex, and join them
    result = ''.join(format(ord(c), '02x') for c in s)
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
 



def get_data(Input_String):
    Input_String = Input_String.strip()

    Data_String = None
    Rx_SingleBuf_Len = 16 - 2           # Number of data transmitter send (we have 2 header)

    Start_String = ":"
    if Input_String[0] == Start_String:
        Data_String = Input_String[len(Start_String): (len(Start_String) + Rx_SingleBuf_Len)]
    else:
        Data_String = None


    # Input_String completely get. Now, we should check the checksum to be sure the data is correct
    if Data_String is not None:
        if len(Input_String[len(Start_String):]) >= Rx_SingleBuf_Len:
            checksum  = 0
            for i in range (0, len(Data_String)-2, 2):
                checksum  += int(Data_String[i:i+2], 16)

            # Calculate LRC (8-bit two's complement)
            checksum  &= 0xFF         # Ensure 8-bit
            checksum  = (checksum  ^ 0xFF) + 0X01
            LRC_Checksum = format(checksum , '02X')

            # LRC_Checksum &= 0xFF         # Ensure 8-bit
            if LRC_Checksum == Data_String[-2:]:
                print("Data is complete and correct")
                device = Data_String[0:2]
                function = Data_String[2:4]
                memory_adress = Data_String[4:8]
                value = Data_String[8:12]
                print(device)
                print(function)
                print(memory_adress)
                print(value)


        elif len(Input_String[len(Start_String):]) < Rx_SingleBuf_Len:
            print("The data you send has problem.")


if __name__ == "__main__":
    send_data(Register_Adress='0800', Data_Value='0000')    
    # send_date(Register_Adress='17D0', Data_Value='0005')    
    send_data(Register_Adress='0800', Data_Value=b'1')    
