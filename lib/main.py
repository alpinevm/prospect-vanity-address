import os
import re
import time
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

class InternalState (enum.Enum):
    STARTING = 1
    MINING = 2
    STOPPING = 3

class TriggerPhrases:
    READ_DEVICES_MATCH = "GPU"
    READ_DEVICES_END = "Initializing OpenCL..." 
    GEN_KEY = "Private:"
    MINING_SPEED = "Total:"

# Get's the filename of the binary needed based on the users OS and architecture
def binary_switcher() -> tuple:
    op_s = platform.system()
    arch = platform.machine()
    if op_s == "Darwin":
        if arch == "arm64":
            filepath = "./bin/macos-arm64/profanity2-macos-arm64"
            permissions = os.stat(filepath).st_mode
            os.chmod(filepath, permissions | 0o111)
            # include start commmand
            return "./bin/macos-arm64", "./profanity2-macos-arm64"

    raise Exception("No binary found for your OS (" + op_s + ") and architecture (" + arch + ")")

def create_seed_wallet() -> tuple[str, str]:
    wallet: LocalAccount = w3.eth.account.create(os.urandom(32))
    return wallet.key.hex(), wallet._key_obj.public_key.to_hex()

def calculate_final_key(seed_private_key: str, mined_key: str) -> str:
    return hex((int(seed_private_key, 16) + int(mined_key, 16)) % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)

def sanity_check(address: str, matching: str, prefix: bool = True) -> bool:
    address = address.lower()[2:]
    matching = matching.lower()
    if prefix:
        return address.startswith(matching)
    else:
        return address.endswith(matching)

# only handle leading matches
def init_miner(matching: str) -> Generator:
    seed_private_key, seed_public_key = create_seed_wallet()
    try:
        binary_dir, miner_binary = binary_switcher()
    except:
        yield {"message": "No binary found for your OS and architecture", "state": MinerOutputState.ERROR}
        return

    # Start the miner
    print("Starting miner...")
    process = subprocess.Popen([miner_binary, "--matching", matching, "-z", seed_public_key[2:]], stdout=subprocess.PIPE, cwd=binary_dir)
    
    STATE = InternalState.STARTING
    buffer = b""
    mining_buffer = b""
    while True:
        chunk = process.stdout.read(1)
        if chunk == b'':
            break
        buffer += chunk
        mining_buffer += chunk
        if chunk.endswith(b'\n'):
            # print(buffer.decode(), end='')
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
                    # check if key matches the address
                    if address.lower() == w3.eth.account.from_key(final_key).address.lower() and sanity_check(address, matching, prefix=True):
                        yield {"data": {"address": address, "private_key": final_key}, "state": MinerOutputState.FOUND}
                        #TODO: Change this to not be a kill when we switch to leading
                        process.kill()
                    else:
                        pass
                        # print("Internal error: Key does not match address")
        # if chunk.endswith(b'\r'):  # look for '\r' instead of '\n'
            # yield { "data": mining_buffer.decode(), end='')
            # mining_buffer = b""
            # print("PLEASE", chunk.decode(), end='')
            # if TriggerPhrases.MINING_SPEED in chunk.decode().strip():
            #     yield {"data": , "state": MinerOutputState.MINING_SPEED}

def dummy_miner(matching: str) -> Generator:
    while True:
        yield {"data": "70 MH/S", "state": MinerOutputState.MINING_SPEED}
        time.sleep(1)

if __name__ == '__main__':
    # test
    miner = init_miner("1231231")
    for data in miner:
        print("FROM GEN", data)

