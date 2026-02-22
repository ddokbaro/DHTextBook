---
title: "lxml 기반 고급 쿼리와 TEI 네임스페이스 제어"
description: "기본 ElementTree의 한계를 뛰어넘어 파이썬 환경에서 완벽한 XPath 1.0과 XSLT 변환을 수행하고, TEI의 까다로운 기본 네임스페이스(xmlns)를 딕셔너리로 통제하는 고급 실무"
---

# lxml 기반 고급 쿼리와 TEI 네임스페이스 제어

앞서 살펴본 파이썬의 기본 `find()`, `findall()` 메서드는 직계 자식을 찾거나 단순한 태그 이름을 검색하는 데에는 유용하지만, 조상을 역추적하거나(`ancestor::`) 속성값의 일부만으로 필터링하는(`contains()`) 복잡한 탐색에는 완전히 무력합니다.

이러한 한계를 극복하고 우리가 배운 XPath의 모든 지식을 파이썬 코드 안에서 100% 발휘하게 해주는 도구가 바로 `"**lxml**"` 라이브러리입니다. 이 장에서는 `lxml`의 고유한 `.xpath()` 메서드 활용법과, 초보 디지털 문헌학자들을 가장 깊은 절망에 빠뜨리는 `"**TEI 네임스페이스(Namespace) 탐색 오류**"`의 원인 및 정보공학적 해결책을 심층적으로 다룹니다.

## 1. 완벽한 XPath 1.0의 지원: `.xpath()`

`lxml`로 파싱된 트리(Tree) 객체나 요소(Element) 객체는 `"**.xpath()**"`라는 전용 메서드를 가집니다. 이 메서드 안에는 우리가 앞서 배운 어떤 복잡한 XPath 표현식이라도 자유롭게 입력할 수 있으며, 결과는 항상 파이썬 `"**리스트(List)**"` 형태로 반환됩니다.



### 1.1 축(Axes)과 다중 조건의 활용
기본 라이브러리에서는 불가능한 형제 노드 탐색이나 복합 논리 필터링이 단 한 줄의 코드로 해결됩니다.

```python
from lxml import etree

tree = etree.parse('magazine_data.xml')

# 1. 축(Axes) 활용: 제목이 '무정'인 기사의 '바로 다음 기사' 추출
next_articles = tree.xpath('//기사[제목="무정"]/following-sibling::기사')

# 2. 내장 함수 활용: 제목에 '독립'이 포함되고, 필자가 있는 기사 추출
target_articles = tree.xpath('//기사[contains(제목, "독립") and 필자]')

for article in target_articles:
    print(article.find("제목").text)
```

### 1.2 노드가 아닌 텍스트/통계 직접 추출
`.xpath()` 메서드는 태그(요소)뿐만 아니라, XPath 연산의 결과인 순수 텍스트 배열이나 숫자형 데이터(통계)를 파이썬 변수로 직접 받아올 수 있습니다.

```python
# text() 함수를 사용하여 텍스트 문자열들만 리스트로 획득
authors = tree.xpath('//기사/필자/text()')
print(authors)  # ['이광수', '최남선', '만해']

# count() 함수를 사용하여 파이썬의 float(실수형) 숫자로 반환받음
article_count = tree.xpath('count(//기사)')
print(f"총 기사 수: {int(article_count)}개")
```

## 2. [핵심 실무] TEI 네임스페이스(Namespace) 제어의 함정

TEI(Text Encoding Initiative) 가이드라인을 준수하여 작성된 모든 XML 문서는 루트 요소(`<TEI>`)에 다음과 같이 기본 네임스페이스가 선언되어 있습니다.

```xml
<TEI xmlns="[http://www.tei-c.org/ns/1.0](http://www.tei-c.org/ns/1.0)">
    <teiHeader>...</teiHeader>
    <text>
        <body><p>본문입니다.</p></body>
    </text>
</TEI>
```

초보 연구자들이 파이썬으로 이 문서를 파싱한 뒤, `tree.xpath('//p')`라고 검색하면 **결과가 텅 빈 리스트(`[]`)로 나오는 치명적인 현상**을 겪게 됩니다. 분명히 눈앞에 `<p>` 태그가 있는데도 파이썬이 찾지 못하는 것입니다.



### 2.1 함정의 원인: 암묵적 소속
루트 요소에 접두사(Prefix) 없는 `xmlns`가 선언되면, 그 하위에 있는 모든 태그(`teiHeader`, `text`, `p` 등)는 눈에 보이지 않지만 암묵적으로 `http://www.tei-c.org/ns/1.0`이라는 소속(Namespace)을 가지게 됩니다. 

그러나 XPath 1.0 표준 엔진은 `"**접두사가 없는 검색어(예: //p)는 소속이 없는(No Namespace) 순수 태그만 검색한다**"`는 융통성 없는 규칙을 가지고 있습니다. 따라서 우리는 파이썬에게 **"내가 찾는 `<p>` 태그는 TEI 소속이다"**라는 것을 명시적으로 알려주어야 합니다.

### 2.2 해결책: 네임스페이스 딕셔너리 매핑 ★
이 문제를 해결하려면 파이썬의 딕셔너리(Dictionary)를 생성하여 긴 URI 주소에 임의의 짧은 별명(Prefix)을 붙여준 뒤, `.xpath()` 메서드의 `namespaces` 파라미터로 넘겨주어야 합니다.

```python
from lxml import etree

tree = etree.parse('tei_document.xml')

# 1. 네임스페이스 딕셔너리 선언 (가상의 접두사 'tei'를 부여)
ns_map = {'tei': '[http://www.tei-c.org/ns/1.0](http://www.tei-c.org/ns/1.0)'}

# 2. xpath 검색 시 모든 태그 앞에 'tei:' 접두사를 붙이고, 딕셔너리를 전달
paragraphs = tree.xpath('//tei:p', namespaces=ns_map)

# 이제 정상적으로 <p> 태그들을 찾아냅니다.
for p in paragraphs:
    print(p.text)
```
이 방식은 TEI 문서뿐만 아니라 더블린 코어(`dc:`), 원시 XML 등 다양한 네임스페이스가 융합(Mashup)된 거대 문헌 데이터를 파싱할 때 충돌을 막아주는 가장 완벽하고 안전한 정보공학적 통제 기법입니다.

## 3. 파이썬 내부에서의 XSLT 일괄 변환 (Batch Transformation)

우리는 앞선 장에서 XSLT 스크립트를 작성하여 XML을 HTML로 변환하는 시각화 원리를 배웠습니다. 파이썬과 `lxml`을 결합하면 수천 개의 TEI/XML 파일을 단 몇 분 만에 일괄적으로 HTML 웹페이지나 순수 텍스트(TXT) 코퍼스로 변환해 내는 자동화 파이프라인을 구축할 수 있습니다.



`lxml.etree.XSLT` 클래스를 사용하면 파이썬 코드 내부에서 XSLT 프로세서를 직접 구동할 수 있습니다.

```python
from lxml import etree
import os

# 1. XSLT 스크립트 파일을 파싱하여 변환기(Transformer) 객체 생성
xslt_doc = etree.parse('tei_to_html.xsl')
transform = etree.XSLT(xslt_doc)

# 2. 변환할 원본 TEI XML 파싱
xml_doc = etree.parse('source_tei.xml')

# 3. 변환기 실행 (XML을 HTML로 변환)
result_html = transform(xml_doc)

# 4. 변환된 결과를 새로운 HTML 파일로 저장
with open('output.html', 'wb') as f:
    f.write(etree.tostring(result_html, pretty_print=True, encoding='UTF-8'))
    
print("XSLT 변환이 완료되었습니다.")
```

이 코드를 파이썬의 파일 시스템 제어 라이브러리(`os`나 `glob`)와 `for` 반복문으로 감싸면, 폴더 안에 있는 10,000개의 고문헌 XML 파일을 순식간에 서비스 가능한 정적 웹사이트(Static Web Site) 파일로 찍어내는 공장이 완성됩니다.

결론적으로 `lxml`은 단순한 읽기 도구가 아니라, XML 데이터베이스를 해체하고 조작하며 새로운 매체로 렌더링하는 전천후 엔진입니다. 그러나 파일의 용량이 기가바이트(GB) 단위로 커지면 이 방식조차 컴퓨터 메모리를 마비시킬 수 있습니다. 

이어지는 장에서는 조선왕조실록과 같이 수 GB에 달하는 초거대 인문학 코퍼스를 메모리 폭발 없이 안전하게 파싱하는 최고급 기술, `"**iterparse를 활용한 이벤트 기반 스트리밍(Event-driven Streaming)**"` 기법을 탐구하겠습니다.

:::{seealso} 📖 참고문헌
* **lxml 공식 문서.** <XPath and XSLT with lxml>.
* **TEI Consortium.** <TEI P5 Guidelines: Namespaces and XML>.
:::