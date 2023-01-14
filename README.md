# fastapi_test
This FastAPI project is for test

### 코딩 컨벤션
- 처음 router의 method 이름을 `signin`, `signup`으로 했지만 이런 경우 일관성을 지키기 어려울 듯 하여 `post_user_signin`과 같이 **http method 명 + method가 어떤 기능을 하는 지를** 나타낼 수 있도록 수정했다.

### 가계부에 들어갈 요소
1. 수입/지출 (amount)
    > 수입과 지출을 같은 컬럼에 두고 +,-로 표기할 지 각자의 컬럼을 갖게 할 지 고민
   - 다른 컬럼: null 값이 많이 생김, 디스크를 많이 차지함
   - 같은 컬럼: sum을 구하거나 할 때 용이
   -> 둘을 같은 컬럼에 두는게 좋을 듯
2. 이름 (item)
3. 메모 (note)
4. event_date (거래 발생 날짜)
5. created_at (ledger 생성 날짜)


### API docs
- Swagger를 적극 활용해 따로 작성할 필요가 없고 서버만 실행 하면 쉽게 확인할 수 있어 용이하다..

### 가계부 API
- 가계부 내역 리스트
- 가계부 내역 생성
- 가계부 내역 수정 `PATCH /ledger/id`
- 가계부 내역 상세 조회 `GET /ledger/id`
- 가계부 내역 삭제 `DELETE /ledger/id`
- 가계부 내역 복제 `POST /ledger/id`
- 가계부 내역 공유 URL -> 토큰 확인