#!/bin/bash

# 함수 정의: 폴더와 파일을 생성하고 기본 템플릿을 입력함
create_file() {
    DIR_PATH=$1
    FILE_NAME=$2
    TITLE=$3

    # 폴더가 없으면 생성
    mkdir -p "$DIR_PATH"
    
    FULL_PATH="$DIR_PATH/$FILE_NAME"

    # 파일이 없을 때만 생성 (기존 내용 덮어쓰기 방지)
    if [ ! -f "$FULL_PATH" ]; then
        echo "---" > "$FULL_PATH"
        echo "title: $TITLE" >> "$FULL_PATH"
        echo "---" >> "$FULL_PATH"
        echo "" >> "$FULL_PATH"
        echo "## $TITLE" >> "$FULL_PATH"
        echo "" >> "$FULL_PATH"
        echo ":::{note}" >> "$FULL_PATH"
        echo "이 챕터는 아직 작성되지 않았습니다." >> "$FULL_PATH"
        echo ":::" >> "$FULL_PATH"
        echo "✅ 생성완료: $FULL_PATH"
    else
        echo "⚠️ 건너뜀 (이미 존재): $FULL_PATH"
    fi
}

echo "🚀 디지털 인문학 교과서 파일 구조 생성을 시작합니다..."

# 0. 랜딩 페이지
if [ ! -f "intro.md" ]; then
    echo "---" > "intro.md"
    echo "title: 서문" >> "intro.md"
    echo "---" >> "intro.md"
    echo "# 디지털 인문학 교과서에 오신 것을 환영합니다" >> "intro.md"
    echo "✅ 생성완료: intro.md"
fi

# 1. Part 1: 이론
create_file "content/part1_theory" "01_dh_history.md" "디지털 인문학의 탄생"
create_file "content/part1_theory" "02_methodology_shift.md" "방법론적 전환: 읽기에서 채굴로"
create_file "content/part1_theory" "03_critical_dh.md" "비판적 디지털 인문학"

# 2. Part 2: 컴퓨팅 원리
create_file "content/part2_computing" "01_turing_von_neumann.md" "튜링 머신과 폰 노이만"
create_file "content/part2_computing" "02_bit_and_memory.md" "비트와 메모리"
create_file "content/part2_computing" "03_network_web_history.md" "네트워크와 웹의 역사"

# 3. Part 3: 인코딩
create_file "content/part3_encoding" "01_ascii_history.md" "ASCII와 서구 중심주의"
create_file "content/part3_encoding" "02_korean_encoding.md" "한글 인코딩의 역사"
create_file "content/part3_encoding" "03_unicode_utf8.md" "유니코드(UTF-8)의 원리"

# 4. Part 4: 비정형 텍스트
create_file "content/part4_regex" "01_plain_text.md" "플레인 텍스트의 힘"
create_file "content/part4_regex" "02_regex_basic.md" "정규표현식 기초"
create_file "content/part4_regex" "03_regex_advanced.md" "정규표현식 심화"

# 5. Part 5: 구조적 데이터
create_file "content/part5_data" "01_tabular_data.md" "표 형식 데이터(CSV)"
create_file "content/part5_data" "02_rdb_concept.md" "관계형 데이터베이스의 이해"
create_file "content/part5_data" "03_sql_basic.md" "SQL 기초"
create_file "content/part5_data" "04_xml_tei.md" "XML과 TEI 마크업"

# 6. Part 6: 의미망
create_file "content/part6_rdf" "01_semantic_web.md" "시맨틱 웹과 RDF"
create_file "content/part6_rdf" "02_ontology_design.md" "온톨로지 설계 기초"

# 7. Part 7: 분석 방법론
create_file "content/part7_analysis" "01_text_mining_flow.md" "텍스트 마이닝 프로세스"
create_file "content/part7_analysis" "02_topic_modeling.md" "토픽 모델링"
create_file "content/part7_analysis" "03_sna_theory.md" "네트워크 분석 이론"
create_file "content/part7_analysis" "04_gis_spatial.md" "공간 정보와 GIS"

# 8. Part 8: AI
create_file "content/part8_ai" "01_ai_paradigm.md" "AI 패러다임의 변화"
create_file "content/part8_ai" "02_deep_learning_basics.md" "딥러닝 기초"
create_file "content/part8_ai" "03_gen_ai_llm.md" "생성형 AI와 LLM"

# 9. Part 9: 인프라 (기존 파일이 있으면 덮어쓰지 않음)
create_file "content/part9_infra" "01_cli_linux.md" "CLI와 리눅스 기초"
create_file "content/part9_infra" "02_web_server_flask.md" "웹 서버 구축"
create_file "content/part9_infra" "03_git_github.md" "Git과 협업"
create_file "content/part9_infra" "04_publish_environment.md" "디지털 출판 환경 구축"
create_file "content/part9_infra" "05_myst_syntax_guide.md" "MyST 문법 가이드"

echo "🎉 모든 파일 생성이 완료되었습니다!"