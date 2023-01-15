### 구현 내역
1. O
2. O
3. 
    1. O
    2. O
    3. O
    4. O
    5. O
    6. O
    7. O


### 고민한 부분들
- 수입과 지출을 같은 컬럼에 두고 +,-로 표기할 지 각자의 컬럼을 갖게 할 지 고민
   - 다른 컬럼: null 값이 많이 생김, 디스크를 많이 차지함
   - 같은 컬럼: sum을 구하거나 할 때 용이
   -> 둘을 같은 컬럼에 두는게 좋을 듯
- 처음 router의 method 이름을 `signin`, `signup`으로 했지만 
이런 경우 일관성을 지키기 어려울 듯 하여 `post_user_signin`과 같이 **http method 명 + method가 어떤 기능을 하는 지를** 나타낼 수 있도록 수정했다.
- ledger는 장부란 뜻이 있기 때문에 router을 ledger로 지었지만 
거래내역을 CRUD하는 경우 ledger란 단어는 어울리지 않는다고 생각했다.
그래서 `/ledger/transaction/{transaction_id}`와 같이 transaction이 ledger에 속하게끔 수정했다.
table 명의 경우 Ledger이기 때문에 의미적으론 맞지만 Ledger 각 row들은 ledger가 아닌 transaction이므로 
Ledger 객체를 반환시 이름이 서로 맞지 않는 문제가 있다.  
- 가계부 내역 삭제 기능의 경우 복수의 내역을 삭제할 수 있는 API가 사용자 편의를 위해 좋은 방법이라고 생각했다.
그래서 body에 넣어진 복수의 id를 이용해 삭제하게끔 하였는데 http method 중 `DELETE`를 쓰는 경우 body에 데이터를 
넣지 못하는 HTTP client도 있기 때문에 고민이 됐다.
그래서 결국 `PATCH` method를 사용했는데 이는 구현한 삭제가 컬럼의 boolean 값을 바꾸는 soft delete 여서 `PATCH`의 의미에 어느정도 부합하기 때문이다. 


### API docs
- Swagger를 적극 활용해 따로 작성할 필요가 없고 서버만 실행 하면 쉽게 확인할 수 있어 용이하다.


### 서버 실행 방법
```shell
# 가상환경 실행 
pip install -r requirements.txt
uvicorn main:app
```