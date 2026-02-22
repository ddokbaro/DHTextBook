---
title: "XSD 데이터 타입 설계: 단순형과 복합형"
description: "내장 데이터 타입(Built-in Type)을 활용한 데이터 객체화와, 단순형(SimpleType)의 정규식 제약(Restriction), 복합형(ComplexType) 설계의 기초"
---

# XSD 데이터 타입 설계: 단순형과 복합형

DTD가 텍스트를 그저 “**단순한 문자열(#PCDATA)**”로만 취급했다면, XML Schema(XSD)는 텍스트를 정수, 날짜, 논리값 등 컴퓨터가 즉각적으로 연산할 수 있는 “**데이터 객체**”로 변환합니다.

이 장에서는 XSD 설계의 가장 핵심적인 두 축인 “**단순형(SimpleType)**”과 “**복합형(ComplexType)**”의 개념을 완벽하게 분리하여 이해하고, `<xs:restriction>`과 정규표현식을 결합하여 잘못된 데이터의 유입을 원천 차단하는 최상급 검증 실무를 학습합니다.

## 1. XSD 요소의 두 가지 핏줄: Simple vs Complex

XSD에서 세상의 모든 XML 요소(Element)는 딱 두 가지 혈통으로 나뉩니다. 이 기준을 명확히 이해하는 것이 XSD 스키마 설계의 출발점입니다.



1. **단순형 (SimpleType):** 자식 요소가 없고, 속성(Attribute)도 없는 순수한 텍스트 값만 가지는 요소입니다. (예: `<발행년도>1920</발행년도>`)
2. **복합형 (ComplexType):** 자식 요소를 하나라도 가지거나, 텍스트뿐일지라도 **속성(Attribute)을 단 하나라도 가지는** 요소입니다. (예: `<잡지명 언어="한글">개벽</잡지명>`)

초보 연구자들이 가장 많이 하는 실수는 텍스트만 들어있는 요소에 속성을 부여해 놓고 이를 단순형으로 설계하여 치명적 오류(Fatal Error)를 발생시키는 것입니다. **속성이 붙는 순간 그 요소는 무조건 복합형(ComplexType)**이 됩니다.

## 2. 기본 요소 선언과 내장 데이터 타입

자식이나 속성이 없는 가장 기본적인 단순형 요소는 `<xs:element>`와 `type` 속성을 사용하여 한 줄로 선언할 수 있습니다. 

```xml
<xs:element name="기사제목" type="xs:string"/>
<xs:element name="페이지수" type="xs:integer"/>
<xs:element name="발행일자" type="xs:date"/>
```

XSD는 W3C 표준에 따라 40개가 넘는 강력한 내장 데이터 타입(Built-in Data Types)을 제공합니다. 
* `xs:string`: 일반적인 문자열
* `xs:integer`: 소수점이 없는 정수 (문자가 섞이면 파서가 에러를 발생시킴)
* `xs:decimal`: 소수점을 포함하는 실수
* `xs:date`: `YYYY-MM-DD` 규격을 강제하는 날짜
* `xs:boolean`: `true`, `false`, `1`, `0`만 허용하는 논리값

## 3. 단순형(SimpleType)의 심화: 제약(Restriction)

내장 데이터 타입만으로도 훌륭하지만, 인문학 데이터 편찬에서는 더 정밀한 통제가 필요합니다. 예를 들어, 페이지 수는 정수(`xs:integer`)여야 하지만, 절대 음수(-5페이지)가 될 수는 없습니다. 

이때 `<xs:simpleType>`과 그 내부의 `<xs:restriction>`(제약) 구문을 사용하여 데이터가 들어올 수 있는 바늘구멍을 깎아냅니다.

### 3.1 값의 범위와 길이 제한
페이지 수를 1 이상 1000 이하로 제한하는 설계는 다음과 같습니다.

```xml
<xs:element name="페이지수">
    <xs:simpleType>
        <xs:restriction base="xs:integer">
            <xs:minInclusive value="1"/>
            <xs:maxInclusive value="1000"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>
```
* `base="xs:integer"`: 기본적으로 정수형을 따르되, 추가 제약을 건다는 의미입니다.
* 문자열의 경우 `<xs:minLength>`와 `<xs:maxLength>`를 사용하여 글자 수를 통제할 수 있습니다.

### 3.2 열거형(Enumeration) 제약
DTD의 `(남 | 여)`와 같이 허용되는 값의 목록을 명시적으로 제한할 때는 `<xs:enumeration>`을 사용합니다.

```xml
<xs:element name="발간상태">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:enumeration value="창간"/>
            <xs:enumeration value="발행중"/>
            <xs:enumeration value="폐간"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>
```

### 3.3 정규표현식(Pattern) 제약의 마법
가장 강력하고 유연한 제약 도구는 `pattern`입니다. 국사편찬위원회의 근현대잡지자료에서 발행 연도를 반드시 “**4자리 숫자**”로만 입력받고 싶다면 정규표현식을 적용합니다.

```xml
<xs:element name="발행년도">
    <xs:simpleType>
        <xs:restriction base="xs:string">
            <xs:pattern value="[0-9]{4}"/>
        </xs:restriction>
    </xs:simpleType>
</xs:element>
```
위 설계도를 적용하면, `<발행년도>1920</발행년도>`는 통과하지만, `<발행년도>일천구백이십년</발행년도>`나 `<발행년도>20</발행년도>`는 즉각 파싱 에러를 내뿜습니다. 인간의 실수를 기계가 원천 차단하는 것입니다.

## 4. 복합형(ComplexType)의 기초: 구조의 확장

앞서 언급했듯, 요소가 자식 요소를 거느리거나 속성(Attribute)을 하나라도 가지게 되면 반드시 `<xs:complexType>`으로 설계해야 합니다.

가장 흔한 형태인 “**자식 요소들을 거느린 요소**”의 설계법을 살펴보겠습니다.

```xml
<xs:element name="서지정보">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="잡지명" type="xs:string"/>
            <xs:element name="발행년도" type="xs:string"/>
        </xs:sequence>
    </xs:complexType>
</xs:element>
```

위 코드에서 `<xs:complexType>` 내부에 있는 `<xs:sequence>`는 **“내부의 요소들이 반드시 명시된 순서대로 등장해야 한다”**는 구조 지시자입니다. 이는 DTD의 쉼표(`,`) 역할을 정확히 대체합니다.

이처럼 복합형 설계는 트리 구조의 가지를 뻗어나가게 하는 뼈대 생성의 핵심입니다. 그러나 자식 요소가 무작위 순서로 와도 될 때는 어떻게 해야 할까요? 특정 요소가 10번 반복 등장해야 할 때는 어떻게 제어할까요? 

이에 대한 해답이자, DTD의 `?`, `*`, `+`, `|` 연산자를 객체 지향적으로 진화시킨 **“구조 지시자와 빈도 제어(minOccurs, maxOccurs)”**의 세계를 다음 장에서 매우 상세하게 파헤쳐 보겠습니다.

:::{seealso} 📖 참고문헌
* **W3C (2004).** <XML Schema Part 2: Datatypes Second Edition>. <a href="https://www.w3.org/TR/xmlschema-2/" target="_blank">W3C Recommendation</a>
:::