---
title: "복잡한 스키마의 모듈화와 확장: include, import, extension"
description: "대규모 디지털 아카이브 구축을 위해 거대한 XSD 파일을 분할하고, 외부 네임스페이스를 융합하며, 객체 지향적으로 데이터 타입을 상속받는 고급 설계 기법"
---

# 복잡한 스키마의 모듈화와 확장: include, import, extension

디지털 인문학 프로젝트가 국가적 규모의 거대한 아카이브로 성장하게 되면, 모든 데이터 규칙을 단 하나의 XSD 파일에 몰아넣는 것은 극도로 비효율적입니다. 수만 줄에 달하는 스키마 코드는 유지보수를 불가능하게 만들고, 여러 학자가 동시에 협업하여 스키마를 갱신하는 것을 가로막습니다.

이러한 문제를 해결하기 위해 XML Schema(XSD)는 현대 소프트웨어 공학의 핵심 개념인 “**모듈화(Modularization)**”와 “**객체 지향적 상속(Inheritance)**”을 문법적으로 완벽하게 지원합니다. 이 장에서는 쪼개진 스키마를 결합하는 `<xs:include>`와 `<xs:import>`, 그리고 기존의 데이터 타입을 재사용하여 새로운 타입을 창조하는 `<xs:extension>` 기법을 심층적으로 다룹니다.

## 1. 동일한 네임스페이스의 병합: `<xs:include>`

대규모 데이터베이스를 설계할 때, 최상위 아키텍트는 유지보수의 편의성을 위해 “**인물 정보 스키마**”, “**서지 정보 스키마**”, “**지리 정보 스키마**” 등으로 물리적인 XSD 파일을 여러 개로 분할하여 개발합니다.

분할된 여러 개의 XSD 파일들이 **모두 동일한 목표 네임스페이스(targetNamespace)를 공유**하고 있을 때, 이들을 하나의 거대한 스키마로 다시 조립하는 명령어가 바로 `<xs:include>`입니다.

**[메인 스키마 파일: `magazine_main.xsd`]**
```xml
<xs:schema xmlns:xs="[http://www.w3.org/2001/XMLSchema](http://www.w3.org/2001/XMLSchema)"
           targetNamespace="[http://dh.aks.ac.kr/magazine](http://dh.aks.ac.kr/magazine)"
           xmlns="[http://dh.aks.ac.kr/magazine](http://dh.aks.ac.kr/magazine)"
           elementFormDefault="qualified">

    <xs:include schemaLocation="author_module.xsd"/>
    <xs:include schemaLocation="article_module.xsd"/>

    <xs:element name="근현대잡지자료">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="기사" maxOccurs="unbounded"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>

</xs:schema>
```

파서(Parser)가 `magazine_main.xsd`를 읽을 때, `<xs:include>`를 만나는 순간 지정된 경로(`schemaLocation`)에 있는 외부 파일들의 내용을 현재 문서의 논리적 공간 안으로 완벽하게 복사하여 붙여넣은 것처럼 처리합니다. 이를 통해 연구진은 각자의 모듈 파일만 독립적으로 관리하면서도, 최종적으로는 완결된 하나의 데이터베이스 규칙을 강제할 수 있습니다.

## 2. 이기종 네임스페이스의 융합: `<xs:import>`

`<xs:include>`가 같은 소속을 가진 아군들의 결합이라면, `<xs:import>`는 **서로 다른 네임스페이스(소속)를 가진 완전히 독립된 스키마를 내 시스템 안으로 끌어들여 융합(Mashup)**하는 강력한 외교적 명령어입니다.



디지털 문헌학 실무에서 모든 데이터 구조를 바닥부터 새로 짜는 것은 어리석은 일입니다. 문헌의 서지 정보는 이미 전 세계 도서관이 공통으로 사용하는 “**더블린 코어(Dublin Core)**” 스키마를 차용하는 것이 상호 운용성 측면에서 압도적으로 유리합니다.

**[이기종 스키마의 수입 설계]**
```xml
<xs:schema xmlns:xs="[http://www.w3.org/2001/XMLSchema](http://www.w3.org/2001/XMLSchema)"
           targetNamespace="[http://dh.aks.ac.kr/magazine](http://dh.aks.ac.kr/magazine)"
           xmlns="[http://dh.aks.ac.kr/magazine](http://dh.aks.ac.kr/magazine)"
           xmlns:dc="[http://purl.org/dc/elements/1.1/](http://purl.org/dc/elements/1.1/)"
           elementFormDefault="qualified">

    <xs:import namespace="[http://purl.org/dc/elements/1.1/](http://purl.org/dc/elements/1.1/)" 
               schemaLocation="[http://www.dublincore.org/schemas/xmls/qdc/dc.xsd](http://www.dublincore.org/schemas/xmls/qdc/dc.xsd)"/>

    <xs:element name="기사">
        <xs:complexType>
            <xs:sequence>
                <xs:element ref="dc:title"/>
                <xs:element ref="dc:creator"/>
                <xs:element name="본문텍스트" type="xs:string"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>

</xs:schema>
```

이 코드는 디지털 인문학 지식망 연결의 정수입니다. `<xs:import>`를 선언할 때는 파일의 위치(`schemaLocation`)뿐만 아니라, 수입해 올 상대방의 소속(`namespace`)을 반드시 함께 명시해야 합니다. 이제 우리의 독자적인 `<기사>` 요소 내부에는 글로벌 표준인 `<dc:title>`과 `<dc:creator>`가 유효한 자식으로 당당하게 자리 잡게 됩니다.

## 3. 데이터 타입의 객체 지향적 확장: `<xs:extension>`

대형 프로젝트에서 인물 정보를 마크업할 때, 잡지의 글을 쓰는 “**필자**”와 잡지를 엮어내는 “**편집자**”는 둘 다 “**사람**”이라는 공통점이 있지만, 각자 요구되는 부가 정보가 다를 수 있습니다. 

이를 위해 각각의 복합형(ComplexType)을 처음부터 똑같이 중복해서 짜는 대신, “**기본 인간 타입**”을 하나 만들어 두고 이를 **상속받아 확장(Extension)**하는 기법을 사용합니다.

**[1단계: 기본 복합형 설계 (부모 타입)]**
```xml
<xs:complexType name="인물기본타입">
    <xs:sequence>
        <xs:element name="이름" type="xs:string"/>
        <xs:element name="출생년도" type="xs:gYear"/>
    </xs:sequence>
</xs:complexType>
```

**[2단계: 기본 타입을 상속받아 확장 (자식 타입)]**
```xml
<xs:complexType name="필자타입">
    <xs:complexContent>
        <xs:extension base="인물기본타입">
            <xs:sequence>
                <xs:element name="소속기관" type="xs:string"/>
            </xs:sequence>
        </xs:extension>
    </xs:complexContent>
</xs:complexType>

<xs:complexType name="편집자타입">
    <xs:complexContent>
        <xs:extension base="인물기본타입">
            <xs:attribute name="직급" type="xs:string"/>
        </xs:extension>
    </xs:complexContent>
</xs:complexType>
```

`<xs:extension base="인물기본타입">` 구문은 부모가 가진 요소와 속성을 고스란히 물려받은 뒤, 그 아래에 선언된 새로운 구조를 덧붙이겠다는 의미입니다. 이를 통해 코드의 중복을 획기적으로 줄이고, 향후 인물의 공통 속성(예: 사망년도)이 추가되어야 할 때 부모 타입 단 한 곳만 수정하면 전체 아카이브 시스템에 일괄 적용되는 엄청난 유지보수 효율성을 확보할 수 있습니다.

결론적으로 XSD의 모듈화와 상속 기능은 XML이 단순한 마크업 문법을 넘어, 그 자체로 고도의 “**객체 지향 데이터베이스(Object-Oriented Database)**” 설계 언어임을 증명합니다. 

이로써 인문학 텍스트를 기계의 뇌 속으로 정밀하게 맵핑하는 DTD와 XSD 스키마의 대장정을 마칩니다. 이어지는 장에서는 이렇게 아름답고 정교하게 짜인 XML 데이터들을 오라클(Oracle)이나 MSSQL과 같은 거대한 **“관계형 데이터베이스(RDB)”** 시스템과 어떻게 물리적으로 결합하고 연산할 것인지, 그 궁극의 실무 활용 단계로 진입하겠습니다.

:::{seealso} 📖 참고문헌
* **W3C (2004).** <XML Schema Part 1: Structures Second Edition>. <a href="https://www.w3.org/TR/xmlschema-1/" target="_blank">W3C Recommendation</a>
:::