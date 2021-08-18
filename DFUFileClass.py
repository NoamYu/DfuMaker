from BinFile import BinFile
import numpy as np
import zlib


class DFUFile:
    """
    docstring
    """
    # TODO: Add vendor and product ID

    def __init__(self, programImages):
        totalSize = 0
        self.programImages = programImages

        self.numOfImages = len(programImages)
        total_image_size = get_total_image_size(self.programImages)
        self.target_prefix = build_traget_prefix(
            total_image_size, self.numOfImages)
        totalSize = self.target_prefix.size + total_image_size
        self.prefix = build_dfu_prefix(totalSize)
        self.suffix = build_dfu_suffix()

    def __del__(self):
        self.dfuFile.close()

    def write_DFU_to_file(self, fileName):
        self.dfuFile = open(fileName, "w+b")
        save_part_to_file(self.prefix, self.dfuFile)
        save_part_to_file(self.target_prefix, self.dfuFile)
        for image in self.programImages:
            image.write_image_to_dfu_file(self.dfuFile)
        save_part_to_file(self.suffix, self.dfuFile)
        write_crc_to_file(self.dfuFile)


def get_total_image_size(images):
    total = 0
    for image in images:
        total += image.size
    return total


def write_crc_to_file(file):
    file.seek(0)
    data = file.read()
    crcVal = calculate_crc32_val(data)
    file.write(crcVal.to_bytes(4, byteorder='little'))


def build_dfu_prefix(size):
    bVersion = 0x01
    bTargets = 0x01
    PREFIX_SIZE = 11

    prefix = np.empty(11, dtype=np.uint8)
    prefix[0] = ord('D')
    prefix[1] = ord('f')
    prefix[2] = ord('u')
    prefix[3] = ord('S')
    prefix[4] = ord('e')
    prefix[5] = bVersion
    save_num_to_buffer_as_bytes_offset(size + PREFIX_SIZE, prefix, 6)
    prefix[10] = bTargets

    return prefix


def build_dfu_suffix():
    ignore_field = 0xFF
    suffix = [ignore_field, ignore_field, ignore_field, ignore_field,
              ignore_field, ignore_field, 0x1A, 0x01, 'U', 'F', 'D', 0X10]

    suffix_np = np.empty(len(suffix), dtype=np.uint8)
    for index, ch in enumerate(suffix):
        if(type(ch) == str):
            suffix_np[index] = ord(ch)

        else:
            suffix_np[index] = ch

    return suffix_np


def build_traget_prefix(size, numberOfImage):
    bAlternateSetting = 0x00
    bAlternateSettingFieldSize = 1
    dwNbElements = numberOfImage
    dwNbElementsFieldSize = 4
    bTargetNamedFieldSize = 4  # bytes
    szTargetNameFieldSize = 255
    bTargetNamed = 0x01

    target_prefix = [ord('T'), ord('a'), ord(
        'r'), ord('g'), ord('e'), ord('t')]
    save_to_target_with_padding(
        bAlternateSetting, bAlternateSettingFieldSize, target_prefix)
    save_to_target_with_padding(
        bTargetNamed, bTargetNamedFieldSize, target_prefix)
    save_string_to_target_with_padding(
        "ST...", szTargetNameFieldSize, target_prefix)
    save_num_to_buffer_as_bytes(size, target_prefix)
    save_to_target_with_padding(
        dwNbElements, dwNbElementsFieldSize, target_prefix)
    target_prefix_np = np.array(target_prefix, dtype=np.uint8)
    return target_prefix_np


def save_to_target_with_padding(value, padding, buffer):
    buffer.append(str(value))
    for i in range(padding - 1):
        buffer.append(0x00)


def save_string_to_target_with_padding(string, padding, buffer):
    for ch in string:
        buffer.append(ord(ch))
    for i in range(padding - len(string)):
        buffer.append(int(0x00))


def save_num_to_buffer_as_bytes(num, buffer):
    buffer.append((num & 0xFF))
    buffer.append((num >> 8) & 0xFF)
    buffer.append((num >> 16) & 0xFF)
    buffer.append((num >> 24) & 0xFF)


def save_num_to_buffer_as_bytes_offset(num, buffer, offset):
    i = 0
    buffer[offset + i] = (num & 0xFF)
    i += 1
    buffer[offset + i] = ((num >> 8) & 0xFF)
    i += 1
    buffer[offset + i] = ((num >> 16) & 0xFF)
    i += 1
    buffer[offset + i] = ((num >> 24) & 0xFF)


def save_part_to_file(part_to_save, file):
    np.savetxt(file, part_to_save, fmt='%c',
               delimiter='', footer='', newline='')


def calculate_crc32_val(delta, accum=0):
    return 0xFFFFFFFF & -zlib.crc32(delta, accum) - 1
