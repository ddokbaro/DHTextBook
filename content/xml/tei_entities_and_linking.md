---
title: "개체명 식별과 텍스트 관계망 구축"
description: "TEI를 활용하여 텍스트 내부의 인물, 장소, 날짜 등 개체명(Named Entity)을 식별하고 정규화하며, 요소 간의 상호 참조를 통해 거대한 시맨틱 관계망을 구축하는 정보공학적 방법론"
---

# 개체명 식별과 텍스트 관계망 구축

텍스트의 거시적 뼈대를 세우고 오탈자를 훌륭하게 교정했다 하더라도, 기계의 관점에서 텍스트는 여전히 의미를 알 수 없는 문자들의 단순한 나열일 뿐입니다. 디지털 인문학이 추구하는 진정한 `"**지식 베이스(Knowledge Base)**"`를 구축하기 위해서는 텍스트 속에 등장하는 특정한 단어들이 현실 세계의 인물, 장소, 사건, 혹은 시간과 숫자라는 사실을 기계에게 가르쳐주어야 합니다.

자연어 처리(NLP) 분야에서는 이를 `"**개체명 식별(Named Entity Recognition, NER)**"`이라고 부릅니다. 이 장에서는 TEI 가이드라인을 활용하여 텍스트 내의 의미론적 개체를 마크업하고, 이들을 정규화(Normalization)하여 외부 데이터베이스(URI) 및 다른 텍스트 요소들과 연결하는 `"**시맨틱 링킹(Semantic Linking)**"`의 실무를 탐구합니다.

## 1. 이름과 참조 문자열 (Names and Referring Strings)

문헌 속에서 특정한 대상(사람, 장소, 사물 등)을 지칭하는 단어나 구절을 `"**참조 문자열(Referring String)**"`이라고 합니다. TEI는 이를 세밀하게 식별하기 위해 범용 요소와 구체적 요소를 함께 제공합니다.

### 1.1 범용 식별자: `<rs>`와 `<name>`
* `"**<rs>**"` (Referring String): 고유명사뿐만 아니라 일반 명사구("그 장군", "우리 동네")로 특정 개체를 지칭할 때 사용하는 가장 포괄적인 태그입니다. `@type` 속성으로 종류를 명시합니다.
* `"**<name>**"`: 문법적으로 명백한 `"**고유명사**"`로 이루어진 이름을 태깅할 때 사용합니다.

```xml
<p>
    <rs type="person">그 위대한 장군</rs>은 마침내 
    <name type="place">한산도</name> 앞바다에 도착했다.
</p>
```

### 1.2 구체적 개체명: `<persName>`, `<placeName>`, `<orgName>`
대규모 데이터베이스 프로젝트에서는 `<name>`보다 훨씬 구체적이고 독립적인 태그 세트를 사용하는 것이 일반적입니다.
* `"**<persName>**"`: 인물명 (내부에 성, 이름, 자, 호 등을 세분화할 수 있음)
* `"**<placeName>**"`: 지명
* `"**<orgName>**"`: 기관 및 조직명

## 2. 데이터의 정규화와 외부 링킹 (Normalization & URI) ★

`이순신`, `충무공`, `통제사 영감`은 텍스트 표기 형태는 완전히 다르지만 현실 세계에서는 동일한 한 사람을 가리킵니다. 이를 컴퓨터가 하나로 묶어서 인식하도록 만드는 과정이 텍스트 인코딩의 꽃이라 불리는 `"**정규화(Normalization)**"`입니다.

TEI는 이를 위해 전역 속성인 `@ref`(Reference)나 `@key`를 제공합니다. 개체를 마크업할 때, 그 개체의 식별자(ID)나 외부 인물 사전의 URI를 속성값으로 부여합니다.

```xml
<p>
    <persName ref="[http://people.aks.ac.kr/front/dirSer/exm/exmView.aks?exmId=EXM_MU_6JOb_1576_000244](http://people.aks.ac.kr/front/dirSer/exm/exmView.aks?exmId=EXM_MU_6JOb_1576_000244)">충무공</persName>께서 
    <date when="1592-07-08">그날</date> 적을 크게 무찌르셨다.
</p>
```
이러한 마크업을 통해 로컬의 텍스트 데이터는 고립을 벗어나, 전 세계의 웹 데이터를 하나로 엮는 `"**연결 개방형 데이터(Linked Open Data, LOD)**"` 생태계에 편입됩니다.

## 3. 날짜와 숫자의 기계가독성 부여

고문헌에 등장하는 시간과 숫자는 현대 컴퓨터 시스템이 연산할 수 없는 형태로 기록되어 있습니다. ("기미년 삼월 일일", "일만 이천 봉" 등)

### 3.1 날짜의 정규화: `<date>`와 `@when`
날짜를 마크업하는 `"**<date>**"` 요소는 반드시 `@when` 속성과 결합하여 ISO 8601 표준 규격(`YYYY-MM-DD`)으로 정규화되어야 합니다.
```xml
<p>
    <date when="1919-03-01">기미년 삼월 일일</date> 정오, 민족의 대표들이 모였다.
</p>
```

### 3.2 숫자의 정규화: `<num>`과 `@value`
한문이나 한글로 적힌 숫자를 아라비아 숫자로 변환하여 `@value` 속성에 담아줍니다.
```xml
<p>
    적군 <num value="100000">십만</num> 대군이 몰려왔으나, 
    아군은 불과 <num value="300">삼백</num> 명뿐이었다.
</p>
```
이러한 처리를 통해 컴퓨터는 "적군이 아군보다 수적으로 우세했다(100,000 > 300)"는 역사적 사실을 수학적으로 연산해 낼 수 있게 됩니다.

## 4. 시맨틱 링킹과 관계망 구축

지금까지 단어 단위의 개체명을 식별했다면, 이제 문서 내외부의 요소들을 끈으로 묶어 거대한 `"**지식 그래프(Knowledge Graph)**"`를 형성할 차례입니다.

### 4.1 단순 상호 참조: `<ref>`와 `<ptr>`
한 지점에서 다른 지점으로 이동하는 하이퍼링크를 생성합니다.
* `"**<ref>**"` (Reference): 클릭할 수 있는 텍스트(Anchor text)가 존재하는 링크입니다.
* `"**<ptr>**"` (Pointer): 텍스트 내용 없이 링크의 주소(`@target`)만을 가지는 빈 요소입니다.

```xml
<p>
    이 사건의 자세한 전말은 <ref target="#chapter_5">제5장</ref>을 참조하시오.
    관련 원본 스캔본은 다음 링크에 있습니다. <ptr target="[http://archive.org/doc123](http://archive.org/doc123)"/>
</p>
```

### 4.2 해석적 링킹: `@corresp`와 `@ana` ★
TEI의 진정한 위력은 명시적인 링크를 넘어, 숨겨진 의미론적 관계(Implicit links)를 연결 속성(Linking attributes)으로 엮어내는 데 있습니다.

* `"**@corresp**"` (Corresponding): 텍스트 내의 두 요소가 서로 대응 관계에 있음을 명시합니다. 다국어 병렬 말뭉치나 번역 동치어를 연결할 때 탁월합니다.
```xml
<seg xml:lang="ko" xml:id="KO1" corresp="#EN1">소년이여, 야망을 가져라!</seg>
<seg xml:lang="en" xml:id="EN1" corresp="#KO1">Boys, be ambitious!</seg>
```

* `"**@ana**"` (Analysis): 텍스트의 특정 구절이 외부에서 정의된 언어학적, 의미론적 해석과 연결됨을 지시합니다. 품사 태깅이나 문장 구조 분석에 주로 쓰입니다.
```xml
<seg type="sentence" ana="#SVO_structure">
    <seg type="word" ana="#Subject">존은</seg>
    <seg type="word" ana="#Object">낸시를</seg>
    <seg type="word" ana="#Verb">사랑한다.</seg>
</seg>
```

이처럼 TEI의 개체명 식별과 링킹 모듈은 아날로그 텍스트를 기계가 분석하고 추론할 수 있는 지능형 데이터베이스로 탈바꿈시킵니다. 

지금까지 문서의 메타데이터, 거시/미시 구조, 편집자의 개입, 개체명 관계망 등 단일 텍스트를 완벽하게 인코딩하는 법을 마스터했습니다. 이제 TEI 대장정의 마지막 장이자, 문헌학의 정수인 여러 판본(Variants)들을 대조하여 최선의 텍스트를 재구성하는 기술, **"비판적 교감본(Critical Edition) 제작"**의 세계로 진입하겠습니다.

:::{seealso} 📖 참고문헌
* **Burnard, Lou, and C. M. Sperberg-McQueen.** <TEI Lite: A Minimalist’s Guide to Text Encoding>. (08 Cross References and Links, 10 Names, Dates, and Numbers).
:::