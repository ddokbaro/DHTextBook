---
title: "관계망 복원 실습: 다중 테이블 JOIN 연산과 서브쿼리(Subquery)의 응용"
description: "정규화로 분리된 인물, 관직, 임용 테이블을 SQL의 JOIN 연산으로 결합하여 역사적 관계망을 복원하고, 쿼리 안의 쿼리(Subquery)를 통해 고난도 인문학 질의를 수행하는 실무 가이드"
---

# 관계망 복원 실습: 다중 테이블 JOIN 연산과 서브쿼리(Subquery)의 응용

앞서 우리는 제1~제3 정규화(Normalization)라는 고통스러운 수술을 통해, 하나의 엑셀 시트에 욱여넣어져 있던 사료들을 `"**인물 테이블**"`, `"**관직 테이블**"`, 그리고 `"**임용(사건) 테이블**"`로 뿔뿔이 흩어놓았습니다. 데이터를 완벽하게 분리하여 무결성을 확보했지만, 역설적으로 인간의 눈으로 역사적 맥락을 한 번에 파악하기는 불가능해졌습니다.

"이순신이 언제 어떤 관직을 거쳤는가?"를 알아내려면, 인물 테이블에서 이순신의 ID를 메모하고, 임용 테이블에서 그 ID를 찾아 관직 ID를 알아낸 뒤, 다시 관직 테이블을 뒤져 관직명을 확인해야 합니다. 이 끔찍한 수작업을 단 한 줄의 코드로 해결하고 흩어진 지식의 조각들을 거대한 관계망(Network)으로 직조해 내는 궁극의 연산, 그것이 바로 `"**JOIN(조인)**"`입니다.

## 1. 관계의 복원: `INNER JOIN` (교집합)

`JOIN`은 두 개 이상의 테이블을 특정 기준(보통은 PK와 FK)에 따라 가로로 병합하여 하나의 거대한 가상 테이블을 만들어내는 연산입니다. 그중에서도 `"**INNER JOIN**"`은 두 테이블 양쪽에 모두 데이터가 존재하는 `"**완벽한 짝(교집합)**"`만을 추출합니다.



### 1.1 인물과 임용 기록의 결합
먼저 인물(`person_tb`)과 임용 사건(`appointment_tb`)을 결합해 보겠습니다. 두 테이블을 잇는 논리적 다리는 바로 `인물ID`입니다.

```sql
SELECT 
    p.person_name AS 이름, 
    a.appoint_date AS 임용일자, 
    a.office_id AS 관직코드
FROM appointment_tb a
INNER JOIN person_tb p 
    ON a.person_id = p.person_id;
```
* **테이블 별칭(Alias):** 쿼리가 길어지는 것을 막기 위해 `person_tb`를 `p`로, `appointment_tb`를 `a`로 줄여 부릅니다.
* **ON 조건절:** 기계에게 `"**A 테이블의 인물ID와 P 테이블의 인물ID가 일치하는 것끼리 줄을 세워라**"`라고 결합의 기준을 명확히 선언합니다.

### 1.2 3개 테이블의 다중 JOIN (N:M 관계의 완벽한 해소)
위의 쿼리 결과에는 아직 '관직코드(O001)'만 보일 뿐 한글 관직명이 없습니다. 관직명은 `office_tb`에 있기 때문입니다. 꼬리에 꼬리를 무는 다중 `JOIN`을 통해 세 개의 테이블을 완벽하게 관통해 보겠습니다.

```sql
SELECT 
    p.person_name AS 이름, 
    o.office_name AS 역임관직, 
    a.appoint_date AS 임용일자
FROM appointment_tb a
INNER JOIN person_tb p ON a.person_id = p.person_id
INNER JOIN office_tb o ON a.office_id = o.office_id
WHERE p.person_name = '이순신'
ORDER BY a.appoint_date ASC;
```
이 쿼리를 실행하는 순간, 분절되어 있던 세 개의 테이블이 0.01초 만에 합체하며 이순신의 평생 관역(Career Path)이 시간순으로 아름답게 정렬되어 출력됩니다. 이것이 바로 관계형 데이터베이스(RDB)가 디지털 인문학에 선사하는 최고의 시너지입니다.

## 2. 소외된 자들의 발굴: `LEFT OUTER JOIN` (차집합의 응용)

`INNER JOIN`이 완벽하게 짝이 맞는 데이터만 보여준다면, `"**LEFT OUTER JOIN**"`은 기준이 되는 왼쪽 테이블의 모든 데이터를 무조건 살려둔 채, 오른쪽 테이블에서 짝을 찾지 못한 빈자리는 `NULL`로 채워서 보여줍니다.

이 기능은 인문학 연구에서 `"**기록이 결핍된 대상(소외된 데이터)**"`을 발굴할 때 압도적인 위력을 발휘합니다.



### 2.1 벼슬길에 오르지 못한 재야의 선비 찾기
인물 테이블에는 존재하지만, 평생 단 한 번도 관직에 임용된 적이 없는 처사(處士)나 산림(山林) 학자들을 찾아야 한다고 가정해 봅시다. `INNER JOIN`을 쓰면 임용 기록이 없는 이들은 결과에서 영영 증발해 버립니다.

```sql
SELECT 
    p.person_name AS 이름, 
    a.appoint_date AS 임용기록
FROM person_tb p
LEFT JOIN appointment_tb a 
    ON p.person_id = a.person_id
WHERE a.appoint_date IS NULL;
```
왼쪽(`person_tb`)의 인물은 모두 불렀는데, 오른쪽(`appointment_tb`)에서 임용 기록을 찾지 못해 임용기록 칸이 텅 비어버린(`IS NULL`) 사람들만 색출해 낸 것입니다. 이처럼 차집합의 논리를 응용하면 사료의 공백 자체가 훌륭한 연구 데이터로 탈바꿈합니다.

## 3. 쿼리 안의 쿼리: 서브쿼리(Subquery)의 지적 유희

JOIN이 테이블을 가로로 길게 붙이는 연산이라면, `"**서브쿼리(Subquery)**"`는 쿼리문 안에 또 다른 쿼리문을 괄호로 중첩하여, 복잡한 인문학적 질문을 단계적으로 해결하는 기법입니다.

### 3.1 조건절(WHERE)에서의 서브쿼리
"우리 데이터베이스에 등록된 인물들 중, 가장 먼저 태어난(생년이 가장 빠른) 사람은 누구인가?"라는 질문을 던져봅시다. 
가장 빠른 생년을 구하는 쿼리(`SELECT MIN(birth_year) FROM person_tb`)와, 그 생년을 가진 사람의 이름을 찾는 쿼리를 두 번 칠 필요 없이 하나로 결합합니다.

```sql
SELECT person_name, birth_year
FROM person_tb
WHERE birth_year = (
    SELECT MIN(birth_year) 
    FROM person_tb
);
```
괄호 안의 서브쿼리가 먼저 실행되어 '1392'라는 값을 도출해 내면, 바깥쪽의 메인 쿼리가 `WHERE birth_year = 1392`로 치환되어 최종적으로 정도전이나 이성계의 이름을 출력해 줍니다. 

### 3.2 IN 연산자와의 결합 (다중 행 서브쿼리)
"조선 후기(1700년대 이후)에 신설된 관직을 역임해 본 모든 인물의 명단"을 추출하려면 어떻게 해야 할까요?

```sql
SELECT DISTINCT p.person_name
FROM person_tb p
INNER JOIN appointment_tb a ON p.person_id = a.person_id
WHERE a.office_id IN (
    SELECT office_id 
    FROM office_tb 
    WHERE establish_year >= 1700
);
```
서브쿼리가 1700년 이후에 만들어진 관직 ID 목록(`O105, O109...`)을 뱉어내면, 메인 쿼리가 `IN` 연산자를 통해 그 관직들 중 하나라도 역임한 인물을 중복 없이(`DISTINCT`) 찾아냅니다. 

## 4. 요약

우리는 이제 엑셀의 VLOOKUP 함수의 굴레를 완벽하게 벗어던졌습니다. 
* `"**INNER JOIN**"`으로 흩어진 테이블을 묶어 시계열적인 관역 데이터를 복원했고,
* `"**LEFT JOIN**"`으로 사료에 기록되지 않은 여백(NULL)을 찾아냈으며,
* `"**서브쿼리(Subquery)**"`로 인간의 복잡한 논리적 사고의 흐름을 단 한 번의 쿼리로 구현해 냈습니다.

원시 사료를 구조화하고, 에러를 돌파하며 데이터를 적재한 뒤, 원하는 지식의 조각을 SQL로 완벽하게 추출해 내는 것까지. 데이터베이스 실무의 모든 과정이 끝났습니다. 
이제 이 기나긴 여정의 대미를 장식할 마지막 장인 **[Part 6. 데이터의 개방과 API 서비스]**로 나아가겠습니다. 내 컴퓨터에 갇혀 있는 이 훌륭한 지식베이스를 코딩 한 줄 없이 전 세계의 학자들과 연결하는 `"**Datasette 기반의 REST API 배포 실무**"`를 만나보겠습니다.