import os
import numpy as np

class BinFile:
    """
    load a bin file to memory
    """

    def __init__(self, fileName, address=0x8000000):
        self.imageFile = open(fileName, "br",)
        self.address = address
        self.size = os.path.getsize(fileName)

        self.prefix = []
        save_num_to_buffer_as_bytes(self.address, self.prefix)
        save_num_to_buffer_as_bytes(self.size, self.prefix)
        self.size += len(self.prefix)

    def close(self):
        self.imageFile.close()

    def write_image_to_dfu_file(self, file):
        save_part_to_file(self.prefix, file)
        self.imageFile.seek(0)
        file.writelines(self.imageFile.readlines())


def save_part_to_file(part_to_save, file):
    np.savetxt(file, part_to_save, fmt='%c',
               delimiter='', footer='', newline='')


def save_num_to_buffer_as_bytes(num, buffer):
    buffer.append(num & 0xFF)
    buffer.append((num >> 8) & 0xFF)
    buffer.append((num >> 16) & 0xFF)
    buffer.append((num >> 24) & 0xFF)
