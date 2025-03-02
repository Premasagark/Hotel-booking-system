from Config import iv, keypass
import binascii
import pyaes, base64
import logging


# Function to generate a key and encrypt a password
def encrypt_password(password: str):
    """
    This function is used for password encryption.
    :param password: Password string
    :return: Encrypted password string
    """
    try:
        plaintext = password

        aes = pyaes.AESModeOfOperationCTR(keypass, pyaes.Counter(iv))
        ciphertext = aes.encrypt(plaintext)
        encrypted = binascii.hexlify(ciphertext).decode("utf-8")
        return encrypted
    except Exception as e:
        logging.exception(str(e))
        raise e


# function to decrypt the password
def decrypt_password(encrypted_data):
    try:
        # Convert the encrypted data from hex back to bytes
        ciphertext = binascii.unhexlify(encrypted_data)

        # Initialize AES in CTR mode with the same key and IV (Counter)
        aes = pyaes.AESModeOfOperationCTR(keypass, pyaes.Counter(iv))

        # Decrypt the ciphertext
        decrypted = aes.decrypt(ciphertext)

        # Decode the decrypted bytes to get the plaintext
        plaintext = decrypted.decode("utf-8")

        return plaintext
    except Exception as e:
        logging.exception(str(e))
        return None



# Convert image to Base64
def image_to_base64(image_file):
    with open(image_file, "rb") as file:
        base64_string = base64.b64encode(file.read()).decode('utf-8')
        return f"data:image/png;base64,{base64_string}"

# Convert Base64 to image
def base64_to_image(base64_string, output_file):
    with open(output_file, "wb") as file:
        file.write(base64.b64decode(base64_string))

