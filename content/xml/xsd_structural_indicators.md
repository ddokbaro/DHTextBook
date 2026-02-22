---
title: "구조 지시자와 빈도 제어: sequence, choice, minOccurs"
description: "DTD의 기호 연산자를 객체 지향적으로 발전시킨 XSD의 구조 지시자와, minOccurs 및 maxOccurs를 활용한 초정밀 빈도 제어 기법"
---

# 구조 지시자와 빈도 제어: sequence, choice, minOccurs

이전 장에서 우리는 요소가 자식을 가지거나 속성을 품을 때 반드시 “**복합형(ComplexType)**”으로 설계해야 함을 배웠습니다. 그렇다면 그 자식 요소들은 어떤 순서로, 몇 번이나 등장해야 할까요?

DTD 시절에는 이 구조를 통제하기 위해 쉼표(`,`), 수직선(`|`), 그리고 물음표(`?`), 별표(`*`), 더하기(`+`)와 같은 수학적 기호들에 의존했습니다. 그러나 XML Schema(XSD)는 이러한 기호들을 폐기하고, 인간의 언어와 직관에 더 가까운 명시적인 “**구조 지시자(Structural Indicators)**”와 “**빈도 제어 속성(Occurrence Indicators)**”으로 진화시켰습니다. 

이 장에서는 인문학 데이터를 설계할 때 가장 많이 사용되는 뼈대 구축의 핵심 문법들을 상세히 해부합니다.

## 1. 초정밀 빈도 제어: minOccurs와 maxOccurs

DTD의 가장 큰 논리적 한계 중 하나는 “**정확히 3번만 등장해야 한다**”거나 “**2번에서 5번 사이로 등장해야 한다**”는 식의 정밀한 숫자 제어가 불가능하다는 것이었습니다. 오직 0번, 1번, 무한대만이 존재했습니다.

XSD는 요소나 구조 지시자의 시작 태그 내부에 `minOccurs`(최소 등장 횟수)와 `maxOccurs`(최대 등장 횟수) 속성을 부여하여 이 문제를 완벽하게 해결했습니다.

* **기본값의 이해:** XSD에서 `minOccurs`와 `maxOccurs`를 아예 적지 않으면, 컴퓨터는 자동으로 “**정확히 1번만 등장해야 한다(minOccurs="1" maxOccurs="1")**”로 간주합니다.
* **무한대의 표현:** 최대 등장 횟수에 제한을 두고 싶지 않을 때는 숫자가 아니라 `"unbounded"`라는 특수 키워드를 사용합니다.

### 1.1 DTD 기호와 XSD 빈도 제어의 완벽한 매핑
과거 DTD의 기호 연산자들은 XSD에서 다음과 같이 명확한 속성값으로 치환됩니다.

1. **선택적 요소 (DTD의 `?`):** 0번 또는 1번
   * `<xs:element name="부제" minOccurs="0" maxOccurs="1"/>`
2. **무한 반복 허용 (DTD의 `*`):** 0번 이상 무한대
   * `<xs:element name="주석" minOccurs="0" maxOccurs="unbounded"/>`
3. **필수 무한 반복 (DTD의 `+`):** 최소 1번 이상 무한대
   * `<xs:element name="저자" minOccurs="1" maxOccurs="unbounded"/>`

### 1.2 XSD만의 초정밀 통제
만약 시조(Sijo) 데이터를 마크업하면서 초장, 중장, 종장이라는 구절이 반드시 “**정확히 3줄**”이어야 한다고 강제하고 싶다면 어떻게 할까요?
```xml
<xs:element name="구절" type="xs:string" minOccurs="3" maxOccurs="3"/>
```
위와 같이 설계하면, 구절이 2개이거나 4개인 데이터는 파서가 즉각 에러 처리하여 데이터베이스의 오염을 막아줍니다.

## 2. 요소의 배치 논리: 3대 구조 지시자

빈도를 통제했다면, 이제 자식 요소들이 줄을 서는 방식(배치 논리)을 지정해야 합니다. XSD는 `<xs:complexType>` 바로 아래에 세 가지 중 하나의 구조 지시자를 선언하여 자식들의 배치를 강제합니다.



### 2.1 `<xs:sequence>`: 엄격한 순차적 배치
DTD의 쉼표(`,`)를 대체하는 지시자입니다. 이 태그 안에 묶인 요소들은 **반드시 작성된 순서대로** XML 문서에 등장해야 합니다.

```xml
<xs:element name="서지정보">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="발행일" type="xs:date"/>
            <xs:element name="잡지명" type="xs:string"/>
            <xs:element name="권호" type="xs:string" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>
```
이 구조에서는 반드시 `<발행일>`이 먼저 나오고 `<잡지명>`이 뒤따라야 합니다. 순서가 바뀌면 유효성 검사에서 탈락합니다.

### 2.2 `<xs:choice>`: 선택적 배치 (택일)
DTD의 수직선(`|`)을 대체하는 지시자입니다. 이 태그 안에 묶인 요소들 중 **오직 하나만** 선택되어 문서에 등장해야 합니다.

```xml
<xs:element name="기사본문">
    <xs:complexType>
        <xs:choice>
            <xs:element name="텍스트" type="xs:string"/>
            <xs:element name="이미지스캔본" type="xs:anyURI"/>
        </xs:choice>
    </xs:complexType>
</xs:element>
```
디지털 아카이브 구축 시, 본문 텍스트가 타이핑되어 있는 경우와 아직 타이핑을 마치지 못해 스캔본 이미지만 제공하는 경우를 엄격히 택일하도록 강제할 때 유용합니다.

### 2.3 `<xs:all>`: 무순서 필수 배치
DTD에서는 거의 구현이 불가능했던 XSD만의 강력하고 편리한 지시자입니다. 이 태그 안에 묶인 요소들은 **순서에 상관없이 자유롭게** 등장할 수 있지만, 각각의 요소가 반드시 1번씩(혹은 minOccurs가 0이라면 0번) 등장해야 합니다.

```xml
<xs:element name="인물정보">
    <xs:complexType>
        <xs:all>
            <xs:element name="이름" type="xs:string"/>
            <xs:element name="출생년도" type="xs:integer"/>
            <xs:element name="직업" type="xs:string"/>
        </xs:all>
    </xs:complexType>
</xs:element>
```
작성자가 이름, 출생년도, 직업의 순서를 어떻게 섞어서 마크업하더라도 파서는 모두 정상적인 데이터로 인정합니다. 단, `<xs:all>`은 그 자체로 `maxOccurs`를 1만 가질 수 있다는 기술적 제약이 존재합니다.

## 3. 실무 응용: 지시자의 중첩 설계

실제 국사편찬위원회의 **한국근현대잡지자료**와 같은 거대 데이터베이스를 설계할 때는, 하나의 지시자만 사용하지 않고 지시자 내부에 다른 지시자를 “**중첩(Nesting)**”하여 복잡한 현실 세계의 논리를 구현합니다.

**[요구사항]**
기사 데이터는 1) `<제목>`이 가장 먼저 와야 하고, 2) 그다음엔 `<텍스트>`나 `<이미지>` 중 하나가 반드시 와야 하며, 3) 마지막으로 `<필자>`가 1명 이상 무한대로 올 수 있다.

```xml
<xs:element name="기사">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="제목" type="xs:string"/>
            
            <xs:choice>
                <xs:element name="텍스트" type="xs:string"/>
                <xs:element name="이미지" type="xs:anyURI"/>
            </xs:choice>
            
            <xs:element name="필자" type="xs:string" minOccurs="1" maxOccurs="unbounded"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>
```

이처럼 `<xs:sequence>` 안에 `<xs:choice>`를 품는 중첩 설계는 인문학 데이터 모델링에서 가장 빈번하게 사용되는 강력한 패턴입니다. 

이제 우리는 XSD를 통해 데이터의 타입(숫자, 문자)과 등장 패턴을 완벽하게 통제할 수 있게 되었습니다. 그러나 전 세계의 방대한 지식 네트워크를 구축하기 위해, 모든 코드를 하나의 거대한 XSD 파일에 몰아넣는 것은 극도로 비효율적입니다. 

이어지는 장에서는 XSD 설계의 마지막 단계이자 대규모 협업 아카이브 구축의 핵심 기술인 **“복잡한 스키마의 모듈화와 확장(import, include)”** 실무로 진입해 보겠습니다.

:::{seealso} 📖 참고문헌
* **W3C (2004).** <XML Schema Part 1: Structures Second Edition>. <a href="https://www.w3.org/TR/xmlschema-1/" target="_blank">W3C Recommendation</a>
:::