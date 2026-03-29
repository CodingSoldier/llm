"""
SQLAlchemy 模型定义模块
包含所有数据库模型类：Employee, Dept, IdCard, User, Role
"""
import enum
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import DateTime, String, DECIMAL, Boolean, func, select, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy.orm import Mapped, mapped_column

from a2_sqlalchemy.db_config import engine


class Base(DeclarativeBase):
    """所有模型类的基类"""
    # 所有的模型类，都有的属性和字段映射
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), comment='记录的创建时间')
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), onupdate=func.now(), comment='记录的最后一次修改时间')


class SexValue(enum.Enum):
    """通过枚举，可以给一些属性（字段）设置预设值"""
    MALE = '男'
    FEMALE = '女'


class Employee(Base):
    """员工的模型类"""

    __tablename__ = 't_emp'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), name='emp_name', unique=True, nullable=False)

    # DECIMAL 其中 10 代表总位数，2 代表小数点后的位数
    sal: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True, comment='员工的基本工资')
    bonus: Mapped[int] = mapped_column(default=0, comment='员工的津贴和奖金')
    is_leave: Mapped[bool] = mapped_column(Boolean, default=False,
                                           comment='员工是否离职，True 代表已经离职，False 代表在职')
    gender: Mapped[SexValue]
    entry_date: Mapped[date] = mapped_column(insert_default=func.now(), nullable=False, comment='入职时间')

    # 和部门表关联的外键
    dept_id: Mapped[Optional[int]] = mapped_column(ForeignKey('t_dept.id'), nullable=True)
    # 定义一个关联属性：该员工所属的部门
    dept: Mapped[Optional['Dept']] = relationship(back_populates='emp_list', cascade='save-update')

    # 定义一个和身份证关联的属性：idc
    idc: Mapped[Optional['IdCard']] = relationship(back_populates='emp')

    def __str__(self):
        return f'{self.name}, {self.gender.value}, {self.sal}, {self.entry_date}, {self.bonus}'


class Dept(Base):
    """部门的模型类"""
    __tablename__ = 't_dept'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), name='dname', unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(50))

    # 定义一个关联属性：一个部门下的所有员工
    emp_list: Mapped[List['Employee']] = relationship(back_populates='dept', cascade='save-update')

    # 定义一个外键：关联到父机构
    pid: Mapped[Optional[int]] = mapped_column(ForeignKey('t_dept.id'), nullable=True)

    # 定义一个关联属性
    children: Mapped[List['Dept']] = relationship(back_populates='parent')
    # 定义一个关联属性
    parent: Mapped[Optional['Dept']] = relationship(back_populates='children', remote_side=[id])

    def __str__(self):
        return f'{self.name}, {self.id}, {self.city}'


class IdCard(Base):
    """身份证的模型类，它和员工之间是一对一的关联关系"""
    __tablename__ = 't_id_card'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    card_number: Mapped[str] = mapped_column(String(18), unique=True, nullable=False, comment='身份证号码')
    origin: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment='籍贯')

    emp_id: Mapped[int] = mapped_column(ForeignKey('t_emp.id'), comment='emp_id')

    # 一对一的关联属性
    emp: Mapped['Employee'] = relationship(single_parent=True, back_populates='idc')


# 多对多关联，先定义中间表
middle_table = Table(
    't_user_role',
    Base.metadata,
    Column('user_id', ForeignKey('t_user.id'), primary_key=True),
    Column('role_id', ForeignKey('t_role.id'), primary_key=True)  # 联合主键
)


class User(Base):
    """用户模型类，它和角色之间是多对多关联"""
    __tablename__ = 't_user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, comment='用户名')
    password: Mapped[str] = mapped_column(String(20), nullable=False, comment='密码')

    # 多对多的关联属性
    roles: Mapped[Optional[List['Role']]] = relationship(secondary=middle_table, back_populates='users')


class Role(Base):
    """角色模型类，它和用户之间是多对多关联"""
    __tablename__ = 't_role'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, comment='角色名字')

    # 多对多的关联属性
    users: Mapped[Optional[List['User']]] = relationship(secondary=middle_table, back_populates='roles')
