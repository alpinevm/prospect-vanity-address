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

[![Downloads][downloads-badge]][releases]

Prospect provides a streamlined interface for **GPU-accelerated** Ethereum vanity address mining.<br>
It integrates [profanity2] as its mining engine and employs well-established cryptographic practices for secure key generation.

[Installation](#installation) •
[TODO](#todo)
</div>

## Getting Started
![Tutorial][tutorial]

## Installation

Prospect can be installed in two ways:

1. **Install Binary:**<br>
   Prospect provides binaries for macOS arm64 and x86_64 machines (M1 Pro + M1 Max). If you require a binary for a different architecture, please [open an issue][issues].
   <details>
   <summary>macOS</summary>

   > We recommend installation via the packaged [dmg](releases).
    <br>
   </details>

2. **Manual Build:**<br>
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
- [x] macOS Binaries
- [ ] Linux Binaries 
- [ ] Windows Binaries 
- [ ] Better input UI

[profanity2]: https://github.com/1inch/profanity2
[downloads-badge]: https://
[tutorial]: github/demo.webp
[downloads-badge]: https://img.shields.io/github/downloads/ajeetdsouza/zoxide/total?logo=github&logoColor=white&style=flat-square
[releases]: https://github.com/alpinevm/prospect-vanity-address/releases
[issues]: https://github.com/alpinevm/prospect-vanity-address/issues/new
