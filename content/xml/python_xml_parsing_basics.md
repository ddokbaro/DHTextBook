---
title: "파이썬 XML 제어의 기초: ElementTree와 lxml"
description: "디지털 인문학 데이터를 파이썬 환경으로 불러오기 위한 xml.etree.ElementTree의 기초 활용법과, 압도적 성능을 자랑하는 lxml 라이브러리의 생태계"
---

# 파이썬 XML 제어의 기초: ElementTree와 lxml

지금까지 우리는 DTD와 XSD로 뼈대를 세우고, TEI 가이드라인을 통해 아날로그 사료를 정밀한 XML 문서로 변환하는 마크업(Markup)의 세계를 탐구했습니다. 그러나 수만 건, 수십 기가바이트(GB)에 달하는 국가 단위의 역사 코퍼스(Corpus)를 연구자가 일일이 눈으로 읽고 수정하는 것은 불가능합니다.

이 방대한 디지털 문헌들을 한 번에 메모리로 불러와(Parsing), 자연어 처리(NLP) 엔진에 넘겨주거나, 새로운 태그를 일괄적으로 삽입하여 다시 파일로 저장하는 궁극의 자동화 도구가 바로 `"**파이썬(Python)**"`입니다. 극도의 효율성을 추구하는 디지털 인문학 실무에서 파이썬은 선택이 아닌 필수입니다. 이 장에서는 파이썬에서 XML을 다루는 두 가지 핵심 라이브러리인 내장 `ElementTree`와 서드파티 `lxml`의 차이를 이해하고, 텍스트 트리를 탐색하고 조작하는 기초를 마스터합니다.

## 1. 라이브러리 생태계: ElementTree vs lxml

파이썬에서 XML 트리를 제어하는 방법론은 크게 두 가지 갈래로 나뉩니다.

### 1.1 내장 라이브러리: `xml.etree.ElementTree`
파이썬을 설치하면 기본적으로 제공되는 표준 라이브러리입니다. 가볍고 외부 의존성이 없어 몇 십 줄짜리 간단한 스크립트를 짤 때 매우 유용합니다. 그러나 C언어 기반 라이브러리에 비해 처리 속도가 다소 느리고, 가장 치명적인 단점으로 앞서 우리가 심도 있게 학습한 `"**XPath 1.0의 복잡한 문법(예: 조상 탐색, 내장 함수 등)을 온전히 지원하지 못한다**"`는 한계가 있습니다.

### 1.2 서드파티 라이브러리: `lxml` ★
방대한 텍스트 데이터를 다루는 디지털 문헌학 실무에서 압도적인 표준으로 자리 잡은 라이브러리입니다. C언어로 작성된 `libxml2`와 `libxslt` 엔진을 기반으로 하여 파싱 및 연산 속도가 타의 추종을 불허합니다. 또한, 완전한 XPath 1.0과 XSLT 1.0을 지원하므로 앞서 배운 모든 고급 탐색 기술을 파이썬 코드 안에서 그대로 구사할 수 있습니다. 
*(설치: 명령 프롬프트나 터미널에서 `pip install lxml` 실행)*

> **[실무 팁]**
> `lxml`은 파이썬 표준 `ElementTree`의 API(명령어 체계)를 거의 100% 호환되게 설계했습니다. 따라서 기초적인 트리 탐색 명령어는 두 라이브러리가 완전히 동일합니다. 본 교재에서는 실무 호환성과 극강의 효율성을 위해 `lxml`의 `etree` 모듈을 기준으로 설명합니다.

## 2. 문서 파싱(Parsing)과 트리 구조 이해

파싱이란 하드디스크에 텍스트 형태로 저장된 XML 문서를 파이썬 프로그램이 이해하고 조작할 수 있는 트리(Tree) 객체로 메모리에 적재하는 과정입니다.

```python
from lxml import etree

# 1. 하드디스크의 파일에서 XML 파싱하기
tree = etree.parse('modern_magazine.xml')
root = tree.getroot()  # 최상위 루트 요소 획득

# 2. 파이썬 문자열(String)에서 직접 파싱하기
xml_string = """
<잡지>
    <서지정보 발행년도="1920">
        <잡지명>개벽</잡지명>
    </서지정보>
    <기사목록>
        <기사 ID="A01">
            <제목>무정</제목>
            <필자>이광수</필자>
        </기사>
    </기사목록>
</잡지>
"""
root = etree.fromstring(xml_string)
```



파이썬 메모리에 적재된 각각의 XML 태그는 `"**Element(요소) 객체**"`가 됩니다. 이 객체는 텍스트를 제어하기 위한 세 가지 핵심 속성을 가집니다.
* `element.tag`: 태그의 이름 (예: `'잡지명'`)
* `element.text`: 태그 안에 들어있는 텍스트 (예: `'개벽'`)
* `element.attrib`: 태그의 속성들을 담고 있는 파이썬 `"**딕셔너리(Dictionary)**"` (예: `{'발행년도': '1920'}`)

## 3. 트리 탐색의 기초 (Traversal)

메모리에 올라간 트리를 위에서 아래로 훑어 내려가는 기초적인 탐색 메서드들을 살펴봅니다.

### 3.1 자식 노드 순회하기
파이썬의 `for` 문을 사용하면, 현재 요소의 바로 아래 직계 자식(Children)들을 순서대로 꺼내볼 수 있습니다.

```python
article_list = root.find("기사목록")

# 기사목록 하위의 모든 <기사> 요소를 순회
for article in article_list:
    print("태그명:", article.tag)
    print("기사번호:", article.attrib["ID"])
    # 출력 결과: 
    # 태그명: 기사 
    # 기사번호: A01
```

### 3.2 기초 검색 메서드 (`find`, `findall`, `iter`)
특정 이름을 가진 요소를 족집게처럼 찾아낼 때 사용하는 세 가지 핵심 메서드입니다.

* `"**element.find('태그명')**"`: 현재 요소의 직계 자식 중 이름이 일치하는 **첫 번째** 요소 단 하나만 반환합니다.
* `"**element.findall('태그명')**"`: 이름이 일치하는 **모든** 직계 자식 요소를 파이썬 리스트(List)로 반환합니다.
* `"**element.iter('태그명')**"`: 직계 자식뿐만 아니라 **모든 후손(Descendants)**들을 샅샅이 뒤져 조건에 맞는 요소를 차례대로 반환하는 제너레이터(Generator)입니다. 계층이 깊은 TEI 문서에서 본문 텍스트만 뽑아낼 때 탁월한 성능을 발휘합니다.

```python
# 문서 전체 계층을 샅샅이 뒤져 모든 <필자> 태그의 텍스트를 추출
for author in root.iter("필자"):
    print(author.text)
    # 출력 결과: 이광수
```

## 4. 노드의 수정과 파일 생성 (XML Writing)

파이썬은 단순히 XML을 읽는 것뿐만 아니라, 기존 데이터를 수정하거나 아예 텅 빈 공간에서 새로운 XML 트리를 구축하여 파일로 저장할 수 있습니다. 수백 개의 파편화된 사료 파일에 동일한 메타데이터(예: `<editor>`)를 일괄적으로 추가해야 할 때 인간의 수작업을 완벽하게 대체합니다.

### 4.1 요소의 생성과 부착 (`SubElement`)
`etree.Element()`로 독립된 태그를 만들고 `append()`로 붙일 수도 있지만, `etree.SubElement()`를 사용하면 부모를 지정함과 동시에 자식을 생성하여 부착하는 과정을 한 줄로 효율적으로 압축할 수 있습니다.

```python
# 새로운 <기사> 요소를 생성하여 기존 '기사목록'에 부착
new_article = etree.SubElement(article_list, "기사")
new_article.set("ID", "A02")  # 속성 추가 (딕셔너리 조작과 동일)

# 자식 요소들 생성 및 텍스트 부여
title = etree.SubElement(new_article, "제목")
title.text = "소년 창간사"

author = etree.SubElement(new_article, "필자")
author.text = "최남선"
```

### 4.2 파일로 내보내기 (`write`)
수정이 완료된 트리는 `write()` 메서드를 통해 다시 하드디스크의 텍스트 파일로 저장합니다. 한국어와 한자가 섞인 동아시아 문헌을 다룰 때는 인코딩(`utf-8`)을 반드시 지정해야 합니다.

```python
# 들여쓰기(pretty_print)를 적용하여 사람이 읽기 편한 UTF-8 파일로 저장
# (참고: pretty_print는 lxml에서만 지원하는 강력한 기능입니다)
tree = etree.ElementTree(root)
tree.write("updated_magazine.xml", encoding="utf-8", xml_declaration=True, pretty_print=True)
```

이 기초적인 파싱과 조작 기능만으로도 우리는 수십 시간이 걸릴 텍스트 정제 작업을 단 몇 초 만에 끝낼 수 있습니다. 그러나 TEI와 같이 구조가 고도로 복잡한 인문학 데이터베이스에서는 `findall` 같은 기초 메서드만으로는 원하는 데이터를 정밀하게 타겟팅하기 어렵습니다. 

이어지는 장에서는 `lxml` 라이브러리의 진정한 위력인 **"XPath의 완벽한 적용과, 파이썬에서 TEI 네임스페이스(Namespace)를 제어하는 고급 실무"**의 세계로 진입하겠습니다.

:::{seealso} 📖 참고문헌
* **lxml 공식 문서.** <lxml - Processing XML and HTML with Python>.
* **Python Documentation.** <xml.etree.ElementTree — The ElementTree XML API>.
:::