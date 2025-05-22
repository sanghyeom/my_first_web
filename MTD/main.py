from fastapi import FastAPI, Request, Form, Depends , Cookie, Response ,  HTTPException, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import get_db, Base, engine
from models import User, Post

from sqlalchemy.orm import Session 

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/assets"), name="static")

templates = Jinja2Templates(directory="frontend")


# 베이스 페이지 부분
@app.get("/base", response_class=HTMLResponse)
async def base(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# 마이 페이지 부분
@app.get("/mypage", response_class=HTMLResponse)
async def read_mypage( 
    request: Request,
    logged_in: str | None = Cookie(default=None)
):
    is_user_logged_in = logged_in is not None
    user_identification = logged_in if is_user_logged_in else None

    context = {
        "request": request,
        "title": "나의 페이지",
        "is_logged_in": is_user_logged_in,
        "user_identification": user_identification 
    }

    return templates.TemplateResponse("mypage.html", context)

# 게시판 목록 부분
@app.get("/web_board", response_class=HTMLResponse)
async def read_web_board( 
    request: Request,
    db: Session = Depends(get_db),
    logged_in: str | None = Cookie(default=None)
):
    is_user_logged_in = logged_in is not None
    user_identification = logged_in if is_user_logged_in else None

    posts = db.query(Post).all()

    context = {
        "request": request,
        "title": "게시판",
        "is_logged_in": is_user_logged_in,
        "user_identification": user_identification,
        "posts": posts 
    }
    return templates.TemplateResponse("web_board.html", context)

# 게시글 상세 페이지 부분
@app.get("/web_board/{post_id}", response_class=HTMLResponse) 
def show_post_detail(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db),
    logged_in: str | None = Cookie(default=None)
):
    print(f"➡️ 게시글 상세 페이지 요청 - ID: {post_id}, 'logged_in' 쿠키 값: {logged_in}")

    is_user_logged_in = logged_in is not None
    user_identification = logged_in if is_user_logged_in else None

    current_user = None # current_user 변수 초기화

    # ✨✨✨ 여기! 로그인 유저 정보 DB에서 가져오는 코드를 다시 넣어줬어! 👇👇👇 ✨✨✨
    if is_user_logged_in:
        # logged_in 쿠키 값으로 DB에서 유저를 찾아서 current_user에 할당!
        current_user = db.query(User).filter(User.identification == logged_in).first()
    # ✨✨✨ 코드 추가 끝! ✨✨✨


    # 게시글 정보 DB에서 가져오기
    post = db.query(Post).filter(Post.id == post_id).first()

    if post is None:
        print(f"❌ 게시글 ID {post_id}를 찾을 수 없습니다.") # post_id로 수정
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    # ✨✨✨ 디버깅 print 구문들은 유지할게! 👇👇👇 ✨✨✨
    print("\n--- 디버깅 정보 ---")
    print(f"로그인 상태 (is_user_logged_in): {is_user_logged_in}")
    print(f"로그인된 유저 (current_user 객체): {current_user}") # 이제 None이 아닐 수도 있어!
    if current_user:
        print(f"로그인된 유저 ID (current_user.id): {current_user.id}")
    else:
        print("로그인된 유저 ID: N/A")
    print(f"조회하는 게시글 (post 객체): {post}")
    if post:
        print(f"조회하는 게시글 ID (post.id): {post.id}")
        print(f"게시글 작성자 ID (post.author_id): {post.author_id}")
    else:
        print("조회하는 게시글 정보: N/A")
    # 템플릿 조건문 예상 결과
    # post가 None일 경우 post.author_id 접근 시 에러나므로 조건 추가
    template_condition_result = False
    if current_user and post: # current_user와 post 둘 다 객체일 때만 비교 가능
        template_condition_result = current_user.id == post.author_id
    print(f"➡️ 템플릿 조건문 (current_user and current_user.id == post.author_id) 예상 결과: {template_condition_result}")
    print("--------------------\n")
    # ✨✨✨ 디버깅 print 구문 끝! ✨✨✨


    context = {
        "request": request,
        "title": post.title,
        "is_logged_in": is_user_logged_in,
        "user_identification": user_identification,
        "post": post,
        "current_user": current_user # ✨✨✨ 여기! current_user를 context에 추가! 👇👇👇 ✨✨✨
    }

    print(f"✅ 게시글 ID {post.id} 상세 페이지 렌더링 성공.") # post_id로 수정
    return templates.TemplateResponse("web_board_detail.html", context)

# 새 글 작성 페이지 (GET) 부분
@app.get("/web_board_create", response_class=HTMLResponse) 
async def write_post_page(
    request: Request,
    logged_in: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if not logged_in:
        return RedirectResponse(url="/login?next=/web_board_create", status_code=303) 
    
    current_user = db.query(User).filter(User.identification == logged_in).first()
    if not current_user:
        response = RedirectResponse(url="/login?next=/web_board_create", status_code=303)
        response.delete_cookie(key="logged_in")
        return response

    is_user_logged_in = True
    user_identification = current_user.identification

    context = {
        "request": request,
        "title": "새 글 작성",
        "is_logged_in": is_user_logged_in,
        "user_identification": user_identification
    }
    return templates.TemplateResponse("web_board_create.html", context)

# 새 글 작성 처리 (POST) 부분
@app.post("/create_post")
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
    logged_in: str | None = Cookie(default=None)
):
    if not logged_in:
        return RedirectResponse(url="/login?next=/web_board_create", status_code=303)

    user = db.query(User).filter(User.identification == logged_in).first() 
    if not user:
        return RedirectResponse(url="/web_board_create?error=user_not_found", status_code=303)

    try:
        new_post = Post(
            title=title,
            content=content,
            author_id=user.id,
        )
        db.add(new_post)
        db.commit() 
        db.refresh(new_post)

        return RedirectResponse(url="/web_board", status_code=303)

    except Exception as e:
        db.rollback()
        return RedirectResponse(url="/web_board_create?error=save_failed", status_code=303)

@app.delete("/web_board/{post_id}/delete") # DELETE 메서드로 요청 받음
async def delete_post(
    post_id: int, # 삭제할 게시글의 ID를 URL에서 가져옴
    db: Session = Depends(get_db), # DB 세션 의존성 주입
    logged_in: str | None = Cookie(default=None) # 로그인된 유저 identification
):
    print(f"➡️ 게시글 삭제 요청 받음 (DELETE) - 게시글 ID: {post_id}, 'logged_in' 쿠키 값: {logged_in}")

    # 1. 로그인 상태 확인 (로그인 안 했으면 삭제 못 함!)
    if not logged_in:
        print(f"❌ 로그인 안 된 유저가 게시글 {post_id} 삭제 시도!")
        raise HTTPException(status_code=403, detail="로그인이 필요합니다.") # 403 에러 발생

    # 2. 로그인 유저 정보 DB에서 가져오기
    current_user = db.query(User).filter(User.identification == logged_in).first()
    if not current_user:
        print(f"❌ 로그인 쿠키 identification ({logged_in})에 해당하는 유저를 DB에서 찾을 수 없음! (게시글 {post_id} 삭제 시도)")
        raise HTTPException(status_code=403, detail="유효하지 않은 사용자 정보입니다.")

    # 3. 삭제하려는 게시글 정보 DB에서 가져오기
    post_to_delete = db.query(Post).filter(Post.id == post_id).first()

    # 4. 게시글이 존재하는지 확인
    if post_to_delete is None:
        print(f"❌ 게시글 ID {post_id}를 찾을 수 없음! (삭제 시도)")
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    # 5. 작성자 본인인지 확인 (핵심 권한 체크!)
    if post_to_delete.author_id != current_user.id:
        print(f"❌ 유저 {current_user.identification} (ID: {current_user.id})이 게시글 {post_to_delete.id} (작성자 ID: {post_to_delete.author_id}) 삭제 권한 없음!")
        raise HTTPException(status_code=403, detail="게시글 작성자만 삭제할 수 있습니다.")

    # 6. 권한 확인 완료! 게시글 삭제 실행!
    try:
        db.delete(post_to_delete) # DB 세션에서 게시글 객체 삭제
        db.commit() # DB에 변경사항 반영 (실제로 삭제)
        print(f"✅ 게시글 ID {post_id} 삭제 성공! (작성자 ID: {current_user.id})")

        # 7. 삭제 성공 메시지 반환 (JSON 응답)
        return {"message": "게시글 삭제 성공!"} 

    except Exception as e:
        # DB 삭제 중 에러 발생 시 롤백 및 에러 처리
        db.rollback() # 에러 발생 전까지의 변경사항 되돌리기
        print(f"❌ 게시글 ID {post_id} 삭제 중 DB 에러 발생: {e}")
        raise HTTPException(status_code=500, detail="게시글 삭제 중 오류가 발생했습니다.") # 500 에러 발생







# 인덱스 페이지 부분
@app.get("/", response_class=HTMLResponse)
async def read_index(
    request: Request,
    logged_in: str | None = Cookie(default=None)
):
    is_user_logged_in = logged_in is not None
    context = {
        "request": request,
        "title": "나의 여행 기록 플랫폼",
        "is_logged_in": is_user_logged_in,
        "user_identification": logged_in
    }
    return templates.TemplateResponse("index.html", context)

# 로그인 페이지 (GET) 부분
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# 로그인 처리 (POST) 부분
@app.post("/login")
async def login_post(
    identification: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)):

    user = db.query(User).filter(User.identification == identification).first()

    if user and user.password == password:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="logged_in", value=user.identification, httponly=True)
        return response
    else:
        return RedirectResponse("/login?login_failed=true", status_code=303) 

# 로그아웃 처리 부분
@app.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="logged_in")
    return response

# 회원가입 페이지 (GET) 부분
@app.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# 회원가입 처리 (POST) 부분
@app.post("/signup")
async def signup_post(
    identification: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db) 
):
    existing_user = db.query(User).filter(User.identification == identification).first()
    if existing_user:
        return RedirectResponse("/signup?error=id_exists", status_code=303)

    try:
        new_user = User(identification=identification, password=password) 
        db.add(new_user)
        db.commit() 
        db.refresh(new_user)
        return RedirectResponse("/login?signup_success=true", status_code=303) 
    except Exception as e:
        db.rollback() 
        return RedirectResponse("/signup?error=db_save_failed", status_code=303)
