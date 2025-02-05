from fastapi import HTTPException, Depends,APIRouter,Body,Security,status
from sqlalchemy.orm import Session
# from database import SessionLocal,engine
from models.users import Base, User, Tasks
from schemas.users import UserCreate, UserResponse, TaskCreate, TaskResponse, UserTaskResponse, UserLogin
from typing import List
from sqlalchemy import select, join, update,text
from sqlalchemy.exc import SQLAlchemyError
from scripts.model import get_Query
# from utils.security import create_access_token
from datetime import timedelta
from utils.security import create_access_token,  verify_token 
from utils.security import is_admin
from database import get_db



router = APIRouter() 


#LOGIN

@router.post("/{login}/", tags=["Authentication"])
def user_login(user : UserLogin , db: Session = Depends(get_db)):
    user_new = db.query(User).filter(User.email == user.email).first()
    if not user_new or not user.password == user_new.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Generate JWT Token
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

#Get Query

@router.post("/{get-Query}/", tags=["Query Execution"], dependencies=[Depends(verify_token)])
def get_query(user_prompt: str = Body(...), db: Session = Depends(get_db)):
    try:
        message = get_Query(user_prompt)
        result = db.execute(text(message))
        rows = result.fetchall()
        column_names = result.keys()
        output = [dict(zip(column_names, row)) for row in rows]
        return output
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Query execution failed: {str(e)}")
    


#USERS

# Read all users

USER_TAG = "Users"
@router.get("/{all_users}/", response_model=list[UserResponse], tags=["Users"], dependencies=[Depends(verify_token)])
def read_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/task/{users}/", response_model=UserResponse, tags=["Users"])
def create_users(user: UserCreate, db: Session = Depends(get_db), admin : User =  Depends(is_admin)):
    print(admin.role)
    new_user = User(username=user.username, email=user.email, password=user.password, role = user.role)
    new_user.created_by = admin.id
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    

@router.get("/task/{user_id}/", response_model=UserResponse, tags=["Users"], dependencies=[Depends(verify_token)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/task/{user_id}/", response_model=UserResponse, tags=["Users"])
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), admin = Depends(is_admin)):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.username = user.username
    existing_user.email = user.email
    existing_user.password = user.password
    db.commit()
    db.refresh(existing_user)
    return existing_user

@router.delete("/task/{user_id}/", response_model=dict, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db), admin = Depends(is_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

#TASKS

TASK_TAG = "Tasks"

@router.get("/{all_tasks}", response_model = list[TaskResponse], tags=[TASK_TAG], dependencies=[Depends(verify_token)])
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(Tasks).all()

@router.get("/task/{task_id}", response_model =TaskResponse, tags=[TASK_TAG], dependencies=[Depends(verify_token)])
def get_task(task_id:int, db: Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail ="task not found")
    return task

@router.post("/task/{tasks}", response_model=TaskResponse, tags=[TASK_TAG], dependencies=[Depends(verify_token)])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Tasks(activity = task.activity, Status = task.Status,user_id = task.user_id, isExisted = task.isExisted)
    db.add(new_task)
    try:
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="activity already existed")
    

@router.put("/task/{task_id}", response_model = TaskResponse, tags=[TASK_TAG], dependencies=[Depends(verify_token)])
def update_task(task_id:int, task:TaskCreate, db:Session = Depends(get_db)):
    existing_task = db.query(Tasks).filter(Tasks.id==task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="task not found")
    existing_task.activity = task.activity
    existing_task.Status = task.Status
    existing_task.isExisted = task.isExisted
    db.commit()
    db.refresh(existing_task)
    return existing_task
    

@router.delete("/task/{task_id}", response_model=dict, tags=[TASK_TAG], dependencies=[Depends(verify_token)])
def delete_task(task_id:int, db:Session = Depends(get_db)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    task.isExisted = False
    db.delete(task)
    db.commit()
    return {"message":"task successfully deleted"}

@router.get("/tasks_user/{user_id}", response_model=UserTaskResponse, dependencies=[Depends(verify_token)])
def tasks_by_user_id(user_id: int, db: Session = Depends(get_db)):
    
    stmt = (
        select(User, Tasks)
        .join(Tasks, User.id == Tasks.user_id)
        .filter(User.id == user_id)
    )

    result = db.execute(stmt).all()

    if not result:
        raise HTTPException(status_code=404, detail="User not found or no tasks available")

    user,_= result[0]  

    tasks = [task for _, task in result]


    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "tasks": tasks    
    }



@router.delete("/task_user/{user_id}", dependencies=[Depends(verify_token)])
def delete_tasks_by_user_id(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Tasks).filter(Tasks.user_id == user_id).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="tasks not found for given user_id")
    for task in tasks:
        task.isExisted = False
        db.commit()
    return {"message": f"{len(tasks)} are successfully deleted"}

@router.put("/task_user/{user_id}", dependencies=[Depends(verify_token)])
def update_task(user_id:int,db:Session = Depends(get_db)):
    tasks = db.query(Tasks).filter(Tasks.user_id==user_id).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="user_id not found")
    for task in tasks:
        if(task.Status == "completed"):
            return {"message":"already completed"}
        else:
            task.Status = "completed"
        db.commit()
    return {"message": "status changed to completed"}
