from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS 설정: 구글 앱스 스크립트 등 외부 도메인에서의 API 접근을 허용합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    array: list[int]
    target: int

@app.post("/binary-search")
def binary_search(req: SearchRequest):
    # 이진 검색은 정렬된 데이터에서만 가능하므로 먼저 오름차순 정렬을 수행합니다.
    sorted_arr = sorted(req.array)
    target = req.target
    
    steps = []
    count = 0
    left = 0
    right = len(sorted_arr) - 1
    found_index = -1

    # 왼쪽 포인터가 오른쪽 포인터보다 커질 때까지 반복
    while left <= right:
        count += 1
        mid = (left + right) // 2  # 중간 인덱스 계산
        mid_val = sorted_arr[mid]
        
        is_match = (mid_val == target)
        
        # 클라이언트 시각화를 위해 현재 탐색 범위를 저장
        steps.append({
            "step": count,
            "left": left,
            "right": right,
            "mid": mid,
            "mid_val": mid_val,
            "match": is_match
        })

        if is_match:
            found_index = mid
            break
        elif mid_val < target:
            left = mid + 1  # 타겟이 더 크면 탐색 범위를 오른쪽 절반으로 축소
        else:
            right = mid - 1 # 타겟이 더 작으면 탐색 범위를 왼쪽 절반으로 축소

    return {
        "original_array": req.array,
        "sorted_array": sorted_arr, # 정렬된 배열을 프론트엔드로 전달
        "steps": steps,
        "count": count,
        "complexity": "$O(\\log N)$", # 이진 검색의 최악 시간 복잡도
        "found_index": found_index
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
