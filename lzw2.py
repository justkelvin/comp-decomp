# compression and decompression algorithms in python using lossless compression algorithms LZW for text files in UTF-8 encoding

# -*- coding: utf-8 -*-
import os
import struct

# LZW compression
class LZW:
    def __init__(self, path):
        self.path = path
        self.codes = {}
        self.reverse_mapping = {}

    # functions for compression:
    def make_codes(self):
        for i in range(256):
            self.codes[chr(i)] = i
        self.codes[''] = 256

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            self.make_codes()

            current_code = ""
            compressed = []

            for char in text:
                current_code += char
                if current_code not in self.codes:
                    self.codes[current_code] = len(self.codes)
                    compressed.append(self.codes[current_code[:-1]])
                    current_code = char

            compressed.append(self.codes[current_code])

            for code in compressed:
                output.write(struct.pack('>H', code))

            print("Compressed")
            return output_path

    # functions for decompression:
    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            current_code = ""
            decompressed = ""

            while True:
                try:
                    code = struct.unpack('>H', file.read(2))[0]
                except struct.error:
                    break

                if code not in self.reverse_mapping:
                    if code == len(self.reverse_mapping):
                        self.reverse_mapping[code] = current_code + current_code[0]
                    else:
                        print("Error")
                decompressed += self.reverse_mapping[code]

                if current_code != "":
                    self.reverse_mapping[len(self.reverse_mapping)] = current_code + self.reverse_mapping[code][0]

                current_code = self.reverse_mapping[code]

            output.write(decompressed)
            print("Decompressed")

# main function
def main():
    lzw = LZW("pg69478.txt")
    compressed_file = lzw.compress()
    lzw.decompress(compressed_file)

if __name__ == "__main__":
    main()
