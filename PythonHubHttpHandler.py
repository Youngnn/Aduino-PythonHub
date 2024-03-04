from http.server import HTTPServer, SimpleHTTPRequestHandler

class PythonHubHttpHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/': self.writeHome() # root or home
        elif self.path == '/measvolt1': self.writeMeasVolt1() # 호출한다
        else: self.writeFail()
    def writeHead(self, nStateCode):
        self.send_response(nStateCode)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def writeHtml(self, sHtml):
        self.wfile.write(sHtml.encode())
    def writeHome(self):
        self.writeHead(200)
        output = '<html><head>'
        output += '<meta http=equiv="Content-type" content="text/html" charset="UTF-8">'
        output += '<title> MyPy web server </title></head>'
        output += '<body>'
        output += '<div><a href="/measvolt1">전압 한 번 측정</a></div>' #home으로 가는 경로
        output += '<div> Iot시스템설계 수업 웹사이트 </div>'
        output += f'<div>current path: {self.path}</div>'
        output += f'<div>current mothod: {self.command}</div>'
        output += '<div> 전압 측정표 <div>'#확인해보기
        output += '<div>' + self.server.gateway.writeHtmlTableVolt() + '<div>' #self.server는 접근경로이다 바꿔주면 안됨
        output += '</body></html>'
        self.writeHtml(output)
    def writeFail(self):
        self.writeHead(404)
    def writeMeasVolt1(self):
        self.server.gateway.insertDbMeasVolt()
        self.writeHead(200)
        output = '<html><head>'
        output += '<meta http=equiv="Content-type" content="text/html" charset="UTF-8">'
        output += '<title>전압 한 번 측정</title></head>'
        output += '<body>'
        output += '<div><a href="/">Home</a></div>' #home으로 가는 경로
        output += '<div>전압 한 번 측정 완료</div>'
        output += f'<div>current path: {self.path}</div>'
        output += f'<div>current mothod: {self.command}</div>'
        output += f'<div>전압 측정값 회수 = {self.server.gateway.countDbVolt()}</div>'#측정
        output += '</body></html>'
        self.writeHtml(output)
        
        
        
        
        