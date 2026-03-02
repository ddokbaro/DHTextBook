---
title: "SQL 실습을 위한 조선시대 인물·관직 통합 데이터셋 구축"
description: "앞선 SQL 질의어 실습(LIKE, JOIN, 서브쿼리 등)을 완벽하게 재현하기 위해, 단 한 번의 실행으로 4개의 테이블과 역사 사료 데이터를 구축하는 통합 SQL 스크립트"
---

# SQL 실습을 위한 조선시대 인물·관직 통합 데이터셋 구축

눈으로 읽는 SQL은 결코 자신의 지식이 되지 않습니다. 앞선 장에서 배운 패턴 매칭(`LIKE`), 관계망 복원(`JOIN`), 그리고 고난도 서브쿼리(Subquery)를 여러분의 환경에서 직접 타이핑하고 결과를 확인해 보아야 합니다.

이 장에서는 복잡한 CSV 임포트 과정 없이, SQL 쿼리 창에 복사하여 붙여넣고 `실행(Run)` 버튼을 누르는 것만으로 완벽하게 정규화된 4개의 조선시대 역사 테이블(본관, 관직, 인물, 임용)과 실습용 마중물 데이터를 생성해 주는 `"**통합 DDL/DML 스크립트**"`를 제공합니다.

## 1. 실습 데이터베이스 초기화 및 테이블 생성 (DDL)

DBeaver나 DB Fiddle(웹 샌드박스)의 SQL 편집창을 열고 아래의 코드를 붙여넣으십시오. 기존에 꼬여있던 테이블을 안전하게 지우고(`DROP`), 새로운 뼈대(`CREATE`)를 세웁니다.

```sql
-- 1. 기존 테이블이 있다면 안전하게 삭제 (초기화를 위함)
DROP TABLE IF EXISTS appointment_tb;
DROP TABLE IF EXISTS person_tb;
DROP TABLE IF EXISTS office_tb;
DROP TABLE IF EXISTS clan_tb;

-- 2. 본관 마스터 테이블 생성
CREATE TABLE clan_tb (
    clan_id VARCHAR(10) PRIMARY KEY,
    clan_name VARCHAR(50) NOT NULL
);

-- 3. 관직 마스터 테이블 생성
CREATE TABLE office_tb (
    office_id VARCHAR(10) PRIMARY KEY,
    office_name VARCHAR(50) NOT NULL,
    rank_grade VARCHAR(20),
    civil_military VARCHAR(10),
    establish_year INT
);

-- 4. 인물 마스터 테이블 생성 (역사적 모호성 패턴 적용)
CREATE TABLE person_tb (
    person_id VARCHAR(10) PRIMARY KEY,
    person_name VARCHAR(50) NOT NULL,
    clan_id VARCHAR(10),
    birth_year INT,
    birth_precision VARCHAR(1),
    death_year INT,
    origin_place VARCHAR(50)
);

-- 5. 임용(관역) 이벤트 테이블 생성 (다대다 교차 테이블)
CREATE TABLE appointment_tb (
    appoint_id VARCHAR(10) PRIMARY KEY,
    person_id VARCHAR(10),
    office_id VARCHAR(10),
    appoint_date DATE,
    resign_date DATE,
    appoint_type VARCHAR(20)
);
```

## 2. 사료 데이터 적재 (DML - INSERT)

뼈대가 완성되었으니, 우리가 앞서 교안에서 다루었던 역사적 인물(이순신, 원균, 이이, 허균 등)과 그들의 관역 데이터를 밀어 넣습니다. 이 데이터는 교안의 모든 예제 쿼리가 정상 작동하도록 치밀하게 설계되었습니다.

```sql
-- [1] 본관 데이터 적재
INSERT INTO clan_tb (clan_id, clan_name) VALUES 
('C01', '덕수이씨'),
('C02', '원주원씨'),
('C03', '전주이씨'),
('C04', '풍천임씨'),
('C05', '봉화정씨'),
('C06', '안동권씨');

-- [2] 관직 데이터 적재 (establish_year 포함)
INSERT INTO office_tb (office_id, office_name, rank_grade, civil_military, establish_year) VALUES 
('O001', '전라좌도수군절도사', '정3품', '서반', 1392),
('O002', '삼도수군통제사', '종2품', '서반', 1593),
('O003', '정읍현감', '종6품', '동반', 1392),
('O004', '백의종군', '없음', '없음', 1392),
('O005', '호조좌랑', '정6품', '동반', 1392),
('O006', '규장각 검교직각', '정3품', '동반', 1776); -- 1700년 이후 신설 관직 (서브쿼리 실습용)

-- [3] 인물 데이터 적재 (NULL 및 모호성 코드 포함)
INSERT INTO person_tb (person_id, person_name, clan_id, birth_year, birth_precision, death_year, origin_place) VALUES 
('P001', '이이', 'C01', 1536, 'D', 1584, '강릉'),
('P002', '원균', 'C02', 1540, 'Y', 1597, '평택'),
('P003', '이순신', 'C01', 1545, 'D', 1598, '한성부 건천동'), -- REPLACE 실습용
('P004', '임성주', 'C04', 1711, 'Y', 1788, '한성부'),     -- REPLACE 실습용
('P005', '이성계', 'C03', 1335, 'Y', 1408, '함흥'),
('P006', '정도전', 'C05', 1342, 'Y', 1398, '영주'),
('P007', '허균', 'C99', NULL, 'U', 1618, '강릉'),        -- IS NULL 실습용 (생년 미상)
('P008', '박처사', 'C06', 1550, 'Y', 1620, '안동');       -- LEFT JOIN 실습용 (임용 기록 없는 재야 선비)

-- [4] 임용 이벤트 데이터 적재 (다대다 관계망)
INSERT INTO appointment_tb (appoint_id, person_id, office_id, appoint_date, resign_date, appoint_type) VALUES 
('H001', 'P003', 'O003', '1589-12-01', '1591-02-12', '제수'), -- 이순신 -> 정읍현감
('H002', 'P003', 'O001', '1591-02-13', '1593-08-14', '특진'), -- 이순신 -> 전라좌수사
('H003', 'P003', 'O002', '1593-08-15', '1597-02-26', '제수'), -- 이순신 -> 통제사
('H004', 'P002', 'O001', '1592-02-13', '1593-01-20', '제수'), -- 원균 -> 전라좌수사
('H005', 'P002', 'O002', '1597-01-20', '1597-08-28', '제수'), -- 원균 -> 통제사
('H006', 'P002', 'O004', '1597-03-01', '1597-07-20', '좌천'), -- 원균 -> 백의종군
('H007', 'P001', 'O005', '1564-05-10', '1565-01-01', '제수'), -- 이이 -> 호조좌랑
('H008', 'P004', 'O006', '1780-03-01', '1782-10-15', '제수'); -- 임성주 -> 규장각 검교직각 (1700년대 이후 관직)
```

## 3. 실습 쿼리 검증 가이드

데이터가 성공적으로 적재되었다면, 이전 교안에서 배웠던 핵심 쿼리들을 직접 실행해 보며 결과를 확인하십시오.

* **[패턴 매칭 실습] `LIKE '이%'`**
  * `person_tb`에서 성씨가 '이'씨인 사람을 검색해 보십시오. (이이, 이순신, 이성계 3명이 검색되어야 정상입니다.)
* **[텍스트 치환 실습] `REPLACE`**
  * `person_tb`에서 `출신지` 컬럼의 '한성부'를 '서울'로 치환하여 조회해 보십시오. (이순신은 '서울 건천동', 임성주는 '서울'로 출력됩니다.)
* **[결측치 추적 실습] `IS NULL`**
  * 생년(`birth_year`)이 `NULL`인 인물을 검색해 보십시오. (기록이 소실된 '허균'이 색출됩니다.)
* **[다중 테이블 결합 실습] `INNER JOIN`**
  * 인물, 임용, 관직 테이블을 조인하여 '이순신'을 검색해 보십시오. (정읍현감 -> 전라좌수사 -> 통제사 순으로 이력이 출력됩니다.)
* **[소외된 데이터 발굴 실습] `LEFT JOIN`**
  * `person_tb`를 왼쪽에 두고 `appointment_tb`를 조인한 뒤, 임용일자가 `NULL`인 인물을 검색해 보십시오. (관직에 나가지 않은 재야 선비 '박처사'가 발굴됩니다.)

이제 여러분의 로컬 환경은 조선시대 사료를 캐내는 완벽한 지식의 발굴터가 되었습니다. 마음껏 데이터를 조작하고 탐구해 보십시오!