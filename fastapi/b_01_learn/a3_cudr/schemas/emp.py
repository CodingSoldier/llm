from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class EmpAddReq(BaseModel):
    """新增员工请求模型"""
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(description="员工姓名")
    sal: float = Field(description="员工基本工资", alias="salary")
    bonus: int = Field(default=0, description="员工津贴和奖金")
    is_leave: bool = Field(default=False, description="员工是否离职")
    gender: str = Field(default="男", description="员工性别", pattern="^(男 | 女)$")
    entry_date: date = Field(description="入职日期")


class EmpResp(BaseModel):
    """新增员工响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(description="员工 ID")
    name: str = Field(description="员工姓名")
    sal: float = Field(description="员工基本工资")
    bonus: int = Field(description="员工津贴和奖金")
    is_leave: bool = Field(description="员工是否离职")
    gender: str = Field(description="员工性别")
    entry_date: date = Field(description="入职日期")

class DeptResp(BaseModel):
    """部门响应体"""
    id: int = Field(description="部门的id")
    name: str = Field(description="部门名称")
    city: str = Field(description="所在城市")


class EmpDeptResp(EmpResp):
    """员工、部门信息"""

    model_config = ConfigDict(from_attributes=True)

    dept_id: Optional[int] = Field(description="员工的部门id")

    dept: Optional[DeptResp] = Field(description="部门信息")

class EmpUpReq(BaseModel):
    """员工更新"""
    id: int = Field(description="员工 ID")
    name: str = Field(description="员工姓名")
    sal: float = Field(description="员工基本工资")
    bonus: int = Field(description="员工津贴和奖金")
    is_leave: bool = Field(description="员工是否离职")
    gender: str = Field(description="员工性别", pattern="^男$|^女$")
    entry_date: date = Field(description="入职日期")

