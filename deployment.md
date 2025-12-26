# GitHub Actions를 활용한 Jupyter Book 자동 배포

이 챕터에서는 로컬 컴퓨터에서 매번 빌드할 필요 없이, GitHub에 소스를 올리기만 하면 자동으로 웹사이트를 만들어 배포해주는 **GitHub Actions** 설정 방법을 다룹니다.

특히 최신 **MyST 엔진(v2 이상)**을 사용할 때 자주 발생하는 경로 문제(`BASE_URL`), 실행 파일 오류(`command not found`), 그리고 사이트가 빈 화면으로 나오는 문제(Jekyll 충돌)를 방지하는 **표준 설정**을 안내합니다.

## 1. 프로젝트 설정 파일 준비 (`myst.yml`)

최신 Jupyter Book은 `_config.yml` 대신 **`myst.yml`**을 사용하여 프로젝트를 설정합니다. 배포 시 오류를 막기 위해 **저자 정보**를 상세히 기록해야 합니다.

```yaml
version: 1
project:
  id: dh-textbook
  title: "나의 디지털 인문학 교과서"
  authors:
    # 이름 오류 방지를 위해 given(이름)과 family(성)를 명확히 분리합니다.
    - name:
        given: "바로"
        family: "김"
  toc:
    - file: intro.md
      # 추가 챕터가 있다면 아래 형식으로 추가합니다.
      # - file: deployment.md

site:
  template: book-theme
```

:::{admonition} 주의: 구 버전 파일 삭제
:class: warning
`myst.yml`을 사용할 때 기존의 `_config.yml`이나 `_toc.yml` 파일이 남아있으면 설정 충돌이 발생할 수 있습니다. 반드시 삭제해 주세요.
:::

## 2. GitHub 저장소 권한 설정

GitHub Actions가 배포를 수행할 수 있도록 권한을 열어주어야 합니다.

1. 저장소 상단의 **Settings** 탭을 클릭합니다.
2. 왼쪽 사이드바에서 **Pages** 메뉴를 선택합니다.
3. **Build and deployment** 섹션의 **Source** 항목을 `Deploy from a branch`에서 **`GitHub Actions`**로 변경합니다.

:::{figure} https://docs.github.com/assets/cb-33924/images/help/pages/pages-source-setting-actions.png
:align: center
:width: 80%
:alt: GitHub Pages Source 설정 화면

Source를 반드시 **GitHub Actions**로 변경해야 합니다.
:::

## 3. 배포 스크립트 작성 (`deploy.yml`)

저장소의 `.github/workflows/` 폴더 안에 **`deploy.yml`** 파일을 만들고 아래 내용을 작성합니다.

이 스크립트는 **MyST 엔진(mystmd)**을 올바르게 설치하고, GitHub Pages의 특성(Jekyll)으로 인한 오류를 자동으로 해결합니다.

```yaml
name: deploy-book

# main 브랜치에 푸시(Push)될 때마다 실행
on:
  push:
    branches:
      - main

# GitHub Pages 배포를 위한 권한 설정 (필수)
permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      # 1. Python 설치 (Jupyter Book 의존성)
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      # 2. Node.js 설치 (MyST 엔진 필수 런타임)
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      # 3. 도구 설치
      - name: Install dependencies
        run: |
          pip install jupyter-book
          # [중요] 'myst-cli' 대신 실행 파일이 포함된 'mystmd'를 설치해야 합니다.
          # -g 옵션으로 전역 설치하여 경로 문제를 방지합니다.
          npm install -g mystmd

      # 4. 책 빌드 (HTML 생성)
      - name: Build the book
        run: |
          # [중요] 저장소 이름(예: /DHTextBook)을 BASE_URL로 지정해야 CSS가 깨지지 않습니다.
          # 본인의 저장소 이름에 맞게 수정하세요.
          export BASE_URL="/DHTextBook"
          myst build --html

      # 5. Jekyll 처리 방지 (.nojekyll 생성)
      # GitHub Pages는 기본적으로 언더바(_)로 시작하는 폴더를 무시합니다.
      # 이 파일이 없으면 _static 폴더가 누락되어 사이트 스타일이 깨집니다.
      - name: Disable Jekyll
        run: |
          touch _build/html/.nojekyll

      # 6. 결과물 업로드
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "_build/html"

      # 7. 실제 배포
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## 4. 트러블슈팅 (자주 묻는 질문)

배포 과정에서 오류가 발생할 경우 다음 사항을 확인하세요.

### Q1. `command not found: myst` 오류가 발생합니다.
설치된 패키지 이름을 확인하세요. `npm install myst-cli`로 설치하면 실행 파일이 없을 수 있습니다. 반드시 **`npm install -g mystmd`**를 사용해야 합니다.

### Q2. 배포는 성공했는데 화면 디자인이 깨져서 보입니다.
CSS 파일을 찾지 못하는 문제입니다. `deploy.yml` 파일에서 `export BASE_URL="/저장소이름"` 부분이 정확한지 확인하세요.

### Q3. 사이트에 접속하니 404 오류가 뜹니다.
`_static` 폴더가 GitHub에 의해 숨겨졌을 가능성이 큽니다. 빌드 단계 직후에 `touch .nojekyll` 명령어가 포함되어 있는지 확인하세요.