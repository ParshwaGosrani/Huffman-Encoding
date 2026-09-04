import heapq
import math
import matplotlib.pyplot as plt
from collections import Counter

# 1. Input Signal - 100 symbols
signal = """
A A B A C A B A A D A B C A A B A C A A
B A D A C B A A A B C A D A B A C A A B
A C A B A A D A C B A A B A C A A D B A
C A B A A A C B A D A B C A A B A C A B
A A C A B D A A B C A A B A C A D B A A
""".split()

# Check input length
print("Number of symbols:", len(signal))

# 2. Frequency and Probability
frequency = Counter(signal)
total_symbols = len(signal)

probability = {
    symbol: frequency[symbol] / total_symbols
    for symbol in frequency
}

# 3. Huffman Tree Node
class Node:
    def __init__(self, symbol=None, frequency=0, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency


# 4. Construct Huffman Tree
heap = []

for symbol, freq in frequency.items():
    heapq.heappush(heap, Node(symbol, freq))

while len(heap) > 1:
    left = heapq.heappop(heap)
    right = heapq.heappop(heap)

    merged = Node(
        symbol=None,
        frequency=left.frequency + right.frequency,
        left=left,
        right=right
    )

    heapq.heappush(heap, merged)

root = heap[0]


# 5. Generate Huffman Codes
huffman_codes = {}

def generate_codes(node, code=""):
    if node is None:
        return

    if node.symbol is not None:
        huffman_codes[node.symbol] = code if code else "0"
        return

    generate_codes(node.left, code + "0")
    generate_codes(node.right, code + "1")


generate_codes(root)


# 6. Display Symbol, Frequency, Probability and Code
print("\nHuffman Coding Table")
print("-" * 50)
print(f"{'Symbol':<10}{'Frequency':<12}{'Probability':<15}{'Code':<10}")
print("-" * 50)

for symbol in sorted(frequency, key=lambda x: frequency[x], reverse=True):
    print(
        f"{symbol:<10}"
        f"{frequency[symbol]:<12}"
        f"{probability[symbol]:<15.4f}"
        f"{huffman_codes[symbol]:<10}"
    )

print("-" * 50)


# 7. Encode Complete Signal
encoded_signal = ""

for symbol in signal:
    encoded_signal += huffman_codes[symbol]

print("\nEncoded Binary Sequence:")
print(encoded_signal)

print("\nEncoded sequence length:", len(encoded_signal), "bits")


# 8. Average Code Length
average_code_length = sum(
    probability[symbol] * len(huffman_codes[symbol])
    for symbol in frequency
)

print("\nAverage Code Length:",
      round(average_code_length, 4), "bits/symbol")


# 9. Entropy
entropy = -sum(
    probability[symbol] * math.log2(probability[symbol])
    for symbol in frequency
)

print("Entropy:",
      round(entropy, 4), "bits/symbol")


# 10. Huffman Coding Efficiency
efficiency = (entropy / average_code_length) * 100

print("Huffman Coding Efficiency:",
      round(efficiency, 2), "%")


# 11. Compression Ratio
# Fixed-length coding for 5 symbols requires 3 bits/symbol
fixed_length_bits = total_symbols * math.ceil(math.log2(len(frequency)))
huffman_bits = len(encoded_signal)

compression_ratio = fixed_length_bits / huffman_bits

print("Original fixed-length bits:", fixed_length_bits)
print("Huffman encoded bits:", huffman_bits)
print("Compression Ratio:",
      round(compression_ratio, 4))


# 12. Decode Huffman Encoded Signal
reverse_codes = {
    code: symbol
    for symbol, code in huffman_codes.items()
}

decoded_signal = []
current_code = ""

for bit in encoded_signal:
    current_code += bit

    if current_code in reverse_codes:
        decoded_signal.append(reverse_codes[current_code])
        current_code = ""

# 13. Verify Decoding
decoded_correctly = decoded_signal == signal

print("\nDecoded Signal:")
print(" ".join(decoded_signal))

print("\nDecoding Verification:",
      "SUCCESS - Decoded signal is identical to original."
      if decoded_correctly
      else "ERROR - Decoded signal is different.")


# 14. Numerical Representation of Original Signal
symbol_values = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5
}

original_numeric = [
    symbol_values[symbol]
    for symbol in signal
]


# Convert binary signal into numbers
encoded_numeric = [
    int(bit)
    for bit in encoded_signal
]


# 15. Plot Original Signal
plt.figure(figsize=(12, 4))

plt.step(
    range(len(original_numeric)),
    original_numeric,
    where="mid"
)

plt.yticks(
    [1, 2, 3, 4, 5],
    ["A", "B", "C", "D", "E"]
)

plt.xlabel("Symbol Position")
plt.ylabel("Symbol")
plt.title("Original Input Signal")
plt.grid(True)

plt.tight_layout()
plt.show()


# 16. Plot Huffman Encoded Signal
plt.figure(figsize=(12, 4))

plt.step(
    range(len(encoded_numeric)),
    encoded_numeric,
    where="mid"
)

plt.yticks([0, 1])
plt.xlabel("Bit Position")
plt.ylabel("Bit")
plt.title("Huffman Encoded Binary Signal")
plt.grid(True)

plt.tight_layout()
plt.show()