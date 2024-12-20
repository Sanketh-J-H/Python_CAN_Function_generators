
def parse_b2t_bms1(data):
    """Parses a B2T_BMS1 CAN message.

    Args:
        data (bytes): Raw CAN message data.

    Returns:
        dict: Parsed signal values.
    """
    if len(data) < 8:
        raise ValueError(f'Invalid data length. Expected at least 8 bytes.')
    result = {}
    raw_value = 0
    byte_order = "little"
    start_byte = 0 // 8
    end_bit = 0 + 8 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 0 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 8) - 1  # Mask to isolate the signal
    result['B2T_TMax'] = raw_value * 1 + -40
    byte_order = "little"
    start_byte = 8 // 8
    end_bit = 8 + 8 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 8 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 8) - 1  # Mask to isolate the signal
    result['B2T_Tmin'] = raw_value * 1 + -40
    byte_order = "little"
    start_byte = 16 // 8
    end_bit = 16 + 8 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 16 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 8) - 1  # Mask to isolate the signal
    result['B2T_ScBatU_H'] = raw_value * 0.1 + 0
    byte_order = "little"
    start_byte = 24 // 8
    end_bit = 24 + 8 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 24 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 8) - 1  # Mask to isolate the signal
    result['B2T_ScBatU_L'] = raw_value * 0.1 + 0
    byte_order = "little"
    start_byte = 32 // 8
    end_bit = 32 + 1 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 32 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 1) - 1  # Mask to isolate the signal
    result['B2T_Mode'] = raw_value * 1 + 0
    byte_order = "little"
    start_byte = 33 // 8
    end_bit = 33 + 3 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 33 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 3) - 1  # Mask to isolate the signal
    result['B2T_TMSWorkMode'] = raw_value * 1 + 0
    byte_order = "little"
    start_byte = 36 // 8
    end_bit = 36 + 1 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 36 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 1) - 1  # Mask to isolate the signal
    result['B2T_BMUWorkMode'] = raw_value * 1 + 0
    byte_order = "little"
    start_byte = 37 // 8
    end_bit = 37 + 1 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 37 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 1) - 1  # Mask to isolate the signal
    result['B2T_HighVCtrl'] = raw_value * 1 + 0
    byte_order = "little"
    start_byte = 40 // 8
    end_bit = 40 + 8 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 40 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 8) - 1  # Mask to isolate the signal
    result['B2T_TargetT'] = raw_value * 1 + -40
    byte_order = "little"
    start_byte = 48 // 8
    end_bit = 48 + 8 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 48 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 8) - 1  # Mask to isolate the signal
    result['B2T_Life'] = raw_value * 1 + -40
    byte_order = "little"
    start_byte = 56 // 8
    end_bit = 56 + 8 - 1
    end_byte = end_bit // 8
    raw_value =int.from_bytes(data[start_byte:end_byte + 1], byte_order)
    # Adjust for bit alignment
    bit_offset = 56 % 8
    raw_value >>= bit_offset
    raw_value &= (1 << 8) - 1  # Mask to isolate the signal
    result['B2T_TAvg'] = raw_value * 1 + -40
    return result

def pack_b2t_bms1(signal_values):
    """Packs signals into a B2T_BMS1 CAN message.

    Args:
        signal_values (dict): Dictionary of signal names and their values.

    Returns:
        bytes: Packed CAN message data.
    """
    data = [0] * 8
    raw_value = int((signal_values['B2T_TMax'] - -40) / 1)
    if raw_value < -40: raw_value = -40
    if raw_value > 215: raw_value = 215
    data[0] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_Tmin'] - -40) / 1)
    if raw_value < -40: raw_value = -40
    if raw_value > 215: raw_value = 215
    data[1] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_ScBatU_H'] - 0) / 0.1)
    if raw_value < 0: raw_value = 0
    if raw_value > 25.5: raw_value = 25.5
    data[2] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_ScBatU_L'] - 0) / 0.1)
    if raw_value < 0: raw_value = 0
    if raw_value > 25.5: raw_value = 25.5
    data[3] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_Mode'] - 0) / 1)
    if raw_value < 0: raw_value = 0
    if raw_value > 1: raw_value = 1
    data[4] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_TMSWorkMode'] - 0) / 1)
    if raw_value < 0: raw_value = 0
    if raw_value > 7: raw_value = 7
    data[4] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_BMUWorkMode'] - 0) / 1)
    if raw_value < 0: raw_value = 0
    if raw_value > 1: raw_value = 1
    data[4] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_HighVCtrl'] - 0) / 1)
    if raw_value < 0: raw_value = 0
    if raw_value > 1: raw_value = 1
    data[4] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_TargetT'] - -40) / 1)
    if raw_value < -40: raw_value = -40
    if raw_value > 215: raw_value = 215
    data[5] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_Life'] - -40) / 1)
    if raw_value < -40: raw_value = -40
    if raw_value > 215: raw_value = 215
    data[6] |= (int(raw_value) >> 0) & 0xFF
    raw_value = int((signal_values['B2T_TAvg'] - -40) / 1)
    if raw_value < -40: raw_value = -40
    if raw_value > 215: raw_value = 215
    data[7] |= (int(raw_value) >> 0) & 0xFF
    return bytes(data)

if __name__ == "__main__":
    data = bytes([0x80, 0x7F, 0xFF, 0x80, 0xa2, 0x00, 0x90, 0xf0])
    b2t_bms1 = parse_b2t_bms1(data)
    print(parse_b2t_bms1(data))
    print(pack_b2t_bms1(b2t_bms1))