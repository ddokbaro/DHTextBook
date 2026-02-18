import os

# 생성할 컴퓨팅 파트의 파일 목록 (넘버링 완전 제거, 의미 기반)
computing_files = [
    "history_overview.md",    # 2단계: 역사 개괄
    "turing_machine.md",      # 3단계: 튜링 머신
    "von_neumann.md",         # 3단계: 폰 노이만
    "moores_law.md",          # 3단계: 무어의 법칙
    "hardware_overview.md",   # 2단계: 하드웨어 개괄
    "logic_and_bit.md",       # 3단계: 논리 연산과 비트
    "storage.md",             # 3단계: 저장장치
    "gpu.md",                 # 3단계: GPU
    "io_interface.md",        # 3단계: 입출력 장치
    "network_protocols.md"    # 2단계: 네트워크 기초
]

# computing 폴더 생성
os.makedirs("content/computing", exist_ok=True)

# 빈 마크다운 파일 생성
for file_name in computing_files:
    file_path = os.path.join("content/computing", file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        title = file_name.replace(".md", "").replace("_", " ").title()
        f.write(f"---\ntitle: \"{title}\"\n---\n# {title}\n\n이곳에 내용이 작성됩니다.\n")

print("✨ 번호 없는 깔끔한 파일 구조가 성공적으로 생성되었습니다!")