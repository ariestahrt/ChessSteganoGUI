import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]

def build_freq_dict(message):
    freq_dict = defaultdict(int)
    for char in message:
        freq_dict[char] += 1
    return freq_dict

def build_huffman_codes(node, current_code, codes):
    if node is not None:
        if node.char is not None:
            codes[node.char] = current_code
        build_huffman_codes(node.left, current_code + '0', codes)
        build_huffman_codes(node.right, current_code + '1', codes)

def compress(message):
    freq_dict = build_freq_dict(message)
    root = build_huffman_tree(freq_dict)

    codes = {}
    build_huffman_codes(root, '', codes)

    compressed_message = ''.join(codes[char] for char in message)
    return compressed_message, root

def decompress(compressed_message, root):
    current_node = root
    decoded_message = ''

    for bit in compressed_message:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_message += current_node.char
            current_node = root

    return decoded_message

if __name__ == '__main__':
    # Example usage:
    message = "aku suka makan nasi padang"
    compressed_message, tree = compress(message)
    print(f"Original message: {message}")
    print(f"Compressed message: {compressed_message}")

    decoded_message = decompress(compressed_message, tree)
    print(f"Decoded message: {decoded_message}")
