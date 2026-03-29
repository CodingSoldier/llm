from datetime import date
from enum import Enum
from typing import List, Annotated

import pydantic
from fastapi import APIRouter, Path, Body
from fastapi.params import Query
from pydantic import BaseModel, Field, field_validator

a1 = APIRouter(prefix='/a1', tags=['接口a1'])

@a1.get("/get01", summary="get接口")
def get01():
    print("a1111")
    return {"success": True}

@a1.get("/emp/{emp_id}", summary="查询单个员工")
def find_emp(emp_id: int):
    print(f"查询运功emp_id={emp_id}")
    return {"data": emp_id}

@a1.delete("/emp/{emp_id}", summary="删除单个员工")
def del_emp(emp_id: int):
    print(f"删除员工emp_id={emp_id}")
    return {"data": emp_id}

class EmpName(Enum):
    zs = "张三"
    ls = "李四"
    ww = "王五"

@a1.put(path="/emp/{emp_name}", summary="修改单个员工", description='修改单个员工')
def update_emp(emp_name: EmpName = Path(description="参数表示参数表示员工名字，只能是：张三，李四，王五其中之一。")):
    print(f"参数emp_name.name={emp_name.name}")
    print(f"参数emp_name.value={emp_name.value}")
    return {"msg": "ok"}

@a1.get("/emp/query/by", summary="搜索员工")
def emp_query(emp_id: int = Query(default=None, description="员工ID"),
              name: str = Query(default=None, description="员工姓名")):
    print(f"emp_id={emp_id}， name={name}")
    return {"msg": "ok"}

@a1.delete("/emp", summary="批量删除员工",  description="删除员工")
def delete_emp(emp_ids: List[int] = Query(default=[], description="员工ID")):
    print(f"员工ID={emp_ids}")
    return {"msg": "ok"}

@a1.post("/emp", summary="添加员工")
def delete_emp(name: str = Query(description="员工姓名", pattern=r'^[a-zA-Z_]\w{5,15}$'),
               age: int = Query(description="添加员工年龄", ge=3, lt=10)):
    print(name)
    print(age)
    return {"msg": "ok"}

@a1.get("/validate-regex")
async def validate_regex(
    username: Annotated[str, Query(pattern=r"^[a-zA-Z0-9_]{3,20}$", message="用户名必须是3-20位的字母数字下划线")]
):
    print(f"Pydantic 版本: {pydantic.__version__}")
    return {"username": username}


class Address(BaseModel):
    """详细地址"""
    province: str
    city: str
    county: str

class Emp(BaseModel):
    """
    员工请求参数的模型类
    """
    name: str = Field(description='员工的名字')
    age: int = Field(description='员工的年龄', ge=18, lt=60, message="")
    birth: date = Field(description='员工的出生日期', default=None)
    addr: Address = Field(default=None, description='员工的详细地址')

    @field_validator('name')  # 自定义一个复杂校验器，针对哪个字段做校验
    def validate_name(cls, value):
        """
        复杂的校验
        :param value:
        :return:
        """
        import re
        result = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{5,16}$', value)
        assert result is not None
        return value


class Address(BaseModel):
    """ 详细地址 """
    province: str
    city: str
    county: str

class Emp(BaseModel):
    """
    员工请求参数的模型类
    """
    name: str = Field(description="员工的名字")
    age: int = Field(description="员工的年龄", ge=8, lt=60)
    birth: date = Field(description="出生日期", default=None)
    addr: Address = Field(default=None, description="员工的详细地址")

    @field_validator("name")
    def validate_name(cls, value):
        """
        复杂的校验
        """
        import re
        result = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{5,16}$', value)
        assert result is not None
        return value

@a1.post("/emp-add", summary="添加员工")
def create_emp(emp: Emp):
    print(emp)
    return emp

"""
请求体传参：json数据
{
"name": value,
"age": value
}
"""
@a1.post("/test", summary="测试添加员工")
def test(name: str = Body(default=None, description="姓名"),
         age: int = Body(default=18, description="年龄")):
    print(name, age)
    return {"msg": "ok"}



















