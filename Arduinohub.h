#pragma once

#include <Voltmeter.h>
#include <StringTok.h>
#include <MyServo.h>
#define NUM_CHECK_LINE (5) //Line이 있는지 없는지 확인하는 것 (횟수)
#define PORT_VOLTMETER (A2) //get volt
#define NUM_PREC (3)
#define PORT_SERVO (3) //swing 90



class ArduinoHub
{
  public: //member
     //생성자
     ArduinoHub(void) {}

    //Method(member 함수)
    void init(void) 
    {
        m_voltmeter.setPort(PORT_VOLTMETER);
        m_servo.setPort(PORT_SERVO);
    }

    void start(void) 
    {
      while(true)
      {
          m_stCmd.appendString(getSerialInput());
          if (!m_stCmd.isEmpty() && m_stCmd.hasLine())
          {
            String sToken = parseCmd();
            exeCmd(sToken);
          }

      }
    }
    
protected:
     //Properties(member 변수) //접근 가능하게 한다.
     int m_nPrec = NUM_PREC;
     StringTok m_stCmd;
     Voltmeter m_voltmeter;
     MyServo m_servo;

     //Method(member 함수)
     String getSerialInput(void)
     {
        StringTok stInput;
        if(Serial.available() > 0){
          stInput.appendSerial();
          if(!stInput.isEmpty()){
          int nCheckLine = 0;
          while (!stInput.hasLine()){  //hasLine함수는 명령어 끝에 t면 enter가 있고 f면 없는 것을 알려주는 함수 //위의 함수 통과시 enter를 가지게 된다.
            stInput.appendSerial(); //appendSerial()은 Serial로부터 입력받아서 StringTok에 붙이기 
            nCheckLine++; //위의 int nCheckLine = 0;에서 받아서 증가
            if (nCheckLine > NUM_CHECK_LINE) break; //더 안정적으로 돌기 위해서 
        }
      }
    }
          return stInput.toString();
    }

    String parseCmd(void) 
    {
        return m_stCmd.cutToken().toString(); //cut and get token 자르면서 가져옴
    }                                       //구문분석후 처리하는 곳

    void exeCmd(String sToken) 
    {
      if (sToken == "get") exeGet();
      else if (sToken == "prec") exePrec();
      else if (sToken == "move") exeMove();
      else if (sToken == "swing") exeSwing();
    }                                      //실행하는 것.

    void exeGet(void)
    {
        String sToken = parseCmd();
        if(sToken == "volt") exeGetVolt();
        else if (sToken == "voltstep") exeGetVoltStep();
        else if (sToken == "servo") exeGetServo();
    }

    void exeGetVolt(void)
    {
      double volt = m_voltmeter.getVolt();
      Serial.println(String(volt, m_nPrec));
    }

    void exeGetVoltStep(void)
    {
      int nStep = m_voltmeter.getStep();
      Serial.println(nStep);
    }

    void exeGetServo(void)
    {
      int nAng = m_servo.getServo();
      Serial.println(nAng);
    }


    void exePrec(void)
    {
      String sToken = parseCmd();
      m_nPrec = sToken.toInt();
      
    }

    void exeMove(void)
    {
      String sToken = parseCmd();
      int nAng = sToken.toInt();
      m_servo.move(nAng);
    }

    void exeSwing(void)
    {
      String sToken = parseCmd();
      int nCount = sToken.toInt();
      m_servo.swing(nCount);
    }
};
