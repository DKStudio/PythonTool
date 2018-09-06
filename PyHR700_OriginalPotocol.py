# c:\python36
# coding = utf-8
import sys
import re
import serial
import logging

def main():
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    handlers = [logging.FileHandler('my.log', 'w', 'utf-8'),])
    # 定義 handler 輸出 sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # 設定輸出格式
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # handler 設定輸出格式
    console.setFormatter(formatter)
    # 加入 hander 到 root logger
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger('HR700')
    ServerStatus = 0
    logger.info("running...")
    logger.info("enter 'quit' for closing the server")
    Run_Command = 'Run_Server Port=([a-zA-Z0-9]+) Baud=([0-9]+) Byte=([7|8]) Parity=(EVEN|NONE|ODD) Stop=([1|2]) TimeOut=(0.[0-9]+)\n'
    Open_Slave_Command = 'open_slave ([0-9]+)\n'
    Close_Slave_Command = 'close_slave ([0-9]+)\n'
    HROpen_Command = '\bO {:0>2d}\r\n'
    HRTS0_Command = 'TS0\r\n'
    HRUpdate_Command = '\bT\r\n'
    HRRead_Command = 'FM1,{0:0>2d},{1:0>2d}\r\n'
    HRClose_Command = '\bC {:0>2d}\r\n'
    try:
        while True:
            cmd = sys.stdin.readline()
            if re.match("quit",cmd):
                logger.info('bye-bye\r\n')
                break
            elif re.match(Run_Command,cmd,re.I):
                Math_Objects = re.match(Run_Command,cmd,re.I)
                Port = Math_Objects.group(1)
                Baud = int(Math_Objects.group(2))
                Byte = int(Math_Objects.group(3))
                ParityString = Math_Objects.group(4).lower()
                if ParityString == 'none':
                    Parity = serial.PARITY_NONE
                elif ParityString == 'even':
                    Parity = serial.PARITY_EVEN
                elif ParityString == 'odd':
                    Parity = serial.PARITY_ODD
                else:
                    logger.info("unknown parity %s" % ParityString)
                Stop = int(Math_Objects.group(5))
                TimeOut = int(Math_Objects.group(6))
                MySerial = serial.Serial(Port,Baud,Byte,Parity,Stop,TimeOut)
                MySerial.open()
                ServerStatus = 1
            elif re.match(Open_Slave_Command,cmd,re.I):
                Math_Objects = re.match(Open_Slave_Command,cmd,re.I)
                Slave_ID = int(Math_Objects.group(1))
                MySerial.write(HROpen_Command.format(Slave_ID))
                MySerial.write(HRTS0_Command)
            #elif 
            else:
                logger.info("unknown command %s" % (cmd))
                
    finally:
        if ServerStatus >= 2:
            MySerial.write(HRClose_Command.format(Slave_ID))
        if ServerStatus >= 1:
            MySerial.close()
        

if __name__ == "__main__":
    main()