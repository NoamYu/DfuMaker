# About
The Command Line DFU tool you never knew you wanted.
Command line tool that can take multiple bin files and convert them into a single DFU file.

# Usage
stm32's DfuSe utility as describe by their website can be used to interact with the STM32 system memory bootloader or any In-Application Programming (IAP) firmware, running from the user Flash, thus allowing internal memories programming through USB.

# Runing the script
You can see the instructions by caliing the script with the --help flag.

## Example 
```
Python ./Stm32DFUMaker.py --bin ./file0.bin,0x800000000 --bin ./file1.bin,0x80002000  --dst
./file.dfu
```
