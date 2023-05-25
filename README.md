<!-- markdownlint-configure-file {
  "MD013": {
    "code_blocks": false,
    "tables": false
  },
  "MD033": false,
  "MD041": false
} -->

<div align="center">

# prospect

Prospect provides a streamlined interface for **GPU-accelerated** Ethereum vanity address mining.<br>
It integrates [profanity2] as its mining engine and employs well-established cryptographic practices for secure key generation.

[Installation](#installation) •
[TODO](#todo)
</div>

## Getting Started
![Tutorial][tutorial]

## Installation
1. **macOs** <br>
    ```bash
    git clone https://github.com/alpinevm/prospect-vanity-address
    cd prospect-vanity-address
    python3 -m pip install -r requirements
    python3 src/main.py
    ```
    
2. **Other platforms:**<br>
   Detailed instructions will be provided soon. In the meantime, follow the steps below to build from source:
    - Prospect relies on [profanity2]. Build the binary from the profanity2 repository and move the binary and OpenCL files to the `/bin` directory.
    - Update `src/lib.py` with the path to your `profanity2` binary.
    - Install Python dependencies with the following command:
      ```bash
      python3 -m pip install -r requirements.txt
      ```
    - Start the UI:
      ```bash
      python3 src/main.py
      ```

## TODO  
- [ ] macOS Binaries
- [ ] Linux Binaries 
- [ ] Windows Binaries 
- [ ] Better input UI
- [ ] Export encrypted keystore json

[profanity2]: https://github.com/1inch/profanity2
[downloads-badge]: https://img.shields.io/github/downloads/alpinevm/prospect-vanity-address/total?logo=github&lo
[tutorial]: github/demo.webp
[releases]: https://github.com/alpinevm/prospect-vanity-address/releases
[issues]: https://github.com/alpinevm/prospect-vanity-address/issues/new
