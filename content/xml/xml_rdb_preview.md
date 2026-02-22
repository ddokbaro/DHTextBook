---
title: "관계형 데이터베이스(RDB)와 XML의 결합"
description: "XML 문서의 계층적 구조를 훼손하지 않고 RDB의 강력한 연산 능력을 결합하는 하이브리드 설계 철학과 MSSQL XQuery, Native XML DB 활용 실무"
---

# [Level 2] 7. 관계형 데이터베이스(RDB)와 XML의 결합 ★ (핵심 실무)

지금까지 우리는 텍스트를 구조화하고(TEI/XML), 검증하며(XSD/Schematron), 탐색하고(XPath), 시각화하는(XSLT) 인문정보학의 텍스트 처리 파이프라인을 완벽하게 구축했습니다. 그러나 실제 수십만 건의 사료가 축적되는 국가 단위의 대형 아카이브를 운영하기 위해서는 텍스트 파일들을 파일 시스템 폴더에 단순히 모아두는 것만으로는 불가능합니다. 

강력한 보안, 트랜잭션 관리, 그리고 수천 명의 동시 접속 처리를 위해서는 반드시 오라클(Oracle), MSSQL, MySQL과 같은 `"**관계형 데이터베이스(RDB)**"` 시스템의 힘을 빌려야 합니다. 그러나 2차원 표(Table) 구조인 RDB와 다차원 트리(Tree) 구조인 XML은 그 태생적 철학이 완전히 다릅니다. 이 장에서는 두 이질적인 시스템을 충돌 없이 결합하는 하이브리드 설계 철학과 실전 쿼리 추출 기법을 심층적으로 다룹니다.

## 1. XML-RDB 하이브리드 설계 철학

초창기 데이터베이스 관리자(DBA)들은 XML 문서를 RDB에 넣기 위해 XML의 모든 태그를 잘게 쪼개어 수십 개의 테이블에 나누어 담는 `"**노드 분해(Shredding)**"` 방식을 취했습니다. 그러나 이 방식은 인문학 문서의 '순서(Document Order)'를 심각하게 훼손했고, 문서를 다시 조립할 때마다 수백 번의 JOIN 연산이 발생하여 시스템을 마비시켰습니다.

이러한 문제를 해결하기 위해 한국학중앙연구원 김현 교수는 인문학 사료에 최적화된 `"**XML 기반 RDB 설계 3원칙**"`을 주창했습니다.



### 1.1 제1원칙: 노드 분해 금지 (문서의 원형 보존)
XML 문서는 인간의 인문학적 사고가 담긴 유기체입니다. 따라서 문서를 쪼개지 말고, 테이블 내에 `XML` 전용 데이터 타입 컬럼을 하나 만들어 **문서 전체를 통째로(As-is) 삽입**해야 합니다. RDB 엔진은 이제 XML 문서 자체를 하나의 거대한 텍스트가 아닌, 내부 구조를 가진 데이터 객체로 인식합니다.

### 1.2 제2원칙: 메타데이터 분리 (검색 속도의 극대화)
수만 건의 XML 컬럼 내부를 매번 뒤져서 검색하는 것은 서버에 엄청난 부하를 줍니다. 따라서 문서의 고유 번호(ID), 제목, 저자, 발행일, 주제어 등 **검색에 자주 사용되는 핵심 정보들만 XML에서 뽑아내어 일반적인 RDB 컬럼(Varchar, Int, Date 등)으로 중복 저장**합니다. 즉, 검색은 가벼운 RDB 컬럼으로 빠르게 수행하고, 상세한 내용은 무거운 XML 컬럼에서 꺼내보는 `"**투-트랙(Two-Track)**"` 전략입니다.

### 1.3 제3원칙: View의 적극적 활용 (데이터의 다각적 투영)
원본 테이블(Base Table)은 하나만 유지하되, 연구자의 필요에 따라 SQL의 뷰(View, 가상 테이블)를 생성하여 데이터를 다각도로 투영합니다. 인물 관계망을 뽑아내는 인물 뷰, 지도에 뿌려줄 좌표를 뽑아내는 GIS 뷰 등을 무한히 생성할 수 있습니다.

## 2. MSSQL XQuery 실전 (핵심 실무)

현재 RDB 시장에서 XML을 가장 강력하고 우아하게 지원하는 엔진은 Microsoft SQL Server(MSSQL)입니다. MSSQL은 W3C 표준인 XPath와 XQuery를 SQL 문법 안에 완벽하게 이식했습니다.

### 2.1 테이블 생성과 데이터 삽입
`XML` 데이터 타입을 지원하므로 손쉽게 테이블을 생성할 수 있습니다. (김현 교수의 제2원칙에 따라 메타데이터 컬럼을 분리한 구조입니다.)

```sql
CREATE TABLE 제주문화유산 (
    유산ID INT PRIMARY KEY,
    유산명 VARCHAR(100),
    시대 VARCHAR(50),
    원문XML XML  /* 전체 XML 문서가 통째로 들어가는 컬럼 */
);

INSERT INTO 제주문화유산 (유산ID, 유산명, 시대, 원문XML)
VALUES (
    1, '돌하르방', '조선시대',
    '<heritage>
        <name>돌하르방</name>
        <category>민속문화재</category>
        <location lat="33.5097" lon="126.5219">제주시 관덕정</location>
        <descriptions>
            <desc type="외형">현무암으로 깎아 만든 수호신</desc>
            <desc type="기능">읍성 성문 앞 배치</desc>
        </descriptions>
    </heritage>'
);
```

### 2.2 핵심 추출 메서드 4인방 ★
MSSQL은 XML 컬럼을 조작하기 위해 4가지 강력한 XQuery 메서드를 제공합니다.



1. `"**.query(XPath)**"`: XML의 특정 조각(노드)을 **XML 형태 그대로** 뜯어옵니다.
   ```sql
   -- <location lat="33.5097" lon="126.5219">제주시 관덕정</location> 덩어리 자체를 반환
   SELECT 원문XML.query('/heritage/location') FROM 제주문화유산;
   ```

2. `"**.value(XPath, 데이터타입)**"`: XML 노드의 속성값이나 텍스트를 **RDB의 일반 데이터(문자, 숫자)로 변환**하여 가져옵니다. 실무에서 가장 많이 쓰입니다. (반드시 `[1]`과 같이 단일 값을 보장하는 순번을 명시해야 합니다.)
   ```sql
   -- XML 내부의 카테고리 텍스트를 VARCHAR 형태로 추출
   SELECT 원문XML.value('(/heritage/category)[1]', 'VARCHAR(50)') AS 분류 
   FROM 제주문화유산;
   ```

3. `"**.exist(XPath)**"`: 특정 노드나 조건을 만족하는 데이터가 존재하는지 **참(1) 또는 거짓(0)**으로 반환합니다. `WHERE` 조건절에서 검색용으로 탁월합니다.
   ```sql
   -- 외형에 대한 설명(desc)이 존재하는 레코드만 검색
   SELECT 유산명 FROM 제주문화유산 
   WHERE 원문XML.exist('/heritage/descriptions/desc[@type="외형"]') = 1;
   ```

4. `"**.nodes(XPath)**"`: 내부에 반복적으로 등장하는 여러 개의 요소들을 쪼개어 **가상의 RDB 행(Row)으로 풀어냅니다(Shredding in memory)**.
   ```sql
   -- 여러 개의 <desc> 태그를 각각의 행으로 분리하여 출력
   SELECT 
       유산명,
       T.c.value('.', 'VARCHAR(100)') AS 상세설명
   FROM 제주문화유산
   CROSS APPLY 원문XML.nodes('/heritage/descriptions/desc') AS T(c);
   ```

### 2.3 실전: 메타 뷰(Meta View)와 GIS 뷰(GIS View) 생성
제3원칙에 따라, 웹 지도(Web Map) 서비스에 제주 문화유산을 뿌려주기 위해 원본 XML 테이블에서 위도와 경도 정보만 핀셋으로 뽑아내어 가상의 뷰를 만듭니다.

```sql
CREATE VIEW View_Jeju_GIS AS
SELECT 
    유산ID,
    유산명,
    원문XML.value('(/heritage/location/@lat)[1]', 'FLOAT') AS 위도,
    원문XML.value('(/heritage/location/@lon)[1]', 'FLOAT') AS 경도
FROM 제주문화유산
WHERE 원문XML.exist('/heritage/location[@lat]') = 1;
```
이제 개발자들은 복잡한 XML 문법을 전혀 몰라도, `SELECT * FROM View_Jeju_GIS`라는 단순한 SQL 구문만으로 즉시 지도 시각화용 위경도 데이터를 얻을 수 있습니다. 이것이 RDB와 XML 하이브리드 설계의 궁극적인 위력입니다.

## 3. MySQL과 Native XML DB의 대안적 접근

MSSQL이 가장 강력하지만, 오픈소스 환경이나 다른 철학을 가진 대안 시스템들도 존재합니다.

### 3.1 MySQL/MariaDB 환경
MySQL은 전통적으로 XML 처리에 약했으나, 제한적으로나마 함수 기반의 처리를 지원합니다.
* `"**ExtractValue(xml컬럼, XPath)**"`: MSSQL의 `.value()`와 유사하게 XML 내부의 텍스트를 추출합니다.
* `"**UpdateXML(xml컬럼, XPath, 새문자열)**"`: XML 내부의 특정 노드 값을 변경합니다.
다만 MySQL은 컬럼 자체의 유효성을 검증하는 XSD 스키마 바인딩이나 고급 XQuery 연산을 지원하지 않아 복잡한 인문학 데이터 모델링에는 한계가 있습니다. (현대 MySQL은 XML보다는 JSON 지원에 훨씬 주력하고 있습니다.)

### 3.2 Native XML DB: eXist-db의 NoSQL 접근법
하이브리드를 거부하고 **"애초에 테이블(Table) 따위는 필요 없다. XML 문서를 원형 그대로 저장하고 검색하자"**는 철학으로 만들어진 시스템이 `"**Native XML 데이터베이스**"`입니다. 

대표적인 오픈소스인 `"**eXist-db**"`는 데이터를 RDB의 행(Row)과 열(Column)로 쪼개지 않고, 파일 시스템의 폴더와 같은 컬렉션(Collection) 단위로 XML 문서를 통째로 쏟아 넣습니다. 그리고 SQL을 전혀 사용하지 않으며, 오직 **XQuery 언어만으로 데이터를 삽입, 수정, 검색**합니다. 방대한 TEI 코퍼스(Corpus)나 계층 구조가 극도로 복잡한 문헌학 아카이브 구축 시 유럽과 미국의 학계에서 폭넓게 사랑받는 시스템입니다.

결론적으로 데이터의 성격이 정형 데이터(메타데이터)와 비정형 데이터(본문 텍스트)가 강하게 결합되어 있다면 MSSQL의 **하이브리드 아키텍처**를, TEI 본문의 복잡성이 극에 달해 테이블 구조에 담기조차 벅차다면 **Native XML DB(eXist-db)**를 선택하는 것이 디지털 인문학 시스템 아키텍트의 올바른 의사결정입니다.

:::{seealso} 📖 참고문헌
* **Microsoft.** <SQL Server XML Data Type and XQuery Documentation>.
* **Meier, Wolfgang.** <eXist: An Open Source Native XML Database>.
:::