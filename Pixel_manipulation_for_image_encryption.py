import os
import sys
from PIL import Image
from tqdm import tqdm

def xor_encrypt_decrypt(pixels, width, height, key):
    for i in tqdm(range(width), desc="Processing columns"):
        for j in range(height):
            r, g, b = pixels[i, j]
            r = r ^ key
            g = g ^ key
            b = b ^ key
            pixels[i, j] = (r, g, b)
    return pixels

def add_key_encrypt_decrypt(pixels, width, height, key):
    for i in tqdm(range(width), desc="Processing columns"):
        for j in range(height):
            r, g, b = pixels[i, j]
            r = (r + key) % 256
            g = (g + key) % 256
            b = (b + key) % 256
            pixels[i, j] = (r, g, b)
    return pixels

def process_image(input_path, output_path, key, algorithm):
    try:
        with Image.open(input_path) as img:
            img = img.convert("RGB")
            pixels = img.load()
            width, height = img.size

            if algorithm == 'xor':
                pixels = xor_encrypt_decrypt(pixels, width, height, key)
            elif algorithm == 'add_key':
                pixels = add_key_encrypt_decrypt(pixels, width, height, key)
            else:
                print("Unsupported algorithm. Choose 'xor' or 'add_key'.")
                return

            img.save(output_path)
            print(f"Image saved to {output_path}")
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Image Encryption/Decryption Tool")
    parser.add_argument("operation", choices=["encrypt", "decrypt"], help="Operation to perform")
    parser.add_argument("input_path", help="Path to the input image file")
    parser.add_argument("output_path", help="Path to save the output image file")
    parser.add_argument("key", type=int, help="Encryption/Decryption key")
    parser.add_argument("--algorithm", choices=["xor", "add_key"], default="xor", help="Encryption algorithm to use")
    
    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        print(f"Error: Input file '{args.input_path}' does not exist.")
        sys.exit(1)
    
    if args.operation not in ["encrypt", "decrypt"]:
        print("Error: Operation must be 'encrypt' or 'decrypt'")
        sys.exit(1)

    print(f"{args.operation.capitalize()}ing image...")
    process_image(args.input_path, args.output_path, args.key, args.algorithm)

if __name__ == "__main__":
    main()