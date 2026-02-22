---
title: "TEI 문서의 뇌: teiHeader와 메타데이터 설계"
description: "디지털 인문학 데이터의 정체성과 학술적 신뢰성을 보장하는 <teiHeader>의 필수 구조와, 한국 고문헌의 특수성을 반영한 서지 및 인코딩 선언(encodingDesc) 실무"
---

# TEI 문서의 뇌: teiHeader와 메타데이터 설계

거대한 XML 텍스트 파일이 인터넷의 바다에 홀로 버려졌을 때, 이 파일이 누가 언제 만든 것인지, 원본 출처는 무엇인지, 어떤 원칙으로 편집되었는지 알 수 없다면 그 데이터는 학술적 가치를 완전히 상실합니다.

TEI(Text Encoding Initiative)는 이러한 비극을 막기 위해, 모든 문서의 최상단에 데이터의 신분증이자 뇌(Brain) 역할을 하는 `"**<teiHeader>**"`를 반드시 배치하도록 강제합니다. 특히 한국과 동아시아의 고문헌 디지털화 프로젝트에서 `<teiHeader>`는 단순히 제목과 저자를 적는 공간을 넘어, 원전의 복잡한 물리적 판본 정보와 디지털 편집자의 학술적 개입을 낱낱이 기록하는 핵심 영역입니다.

## 1. <teiHeader>의 4대 거시 구조

`<teiHeader>` 내부는 논리적으로 엄격하게 구분된 4개의 주요 자식 요소로 구성됩니다. 이 중 첫 번째인 `<fileDesc>`는 절대 생략할 수 없는 필수 요소입니다.



```xml
<teiHeader>
    <fileDesc>...</fileDesc>       
    <encodingDesc>...</encodingDesc> 
    <profileDesc>...</profileDesc>   
    <revisionDesc>...</revisionDesc> 
</teiHeader>
```

## 2. 서지 정보: `<fileDesc>`의 정교화

`<fileDesc>`(File Description)는 컴퓨터 파일 그 자체에 대한 정보와, 그 파일이 바탕을 두고 있는 아날로그 원전(Source)에 대한 정보를 함께 기술합니다. 한국 고문헌은 판본(Edition)에 따라 내용 차이가 크고 소장처와 수집 경위가 중요하므로 이 영역의 세분화가 필수적입니다.

### 2.1 제목과 책임의 명시: `<titleStmt>`
전자 문서의 제목과 이 디지털 문서를 생산하는 데 기여한 사람들을 기록합니다. 
장서각 고문서 아카이브와 같은 실무 프로젝트에서는 원전의 한문 제목, 현대어 번역 제목, 그리고 데이터베이스 식별을 위한 유형적 제목을 명확히 구분하여 병기하는 방식을 취합니다.

```xml
<titleStmt>
    <title type="main">안동김씨 분재기(分財記)</title>
    <title type="translated">안동 김씨 가문의 재산 상속 문서</title>
    <author>김아무개</author>
    <editor>디지털인문학연구소</editor>
</titleStmt>
```

### 2.2 출판 및 배포 정보: `<publicationStmt>`
이 전자 문서의 배포처와 저작권, 라이선스 권한을 명시합니다. 공공 사료의 개방형 연결 데이터(LOD) 활용 및 학술적 공유를 위해 매우 중요한 영역입니다.

### 2.3 원본 사료의 물리적 기술: `<sourceDesc>` ★
현재 인코딩하고 있는 디지털 텍스트가 어떤 아날로그 원전에 바탕을 두고 있는지 기술합니다. 

단순히 책 이름만 적는 서구식 관행을 넘어, 한국 서지학의 전통을 디지털로 계승하기 위해 필사본(Manuscript), 목판본(Woodblock print), 활자본(Movable type print) 여부를 명시하고, 한 페이지의 줄 수와 한 줄의 글자 수(行款, 행관), 종이의 재질 등을 세밀하게 기록합니다.

```xml
<sourceDesc>
    <bibl>
        <title>조선왕조실록</title>
        <edition>태백산사고본(太白山史庫本)</edition>
        <extent>목판본, 권지 15</extent>
        <repository>국가유산청 국립고궁박물관</repository>
    </bibl>
</sourceDesc>
```

## 3. 인코딩 선언: `<encodingDesc>`와 편집 원칙

`<encodingDesc>`(Encoding Description)는 아날로그 텍스트를 디지털로 옮기는 과정에서 연구진이 어떠한 `"**철학적, 기술적 관점**"`을 적용했는지를 세상에 선언하는 곳입니다. 고도화된 아카이브일수록 이곳에 정밀한 가이드라인을 새겨 넣습니다.

### 3.1 편집 원칙 선언: `<editorialDecl>`
구두점이 없는 원문에 구두점을 어떻게 삽입했는지, 탈자나 오자를 어떻게 교정했는지, 한자의 정규화(Normalization)는 어떤 원칙으로 진행했는지를 서술형 텍스트나 하위 요소(`<punctuation>`, `<normalization>`)로 명시합니다. 
* **실무 활용:** 승정원일기 디지털화 작업 시, 이두나 차자 표기를 어떻게 현대 컴퓨터 환경에 맞게 풀어서 입력했는지에 대한 룰을 이곳에 기록하여 후속 연구자들에게 텍스트의 변형 근거를 제공합니다.

### 3.2 참조 체계 선언: `<refsDecl>`
전자 텍스트 내부의 특정 위치를 찾기 위한 주소 체계를 선언합니다. 한국문집총간이나 대장경 등에서 권(卷), 장(張), 행(行)으로 이어지는 동아시아 고문헌 고유의 3단계 참조 체계가 어떻게 XML의 논리적 구조(`<div1>`, `<div2>`)와 맵핑되는지를 정의합니다.

### 3.3 외자(Gaiji)와 이체자 정의: `<charDecl>` ★
동아시아 디지털 인문학에서 가장 난도가 높은 `"**외자(Gaiji)**"` 처리를 담당하는 핵심 요소입니다. 유니코드에 없는 특수한 기호, 벽자, 혹은 이체자(예: 說과 説, 靑과 青)를 본문에서 사용하기 위해, 헤더에서 미리 그 문자의 존재를 선언하고 이미지(글리프)를 매핑해 둡니다.

```xml
<encodingDesc>
    <charDecl>
        <char xml:id="gaiji_001">
            <charName>특수 형태의 靑</charName>
            <mapping type="standard">靑</mapping>
            <figure>
                <graphic url="images/gaiji_001.png" mimeType="image/png"/>
            </figure>
        </char>
    </charDecl>
</encodingDesc>
```
이 선언을 마친 후, 본문에서는 `<g ref="#gaiji_001"/>`와 같은 방식으로 호출하여 사용합니다. 이는 검색성(표준자 '靑'으로 검색 가능)을 완벽하게 유지하면서도 원전의 시각적 형태(자형 이미지)를 손실 없이 보존하는 정보공학적 해결책입니다. 블라인드 교환(Blind Interchange) 환경에서도 타 연구자가 이 문자의 실체를 정확히 파악할 수 있게 해줍니다.

## 4. 메타데이터의 생명력: 프로파일과 이력 관리

### 4.1 텍스트의 맥락: `<profileDesc>`
텍스트가 생산된 상황(창작 연도, 장소), 사용된 언어(`<langUsage>`), 그리고 텍스트의 장르나 주제 분류(`<textClass>`)를 기록합니다. 문중 고문서 관계망을 구축할 때, 문서가 작성된 사회적 맥락이나 수발신자의 신분 정보가 이곳에 요약될 수 있습니다.

### 4.2 이력 추적: `<revisionDesc>`
문서가 생성된 이후 누가, 언제, 어떤 수정을 가했는지를 기록하는 리비전 컨트롤(Revision Control) 구역입니다. 다수의 학자가 수년에 걸쳐 교열하는 대규모 장기 프로젝트에서 데이터의 무결성을 증명하는 감사 추적(Audit Trail) 역할을 수행합니다.

결론적으로 한국 고문헌의 `<teiHeader>` 작성은 단순한 꼬리표 달기가 아닙니다. 아날로그 사료가 지닌 물성(物性)과 문헌학자들의 치열한 고증 과정을 기계의 언어로 번역하여 영구히 보존하는 `"**메타데이터 예술**"`입니다. 

문서의 뇌를 완벽하게 설계했으니, 이어지는 장에서는 실제 텍스트가 담기는 몸통, 즉 **“본문(Body)의 거시적, 미시적 구조화와 이정표 마크업”**에 대해 심층적으로 다루겠습니다.

:::{seealso} 📖 참고문헌
* **TEI Consortium.** <TEI P5 Guidelines: The TEI Header>.
* **Burnard, Lou, and C. M. Sperberg-McQueen.** <A Gentle Introduction to XML>.
:::