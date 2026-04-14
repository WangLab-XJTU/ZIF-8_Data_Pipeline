# logger.py
from datetime import datetime

class Logger(object):


    def __init__(self,file_name='Log.log',format_time = "%m-%d %H:%M:%S"):
        
        self.file_name = file_name
        self.format_time = format_time


    def info(self,info):

        time = datetime.now().strftime(self.format_time)
        with open(self.file_name,'a') as f:
            f.write(f'{time} [INFO] {info}\n')
    
    def error(self,error):

        time = datetime.now().strftime(self.format_time)
        with open(self.file_name,'a') as f:
            f.write(f'{time} [ERROR] {error}\n')
    
        

if __name__ == "__main__":
    Log = Logger()
    Log.info('Hello!')
    Log.error('ERROR')