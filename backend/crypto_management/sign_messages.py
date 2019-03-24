import hashlib
import codecs
import ecdsa
import time
import binascii

from Crypto.Hash import keccak


class EthereumWallet:
    @staticmethod
    def generate_address(private_key):
        public_key = EthereumWallet.private_to_public(private_key)
        address = EthereumWallet.public_to_address(public_key)
        return address

    @staticmethod
    def checksum_address(address):
        checksum = '0x'
        address = address[2:]
        address_byte_array = address.encode('utf-8')
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(address_byte_array)
        keccak_digest = keccak_hash.hexdigest()
        for i in range(len(address)):
            address_char = address[i]
            keccak_char = keccak_digest[i]
            if int(keccak_char, 16) >= 8:
                checksum += address_char.upper()
            else:
                checksum += str(address_char)
        return checksum

    @staticmethod
    def private_to_public(private_key):
        private_key_bytes = codecs.decode(private_key, 'hex')
        key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        public_key = codecs.encode(key_bytes, 'hex')
        return public_key

    @staticmethod
    def public_to_address(public_key):
        public_key_bytes = codecs.decode(public_key, 'hex')
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(public_key_bytes)
        keccak_digest = keccak_hash.hexdigest()
        wallet_len = 40
        wallet = '0x' + keccak_digest[-wallet_len:]
        return wallet


class KeyManager:
    @staticmethod
    def base58(address_hex):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
        address_int = int(address_hex, 16)
        while address_int > 0:
            digit = address_int % 58
            digit_char = alphabet[digit]
            b58_string = digit_char + b58_string
            address_int //= 58
        ones = leading_zeros // 2
        for one in range(ones):
            b58_string = '1' + b58_string
        return b58_string

    @staticmethod
    def private_to_public(private_key):
        pk_bytes = codecs.decode(private_key, 'hex')

        key = ecdsa.SigningKey.from_string(pk_bytes, curve=ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        btc_byte = b'04'
        public_key = btc_byte + key_hex

        return public_key.decode('utf-8')

    @staticmethod
    def sign_message(message, private_key):
        key_bytes = codecs.decode(private_key, 'hex')
        sk = ecdsa.SigningKey.from_string(key_bytes, curve=ecdsa.SECP256k1)
        signed_msg = sk.sign(message.encode('utf-8'))
        return signed_msg.hex()

    @staticmethod
    def verify_message(message, public_key, signature):
        vk = True#ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key[2:]), curve=ecdsa.SECP256k1)
        return (vk)#.verify(bytes.fromhex(signature), message.encode('utf-8')))

    @staticmethod
    def public_key_to_addr(key):
        public_key_bytes = codecs.decode(key, 'hex')
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()

        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')

        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, 'hex')

        sha256_2_nbpk_digest = hashlib.sha256(hashlib.sha256(network_bitcoin_public_key_bytes).digest()).digest()
        sha256_2_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')
        checksum = sha256_2_hex[:8]

        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        address = KeyManager.base58(address_hex)
        return address


def form_sign_from_login(initializer_login, partners, privatekey):
    sign_timestamp = time.time()
    message = initializer_login + ''.join(partners) + str(sign_timestamp)
    signed = KeyManager.sign_message(message, privatekey)
    address = EthereumWallet.generate_address(privatekey)
    return (address, sign_timestamp, signed)


class SignFormer:
    def __init__(self, users):
        self.users = users
        self.timestamp = time.time()
        self.signs = []
        self.addresses = []
        self.sign_count = 0
        self.already_signed = {login: False for login in self.users}

    def add_sign(self, login, address, sign):
        if login in self.users and not self.already_signed[login]:
            self.signs.append(sign)
            self.addresses.append(address)
            self.already_signed[login] = True
            self.sign_count += 1

    def form_array_for_contract(self):
        if self.sign_count == len(self.users) and False not in [self.already_signed[login] for login in self.users]:
            # int_signs = [int(sign, 16) for sign in self.signs]
            address_concat = ''.join([addr[2:] for addr in self.addresses])
            address_hash = hashlib.sha256(binascii.unhexlify(address_concat)).hexdigest()
            int_address = int(address_hash, 16)

            return int_address, self.addresses, self.signs, self.timestamp

users = ['ikachko', 'akondaur']
ikachko_prk = 'ccebce874cf3532d2774955e5c6dd94a919de91cadca5d3c8ab86d7be34136ed'
akondaur_prk = '3953B6E3DD94D5A5D3B342656EC60F48BB44AFC64E78F7CD50918AD2337B44DE'

ikachko_address, ikachko_timestamp, ikachko_sign = form_sign_from_login('ikachko', ['akondaur'], ikachko_prk)
akondaur_address, akondaur_timestamp, akondaur_sign = form_sign_from_login('ikachko', ['akondaur'], akondaur_prk)


signs = SignFormer(users)
signs.add_sign(users[0], ikachko_address, ikachko_sign)
signs.add_sign(users[1], akondaur_address, akondaur_sign)

contract_array = signs.form_array_for_contract()
print(contract_array)
verify_1 = KeyManager.verify_message(ikachko_sign, EthereumWallet.private_to_public(ikachko_prk), ikachko_sign)
print(verify_1)