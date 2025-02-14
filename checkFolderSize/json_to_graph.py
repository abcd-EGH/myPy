import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from size_to_json import load_filesize_per_dir, WORK_DIR, OUT_DIR, FOLDER_SIZE_JSON_PATH

# 그래프 데이터를 저장할 JSON 파일 경로
PLOT_DATA_JSON_PATH = OUT_DIR / "plot_data.json"

def dump_plot_data(input_json: Path, output_json: Path) -> None:
    """
    폴더 크기 정보를 담은 JSON 파일에서 데이터를 읽어
    그래프를 그리기 위한 데이터를 별도의 JSON 파일로 저장하는 함수입니다.
    input_json: 폴더 크기 정보를 담은 JSON 파일 경로
    output_json: 그래프 데이터를 저장할 JSON 파일 경로
    """
    size_per_path = load_filesize_per_dir(input_json)
    size_per_stem = {Path(path).stem: size for path, size in size_per_path.items() if size > 0}
    plot_data = dict(
        stem=list(size_per_stem.keys()),
        size=list(size_per_stem.values()),
    )

    with open(output_json, "w", encoding="utf-8") as fp:
        json.dump(plot_data, fp, ensure_ascii=False, indent=2)

def load_plot_data(json_path: Path) -> dict[str, list]:
    """
    JSON 파일에서 그래프를 그리기 위한 데이터를 불러오는 함수입니다.
    json_path: JSON 파일 경로
    """
    if json_path.is_file():
        with open(json_path, encoding="utf-8") as fp:
            return json.load(fp)
    return {}

if __name__ == "__main__":
    print(f"{WORK_DIR=}, {OUT_DIR=}, {FOLDER_SIZE_JSON_PATH=}, {PLOT_DATA_JSON_PATH=}")
    
    # 폴더 크기 정보를 담은 파일을 읽어 그래프 데이터를 생성하여 별도 파일에 저장
    dump_plot_data(FOLDER_SIZE_JSON_PATH, PLOT_DATA_JSON_PATH)

    # 그래프 데이터를 불러와서 matplotlib로 시각화
    plot_data = load_plot_data(PLOT_DATA_JSON_PATH)
    sizes = np.array(plot_data["size"])
    stems = np.array(plot_data["stem"])
    
    # 파일 크기를 로그 변환한 값 계산
    log_size = np.log(sizes)
    
    # log_size 기준 내림차순 정렬 (인덱스 역순 정렬)
    sorted_indices = np.argsort(-log_size)
    sorted_log_size = log_size[sorted_indices]
    sorted_stems = stems[sorted_indices]

    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    ax.barh(sorted_stems, sorted_log_size)
    ax.invert_yaxis()  # y축을 반전하여 가장 큰 값이 위에 표시되도록 함.
    ax.grid(True, axis="x")  # 축 그리드
    ax.tick_params(labelbottom=False, length=0, labelsize=15)  # 축 눈금

    fig.set_layout_engine("tight")  # 차트 여백 조정
    fig.savefig(OUT_DIR / f"{Path(__file__).stem}.png")
