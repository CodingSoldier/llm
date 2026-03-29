from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from a2_sqlalchemy.db_config import get_session
from models import Employee, SexValue
from a3_cudr.schemas.emp import EmpAddReq, EmpAddResp

cudr = APIRouter(prefix='/cudr', tags=['增删改查接口'])


@cudr.post('/employee', response_model=EmpAddResp)
def add_employee(req: EmpAddReq, session: Session = Depends(get_session)):
    """新增员工"""
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
    return EmpAddResp.model_validate(emp)