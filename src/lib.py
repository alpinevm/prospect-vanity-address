import os
import re
import platform
from typing import Generator
import enum
import subprocess

from web3.auto import w3
from eth_account.signers.local import (
    LocalAccount,
)

class MinerOutputState (enum.Enum):
    MINING_SPEED = 1
    FOUND = 2
    ERROR = 3
    DEVICE_DATA = 4
    INITIALIZING = 5

class InternalState (enum.Enum):
    STARTING = 1
    MINING = 2
    STOPPING = 3

class TriggerPhrases:
    READ_DEVICES_MATCH = "GPU"
    READ_DEVICES_END = "Initializing OpenCL..." 
    GEN_KEY = "Private:"
    MINING_SPEED = "Total:"

def simple_miner(matching: str, prefix=True) -> Generator:
    print("Using simple miner...")
    while True:
        randomness = os.urandom(32)
        wallet: LocalAccount = w3.eth.account.create(randomness)
        if validate_wallet(wallet.address, matching, prefix=prefix):
            yield {
                "data": {
                    "address": wallet.address,
                    "private_key": wallet.key.hex()
                },
                "state": MinerOutputState.FOUND
            }
            break

# Get's the filename of the binary needed based on the users OS and architecture
def binary_switcher() -> tuple:
    op_s = platform.system()
    arch = platform.machine()
    print (op_s, arch)

    if op_s == "Darwin":
        if arch == "arm64":
            filepath = "./bin/macos-arm64/profanity2-macos-arm64"
            permissions = os.stat(filepath).st_mode
            os.chmod(filepath, permissions | 0o111)
            # include start commmand
            return "./bin/macos-arm64", "./profanity2-macos-arm64"
        if arch == "x86_64":
            filepath = "./bin/macos-x86_64/profanity2-macos-x86_64"
            permissions = os.stat(filepath).st_mode
            os.chmod(filepath, permissions | 0o111)
            # include start commmand
            return "./bin/macos-x86_64", "./profanity2-macos-x86_64"

    raise Exception("No binary found for your OS (" + op_s + ") and architecture (" + arch + ")")

def create_seed_wallet() -> tuple[str, str]:
    wallet: LocalAccount = w3.eth.account.create(os.urandom(32))
    return wallet.key.hex(), wallet._key_obj.public_key.to_hex()

def calculate_final_key(seed_private_key: str, mined_key: str) -> str:
    return hex((int(seed_private_key, 16) + int(mined_key, 16)) % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)

def validate_wallet(address: str, matching: str, prefix: bool = True) -> bool:
    address = address.lower()[2:]
    matching = matching.lower()
    if prefix:
        return address.startswith(matching)
    else:
        return address.endswith(matching)

def address_can_be_mined(matching: str) -> bool:
    # check each character see if they are a valid hex character
    if len(matching) > 40:
        return False
    for char in matching:
        if char not in "0123456789abcdef":
            return False
    return True

def fill_matching(matching: str, prefix=True) -> str:
    if prefix:
        return matching + "X" * (40 - len(matching))
    return "X" * (40 - len(matching)) + matching

# only handle leading matches
def init_miner(matching: str, prefix=True) -> Generator:
    # check if the address can be mined
    if not address_can_be_mined(matching):
        yield {"message": "Invalid Search String -  Address cannot be mined", "state": MinerOutputState.ERROR}
        return
    
    if len(matching) <= 2:
        # run simple miner, b/c of profanity2 bug...
        # b/c this is so compuationally light,
        # we can just run it in the main thread (and in python)
        yield from simple_miner(matching, prefix=prefix)
        return;

    seed_private_key, seed_public_key = create_seed_wallet()
    try:
        binary_dir, miner_binary = binary_switcher()
    except:
        yield {"message": "No binary found for your OS and architecture", "state": MinerOutputState.ERROR}
        return

    # Start the miner
    print("Starting miner...")
    process = subprocess.Popen([miner_binary, "--matching", fill_matching(matching, prefix), "-z", seed_public_key[2:]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=binary_dir)
    # creating mining stderr reading thread
    
    STATE = InternalState.STARTING
    buffer = b""
    while True:
        chunk = process.stdout.read(1)  # read byte by byte
        if chunk == b'':  # end of output
            break
        buffer += chunk
        if chunk in [b'\n', b'\r']:
            output = buffer.decode().strip()
            buffer = b""
            if InternalState.STARTING == STATE:
                if TriggerPhrases.READ_DEVICES_MATCH in output:
                    yield {"data": output, "state": MinerOutputState.DEVICE_DATA}
                elif TriggerPhrases.READ_DEVICES_END in output:
                    STATE = InternalState.MINING
            if InternalState.MINING:
                if TriggerPhrases.GEN_KEY in output:
                    match = re.search(r'Private: (?P<private>0x[0-9a-fA-F]+) Address: (?P<address>0x[0-9a-fA-F]+)', output)
                    if match is None:
                        continue
                    private_key = match.group('private')
                    address = match.group('address')
                    # calculate final key
                    final_key = calculate_final_key(seed_private_key, private_key)
                    print("Found key", final_key)

                    # check if key matches the address
                    if address.lower() == w3.eth.account.from_key(final_key).address.lower() and validate_wallet(address, matching, prefix=prefix):
                        yield {"data": {"address": address, "private_key": final_key}, "state": MinerOutputState.FOUND}
                        #TODO: Change this to not be a kill when we switch to leading
                        process.kill()
                        break
                    else:
                        print("Address does not truly match", address, final_key)
                elif TriggerPhrases.MINING_SPEED in output:
                    match = re.search(r'Total:\s*(?P<total>\d+\.\d+)\s*(?P<unit>\w+)', output)
                    if match is None:
                        continue
                    total = float(match.group('total'))
                    unit = match.group('unit')
                    yield {"data": {"speed": total, "units": unit}, "state": MinerOutputState.MINING_SPEED}

def test_search(search_string: str):
    miner = init_miner(search_string)
    for data in miner:
        print("Generator:", data)

if __name__ == '__main__':
    string = input("Enter search string: ")
    test_search(string)
    
