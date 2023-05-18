import os
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

# Get's the filename of the binary needed based on the users OS and architecture
def binary_switcher() -> str:
    op_s = platform.system()
    arch = platform.machine()
    if op_s == "Darwin":
        if arch == "arm64":
            filepath = "./bin/profanity2-macos-arm64"
            permissions = os.stat(filepath).st_mode
            os.chmod(filepath, permissions | 0o111)
            return filepath 

    raise Exception("No binary found for your OS (" + op_s + ") and architecture (" + arch + ")")

def create_seed_wallet() -> tuple[str, str]:
    wallet: LocalAccount = w3.eth.account.create(os.urandom(32))
    return wallet.key.hex(), wallet._key_obj.public_key.to_hex()

def calculate_final_key(seed_private_key: str, mined_key: str) -> str:
    return hex((int(seed_private_key, 16) + int(mined_key, 16)) % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)

# only handle leading matches
def init_miner(matching: str) -> Generator:
    seed_private_key, seed_public_key = create_seed_wallet()
    try:
        miner_binary = binary_switcher()
    except:
        yield {"message": "No binary found for your OS and architecture", "state": MinerOutputState.ERROR}
        return

    # Start the miner
    print("Starting miner...")
    process = subprocess.Popen([miner_binary, "--matching", matching, "-z", seed_public_key[2:]], stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            # Do something with the output
            print(output.strip())

def dummy_miner(matching: str) -> Generator:
    while True:
        yield {"data": "70 MH/S", "state": MinerOutputState.MINING_SPEED}
        time.sleep(1)

if __name__ == '__main__':
    # test
    miner = dummy_miner("0x123")
    for i in miner:
        print(i)

