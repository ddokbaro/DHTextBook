import os

# 목차 구조 정의 (의미 기반 폴더 및 파일명)
structure = {
    "content/theory": ["dh_history.md", "methodology_shift.md", "critical_dh.md"],
    "content/computing": ["turing_to_pc.md", "bit_and_memory.md", "network_protocols.md"],
    "content/encoding": ["ascii_history.md", "korean_encoding.md", "unicode_utf8.md"],
    "content/regex": ["plain_text.md", "regex_basic.md", "regex_advanced.md"],
    "content/xml": ["xml_fundamentals.md", "tei_guidelines.md", "digital_archives_practice.md"],
    "content/rdb": ["tabular_data.md", "rdb_concept.md", "sql_basic_and_advanced.md"],
    "content/rdf": ["semantic_web.md", "ontology_design.md", "korean_studies_lod.md"],
    "content/stats": ["descriptive_statistics.md", "probability_distributions.md", "eda_with_python.md"],
    "content/text_mining": ["text_mining_flow.md", "morphological_analysis.md", "topic_modeling.md"],
    "content/network": ["network_theory_basics.md", "centrality_and_community.md", "sna_practice.md"],
    "content/spatial": ["gis_fundamentals.md", "spatial_data_mapping.md", "historical_gis_cases.md"],
    "content/visualization": ["efficient_info_vis.md", "python_dataviz_tools.md", "network_and_spatial_vis.md"],
    "content/multimedia": ["3d_modeling_archives.md", "drone_photogrammetry.md"],
    "content/ai_basics": ["ai_paradigm.md", "deep_learning_architecture.md"],
    "content/llm": ["gen_ai_mechanisms.md", "open_source_llm.md"],
    "content/prompting": ["prompt_design_principles.md", "few_shot_and_cot.md"],
    "content/ai_application": ["ai_for_literature_and_emotion.md", "distant_reading_techniques.md", "graph_rag.md"],
    "content/infra": ["cli_linux.md", "git_github.md", "myst_syntax_guide.md", "publish_environment.md"]
}

print("파일 생성을 시작합니다...")

# 폴더 및 빈 Markdown 파일 생성
for folder, files in structure.items():
    os.makedirs(folder, exist_ok=True)
    for file in files:
        file_path = os.path.join(folder, file)
        # 파일이 이미 존재하지 않을 때만 생성 (덮어쓰기 방지)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                # 파일명에서 _를 공백으로 바꾸고, 첫 글자를 대문자로 만들어 기본 제목(#)으로 삽입
                title = file.replace(".md", "").replace("_", " ").title()
                f.write(f"# {title}\n\n내용을 입력하세요.\n")

print("✅ 모든 폴더와 마크다운 파일(총 50여 개)이 성공적으로 생성되었습니다!")