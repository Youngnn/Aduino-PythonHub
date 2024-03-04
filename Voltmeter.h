#pragma once //전직적인 명칭 => pragma, 한 번만 include한다. =>once 

class Voltmeter //class 정의 (자바와 같은 방식) //객체의 특징은 캡슐화 class {}의 {}로 감싸 캡슐화 해준 것.
{
    
}; //접근권한을 줄 수 있다. 접근권한은 public을 주어-> 외부접근이 가능하게 만든다.
   //접근방법 : class이름 쓰고 .찍고 접근, private는 외부접근 절대 불가

public:
 //public은 전체를 주고 외부접근 가능하고 상속접근이 가능하다.
                    //Constructor이다.  -> Voltmeter라는 같은 이름을 썼기에 Constructor
        Voltmeter(void) {} //void는입력없다고 표시해준 것.
        Voltmeter(int nVoltPort) //위처럼 없던가, 입력을 넣어 포트를 초기화 시킬 수 도 있다.
        {
            int m_nVoltPort = nVoltPort; //저장시킴
        }
          //private: //private는 한 곳만 주고 상속접근이 불가능하다.
protected : //외부접근이 불가능하지만 상속접근은 가능하다.
          //Properties(멤버 변수)
          int m_nVoltPort; //m_ : 멤버라는 뜻
};