import serial
import time
#s = serial.Serial('COM6',9600)
#s = serial.Serial('COM3',19200)
#cmd = '*RUN\x0D'
#cmd='*STP\x0D'
#s.write(cmd)


class pump( object ):
    def __init__( self, port = 'COM10', baud = 19200,timeout=1):
        self.ser = serial.Serial(port, baud, timeout=timeout)
        print('Connect to pump at: %s'%self.ser.name)
    def cmd(self, cmds):
        cmd_ = '%s\x0D'%cmds
        self.ser.write(cmd_)

    def find_pumps(self,tot_range=10):
        '''Not test yet'''
        pumps = []
        for i in range(tot_range):
            self.ser.write('%iADR\x0D'%i)
            output = self.ser.readline()
            if len(output)>0:
                pumps.append(i)
        self.pumps=pumps        
        return pumps        

    def get_direction(self, pump=0):
        ser = self.ser
        cmd = '%iDIR\x0D'%pump
        ser.write(cmd)
        output = ser.readline()
        sign = '+'
        if output[4:7]=='WDR':
            sign = '-'        
        return sign

    def set_direction(self, direction='INF', pump=0):
        '''INF for in; WDR for withdraw'''
        cmd = ''
        ser = self.ser
        #direction = 'INF'
        #if flowrate<0: direction = 'WDR'
        frcmd = '%iDIR%s\x0D'%(pump,direction)
        ser.write(frcmd)
        output = ser.readline()
        if '?' in output: print frcmd.strip()+' from set_rate not understood'

    def set_rate(self, flowrate, unit='UM*', pump=0):
        cmd = ''
        ser = self.ser
        direction = 'INF'
        if flowrate<0: direction = 'WDR'
        frcmd = '%iDIR%s\x0D'%(pump,direction)
        ser.write(frcmd)
        output = ser.readline()
        if '?' in output: print frcmd.strip()+' from set_rate not understood'
        fr = abs(flowrate) 
        cmd += str(pump)+'RAT'+str(fr)[:5]+ unit
        cmd += '\x0D'
        ser.write(cmd)
        output = ser.readline()
        if '?' in output: print cmd.strip()+' from set_rates not understood'

    def set_diameter(self,dia, pump = 0):
        ser = self.ser
        cmd = '%iDIA%s\x0D'%(pump,dia)
        ser.write(cmd)
        output = ser.readline()
        if '?' in output: print cmd.strip()+' from set_diameter not understood'

        
    def get_diameter(self,pump=0):
        ser = self.ser
        cmd = '%iDIA\x0D'%pump
        ser.write(cmd)
        output = ser.readline()
        if '?' in output: print cmd.strip()+' from get_diameter not understood'
        dia = output[4:-1]
        return dia
    
    def set_volume(self,vol, unit='UL', pump = 0):
        ser = self.ser
        cmd = '%iVOL %s\x0D'%(pump,vol )
        #print(cmd)
        ser.write(cmd)
        #cmd = '%iVOL %s\x0D'%(pump , unit)
        #ser.write(cmd)        
        output = ser.readline()
        if '?' in output: print cmd.strip()+' from set_volme not understood'

        
    def get_volume(self,pump=0):
        ser = self.ser
        cmd = '%iVOL\x0D'%pump
        ser.write(cmd)
        output = ser.readline()
        if '?' in output: print cmd.strip()+' from get_vol not understood'
        #print(output)
        vol = output[4:-3]
        unit = output[-3:-1]
        return float(vol), unit
    
    def get_dispense(self,  direction='INF', pump = 0):
        #_,unit = self.get_volume()
        ser = self.ser
        cmd = '%iDIS\x0D'%(pump )
        ser.write(cmd)
        output = ser.readline()
        if '?' in output: print cmd.strip()+' from get_dispense not understood'
        unit = output[-3:-1]
        if direction=='INF':
            output= output[5:10]
        elif direction=='WDR':
            output= output[11:16]
        return float(output), unit
        
        
    def reset_dispense(self,direction='INF', pump=0):
        ser = self.ser
        cmd = '%iCLD %s\x0D'%(pump,direction)
        ser.write(cmd)
        output = ser.readline()
        if '?' in output: print cmd.strip()+' from reset_dispense not understood'
 
    
    def get_rate(self,pump=0):
        #get direction
        ser = self.ser
        cmd = '%iDIR\x0D'%pump
        ser.write(cmd)
        output = ser.readline()
        sign = '+'
        if output[4:7]=='WDR':
            sign = '-'
        cmd = '%iRAT\x0D'%pump
        ser.write(cmd)
        output = ser.readline()
        if '?' in output: print cmd.strip()+' from get_rate not understood'
        units = output[-3:-1]
        #print(units)
        if units=='NH':
            rate = str(float(output[4:-3])*1000)
        elif units=='UH':
            rate = output[4:-3] + ' ul/hour'
        elif units=='MH':
            rate = str(float(output[4:-3])*1000)  + ' ml/hour'   
        elif units=='UM':
            rate = output[4:-3] + ' ul/min'            
        return sign+rate

    

    def run(self, pump=None):
        '''pump should be '00' or '01', which is set by
            setup on the controller pannel'''
        cmd = 'RUN'
        if pump is not None:
            cmd=str(pump) +  cmd
        self.cmd( cmd )
        
    def stop(self, pump=None):
        '''pump should be '00' or '01', which is set by
            setup on the controller pannel'''        
        cmd = 'STP'
        if pump is not None:
            cmd=str(pump) +  cmd
        self.cmd( cmd )
        
    def get_version(self):
        cmd = 'ver\x0D'
        self.ser.write(cmd) 
    def set_(self):
        pass
        
s = pump( )
def setp( vol=50, rate=10):
    s.set_volume(vol)
    s.set_rate(rate)
    s.reset_dispense()
#    s.run()
def start():
    s.reset_dispense()
    s.run()
    
def monitor():    
    for i in range(50):
        print(i,s.get_dispense() )
        time.sleep(5)
        
def start_pump( rate ):
    s.set_rate( rate )
    s.run()
def stop_pump( ):
    s.stop()
    



###An example
## set dispense volme as .3 ul
## set rate as 3 ul / min
## Code:
if False:#True:#False:
    s.set_volume(.3)
    s.set_rate( 3 )
    s.reset_dispense()  #set dispense volume to 0
    s.run()
    #s.stop()




    
