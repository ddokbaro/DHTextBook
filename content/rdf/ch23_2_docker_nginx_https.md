---
title: "23.2. Docker 기반 배포 및 Nginx 역방향 프록시/HTTPS 트러블슈팅"
description: "거대한 Wikibase 생태계를 컨테이너 기술인 Docker를 활용해 리눅스 서버에 단숨에 배포하고, Nginx와 Certbot(HTTPS)을 통해 실무 환경에 맞는 안전한 웹 서비스를 개방하는 인프라 구축법을 심층 학습합니다."
---

# 23.2. Docker 기반 배포 및 Nginx 역방향 프록시/HTTPS 트러블슈팅

## 1. 도입: "의존성 지옥(Dependency Hell)"에서 우리를 구원할 마법의 상자

23장의 도입부에서 살펴보았듯, Wikibase는 단일 프로그램이 아닙니다. PHP 기반의 MediaWiki, 관계형 DB인 MariaDB, 시맨틱 엔진인 Blazegraph, 검색 엔진인 ElasticSearch, 캐시 서버인 Redis 등 수많은 소프트웨어가 각자의 버전을 정확히 맞추고 복잡한 포트로 서로 통신해야만 비로소 구동되는 '극악의 난이도'를 자랑합니다.

과거에는 이 6~7개의 거대한 톱니바퀴들을 텅 빈 리눅스 서버에 일일이 수동으로 설치했습니다. MariaDB 버전을 올렸더니 PHP가 뻗고, Java 버전을 바꿨더니 Blazegraph가 죽어버리는 이른바 **'의존성 지옥(Dependency Hell)'** 속에서, 수많은 디지털 인문학 연구실이 인프라 구축의 통곡의 벽을 넘지 못하고 프로젝트를 포기하곤 했습니다. 

하지만 현대 클라우드 인프라 기술의 축복인 **"Docker(도커)"**가 등장하면서 상황은 180도 달라졌습니다.

도커는 이 복잡하고 예민한 프로그램들과 그에 필요한 설정 파일들을 각각 **'컨테이너(Container)'**라는 완벽하게 격리된 가상의 상자에 포장해 둡니다. 우리는 복잡한 설치 과정 없이, 독일 위키미디어 지부가 미리 만들어둔 **설계도(`docker-compose.yml`)** 한 장만 서버에서 실행하면 됩니다. 수 분 만에 거대한 지식 생태계가 톱니바퀴 하나 어긋남 없이 통째로 서버에 띄워집니다.

## 2. 실전 적용 1단계: Wikibase Docker Pipeline 일괄 배포

리눅스(Ubuntu 22.04 LTS 권장) 터미널에 원격 접속하여, 이 웅장한 컨테이너 군단을 소환해 보겠습니다.

### 2.1. Docker 및 Docker Compose 엔진 설치
먼저 텅 빈 서버에 도커 엔진을 설치하고, 켤 때마다 `sudo`를 치는 번거로움을 없애기 위해 권한을 부여합니다.

```bash
# 1. 시스템 패키지 갱신 및 Docker 통합 설치
sudo apt-get update
sudo apt-get install docker.io docker-compose -y

# 2. 서버 재부팅 시 도커 데몬 자동 실행 등록
sudo systemctl enable docker

# 3. 현재 접속 중인 리눅스 유저($USER)에게 도커 제어 권한 부여
sudo usermod -aG docker $USER
```
*(주의: 3번 명령어 실행 후, 터미널 접속을 완전히 끊고(Exit) 다시 SSH로 재접속해야 권한이 정상적으로 적용됩니다.)*

### 2.2. 공식 설계도 다운로드 및 컨테이너 가동
도커가 준비되었다면, Wikibase를 띄우는 것은 명령어 단 세 줄이면 충분합니다.

```bash
# 1. 원하는 경로에 Wikibase를 담을 폴더를 만들고 진입합니다.
mkdir my-wikibase && cd my-wikibase

# 2. 공식 배포판의 설계도(yml)와 환경 변수(env) 파일을 다운로드합니다.
wget [https://raw.githubusercontent.com/wmde/wikibase-release-pipeline/add-wdtk-docker/docker-compose.yml](https://raw.githubusercontent.com/wmde/wikibase-release-pipeline/add-wdtk-docker/docker-compose.yml)
wget [https://raw.githubusercontent.com/wmde/wikibase-release-pipeline/add-wdtk-docker/template.env](https://raw.githubusercontent.com/wmde/wikibase-release-pipeline/add-wdtk-docker/template.env)

# 3. 템플릿 파일의 이름을 시스템이 읽을 수 있도록 숨김 파일(.env)로 변경합니다.
mv template.env .env

# 4. 백그라운드(-d)에서 전체 생태계 컨테이너 군단을 일괄 실행합니다.
docker-compose up -d
```
명령어를 치면 터미널 화면에 수많은 컨테이너 상자들이 다운로드되고 하나씩 `Done` 사인을 띄우는 장관이 펼쳐집니다. 약 5분 정도 시스템이 초기화될 시간을 준 뒤, 브라우저에서 `http://서버IP:8181`에 접속해 보십시오. 감격스럽게도 여러분만의 독립적인 Wikibase 메인 화면이 열릴 것입니다.

## 3. 실전 적용 2단계: Nginx 역방향 프록시와 HTTPS (Certbot)

화면이 떴다고 해서 인프라 구축이 끝난 것이 아닙니다. `http://192.168.x.x:8181` 처럼 IP 주소와 포트 번호가 흉측하게 노출된 시스템은 실무 프로젝트나 공식 서비스로 절대 사용할 수 없습니다. 또한 HTTP 상태에서는 연구원들이 로그인할 때 입력하는 비밀번호가 암호화되지 않고 허공에 뿌려집니다.

이를 해결하기 위해 우리는 **Nginx(엔진엑스)**라는 고성능 웹 서버를 도커 컨테이너 앞단에 세우는 **'역방향 프록시(Reverse Proxy)'** 기술을 적용해야 합니다. Nginx가 문지기 역할을 하며, 깔끔한 도메인(예: `data.koreanstudies.kr`)으로 들어오는 외부 요청을 내부의 8181 포트로 은밀하게 넘겨주는 구조입니다.

### 3.1. Nginx 문지기 설치 및 도메인 연결
```bash
# 1. Nginx 설치
sudo apt-get install nginx -y

# 2. Nginx 설정 파일 생성 및 편집
sudo nano /etc/nginx/sites-available/wikibase
```

에디터가 열리면 아래와 같이 작성합니다. (미리 기관이나 도메인 업체에서 구매한 실제 도메인이 서버 IP와 연결되어 있어야 합니다.)
```nginx
server {
    listen 80;
    server_name data.yourdomain.com; # 여러분이 구매한 실제 도메인 입력

    location / {
        proxy_pass http://localhost:8181; # 도커에서 구동 중인 Wikibase 포트로 패스
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
저장(Ctrl+O) 후 빠져나와(Ctrl+X), 이 설정 파일을 가동 폴더로 심볼릭 링크 처리하고 Nginx를 재시작합니다.
```bash
sudo ln -s /etc/nginx/sites-available/wikibase /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 3.2. Certbot을 이용한 HTTPS(자물쇠 아이콘) 무료 발급
이제 이 도메인에 완벽한 암호화 보안을 씌웁니다. 무료 글로벌 인증 기관인 Let's Encrypt의 도구(Certbot)를 사용합니다.

```bash
# Certbot 패키지 설치
sudo apt-get install certbot python3-certbot-nginx -y

# Nginx 환경을 자동으로 분석하여 HTTPS 인증서를 발급하고 덮어씌우는 마법의 명령어
sudo certbot --nginx -d data.yourdomain.com
```
터미널에서 이메일을 입력하고 약관에 동의(Y)한 뒤, `Redirect` 여부를 묻는 창이 나오면 모든 트래픽을 안전하게 HTTPS로 돌려주는 **2번(Redirect)**을 선택하십시오. 이제 브라우저에 도메인을 치면, 아름다운 자물쇠 아이콘과 함께 완벽하게 암호화된 협업 캔버스가 열립니다.

## 4. 실무 트러블슈팅 (Street-smart Tips)

**시맨틱 아키텍트의 피눈물: "설치했는데 ElasticSearch 컨테이너가 자꾸 혼자 죽습니다!"**

처음 `docker-compose up -d`를 실행한 후, `docker ps` 명령어로 구동 상태를 확인해 보면 다른 건 다 건강하게 켜져 있는데 유독 **`elasticsearch`** 컨테이너만 사라져 있거나 `Exited (78)` 에러를 뿜으며 자꾸 죽는 현상은 거의 100% 발생합니다. 

이로 인해 쿼리는 돌아가지만 검색창에 '이순신'을 쳤을 때 자동완성(Autocomplete)이 먹통이 되는 재앙이 벌어집니다.

**[승리하는 아키텍트의 리눅스 커널(Kernel) 튜닝법]**
ElasticSearch는 방대한 텍스트 색인을 위해 가상 메모리 매핑(mmap)을 엄청나게 많이 생성합니다. 그런데 리눅스 OS는 기본적으로 한 프로그램이 생성할 수 있는 메모리 맵의 한도(max_map_count)를 매우 낮게(보통 65,530) 잡아둡니다. 이 한도에 부딪힌 컨테이너가 질식해서 죽어버리는 것입니다.

도커 내부가 아니라, 리눅스 호스트 서버의 뼈대 설정을 강제로 튜닝해야 합니다.
1. 터미널에서 `sudo nano /etc/sysctl.conf`를 엽니다.
2. 파일의 맨 밑바닥 빈 줄에 **`vm.max_map_count=262144`** 라고 정확히 타이핑하고 저장합니다.
3. 이 변경 사항을 서버 재부팅 없이 즉시 시스템에 꽂아넣기 위해 **`sudo sysctl -p`** 명령어를 실행합니다.
4. 이제 다시 `docker-compose up -d`를 실행하십시오. 질식했던 ElasticSearch가 깊은숨을 내쉬며 안정적으로 구동되는 모습을 볼 수 있습니다.

## 5. 요약

* 복잡하고 예민한 **Wikibase 생태계**는, 각각의 프로그램을 완벽하게 포장해 둔 **Docker Compose** 기술을 활용하여 `yml` 설계도 한 장으로 리눅스 서버에 단숨에 배포할 수 있습니다.
* 실무 서비스 운영을 위해서는 포트 번호 직접 노출을 막는 **Nginx 역방향 프록시**를 구성하고, **Certbot**을 통해 HTTPS 암호화 통신을 구축하여 보안의 벽을 세워야 합니다.
* 컨테이너 일괄 실행 시 반드시 죽어버리는 ElasticSearch 에러를 막으려면, 리눅스 호스트의 **`vm.max_map_count`** 메모리 매핑 값을 대폭 늘려주는 커널 튜닝이 필수적입니다.

이제 모든 인프라 세팅이 끝났습니다. 전 세계 학자들과 연구원들이 여러분의 `data.yourdomain.com`에 접속하여 자유롭게 아이템을 생성할 수 있습니다.

하지만, 이 거대한 생태계 내부에서 데이터가 어떻게 흘러가는지 그 심장부의 비밀을 모르면, 데이터를 입력해도 SPARQL 쿼리 화면에 나오지 않는 재앙을 겪게 됩니다. 다음 장인 **"23.3. 백엔드 동기화 파이프라인: 미디어위키 JSON에서 Blazegraph로의 '먼징(Munging)'"**으로 진입하여, 여러분이 GUI에서 입력한 데이터가 어떻게 실시간으로 W3C 표준 RDF 트리플로 해체되고 동기화되는지 그 내부 아키텍처를 해부해 보겠습니다.