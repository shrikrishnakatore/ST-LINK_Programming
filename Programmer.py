import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
os.environ["PATH"] ="path_to_stm32cubeprogrammer;"+ os.environ["PATH"]
fname ="Filename.bin"

class stmdevice:
    def __init__(self):
        self.result=''
    
    def unlock(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -ob rdp=0xAA',capture_output=True,text=True).stdout
        if ("Option Bytes successfully programmed" in self.result) or ("Warning: Option Byte: rdp, value: 0xAA, was not modified.\n\nWarning: Option Bytes are unchanged, Data won't be downloaded" in self.result) :
            return 0
        else:
            if("Error: No STM32 target found!" in self.result):
                print("Check device power and Programmer connection\n\r")
            return -1
    def program_BootOptions(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -ob BOOT_LOCK=0x1 -ob nBOOT0=0x0 -ob nSWBOOT0=0x0 -ob nBOOT1=0x1',capture_output=True,text=True).stdout
        if ("Option Bytes successfully programmed" in self.result) or ("Warning: Option Byte: nboot1, value: 0x1, was not modified.\n\nWarning: Option Bytes are unchanged, Data won't be downloaded" in self.result) :
            return 0
        else:
            return -1
    def lock(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -ob BOOT_LOCK=0x1 -ob nBOOT0=0x0 -ob nSWBOOT0=0x0 -ob nBOOT1=0x1 -ob RDP=0xBB',capture_output=True,text=True).stdout
        if ("Option Bytes successfully programmed" in self.result) or ("Warning: Option Byte: rdp, value: 0xBB, was not modified.\n\nWarning: Option Bytes are unchanged, Data won't be downloaded" in self.result) :
            return 0
        else:
            return -1
            
    def program_OB(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -ob BOOT_LOCK=0x1 -ob nBOOT0=0x0 -ob nSWBOOT0=0x0 -ob nBOOT1=0x1 -ob',capture_output=True,text=True).stdout
        if ("Option Bytes successfully programmed" in self.result) or ("Warning: Option Byte: rdp, value: 0xBB, was not modified.\n\nWarning: Option Bytes are unchanged, Data won't be downloaded" in self.result) :
            return 0
        else:
            return -1
    
    def reset(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -rst',capture_output=True,text=True).stdout
        if ("Software reset is performed" in self.result) :
            return 0
        else:
            return -1
    
    def hard_reset(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -HardRst',capture_output=True,text=True).stdout
        if ("Hard reset is performed" in self.result) :
            return 0
        else:
            return -1
        
    def run(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -run',capture_output=True,text=True).stdout
        if ("Core run" in self.result) :
            return 0
        else:
            return -1
    
    def erase(self):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -vb 1 --erase all',capture_output=True,text=True).stdout
        if ("Mass erase successfully achieved" in self.result):
            return 0
        else:
            return -1
    
    def flash(self,fname):
        self.result = subprocess.run('STM32_Programmer_CLI.exe --connect port=SWD freq=24000 ap=0 mode=UR -vb 1 --download '+ fname + ' 0x08000000'+' --verify',capture_output=True,text=True).stdout
        if ("Download verified successfully" in self.result):
            return 0
        else:
            return -1

def main():
    device = stmdevice()
    while(1):
        print("\n\rProgramming with  \r\nFILE : "+fname)
        input("\n\rPress ENTER to continue...")
        if device.unlock()==0 :
            print("\n\rDEVICE ULOCKED")
        else:
            print("\n\rDEVICE UNLCOK_ERROR !!!!")
            continue
        if device.program_BootOptions()==0 :
            print("\n\rOPTION BYTES PROGRAMMED")
        else:
            print("\n\rOPTION BYTES PROGRAMING ERROR !!!!")
            continue
        if device.erase()==0 :
            print("\n\rDEVICE ERASED")
        else:
            print("\n\rDEVICE ERASE ERROR!!!!")
            continue
        if device.flash(fname)==0 :
            print("\n\rDEVICE PROGRAMMED")
        else:
            print("\n\rDEVICE PROGRAMMIMG ERROR !!!!")
            continue
        if device.reset()==0 :
            print("\n\rDEVICE RESET DONE")
        else:
            print("\n\rDEVICE RESET ERROR !!!!")
            continue
        if device.reset()==0 :
            print("\n\rDEVICE RESET DONE")
        else:
            print("\n\rDEVICE RESET ERROR !!!!")
            continue
        print("\n\rDEVICE PROGRAMMED SUCCESSFULLY\n\r")
        print("\n\r===========================================\n\r\n\r")
    

main()
 
