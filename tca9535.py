from periphery import I2C
from enum import IntEnum
import math
import time

class Pin(IntEnum):
    P0_0 = (1 << 0) 
    P0_1 = (1 << 1)
    P0_2 = (1 << 2)
    P0_3 = (1 << 3)
    P0_4 = (1 << 4)
    P0_5 = (1 << 5)
    P0_6 = (1 << 6)
    P0_7 = (1 << 7)

    P1_0 = (1 << 8)
    P1_1 = (1 << 9)
    P1_2 = (1 << 10) 
    P1_3 = (1 << 11)
    P1_4 = (1 << 12)
    P1_5 = (1 << 13)
    P1_6 = (1 << 14) 
    P1_7 = (1 << 15)

class Mode(IntEnum):
    OUTPUT = 0
    INPUT = 1

class Value(IntEnum):
    HIGH = 1  
    LOW = 0

class TCA9535():
    def __init__(self, i2c_bus='/dev/i2c-0', address=0x20):
        # I2C bus
        self.i2c = I2C(i2c_bus)

        # i2c address
        self.address = address

        # Control registers address 
        self.INPUT_PORT_0_ADDR = 0x00 
        self.INPUT_PORT_1_ADDR = 0x01
        self.OUTPUT_PORT_0_ADDR = 0x02
        self.OUTPUT_PORT_1_ADDR = 0x03
        self.POLARITY_INV_PORT_0_ADDR = 0x04
        self.POLARITY_INV_PORT_1_ADDR = 0x05
        self.CONF_PORT_0_ADDR = 0x06
        self.CONF_PORT_1_ADDR = 0x07

        # Control register values(default)
        self.INPUT_PORT_0 = 0x00 
        self.INPUT_PORT_1 = 0x00
        self.OUTPUT_PORT_0 = 0xFF
        self.OUTPUT_PORT_1 = 0xFF
        self.POLARITY_INV_PORT_0 = 0x00
        self.POLARITY_INV_PORT_1 = 0x00
        self.CONF_PORT_0 = 0xFF
        self.CONF_PORT_1 = 0xFF

        # Read registers from device
        # Input Port 0 
        self.INPUT_PORT_0 = self.read_register(self.INPUT_PORT_0_ADDR)
        print("INPUT_PORT_0 = 0x{:02x}".format(self.INPUT_PORT_0))

        # Input Port 1
        self.INPUT_PORT_1 = self.read_register(self.INPUT_PORT_1_ADDR)
        print("INPUT_PORT_1 = 0x{:02x}".format(self.INPUT_PORT_1))

        # Output Port 0
        self.OUTPUT_PORT_0 = self.read_register(self.OUTPUT_PORT_0_ADDR)
        print("OUTPUT_PORT_0 = 0x{:02x}".format(self.OUTPUT_PORT_0)) 

        # Output Port 1
        self.OUTPUT_PORT_1 = self.read_register(self.OUTPUT_PORT_1_ADDR)
        print("OUTPUT_PORT_1 = 0x{:02x}".format(self.OUTPUT_PORT_1))

        # Polarity Inversion Port 0 
        self.POLARITY_INV_PORT_0 = self.read_register(self.POLARITY_INV_PORT_0_ADDR)
        print("POLARITY_INV_PORT_0 = 0x{:02x}".format(self.POLARITY_INV_PORT_0))

        # Polarity Inversion Port 1
        self.POLARITY_INV_PORT_1 = self.read_register(self.POLARITY_INV_PORT_1_ADDR)
        print("POLARITY_INV_PORT_1 = 0x{:02x}".format(self.POLARITY_INV_PORT_1))

        # Configuration Port 0
        self.CONF_PORT_0 = self.read_register(self.CONF_PORT_0_ADDR)
        print("CONF_PORT_0 = 0x{:02x}".format(self.CONF_PORT_0))

        # Configuration Port 1
        self.CONF_PORT_1 = self.read_register(self.CONF_PORT_1_ADDR)
        print("CONF_PORT_1 = 0x{:02x}".format(self.CONF_PORT_1))


    def pin_mode(self, pin, mode):
        p = int(pin)
        m = int(mode)

        # PORT_1 (P1_0, ... P1_7)        
        if p > 255:
            p = p >> 8
            # mode
            if m:
                # input mode
                self.CONF_PORT_1 = self.CONF_PORT_1 | p
                print("--Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print("--CONF_PORT_1: 0b{:08b}".format(self.CONF_PORT_1))
            else:
                # output mode
                self.CONF_PORT_1 = self.CONF_PORT_1 & ~p        
                print("--Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print("--CONF_PORT_1: 0b{:08b}".format(self.CONF_PORT_1))
            self.write_register(self.CONF_PORT_1_ADDR, self.CONF_PORT_1)

        # PORT_0 (P0_0, ... P0_7)
        else:
            # mode
            if m:
                # input mode
                self.CONF_PORT_0 = self.CONF_PORT_0 | p
                print("--Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print("--CONF_PORT_0: 0b{:08b}".format(self.CONF_PORT_0))

            else:
                # output mode
                self.CONF_PORT_0 = self.CONF_PORT_0 & ~p
                print("--Pin:{}  Mode:{}".format(int(math.log2(p)), m))
                print("--CONF_PORT_0: 0b{:08b}".format(self.CONF_PORT_0))
            self.write_register(self.CONF_PORT_0_ADDR, self.CONF_PORT_0)

                
    def write_pin(self, pin, value):
        p = int(pin)
        v = int(value)
        # PORT_1 (P1_0, ... P1_7)        
        if p > 255:
            p = p >> 8
            # value
            if v:
                # high value
                self.OUTPUT_PORT_1 = self.OUTPUT_PORT_1 | p
                print("--Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print("--OUTPUT_PORT_1:{0:b}".format(self.OUTPUT_PORT_1))
            else:
                # low value
                self.OUTPUT_PORT_1 = self.OUTPUT_PORT_1 & ~p        
                print("--Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print("--OUTPUT_PORT_1:{0:b}".format(self.OUTPUT_PORT_1))
        
            self.write_register(self.OUTPUT_PORT_1_ADDR, self.OUTPUT_PORT_1)
        
        # PORT_0 (P0_0, ... P0_7)
        else:
            # value
            if v:
                # high value
                self.OUTPUT_PORT_0 = self.OUTPUT_PORT_0 | p
                print("--Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print("--OUTPUT_PORT_0:{0:b}".format(self.OUTPUT_PORT_0))  
            else:
                # low value
                self.OUTPUT_PORT_0 = self.OUTPUT_PORT_0 & ~p        
                print("--Pin:{}  Value:{}".format(int(math.log2(p)), v))
                print("--OUTPUT_PORT_0:{0:b}".format(self.OUTPUT_PORT_0))
 
            self.write_register(self.OUTPUT_PORT_0_ADDR, self.OUTPUT_PORT_0)

    def read_pin(self, pin):
        p = int(pin)
        
        # PORT_1 (P1_0, ... P1_7)        
        if p > 255:
            p = p >> 8
            # Read I2C PORT_1
            self.INPUT_PORT_1 = self.read_register(self.INPUT_PORT_1_ADDR)
            r = Value.HIGH if (self.INPUT_PORT_1 & p) > 0 else Value.LOW
            return r
        # PORT_0 (P0_0, ... P0_7)
        else:
            # Read I2C PORT_0
            self.INPUT_PORT_0 = self.read_register(self.INPUT_PORT_0_ADDR)
            r = Value.HIGH if (self.INPUT_PORT_0 & p) > 0 else Value.LOW
            return r
                
    def read_register(self, register):
        msgs = [I2C.Message([register]), I2C.Message([0x00], read = True)]
        self.i2c.transfer(self.address, msgs)
        return msgs[1].data[0]

    def write_register(self, register, value):
        msgs = [I2C.Message([register, value])]
        self.i2c.transfer(self.address, msgs)
        time.sleep(0.005) #sleep for 5ms

    def set_polarity(self, port0 = 0x00, port1 = 0x00):
        self.POLARITY_INV_PORT_0 = port0
        self.POLARITY_INV_PORT_1 = port1
        self.write_register(self.POLARITY_INV_PORT_0_ADDR, port0)
        self.write_register(self.POLARITY_INV_PORT_1_ADDR, port1)

    def config_ports(self, port0 = 0x00, port1 = 0x00):
        self.CONF_PORT_0 = port0 
        self.CONF_PORT_1 = port1
        self.write_register(self.CONF_PORT_0_ADDR, port0)
        self.write_register(self.CONF_PORT_1_ADDR, port1)

    def set_ports(self, port0 = 0x00, port1 = 0x00):
        self.OUTPUT_PORT_0 = port0 
        self.OUTPUT_PORT_1 = port1 
        self.write_register(self.OUTPUT_PORT_0_ADDR, port0)
        self.write_register( self.OUTPUT_PORT_1_ADDR, port1)

    def get_ports(self):
        self.INPUT_PORT_0 = self.read_register(self.INPUT_PORT_0_ADDR)
        self.INPUT_PORT_1 = self.read_register(self.INPUT_PORT_1_ADDR)
        return (self.INPUT_PORT_0, self.INPUT_PORT_1)

    def print_all_registers(self):
        # Read registers from device
        # Input Port 0 
        self.INPUT_PORT_0 = self.read_register(self.INPUT_PORT_0_ADDR)
        print("INPUT_PORT_0 = 0x{:02x}".format(self.INPUT_PORT_0))

        # Input Port 1
        self.INPUT_PORT_1 = self.read_register(self.INPUT_PORT_1_ADDR)
        print("INPUT_PORT_1 = 0x{:02x}".format(self.INPUT_PORT_1))

        # Output Port 0
        self.OUTPUT_PORT_0 = self.read_register(self.OUTPUT_PORT_0_ADDR)
        print("OUTPUT_PORT_0 = 0x{:02x}".format(self.OUTPUT_PORT_0)) 

        # Output Port 1
        self.OUTPUT_PORT_1 = self.read_register(self.OUTPUT_PORT_1_ADDR)
        print("OUTPUT_PORT_1 = 0x{:02x}".format(self.OUTPUT_PORT_1))

        # Polarity Inversion Port 0 
        self.POLARITY_INV_PORT_0 = self.read_register(self.POLARITY_INV_PORT_0_ADDR)
        print("POLARITY_INV_PORT_0 = 0x{:02x}".format(self.POLARITY_INV_PORT_0))

        # Polarity Inversion Port 1
        self.POLARITY_INV_PORT_1 = self.read_register(self.POLARITY_INV_PORT_1_ADDR)
        print("POLARITY_INV_PORT_1 = 0x{:02x}".format(self.POLARITY_INV_PORT_1))

        # Configuration Port 0
        self.CONF_PORT_0 = self.read_register(self.CONF_PORT_0_ADDR)
        print("CONF_PORT_0 = 0x{:02x}".format(self.CONF_PORT_0))

        # Configuration Port 1
        self.CONF_PORT_1 = self.read_register(self.CONF_PORT_1_ADDR)
        print("CONF_PORT_1 = 0x{:02x}".format(self.CONF_PORT_1))