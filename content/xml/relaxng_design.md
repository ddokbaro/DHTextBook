---
title: "대안적 스키마 설계: RelaxNG의 직관적 트리 패턴"
description: "XSD의 복잡성을 극복하고 인간 친화적인 문법으로 XML의 트리 구조를 검증하는 RelaxNG(XML/Compact 문법)의 철학과 실무"
---

# 대안적 스키마 설계: RelaxNG의 직관적 트리 패턴

DTD는 문법이 이질적이고 데이터 타입이 부재했으며, 이를 극복하기 위해 등장한 XML Schema(XSD)는 강력하지만 인간이 읽고 쓰기에는 지나치게 장황하고 복잡(Verbose)하다는 비판을 받았습니다. 

이러한 XSD의 복잡성에 반발하여, 제임스 클라크(James Clark)를 위시한 컴퓨터 과학자들은 수학적 정형 언어 이론에 기반을 둔 훨씬 우아하고 직관적인 스키마 언어인 “**RelaxNG(REgular LAnguage for XML Next Generation)**”를 창안했습니다. 이 장에서는 트리 패턴 매칭(Tree Pattern Matching)을 통해 XML 문서의 구조를 직관적으로 검증하는 RelaxNG의 철학과, 디지털 문헌학 실무에서 각광받는 “**컴팩트 문법(Compact Syntax)**” 설계법을 심층적으로 다룹니다.

## 1. RelaxNG의 철학과 트리 패턴 매칭

RelaxNG의 핵심 철학은 “**스키마 설계는 복잡한 객체 지향 프로그래밍이 아니라, 직관적인 패턴 매칭이어야 한다**”는 것입니다. 

파서(Parser)는 RelaxNG 스키마에 정의된 논리적 나무(Tree)의 형태와, 실제 작성된 XML 문서의 나무 형태를 겹쳐본 뒤, 두 패턴이 완벽하게 일치하는지만을 수학적으로 검증합니다. 복잡한 상속이나 객체 지향적 개념을 배제하여 인문학 전공자들도 쉽게 스키마의 뼈대를 파악할 수 있도록 진입 장벽을 대폭 낮추었습니다.



## 2. 두 가지 얼굴: XML 문법과 컴팩트 문법(RNC)

RelaxNG의 가장 큰 특징은 완벽하게 동일한 논리 구조를 “**두 가지 다른 문법**”으로 작성할 수 있다는 점입니다.

1. **XML 문법 (`.rng`):** XSD처럼 XML 태그 형태로 스키마를 작성합니다. 기계가 처리하기에는 좋으나 사람이 읽고 쓰기에는 여전히 태그가 너무 많아 피로감을 줍니다.
2. **컴팩트 문법 (`.rnc`, Compact Syntax):** XML 태그의 껍데기를 모두 벗겨내고, 텍스트 기반의 직관적인 기호로 구조를 표현합니다. EBNF(확장 배커스-나우르 표기법)나 JSON과 유사하여 가독성이 압도적으로 뛰어납니다.

디지털 인문학계, 특히 방대한 텍스트 규칙을 다루는 TEI(Text Encoding Initiative) 커뮤니티에서는 스키마를 커스텀할 때 이 “**컴팩트 문법(RNC)**”을 압도적으로 선호합니다. 따라서 본 장에서도 실무적 활용도가 높은 컴팩트 문법을 중심으로 설명합니다.

## 3. 컴팩트 문법(RNC)의 기초 설계

RelaxNG 컴팩트 문법은 중괄호(`{ }`)와 등호(`=`)를 사용하여 요소의 포함 관계를 시각적으로 매우 깔끔하게 표현합니다.

### 3.1 요소(Element)와 속성(Attribute)의 선언
`<잡지 발행년도="1920">개벽</잡지>`라는 XML을 검증하기 위한 RNC 설계는 다음과 같습니다.

```relaxng
element 잡지 {
    attribute 발행년도 { text },
    text
}
```
* `element`와 `attribute`라는 예약어를 사용하여 명시적으로 구조를 선언합니다.
* 쉼표(`,`)는 DTD와 마찬가지로 순차적 등장을 의미합니다. 즉, 속성이 먼저 선언되고 그 뒤에 일반 텍스트가 나온다는 패턴을 정의한 것입니다.

### 3.2 빈도 제어 연산자의 부활
RelaxNG는 XSD의 무거운 `minOccurs`, `maxOccurs` 대신, 연구자들에게 친숙한 DTD와 정규표현식의 기호 연산자(`?`, `*`, `+`)를 다시 채택하여 간결함을 극대화했습니다.

```relaxng
element 기사 {
    element 제목 { text },
    element 부제 { text }?,  # 0번 또는 1번 (선택)
    element 필자 { text }+,  # 1번 이상 무한대 (필수)
    element 주석 { text }* # 0번 이상 무한대 (선택적 반복)
}
```

## 4. 무순서 배치 연산자: Interleave (`&`)

RelaxNG가 XSD를 압도하는 가장 강력하고 유연한 기능 중 하나가 바로 “**인터리브(Interleave, `&`)**” 연산자입니다. 

XSD의 `<xs:all>`은 자식 요소들의 순서를 자유롭게 섞을 수 있게 해주지만, 각 요소가 반드시 1번씩만 등장해야 한다는 치명적인 제약이 있었습니다. 반면 RelaxNG의 `&` 연산자는 “**순서는 상관없지만, 각각의 요소가 가진 빈도 규칙(+, * 등)은 철저히 지켜라**”라는 고도의 패턴 융합을 단 한 줄의 기호로 가능하게 합니다.

```relaxng
element 메타데이터 {
    element 발행일 { text } &
    element 저자 { text }+ &
    element 삽화 { text }*
}
```
* **해석:** 발행일 1번, 저자 1명 이상, 삽화 0개 이상이 등장해야 하는데, 이 세 가지 요소가 **XML 문서 내에서 어떤 순서로 뒤섞여 등장하더라도** 모두 유효한 문서로 인정합니다. 형태가 자유로운 고문헌이나 파편화된 역사 사료를 모델링할 때 이보다 훌륭한 문법은 없습니다.

## 5. XSD 데이터 타입의 수용

RelaxNG는 XSD의 복잡한 구조 문법은 거부했지만, XSD가 W3C 표준으로 정립해 놓은 44가지의 “**내장 데이터 타입(Built-in Data Types)**”의 강력함은 그대로 수용했습니다. 

스키마 상단에 데이터 타입 라이브러리(Datatypes)를 선언하면, RNC 내부에서 `xsd:integer`, `xsd:gYear` 등을 자유롭게 가져다 쓸 수 있습니다.

```relaxng
datatypes xsd = "[http://www.w3.org/2001/XMLSchema-datatypes](http://www.w3.org/2001/XMLSchema-datatypes)"

element 서지정보 {
    element 발행년도 { xsd:gYear },
    element 페이지수 { xsd:integer }
}
```

## 6. 실전 인문학 데이터 설계: RNC 활용

거대 데이터베이스의 기사 스키마를 RelaxNG 컴팩트 문법(RNC)으로 통합 설계해 보겠습니다. XSD로 작성했다면 수십 줄이 넘어갈 코드가 어떻게 한눈에 들어오는 직관적인 텍스트로 압축되는지 확인해 보십시오.

**[RelaxNG 컴팩트 문법 설계 실전]**
```relaxng
datatypes xsd = "[http://www.w3.org/2001/XMLSchema-datatypes](http://www.w3.org/2001/XMLSchema-datatypes)"

start = element 잡지자료 {
    element 메타데이터 {
        attribute 잡지ID { xsd:ID },
        element 잡지명 { text },
        element 창간년도 { xsd:gYear },
        element 권호 { text }?
    },
    element 기사목록 {
        element 기사 { 기사패턴 }+
    }
}

# 복잡한 패턴은 변수처럼 정의하여 재사용 가능 (패턴 모듈화)
기사패턴 = 
    attribute 기사ID { xsd:ID },
    element 제목 { text },
    element 필자 { text }+,
    ( element 본문 { text } | element 스캔본 { xsd:anyURI } )
```

위의 예시에서 볼 수 있듯, `start`라는 키워드로 문서의 루트 요소를 명시적으로 지정하고, 복잡한 `<기사>` 내부의 구조를 `기사패턴`이라는 이름으로 모듈화하여 재사용하는 방식은 일반적인 프로그래밍의 변수 선언만큼이나 직관적입니다. 

결론적으로 RelaxNG는 XSD의 수학적 엄밀성(데이터 타입 검증)과 DTD의 가독성(기호 연산자)을 모두 취한, 설계자 친화적인 하이브리드 언어입니다. 이러한 인간 친화적인 특성 때문에 인문학 표준 인코딩 그룹은 스키마 제어 도구로 RelaxNG를 널리 채택하고 있습니다.

구조와 타입을 통제하는 선언적 언어를 마스터했으니, 이어지는 장에서는 이 거대한 XML 트리 구조 속에서 내가 원하는 특정 정보만을 핀셋처럼 집어내고, 구조적 패턴이 아닌 '비즈니스 룰' 자체를 검증하는 또 다른 패러다임, “**XPath 기반의 Schematron**”의 세계로 나아가겠습니다.

:::{seealso} 📖 참고문헌
* **Clark, James (2001).** <RELAX NG Compact Syntax>. <a href="https://www.oasis-open.org/committees/relax-ng/compact-20021121.html" target="_blank">OASIS Committee Specification</a>
:::