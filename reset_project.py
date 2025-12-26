import os
import shutil

# 1. 뼈대 데이터 정의 (파일명: 제목)
structure = {
    "intro.md": {
        "title": "서문",
        "content": """# 환영합니다!

이 페이지는 **디지털 인문학 교과서**의 온라인 버전입니다.

한국학중앙연구원 디지털 인문학 수업을 위해 제작되었으며, 인문학적 상상력과 디지털 기술의 구현 원리를 통합적으로 학습하는 것을 목표로 합니다.

## 📚 교과서 구성

이 교과서는 크게 세 가지 파트로 구성되어 있습니다.

1.  **기반(Foundations):** 컴퓨팅의 역사와 문자의 디지털 재현
2.  **데이터(Data):** 텍스트의 구조화와 데이터베이스 구축
3.  **분석과 확장(Analysis):** 텍스트 마이닝, 시각화, 그리고 인공지능

:::{note}
이 교과서는 지속적으로 업데이트됩니다.
:::
""",
        "hide_authors": True
    },
    
    # Part 1
    "content/part1_theory/01_dh_history.md": "디지털 인문학의 탄생",
    "content/part1_theory/02_methodology_shift.md": "방법론적 전환: 읽기에서 채굴로",
    "content/part1_theory/03_critical_dh.md": "비판적 디지털 인문학",

    # Part 2
    "content/part2_computing/01_turing_von_neumann.md": "튜링 머신과 폰 노이만",
    "content/part2_computing/02_bit_and_memory.md": "비트와 메모리",
    "content/part2_computing/03_network_web_history.md": "네트워크와 웹의 역사",

    # Part 3
    "content/part3_encoding/01_ascii_history.md": "ASCII와 서구 중심주의",
    "content/part3_encoding/02_korean_encoding.md": "한글 인코딩의 역사",
    "content/part3_encoding/03_unicode_utf8.md": "유니코드(UTF-8)의 원리",

    # Part 4
    "content/part4_regex/01_plain_text.md": "플레인 텍스트의 힘",
    "content/part4_regex/02_regex_basic.md": "정규표현식 기초",
    "content/part4_regex/03_regex_advanced.md": "정규표현식 심화",

    # Part 5
    "content/part5_data/01_tabular_data.md": "표 형식 데이터(CSV)",
    "content/part5_data/02_rdb_concept.md": "관계형 데이터베이스의 이해",
    "content/part5_data/03_sql_basic.md": "SQL 기초",
    "content/part5_data/04_xml_tei.md": "XML과 TEI 마크업",

    # Part 6
    "content/part6_rdf/01_semantic_web.md": "시맨틱 웹과 RDF",
    "content/part6_rdf/02_ontology_design.md": "온톨로지 설계 기초",

    # Part 7
    "content/part7_analysis/01_text_mining_flow.md": "텍스트 마이닝 프로세스",
    "content/part7_analysis/02_topic_modeling.md": "토픽 모델링",
    "content/part7_analysis/03_sna_theory.md": "네트워크 분석 이론",
    "content/part7_analysis/04_gis_spatial.md": "공간 정보와 GIS",

    # Part 8
    "content/part8_ai/01_ai_paradigm.md": "AI 패러다임의 변화",
    "content/part8_ai/02_deep_learning_basics.md": "딥러닝 기초",
    "content/part8_ai/03_gen_ai_llm.md": "생성형 AI와 LLM",

    # Part 9 (내용이 있는 파일들은 별도 처리)
    "content/part9_infra/01_cli_linux.md": "CLI와 리눅스 기초",
    "content/part9_infra/02_web_server_flask.md": "웹 서버 구축",
    "content/part9_infra/03_git_github.md": "Git과 협업",
}

# 2. 내용이 있는 가이드 파일 내용 정의 (Part 9)
guide_publish_content = """## 1. GitHub Actions 배포 설정

이 교과서는 GitHub Actions를 통해 자동으로 배포됩니다. `deploy.yml` 설정이 핵심입니다.

:::{tip}
반드시 `mystmd` 패키지를 설치해야 하며, `BASE_URL` 환경 변수를 저장소 이름에 맞게 설정해야 합니다.
:::
"""

guide_myst_content = """## 1. 텍스트 강조

* **굵게**: `**굵게**`
* *기울임*: `*기울임*`
* `코드`: `` `코드` ``

## 2. 블록 인용 (Admonitions)

:::{note}
이것은 노트입니다.
:::

:::{warning}
이것은 경고입니다.
:::

## 3. 이미지

:::{figure} image.png
:name: my-fig
:width: 80%

캡션 내용
:::
"""

# 3. 초기화 및 생성 로직
def reset_and_build():
    print("🧹 기존 데이터 삭제 중...")
    if os.path.exists("content"):
        shutil.rmtree("content")
        print(" - 'content' 폴더 삭제 완료")
    
    if os.path.exists("intro.md"):
        os.remove("intro.md")
        print(" - 'intro.md' 삭제 완료")

    print("\n🏗️ 파일 재생성 시작 (UTF-8 No-BOM)...")
    
    # 일반 챕터 생성
    for path, data in structure.items():
        # 폴더 생성
        if "/" in path:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # 메타데이터 및 본문 구성
        if isinstance(data, dict): # intro.md 같은 특수 케이스
            title = data["title"]
            body = data["content"]
            hide_opt = "hide:\n  - authors\n  - affiliations\n" if data.get("hide_authors") else ""
        else: # 일반 챕터
            title = data
            body = f"## {title}\n\n::{{note}}\n이 챕터는 아직 작성되지 않았습니다.\n:::\n"
            hide_opt = ""

        # Frontmatter 조립 (빈 줄 없이 완벽하게)
        final_content = f"---\ntitle: {title}\n{hide_opt}---\n\n{body}"

        # 파일 쓰기
        with open(path, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f" - 생성: {path}")

    # 가이드 파일 별도 생성 (내용 채움)
    # 1. 설치/배포 가이드
    pub_path = "content/part9_infra/04_publish_environment.md"
    pub_content = f"---\ntitle: 디지털 출판 환경 구축\n---\n\n{guide_publish_content}"
    with open(pub_path, "w", encoding="utf-8") as f:
        f.write(pub_content)
    print(f" - 생성(내용포함): {pub_path}")

    # 2. MyST 문법 가이드
    myst_path = "content/part9_infra/05_myst_syntax_guide.md"
    myst_content = f"---\ntitle: MyST 문법 가이드\n---\n\n{guide_myst_content}"
    with open(myst_path, "w", encoding="utf-8") as f:
        f.write(myst_content)
    print(f" - 생성(내용포함): {myst_path}")

if __name__ == "__main__":
    reset_and_build()
    print("\n🎉 프로젝트가 완벽하게 초기화되었습니다!")
    print("👉 터미널에서 'myst clean --all' 후 'myst start'를 실행하세요.")