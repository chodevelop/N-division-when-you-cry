import os
from PIL import Image

# 분할할 이미지 파일이 있는 디렉터리 경로
input_folder = os.path.dirname(os.path.abspath(__file__))  # .py 파일이 있는 디렉터리
output_base_folder = os.path.join(input_folder, "output_tiles")

# 가로 cols개, 세로 rows개로 분할
cols, rows = 42, 43  # 예: 3x3 분할. 원하는 값으로 변경 가능

# 디렉터리가 존재하지 않으면 생성
os.makedirs(output_base_folder, exist_ok=True)

# 이미지 cols x rows 분할 함수
def split_image(image_path, output_folder, cols, rows):
    # 이미지 열기
    image = Image.open(image_path)
    width, height = image.size
    
    # 이미지 크기 확인 (cols x rows 조건 만족하지 않을 시 오류 발생)
    if width < cols or height < rows:
        raise ValueError(f"Image {os.path.basename(image_path)} is too small for {cols}x{rows} splitting. Minimum size: {cols}x{rows} pixels.")
    
    # 각 작은 이미지의 크기 계산
    tile_width = width // cols
    tile_height = height // rows

    # cols x rows 그리드로 이미지를 분할하여 저장
    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            upper = row * tile_height
            right = left + tile_width
            lower = upper + tile_height
            
            # 작은 이미지 생성
            cropped_image = image.crop((left, upper, right, lower))

            # RGB 모드로 변환 후 저장 (투명도 제거)
            if cropped_image.mode == "RGBA":
                cropped_image = cropped_image.convert("RGB")
                
            # 파일명 지정 및 저장
            output_image_name = f"tile_{row}_{col}.jpg"
            output_image_path = os.path.join(output_folder, output_image_name)
            cropped_image.save(output_image_path)
            print(f"Saved {output_image_path}")

# 디렉터리 내 모든 jpg 및 png 파일에 대해 cols x rows 분할 수행
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(input_folder, filename)
        
        # 각 파일마다 고유한 폴더 생성
        individual_output_folder = os.path.join(output_base_folder, os.path.splitext(filename)[0])
        os.makedirs(individual_output_folder, exist_ok=True)
        
        # 이미지 분할 수행 (오류 발생 시 예외 처리)
        try:
            split_image(image_path, individual_output_folder, cols, rows)
        except ValueError as e:
            print(e)
