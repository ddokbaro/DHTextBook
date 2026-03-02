---
title: "22.1. Neo4j 데이터베이스 인프라 구축 및 Cypher 질의어 기초"
description: "산업계 표준 속성 그래프인 Neo4j를 우분투 리눅스(Ubuntu Linux) 서버에 완벽하게 안착시키고, 아스키 아트(ASCII Art) 철학을 담은 질의어 사이퍼(Cypher)의 문법적 구조를 상세히 해부합니다."
---

# 22.1. Neo4j 데이터베이스 인프라 구축 및 Cypher 질의어 기초

## 1. 도입: 관계(Relationship)를 '1급 시민'으로 대접하는 데이터베이스

우리는 지금까지 W3C 표준인 RDF(Resource Description Framework)를 통해 지식을 '주어-서술어-목적어'의 트리플(Triple) 단위로 쪼개는 엄밀함을 배웠습니다. 하지만 대규모 인물 네트워크나 복잡한 문헌 전승 계보를 다룰 때, 실무 아키텍트들은 종종 답답함을 느낍니다. 

**"A가 B에게 편지를 보냈다(A -> sent_letter_to -> B)"**라는 관계가 있을 때, 그 편지를 보낸 '날짜', '장소', '내용'을 화살표 자체에 기록하고 싶다면 어떻게 해야 할까요? RDF에서는 이를 표현하기 위해 화살표 자체를 다시 노드로 만드는 '구체화(Reification)'라는 끔찍하고 복잡한 우회로를 거쳐야 합니다.

이때 등장하는 **Neo4j(네오포제이)**는 **"관계(Relationship)를 데이터의 1급 시민(First-class Citizen)으로 대접한다"**는 철학을 가진 **속성 그래프(Property Graph)** 엔진입니다. 관계를 나타내는 화살표 위에 수십, 수백 개의 속성(Property)을 포스트잇처럼 직접 붙일 수 있는 이 유연한 산업계 표준 엔진을 우리 리눅스 서버에 완벽하게 안착시켜 보겠습니다.

## 2. 실전 적용 1단계: Neo4j 서버 인프라 구축의 정석

리눅스(Ubuntu 22.04 LTS 권장) 터미널에서 설치를 진행합니다. Neo4j는 매우 무겁고 예민한 Java 애플리케이션이므로, 뼈대를 세우는 과정부터 엄격한 절차를 밟아야 합니다.

### 2.1. 기반 환경 조성 (Java 17 설치)
Neo4j 5.x 최신 버전은 구형 Java(8, 11)에서는 아예 구동되지 않으며, 반드시 **Java 17** 환경을 요구합니다. (21장에서 Apache Jena를 위해 설치했던 Java 11과 충돌하지 않도록 주의합니다.)

```bash
# 1. 시스템 패키지 목록을 최신화합니다.
sudo apt-get update

# 2. OpenJDK 17을 설치합니다.
sudo apt-get install openjdk-17-jdk -y

# 3. 설치된 버전을 확인합니다. (openjdk version "17.0.x" 출력을 반드시 확인!)
java -version
```

### 2.2. GPG 키 등록 및 공식 레포지토리(Repository) 추가
우분투의 기본 저장소에 있는 Neo4j는 버전이 너무 낮습니다. 따라서 Neo4j 공식 서버에서 직접 최신 패키지를 끌어올 수 있도록 통로를 개척해야 합니다.

```bash
# 1. 패키지의 위변조를 막기 위한 Neo4j 공식 GPG 인증키를 서버에 등록합니다.
wget -O - [https://debian.neo4j.com/neotechnology.gpg.key](https://debian.neo4j.com/neotechnology.gpg.key) | sudo apt-key add -

# 2. 우분투의 소스 리스트(sources.list.d)에 Neo4j 공식 저장소 주소를 영구적으로 기입합니다.
echo 'deb [https://debian.neo4j.com](https://debian.neo4j.com) stable 5' | sudo tee -a /etc/apt/sources.list.d/neo4j.list

# 3. 저장소 목록을 갱신하고 대망의 Neo4j를 설치합니다.
sudo apt-get update
sudo apt-get install neo4j -y
```

### 2.3. 서비스 데몬(Daemon) 등록 및 구동
설치된 Neo4j를 리눅스의 시스템 데몬으로 등록하여, 서버가 재부팅되어도 자동으로 켜지도록 설정합니다.

```bash
# 서버 부팅 시 Neo4j 자동 실행 등록
sudo systemctl enable neo4j

# Neo4j 엔진 즉시 가동
sudo systemctl start neo4j

# 구동 상태 확인 (초록색으로 'active (running)'이 뜨면 성공입니다)
sudo systemctl status neo4j
```

## 3. 실전 적용 2단계: 서버 통로 개방과 환경 설정 (`neo4j.conf`)

Neo4j가 돌고 있어도, 이 상태로는 외부(연구실 PC)에서 절대 접속할 수 없습니다. 철저한 보안을 위해 기본적으로 서버 내부(`localhost`) 접속만 허용되어 있기 때문입니다. 설정 파일의 심장부를 건드려야 합니다.

```bash
# 리눅스 텍스트 에디터(nano)로 설정 파일을 엽니다.
sudo nano /etc/neo4j/neo4j.conf
```

편집기가 열리면 화살표 키로 이동하며 다음 항목들을 찾아 주석(`#`)을 해제하고 값을 수정합니다.

1. **외부 접속 허용 (Listen Address)**
   * `server.default_listen_address=0.0.0.0` (이 한 줄의 주석을 푸는 순간, 전 세계의 IP에서 여러분의 서버로 들어올 수 있는 논리적 문이 열립니다.)
2. **웹 브라우저 포트 개방 (HTTP/HTTPS)**
   * `server.http.enabled=true`
   * `server.http.listen_address=:7474` (GUI 화면 접속용 포트입니다.)
3. **데이터 통신 포트 개방 (Bolt)**
   * `server.bolt.enabled=true`
   * `server.bolt.listen_address=:7687` (파이썬 등 외부 프로그램이 쿼리를 날릴 때 쓰는 고속 통신 포트입니다.)

설정을 저장(Ctrl+O, Enter)하고 빠져나온(Ctrl+X) 뒤, 방화벽을 열고 서버를 재시작합니다.
```bash
# 우분투 방화벽(UFW)에서 7474, 7687 포트 개방
sudo ufw allow 7474/tcp
sudo ufw allow 7687/tcp

# 변경된 설정 적용을 위해 Neo4j 재시작
sudo systemctl restart neo4j
```

## 4. 실전 적용 3단계: Cypher 질의어의 '아스키 아트' 문법 해부

이제 크롬 브라우저를 열고 `http://여러분의_서버_IP:7474`로 접속합니다. 초기 ID/비밀번호인 `neo4j/neo4j`를 입력하고 새 비밀번호를 설정하면, 화려한 Neo4j Browser 시각화 캔버스가 나타납니다.

Neo4j를 다루는 언어인 **Cypher(사이퍼)**는 기계를 위한 언어가 아니라, 인간이 화이트보드에 동그라미와 선을 그리는 행위를 텍스트로 옮긴 **"아스키 아트(ASCII Art)"** 철학의 결정체입니다.

상단 입력창에 다음의 쿼리를 순서대로 입력하며 문법을 해부해 보겠습니다.

### 4.1. 노드(Node)의 생성과 묘사
노드는 둥그니까 소괄호 `()`로 표현합니다.

```cypher
// 변수(p1), 라벨(Person), 속성(name, role)을 정의하여 생성합니다.
CREATE (p1:Person {name: "유성룡", role: "영의정"})
CREATE (p2:Person {name: "이순신", role: "삼도수군통제사"})
```

### 4.2. 관계(Relationship)의 생성과 묘사
화살표는 실선 `--`과 꺾쇠 `>`를 조합하고, 그 안의 관계명은 각지니까 대괄호 `[]`로 표현합니다.

```cypher
// 유성룡(p1)에서 이순신(p2)으로 이어지는 화살표를 그리고, 그 화살표 위에 'since'라는 포스트잇을 붙입니다.
MATCH (p1:Person {name: "유성룡"}), (p2:Person {name: "이순신"})
CREATE (p1)-[:RECOMMENDED {since: 1591, reason: "탁월한 무공"}]->(p2)
```

### 4.3. 패턴 매칭(Pattern Matching)을 통한 탐색
SPARQL의 `WHERE` 절에 해당하는 것이 Cypher의 `MATCH`입니다. 그림을 그리듯 원하는 패턴을 입력하면 기계가 찾아냅니다.

```cypher
// "유성룡이 천거한(RECOMMENDED) 모든 사람(target)을 찾아서, 그 사람의 이름과 천거 연도를 출력하라"
MATCH (source:Person {name: "유성룡"})-[rel:RECOMMENDED]->(target:Person)
RETURN target.name AS 추천받은자, rel.since AS 추천연도
```

## 5. 실무 트러블슈팅 (Street-smart Tips)

**시맨틱 아키텍트의 피눈물: "서버가 시작되자마자 죽어버립니다 (Port Conflict)"**

21장에서 Virtuoso나 다른 웹 서버를 띄워놓은 상태에서 Neo4j를 설치했을 때 100% 발생하는 **포트 충돌(Port Conflict)** 현상입니다. 리눅스에서는 한 포트(문)를 두 프로그램이 동시에 쓸 수 없습니다.

**[승리하는 아키텍트의 해결책]**
터미널에서 `sudo netstat -tulpn | grep 7474`를 쳐서 누가 해당 포트를 점유하고 있는지 확인하십시오. 만약 겹친다면, `neo4j.conf`에서 과감하게 포트를 피신시켜야 합니다.
`server.http.listen_address=:17474`
`server.bolt.listen_address=:17687`
이렇게 포트를 바꾼 뒤, 방화벽(UFW)도 17474번을 새로 열어주면 평화롭게 두 엔진을 한 서버에서 돌릴 수 있습니다.

**시맨틱 아키텍트의 건망증: "비밀번호를 잃어버렸습니다. 재설치해야 합니까?"**

초기 접속 시 억지로 비밀번호를 바꾸게 만들다 보니, 대충 입력했다가 다음 날 접속을 못 해 발을 동동 구르는 연구원들이 많습니다.

**[승리하는 아키텍트의 권한 초기화법]**
절대 재설치하지 마십시오. 리눅스 시스템 관리자는 물리적 파일에 접근할 수 있습니다.
터미널에서 `sudo rm /var/lib/neo4j/data/dbms/auth` 명령어로 인증(Auth) 파일을 날려버리십시오. 그리고 `sudo systemctl restart neo4j`로 재시작하면, 다시 초기 계정인 `neo4j/neo4j`로 접속하여 새 생명을 얻을 수 있습니다.

## 6. 요약 및 다음 단계

* **Neo4j**는 관계의 풍부함을 직관적으로 담아내는 속성 그래프 엔진으로, 리눅스 서버에 안착시키기 위해서는 **Java 17 환경 구축**과 **GPG 인증** 등 체계적인 인프라 설계가 필요합니다.
* **`neo4j.conf`** 수정은 Neo4j를 개인용 프로그램에서 글로벌 서버로 탈바꿈시키는 핵심 관문이며, 외부 접속 허용(`0.0.0.0`)과 포트 튜닝이 필수적입니다.
* **Cypher** 질의어는 `()`와 `[]`, `->`를 이용해 화이트보드에 그림을 그리듯 노드와 관계를 선언하는 직관적인 아스키 아트 문법을 제공합니다.

기초 공사와 언어 습득이 끝났습니다. 이제 이 텅 빈 캔버스에 수백만 개의 데이터를 쏟아붓고 연산할 차례입니다.

다음 장인 **"22.2. 대규모 네트워크 탐색(Traversal)과 Graph Data Science (GDS) 알고리즘 적용"**으로 대망의 진입을 하여, 우리가 만든 서버의 한계를 시험하고 역사적 인물들의 권력 지도를 수학적으로 그려내는 짜릿한 데이터 과학의 세계를 열어보겠습니다!