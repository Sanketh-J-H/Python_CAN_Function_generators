def parse_b2t_bms1(data):
    """Parses a B2T_BMS1 CAN message with signed and unsigned signals.

    Args:
        data (bytes): Raw CAN message data.

    Returns:
        dict: Parsed signal values.
    """
    if len(data) < 8:
        raise ValueError('Invalid data length. Expected at least 8 bytes.')

    result = {}

    # Helper function to extract and decode a signal
    def extract_signal(data, start_bit, length, is_big_endian, factor, offset, is_signed):
        if is_big_endian:
            byte_order = "big"
        else:
            byte_order = "little"
        start_byte = start_bit // 8
        end_bit = start_bit + length
        end_byte = (end_bit - 1) // 8
        raw_value = int.from_bytes(data[start_byte:end_byte + 1], byte_order)

        # Adjust for bit alignment
        bit_offset = start_bit % 8
        raw_value >>= bit_offset
        raw_value &= (1 << length) - 1  # Mask to isolate the signal

        # Handle signed values
        if is_signed and (raw_value & (1 << (length - 1))):  # Check the MSB for negative values
            raw_value -= (1 << length)  # Apply two's complement

        # Apply scaling and offset
        return raw_value * factor + offset

    # Parse each signal
    result['B2T_TMax'] = extract_signal(data, 0, 8, False, 1, -40, True)  # Signed
    result['B2T_Tmin'] = extract_signal(data, 8, 8, False, 1, -40, True)  # Signed
    result['B2T_ScBatU_H'] = extract_signal(data, 16, 8, False, 0.1, 0, False)  # Unsigned
    result['B2T_ScBatU_L'] = extract_signal(data, 24, 8, False, 0.1, 0, False)  # Unsigned
    result['B2T_Mode'] = extract_signal(data, 32, 1, False, 1, 0, False)  # Unsigned
    result['B2T_TMSWorkMode'] = extract_signal(data, 33, 3, False, 1, 0, False)  # Unsigned
    result['B2T_BMUWorkMode'] = extract_signal(data, 36, 1, False, 1, 0, False)  # Unsigned
    result['B2T_HighVCtrl'] = extract_signal(data, 37, 1, False, 1, 0, False)  # Unsigned
    result['B2T_TargetT'] = extract_signal(data, 40, 8, False, 1, -40, True)  # Signed
    result['B2T_Life'] = extract_signal(data, 48, 8, False, 1, -40, True)  # Signed
    result['B2T_TAvg'] = extract_signal(data, 56, 8, False, 1, -40, True)  # Signed

    return result

def pack_b2t_bms1(signals):
    """Packs a B2T_BMS1 CAN message into a raw byte array.

    Args:
        signals (dict): A dictionary with signal names as keys and their values as data.

    Returns:
        bytes: Packed raw CAN message data.
    """
    
    # Initialize a list of 8 bytes (CAN message is 8 bytes long)
    data = [0] * 8

    # Helper function to pack a signal into the appropriate byte(s)
    def pack_signal(start_bit, length, is_big_endian, factor, offset, is_signed, value):
        # Apply scaling and offset
        raw_value = (value - offset) / factor

        # Handle signed values (two's complement)
        if is_signed:
            if raw_value < 0:
                raw_value = (1 << length) + raw_value  # Convert to two's complement
        else:
            # Ensure the value fits within the range
            raw_value = max(0, min((1 << length) - 1, raw_value))

        # Pack the value into the correct bits
        start_byte = start_bit // 8
        bit_offset = start_bit % 8
        raw_value = int(raw_value)  # Convert to integer

        for i in range(length):
            if raw_value & (1 << (length - i - 1)):
                data[start_byte] |= (1 << (7 - (bit_offset + i) % 8))
            if bit_offset + i + 1 >= 8:
                start_byte += 1

        return data

    # Packing each signal into the data array
    data = pack_signal(0, 8, False, 1, -40, True, signals['B2T_TMax'])  # Signed
    data = pack_signal(8, 8, False, 1, -40, True, signals['B2T_Tmin'])  # Signed
    data = pack_signal(16, 8, False, 0.1, 0, False, signals['B2T_ScBatU_H'])  # Unsigned
    data = pack_signal(24, 8, False, 0.1, 0, False, signals['B2T_ScBatU_L'])  # Unsigned
    data = pack_signal(32, 1, False, 1, 0, False, signals['B2T_Mode'])  # Unsigned
    data = pack_signal(33, 3, False, 1, 0, False, signals['B2T_TMSWorkMode'])  # Unsigned
    data = pack_signal(36, 1, False, 1, 0, False, signals['B2T_BMUWorkMode'])  # Unsigned
    data = pack_signal(37, 1, False, 1, 0, False, signals['B2T_HighVCtrl'])  # Unsigned
    data = pack_signal(40, 8, False, 1, -40, True, signals['B2T_TargetT'])  # Signed
    data = pack_signal(48, 8, False, 1, -40, True, signals['B2T_Life'])  # Signed
    data = pack_signal(56, 8, False, 1, -40, True, signals['B2T_TAvg'])  # Signed

    return bytes(data)


if __name__ == "__main__":
    data = bytes([0x80, 0x7F, 0xFF, 0x80, 0x01, 0x00, 0x90, 0xf0])
    b2t_bms1 = parse_b2t_bms1(data)
    print(parse_b2t_bms1(data))
    print(pack_b2t_bms1(b2t_bms1))