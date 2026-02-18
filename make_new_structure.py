import os

# 생성할 컴퓨팅 파트의 파일 목록 (최종 구조 반영)
computing_files = [
    "01_history_overview.md",
    "01_1_turing.md",
    "01_2_von_neumann.md",
    "01_3_moores_law.md",
    "02_hardware_overview.md",
    "02_1_logic_and_bit.md",
    "02_2_storage.md",
    "02_3_gpu.md",
    "02_4_io_interface.md",
    "03_network_protocols.md"
]

# computing 폴더 생성
os.makedirs("content/computing", exist_ok=True)

# 빈 마크다운 파일 생성
for file_name in computing_files:
    file_path = os.path.join("content/computing", file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        # 파일명 기반으로 임시 제목과 Frontmatter 작성
        title = file_name.replace(".md", "").replace("_", " ").title()
        f.write(f"---\ntitle: \"{title}\"\n---\n# {title}\n\n이곳에 내용이 작성됩니다.\n")

print("✨ 컴퓨팅 파트의 새로운 파일 구조가 성공적으로 생성되었습니다!")