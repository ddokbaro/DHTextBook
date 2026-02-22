---
title: "XSLT: XML 데이터의 시각화와 구조 변환"
description: "기계가독형 XML 데이터를 인간이 읽을 수 있는 HTML 웹페이지나 다른 형태의 문서 구조로 렌더링하는 XSLT의 템플릿 철학과 핵심 제어 문법"
---

# XSLT: XML 데이터의 시각화와 구조 변환

우리는 앞선 장들을 통해 텍스트에 DTD와 XSD라는 뼈대를 세우고, XPath라는 정밀한 메스를 통해 원하는 데이터를 핀셋처럼 추출하는 방법을 마스터했습니다. 그러나 태그로 빽빽하게 둘러싸인 순수한 XML 문서는 컴퓨터에게는 완벽한 데이터베이스일지 몰라도, 인간 연구자나 일반 대중이 읽고 감상하기에는 극도로 불편한 형태입니다.

XML 데이터가 세상과 소통하기 위해서는 아름다운 웹페이지(HTML)나 정갈한 인쇄물(PDF), 혹은 다른 시스템이 요구하는 새로운 형태의 XML로 모습을 바꾸어야 합니다. 이 위대한 형태 변환을 수행하는 마법의 언어가 바로 `"**XSLT(eXtensible Stylesheet Language Transformations)**"`입니다. 이 장에서는 XPath를 엔진으로 삼아 데이터를 재조립하는 XSLT의 템플릿(Template) 철학과 핵심 변환 실무를 다룹니다.

## 1. XSLT의 철학: 템플릿 기반의 변환(Transformation)

XSLT의 작동 원리는 기존의 절차적 프로그래밍(C, Java 등)과는 완전히 다릅니다. XSLT는 `"**규칙 기반(Rule-based)**"`의 변환 언어입니다. 

개발자가 문서의 처음부터 끝까지 어떻게 렌더링할지 순서대로 지시하는 것이 아니라, `"**이러한 노드를 만나면, 이렇게 껍데기를 씌워라**"`라는 형태의 **틀(Template)**들을 미리 여러 개 만들어 둡니다. 그러면 XSLT 프로세서(Processor)가 XML 문서를 위에서부터 훑어 내려가다가 템플릿의 조건에 맞는 노드를 발견할 때마다 해당 틀을 덮어씌워 새로운 문서를 찍어내는 방식입니다.

이러한 특성 때문에 XPath의 강력한 경로 탐색 능력이 XSLT의 심장부로 완벽하게 융합되어 사용됩니다.

## 2. XSLT 문서의 뼈대와 루트 템플릿

XSLT 문서(`.xsl` 확장자) 역시 완벽한 웰폼드(Well-formed) XML 문서의 문법을 따릅니다. 따라서 최상단에 XML 선언과 함께 `xsl` 네임스페이스를 선언해야 합니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="[http://www.w3.org/1999/XSL/Transform](http://www.w3.org/1999/XSL/Transform)">
    
    <xsl:template match="/">
        <html>
            <head>
                <title>한국근현대잡지자료 아카이브</title>
            </head>
            <body>
                <h1>잡지 기사 목록</h1>
                </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
```

여기서 가장 중요한 것은 `<xsl:template match="/">`입니다. `match` 속성 안에 들어간 XPath `/`는 XML 문서의 최상위 뿌리를 의미합니다. 즉, 이 템플릿은 변환기가 문서에 진입하자마자 가장 먼저 실행되는 `"**마스터 뼈대**"`이며, 이 안에 우리가 렌더링하고자 하는 HTML 웹페이지의 기본 껍데기(`<html>`, `<body>` 등)를 배치합니다.

## 3. 핵심 변환 명령어 (The Workhorses)

이제 HTML 껍데기 안에 실제 XML의 살점(데이터)을 채워 넣을 차례입니다. XSLT에서 가장 빈번하게 사용되는 3대 핵심 명령어를 살펴보겠습니다.

### 3.1 텍스트 추출: `<xsl:value-of>`
XPath 경로를 탐색하여 해당 노드가 품고 있는 순수한 텍스트 문자열(PCDATA)을 뽑아내어 화면에 출력합니다.

```xml
<h2><xsl:value-of select="/잡지/서지정보/잡지명"/></h2>
```
* **결과:** XML에 `<잡지명>개벽</잡지명>`이라고 되어 있었다면, 화면에는 `<h2>개벽</h2>`이라고 예쁘게 출력됩니다.

### 3.2 반복문(Loop): `<xsl:for-each>` ★
하나의 잡지 안에는 수십 편의 기사가 들어있습니다. 이 기사들의 목록을 HTML 표(Table)나 리스트로 찍어낼 때 사용하는 가장 강력한 반복문입니다. `select` 속성에 복수 개의 노드를 가리키는 XPath를 넣어줍니다.

```xml
<ul>
    <xsl:for-each select="/잡지/기사목록/기사">
        <li>
            <xsl:value-of select="제목"/> 
            (필자: <xsl:value-of select="필자"/>)
        </li>
    </xsl:for-each>
</ul>
```
* **해석:** 변환기는 `<기사>` 노드를 만날 때마다 루프(Loop)를 돌며 `<li>` 태그를 새롭게 생성합니다. 주의할 점은 `<xsl:for-each>` 내부로 진입하면 기준점이 해당 노드로 바뀐다는 것입니다. 따라서 내부의 `<xsl:value-of>`에서는 절대 경로(`/잡지/...`)를 쓰지 않고 현재 위치를 기준으로 한 자식 노드(`제목`, `필자`)만 적어주면 됩니다.

### 3.3 정렬: `<xsl:sort>`
`<xsl:for-each>` 바로 밑에 사용하여, 반복되어 출력되는 데이터들의 순서를 동적으로 재배치합니다.

```xml
<xsl:for-each select="/잡지/기사">
    <xsl:sort select="발행년도" order="descending" data-type="number"/>
    </xsl:for-each>
```
* **해석:** 기사들을 단순히 XML에 타이핑된 순서대로 보여주지 않고, `발행년도`를 기준으로 내림차순(최신 기사가 위로 오게) 정렬하여 화면에 렌더링합니다.

## 4. 논리적 분기 (Conditional Logic)

화면을 렌더링하다 보면 데이터의 상태에 따라 디자인을 다르게 적용해야 할 때가 있습니다. (예: 완간된 잡지는 붉은색 텍스트로 표시 등)

### 4.1 단순 조건: `<xsl:if>`
특정 XPath 조건이 참(True)일 때만 내부의 HTML이나 텍스트를 출력합니다.

```xml
<xsl:if test="@상태='완간'">
    <span style="color:red;">[완간됨]</span>
</xsl:if>
```

### 4.2 다중 분기: `<xsl:choose>`
프로그래밍의 `if-else if-else` 구조와 완벽히 동일합니다. 다양한 경우의 수에 따라 출력을 제어합니다.

```xml
<xsl:choose>
    <xsl:when test="조회수 &gt; 1000">
        <b>인기 기사</b>
    </xsl:when>
    <xsl:when test="조회수 = 0">
        <i>조회수 없음</i>
    </xsl:when>
    <xsl:otherwise>
        일반 기사
    </xsl:otherwise>
</xsl:choose>
```
*(참고: XML 문법 내에 작성되므로 꺾쇠 기호를 쓸 수 없어 부등호 `>` 대신 `&gt;` 엔티티를 사용해야 합니다.)*

## 5. 실전 아카이브 렌더링 (Practicum)

앞서 배운 모든 기술을 총동원하여, 뼈대만 있는 `<근현대잡지자료>` XML 데이터를 연구자들이 한눈에 볼 수 있는 깔끔한 HTML 테이블 데이터베이스로 변환하는 XSLT 코드를 완성해 보겠습니다.

**[XSLT 스크립트 작성]**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="[http://www.w3.org/1999/XSL/Transform](http://www.w3.org/1999/XSL/Transform)">

    <xsl:template match="/">
        <html>
            <head><title>잡지 아카이브</title></head>
            <body>
                <h1><xsl:value-of select="//잡지명"/> 기사 색인</h1>
                
                <table border="1">
                    <tr bgcolor="#cccccc">
                        <th>연번</th>
                        <th>기사 제목</th>
                        <th>필자</th>
                        <th>발행년도</th>
                    </tr>
                    
                    <xsl:for-each select="//기사">
                        <xsl:sort select="발행년도" order="ascending"/>
                        
                        <tr>
                            <td><xsl:value-of select="position()"/></td>
                            <td><xsl:value-of select="제목"/></td>
                            <td>
                                <xsl:choose>
                                    <xsl:when test="필자">
                                        <xsl:value-of select="필자"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <i>작자 미상</i>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </td>
                            <td><xsl:value-of select="발행년도"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
```

이 XSLT 파일을 웹 브라우저나 파이썬(Python)의 `lxml` 라이브러리를 통해 원본 XML과 결합시키면, 태그로 어지럽던 데이터가 즉시 정렬 기능과 조건부 서식이 적용된 아름다운 시각적 인터페이스로 탈바꿈합니다. 

결론적으로 XSLT는 기계의 언어(XML)를 인간의 언어(시각 매체)로 번역해 주는 위대한 통역가입니다. 구조의 분리, 논리적 검증, 경로 탐색, 그리고 최종적인 시각화까지 마침내 우리는 아날로그 텍스트를 디지털 생태계에 완벽하게 안착시키는 디지털 문헌학의 거대한 파이프라인을 완성했습니다.

:::{seealso} 📖 참고문헌
* **W3C (1999).** <XSL Transformations (XSLT) Version 1.0>. <a href="https://www.w3.org/TR/xslt" target="_blank">W3C Recommendation</a>
:::