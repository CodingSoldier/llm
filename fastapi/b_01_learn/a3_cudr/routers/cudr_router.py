from pydoc import describe
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query, Body, Path
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from a2_sqlalchemy.db_config import get_session
from models import Employee, SexValue
from a3_cudr.schemas.emp import EmpAddReq, EmpResp, EmpDeptResp, EmpUpReq

cudr = APIRouter(prefix='/cudr', tags=['增删改查接口'])


@cudr.post('/employee', response_model=EmpResp)
def add_employee(req: EmpAddReq, session: Session = Depends(get_session)):
    """新增员工"""
    db_emp = session.execute(select(Employee).where(Employee.name == req.name)).first()
    if db_emp:
        raise HTTPException(status_code=405, detail="员工姓名已经存在，请修改姓名再提交")

    # 使用 model_dump 将请求数据转换为字典，并添加默认值
    emp_data = req.model_dump()
    
    # 将 gender 字符串转换为 SexValue 枚举
    emp_data['gender'] = SexValue(emp_data['gender'])

    
    # 创建 Employee 实例
    emp = Employee(**emp_data)
    
    # 添加到数据库
    session.add(emp)
    session.commit()
    session.refresh(emp)
    
    # 返回响应，使用 model_validate 方法
    return EmpResp.model_validate(emp)


@cudr.get(path="/emp/detail/{id}", description="查询单个员工", response_model=EmpDeptResp)
def emp_detail(id: int, session: Session=Depends(get_session)):
    db_emp = session.get(Employee, id)
    if db_emp:
        return db_emp
    else:
        raise HTTPException(status_code=401, detail="没有数据")


@cudr.get(path="/page", response_model=List[EmpResp])
def get_page(
        page_index: int = Query(default=1, description="页码"),
        page_size: int = Query(default=10, description="页数"),
        session: Session=Depends(get_session)):
    offset = (page_index - 1) * page_size
    return session.scalars(select(Employee).offset(offset).limit(page_size)).all()


@cudr.put("/emp/update")
def emp_update(
        emp_up: EmpUpReq,
        session: Session = Depends(get_session)):
    # 将请求数据转换为字典
    update_data = emp_up.model_dump(
        exclude_unset=True,
        exclude_none=True
    )
    
    # 如果包含 gender 字段，需要将其转换为 SexValue 枚举
    if 'gender' in update_data:
        update_data['gender'] = SexValue(update_data['gender'])
    
    stmt = update(Employee).where(Employee.id == emp_up.id).values(**update_data)
    session.execute(stmt)
    session.commit()
    return "success"

@cudr.delete(path="/emp/{id}", description="删除员工")
def delete_emp(
        id: int = Path(description="员工id"),
        session: Session = Depends(get_session)):
    session.execute(delete(Employee).where(Employee.id == id))
    session.commit()
    return "success"





