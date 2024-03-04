from serial import Serial
import time
import psycopg2

class PythonHub:
    # Private Properties (Variables): 변수
    
    __sDefComName = 'COM6' # default value: sComName
    __nDefComBps = 9600 # default value: nComBps
    __defWaitTime = 0.5 # 단위 : 초
    
    # Constructor
    def __init__(self, sComName = __sDefComName, nComBps = __nDefComBps): # constructor
        self.ard = Serial(sComName, nComBps)
        self.clearSerial()
        self.tpVolt = ()
        self.tpVoltTime = ()
        self.conn = None
        self.cur = None
        self.clearVolt()
    def __del__(self): #destructor
        if self.ard.isOpen(): self.ard.close()
    
    #Public Methods
    def wait():
        time.sleep(PythonHub.__defWaitTime)
        
    
    # Serial Methods
    def readSerial(self):
        nRead = self.ard.inWaiting()
        if nRead > 0:
            btResult = self.ard.read(nRead)
            sResult = btResult.decode()
            return sResult
        else: return ''
    
    def writeSerial(self, sCmd):
        btCmd = sCmd.encode()
        return self.ard.write(btCmd)
    def clearSerial(self):
        PythonHub.wait()
        self.readSerial()
    def setSerialPrec(self, nPrec):
        nPrec = int(nPrec)
        self.talk('prec ' + str(nPrec))
    def talk(self, sCmd):
        return self.writeSerial(sCmd + '\n')
    def listen(self):
        PythonHub.wait()
        sResult = self.readSerial()
        return sResult.strip() # 좌우 공백 제거 
    def talkListen(self, sCmd):
        self.talk(sCmd)
        return self.listen()
        
    
    
    # Voltmeter Methods
    def getVolt(self):
        try:
            sVolt = self.talkListen('get volt')
            volt = float(sVolt)
            return volt
        except:
            print('Serial error')
            return 0.
    def getStep(self):
        try:
            sStep = self.talkListen('get voltstep')
            step = float(sStep)
            return step
        except:
            print('Serial error')
            return 0.
    def addVolt(self):
        measTime = time.time()
        volt = self.getVolt()
        if volt >= 0.:
            self.tpVolt += (volt,)
            self.tpVoltTime += (measTime,)
            print(f'volt = {volt} @ time = {measTime}')
            return True
        else: return False
        
    def sampleVolt(self, nCount, waitTime = __defWaitTime):
        i = 0
        while i < nCount:
            bResult = self.addVolt() # 성공: True, 실패: False
            if bResult:
                time.sleep(waitTime)
                i += 1
        
    def printVolt(self):
        for (volt, measTime) in zip(self.tpVolt, self.tpVoltTime):
            print(f'volt = {volt} @ time = {time.ctime(measTime)}')
            
    def clearVolt(self):
        self.tpVolt = ()
        self.tpVoltTime = () 
        
    
        
    # Motor Methods
    def moveMotor(self, nAng):
        nAng = int(nAng)
        self.talk('move ' + str(nAng))
        
    def swingMotor(self, num):
        num = int(num)
        self.talk('swing ' + str(num))

  # PostgreSQL Methods
    def connectDb(self):
        self.conn = psycopg2.connect(host='localhost', dbname='iot_db', user ="postgres", password="1234", port="5432")
        self.cur = self.conn.cursor()
    def closeDb(self):
        self.cur.close()
        self.conn.close()
    def exeCommit(self, sCmd):
        self.cur.execute(sCmd)
        self.conn.commit()
    def countDbVolt(self):
        self.connectDb()
        self.exeCommit('SELECT COUNT(*) FROM volt_table')
        nCount = self.cur.fetchone()[0]
        self.closeDb()
        return nCount
    
    def insertDbMeasVolt(self):
        # Arduino method
        measTime = time.time()
        volt = self.getVolt()
        while volt < 0:
            measTime = time.time()
            volt = self.getVolt()
        # PostgreSQL method
        nDbCount = self.countDbVolt()
        id = nDbCount + 1
        self.connectDb()
        self.exeCommit(f'INSERT INTO volt_table (id, volt, meas_time) VALUES ({id}, {volt}, {measTime})')
        self.closeDb()
    
    def insertDbAllVolt(self):
        nDbCount = self.countDbVolt()
        id = nDbCount + 1
        self.connectDb()
        for (volt, measTime) in zip(self.tpVolt, self.tpVoltTime):
            self.cur.execute(f'INSERT INTO volt_table (id, volt, meas_time) VALUES ({id}, {volt}, {measTime})')
            id += 1
        self.conn.commit()
        self.closeDb()
        self.clearVolt()
        
    def loadDbVolt(self):
        self.connectDb()
        self.exeCommit('SELECT volt, meas_time FROM volt_table')
        result = self.cur.fetchall()
        self.closeDb()
        for i in range (len(result)):
            volt = result[i][0]
            measTime = result[i][1]
            self.tpVolt +=(volt,)
            self.tpVoltTime +=(measTime,)
        self.printVolt()
    
    #Server Methods
    def writeHtmlTableVolt(self): #table 붙이기
        self.clearVolt() #튜플에 있는거 지우고
        self.loadDbVolt() #load 호출
        output = '<table border ="1"><thead>' #윤곽선 table 만듬
        output += '<tr><th>순서</th><th>전압(V)</th><th>측정 날짜 및 시간</th></tr>'
        output += '</thead><tbody>'
        i = 0 
        for (volt, measTime) in zip(self.tpVolt, self.tpVoltTime): #for로 돌려주기 튜플에 접근하기 위해서  load해주었기 때문에
            i += 1
            output += f'<tr><td>{i}</td><td>{volt}</td><td>{time.ctime(measTime)}</td></tr>'  
            #튜플이 두개여서 zip으로 묶어준것이고 output에 담아준 것
            
        output += '</tbody></table>'
        return output
        
        
        