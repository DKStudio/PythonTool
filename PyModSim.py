# c:\python36
# coding = utf-8
import sys
import re
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial


def main():
    #main function
    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
    ServerStatus = 0
    logger.info("running...")
    logger.info("enter 'quit' for closing the server")
    Run_Command = 'Run_Server Port=([a-zA-Z0-9]+)\n'
    Add_Slave_Command = 'add_slave ([0-9]+)\n'
    Add_Block_Command = 'add_block ([0-9]+) (\'[a-zA-Z0-9]+\') ([1234]) ([0-9]+) ([0-9]+)\n'
    Set_Values = "set_values ([0-9]+) (\'[a-zA-Z0-9]+\') ([0-9]+) values=\'([0-9][0-9,]*)\'\n"
    try:
        while True:
            cmd = sys.stdin.readline()
            if re.match("quit",cmd):
                sys.stdout.write('bye-bye\r\n')
                break
            elif re.match(Run_Command,cmd,re.I):
                Port=re.match(Run_Command,cmd,re.I).group(1)
                logger.info("Port={}".format(Port))
                Server = modbus_rtu.RtuServer(serial.Serial(Port))
                Server.start()
                ServerStatus = 1
            elif re.match(Add_Slave_Command,cmd,re.I):
                if ServerStatus >= 1:
                    AddSlave_ID = int(re.match(Add_Slave_Command,cmd,re.I).group(1))
                    Server.add_slave(AddSlave_ID)
                    ServerStatus = 2
                    logger.info("Add Slave={}".format(AddSlave_ID))
                else:
                    logger.info("Server not running.")
            elif re.match(Add_Block_Command,cmd,re.I):
                if ServerStatus >= 2:
                    Math_Objects = re.match(Add_Block_Command,cmd,re.I)
                    Slave = Server.get_slave(int(Math_Objects.group(1)))
                    name = Math_Objects.group(2)
                    block_type = int(Math_Objects.group(3))
                    starting_address = int(Math_Objects.group(4))
                    length = int(Math_Objects.group(5))
                    Slave.add_block(name,block_type,starting_address,length)
                    ServerStatus = 3
                    logger.info("add_block in Slave={} name={} block_type={} starting_address={} length={}".format(Math_Objects.group(1),Math_Objects.group(2),Math_Objects.group(3),Math_Objects.group(4),Math_Objects.group(5)))
                else:
                    logger.info("no slave.")
            elif re.match(Set_Values,cmd,re.I):
                if ServerStatus >= 3:
                    Math_Objects = re.match(Set_Values,cmd,re.I)
                    Slave = Server.get_slave(int(Math_Objects.group(1)))
                    name = Math_Objects.group(2)
                    address = int(Math_Objects.group(3))
                    values = []
                    valuesString = Math_Objects.group(4).split(',')
                    for val in valuesString[0:]:
                        values.append(int(val))
                    Slave.set_values(name, address, values)
                    values = Slave.get_values(name, address, len(values))
                    logger.info("set_values in Slave={} name={} address={} values={}".format(Math_Objects.group(1),Math_Objects.group(2),Math_Objects.group(3),str(values)))
                else:
                    logger.info("no block.")
            else:
                sys.stdout.write("unknown command %s" % (cmd))

            




    finally:
        if ServerStatus == 1:
            sys.stdout.write("Server release")
            Server.remove_all_slaves()
            Server.stop()
            ServerStatus = 0

if __name__ == "__main__":
    main()