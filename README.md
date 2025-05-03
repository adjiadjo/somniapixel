# SomniaPixel Bot

A Python bot for interacting with the SomniaPixel Canvas on the Somnia Shannon testnet. The bot randomly colors pixels on the canvas by making transactions to the `PixelCanvas` contract.

## Features
- Randomly selects `x`, `y` coordinates within the canvas (1024x1024).
- Randomly generates a color (RGB).
- Sends transactions to the `PixelCanvas` contract to color the selected pixel.
- Waits 3 seconds between each transaction.
- Provides transaction details, including pixel coordinates and color.

## Requirements

- Python 3.x
- `pip` package manager
- Somnia Shannon testnet STT (native token) for gas fees

## Installation
**Clone the repository:**
   ```bash
   git clone https://github.com/adjiadjo/somniapixel.git
   cd somniapixel
   ```
**Install Python 3 and pip (if not installed already):**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
**Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

**Usage**
 Run the bot:
   ```bash
   python3 somniapixel.py
   ```

Input your wallet private key when prompted. (Make sure your wallet has enough STT for gas fees and pixel coloring.)

Input the number of loops to decide how many transactions the bot will send.
