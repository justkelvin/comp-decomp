# compression and decompression algorithms in python using lossless compression algorithms like Huffman coding and LZW

import heapq
import os
from collections import Counter

# Huffman coding compression algorithm in python using heapq and Counter from collections
class HuffmanCoding:
    def __init__(self, path):
        """ Initializes the path and heap """
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {} # used for decompression

    # functions for compression:
    def make_frequency_dict(self, text):
        """ Returns a dictionary with the frequency of each character in the text """
        return Counter(text)

    def make_heap(self, frequency_dict):
        """ Makes a heap from the frequency dictionary """
        for key in frequency_dict:
            node = HuffmanNode(key, frequency_dict[key]) # create a Huffman node for each key in the frequency dictionary
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        """ Merges the nodes of the heap until there is only one node left """
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = HuffmanNode(None, node1.freq + node2.freq) # create a new node with the sum of the frequencies of the two nodes
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        """ Makes the codes for the characters in the text """
        if root is None: # if the root is None, return
            return

        if root.char is not None: # if the root is a leaf node, add the current code to the codes dictionary
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        # if the root is not a leaf node, add 0 to the current code and call the function recursively for the left child
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        """ Makes the codes for the characters in the text """
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code) # call the helper function

    def get_encoded_text(self, text):
        """ Returns the encoded text """
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        """ Pads the encoded text to make it a multiple of 8 bits """
        extra_padding = 8 - len(encoded_text) % 8 # calculate the extra padding
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding) # add the padded info to the encoded text
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        """ Returns a byte array from the padded encoded text """
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        # run a loop over the padded encoded text in steps of 8 bits
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        """ Compresses a file and returns the output path """
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        # read text from file and make frequency dictionary using the text and then make a heap from the frequency dictionary
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency_dict = self.make_frequency_dict(text)
            self.make_heap(frequency_dict)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b)) # write to output file

            print("Compression of file is done and the output path is: " + output_path)
            return output_path

    # functions for decompression:
    def remove_padding(self, padded_encoded_text):
        """ Removes the padding of the padded encoded text and returns the encoded text """
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] # remove the padded info from the padded encoded text
        encoded_text = padded_encoded_text[:-1 * extra_padding] # remove the extra padding from the padded encoded text

        return encoded_text

    def decode_text(self, encoded_text):
        """ Decodes the encoded text and returns the decompressed text and the output path """
        current_code = ""
        decoded_text = ""

        # run a loop over the encoded text and keep adding the bits to the current code until the current code is in the reverse mapping
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        """ Decompresses a file and returns the output path and the decompressed text """
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        # read the compressed file and get the padded encoded text and then remove the padding from the padded encoded text
        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""
            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string) # remove the padding from the padded encoded text

            decompressed_text = self.decode_text(encoded_text) # decode the encoded text to get the decompressed text

            output.write(decompressed_text) # write the decompressed text to the output file
            print("Decompression of file is done and the output path is: " + output_path)
            return output_path

# huffman node class for the heap and the tree nodes of the huffman tree 
class HuffmanNode:
    def __init__(self, char, freq):
        """ Initializes the node with the character and the frequency of the character """
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # defining comparators less_than and equals
    def __lt__(self, other):
        """ Overriding the < operator """
        return self.freq < other.freq

    def __eq__(self, other):
        """ Overriding the equals operator """
        if(other == None):
            return False
        if(not isinstance(other, HuffmanNode)): # check if the other object is of type HuffmanNode
            return False
        return self.freq == other.freq

# run the program 
if __name__ == "__main__":
    path = "input_lowercase.txt" # path of the file to be compressed and decompressed 
    h = HuffmanCoding(path) # create a HuffmanCoding object

    output_path = h.compress() # compress the file and get the output path of the compressed file
    print("Compressed file path: " + output_path)

    decompressed_path = h.decompress(output_path) # decompress the file and get the output path of the decompressed file
    print("Decompressed file path: " + decompressed_path)
