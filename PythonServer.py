from http.server import HTTPServer
from PythonHubHttpHandler import PythonHubHttpHandler # form module file import object (class) #모듈에서 가져오는 것
from PythonHub import PythonHub

class PythonServer:
    
    __defHostName = 'localhost' #인터넷 연결안되어 있으니까 localhost라고 적음
    __nDefPort = 8080 #포트도 default값으로 받게한다.
    def __init__(self, hostName = __defHostName, nPort = __nDefPort): #디폴트 값으로 받게
        self.hostName = hostName	#저장하는 부분
        self.nPort = nPort	#저장하는 부분
        self.webServer = HTTPServer((hostName, nPort), PythonHubHttpHandler)
        self.pyHub = None    #초기화 (오류를 막기위해)

    def initPythonHub(self): #생성해야한다.
        self.pyHub = PythonHub()
    def run(self):
        print(f'My web server started at http://{self.hostName}:{self.nPort}')
        self.webServer.gateway = self.pyHub  #이 길로만 가게 해준다.
        self.webServer.serve_forever()
        