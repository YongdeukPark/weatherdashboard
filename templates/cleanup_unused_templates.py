# 이 파일은 templates 폴더에서 사용하지 않는 파일을 정리하기 위한 스크립트입니다.
# 아래 파일들은 현재 코드에서 사용하지 않으므로 삭제 대상입니다.
# - combined_dashboard.html
# - dashboard.html
# - dashboard_format.png
# - interactive_map_dashboard.html
# - map_dashboard.html

import os

unused_files = [
    'combined_dashboard.html',
    'dashboard.html',
    'dashboard_format.png',
    'interactive_map_dashboard.html',
    'map_dashboard.html',
]

for fname in unused_files:
    path = os.path.join(os.path.dirname(__file__), fname)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted: {fname}")
    else:
        print(f"Not found: {fname}")
