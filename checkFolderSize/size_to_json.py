from pathlib import Path
import json

WORK_DIR = Path(__file__).parent  # 현재 파일의 경로
OUT_DIR = WORK_DIR / 'output'
FOLDER_SIZE_JSON_PATH = OUT_DIR / "folder_sizes.json"  # 폴더 크기 정보를 저장할 JSON 파일

def get_total_filesize(base_dir: Path, pattern: str = "*") -> int:
    """
    파일 크기를 계산하는 함수입니다.
    base_dir: 파일 크기를 계산할 디렉토리
    pattern: 파일 크기를 계산할 파일 패턴 (glob 패턴)
    """
    total_bytes = 0
    for fullpath in base_dir.glob(pattern):
        if fullpath.is_file():
            total_bytes += fullpath.stat().st_size
    return total_bytes

def dump_dirnames(base_dir: Path, json_path: Path) -> None:
    """
    디렉토리 목록을 JSON 파일로 저장하는 함수입니다.
    base_dir: 디렉토리 목록을 저장할 디렉토리
    json_path: JSON 파일 경로
    """
    dirs = []
    for path in base_dir.iterdir():
        if path.is_dir():
            dirs.append(path.as_posix())
    dirs_sorted = sorted(dirs)

    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump(dirs_sorted, fp, ensure_ascii=False, indent=2)

def load_dirnames(json_path: Path) -> list[str]:
    """
    JSON 파일에서 디렉토리 목록을 불러오는 함수입니다.
    json_path: JSON 파일 경로
    """
    if json_path.is_file():
        with open(json_path, encoding="utf-8") as fp:
            return json.load(fp)
    return []

def dump_filesize_from_dirnames(json_path: Path) -> None:
    """
    디렉토리 목록을 기반으로 각 디렉토리의 파일 크기를 계산하여 JSON 파일로 저장하는 함수입니다.
    json_path: JSON 파일 경로
    """
    dirs = load_dirnames(json_path)
    result = {}
    for path_str in dirs:
        path = Path(path_str)
        filesize = get_total_filesize(path, pattern="**/*")
        result[path.as_posix()] = filesize

    # 폴더 용량을 기준으로 내림차순 정렬
    sorted_result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump(sorted_result, fp, ensure_ascii=False, indent=2)

def load_filesize_per_dir(json_path: Path) -> dict[str, int]:
    """
    JSON 파일에서 디렉토리 별 파일 크기를 불러오는 함수입니다.
    json_path: JSON 파일 경로
    """
    if json_path.is_file():
        with open(json_path, encoding="utf-8") as fp:
            return json.load(fp)
    return {}

if __name__ == '__main__':
    print(f"{WORK_DIR=}, {OUT_DIR=}, {FOLDER_SIZE_JSON_PATH=}")
    
    # output 디렉토리 생성 (이미 있으면 무시)
    OUT_DIR.mkdir(exist_ok=True)
    
    # 현재 작업 디렉토리 기준 파일 크기 계산 예시
    base_dir = WORK_DIR
    filesize = get_total_filesize(base_dir, pattern="*")
    print(f"{base_dir.as_posix()=}, {filesize=} bytes")
    
    # 홈 디렉토리의 하위 폴더 목록을 저장한 후, 각 폴더의 파일 크기를 계산하여 저장
    dump_dirnames(Path.home(), FOLDER_SIZE_JSON_PATH)
    dump_filesize_from_dirnames(FOLDER_SIZE_JSON_PATH)
