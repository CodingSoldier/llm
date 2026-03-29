from datetime import date
from typing import List, Optional

from certifi import where
from sqlalchemy import String, ForeignKey, create_engine, Table, Column, select, extract, func, desc
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker

from a2_sqlalchemy.a2_cudr import Base, Employee, SexValue
from a2_sqlalchemy.db_config import engine


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


# if __name__ == '__main__':
#     # 创建表
#     Base.metadata.create_all(engine)


if __name__ == '__main__':
    with (sessionmaker(engine).begin() as session):
        # # 新增
        # dept = Dept(name="北京总公司", city="北京")
        # emp1 = Employee(name='aaa', sal=4000, bonus=800, gender=SexValue.MALE, entry_date=date(2019, 10, 23))
        # emp2 = Employee(name='bbb', sal=7000, bonus=900, gender=SexValue.MALE, entry_date=date(2018, 8, 23))
        #
        # # emp1.dept = dept
        # # emp2.dept = dept
        #
        # dept.emp_list = [emp1, emp2]
        #
        # session.add(dept)

        # # 修改：给张三设置一个部门为“北京总公司”
        # emp = session.get(Employee, 2)
        # dept = session.get(Dept, 2)
        # emp.dept_id = dept.id

        # # # 查询
        # dept = session.get(Dept, 2)
        # print(dept.name)
        # #
        # # 查出部门下的所有员工
        # # 懒加载查询
        # for emp in dept.emp_list:
        #     print(emp)

        # 查询员工所在部门的名称
        # emp = session.get(Employee, 2)
        # print(emp.dept.name)

        # 属性结构插入数据
        # d1 = Dept(name="行政部", pid=1, city="北京")
        # d2 = Dept(name="湖南分公司", pid=1, city="长沙")
        # d3 = Dept(name="销售部", pid=d2, city="长沙")
        # session.add(d1)
        # session.add(d2)

        # # 给张三新增一个身份证
        # idc = IdCard(card_number='3456565', emp_id=3)
        # session.add(idc)

        # # 获取员工的身份证号
        # emp = session.get(Employee, 3)
        # print(emp)
        # print(emp.idc.card_number)

        # # 多对多操作
        # u1 = User(username='zs', password="2425345434")
        # u2 = User(username='ls', password="5345434")
        #
        # r1 = Role(name="超管")
        # r2 = Role(name="系统管理员")
        #
        # u1.roles = [r1, r2]
        # u2.roles = [r2]
        #
        # session.add(u1)


        # 关联查询
        # 1、查询2018年入职的员工姓名以及该员工的所在部门名称
        # stmt = select(Employee.name.label("ename"), Dept.name.label('dname')).join(Dept, isouter=True).where(extract("year", Employee.entry_date) == 2018)

        # 2、查询身份证号码是：3456565的员工信息、部门名称
        # stmt = select(Employee.name, Dept.name).join(Dept, isouter=True).join(IdCard).where(IdCard.card_number == "3456565")

        # # 3、查询部门以及部门的员工数量
        # stmt = select(Dept, func.count(Employee.id))\
        #     .join(Employee, isouter=True)\
        #     .group_by(Dept.id)

        # # 查询有超过 1 个角色的用户及其角色数量
        # sub_stmt = select(User.username, func.count(Role.id).label("role_count"))\
        #     .join(User.roles)\
        #     .group_by(User.id)\
        #     .subquery()
        # stmt = select(sub_stmt.c.username, sub_stmt.c.role_count).where(sub_stmt.c.role_count > 1)
        #
        # 统计每个部门的员工数量，并按员工数量从多到少排
        stmt = select(Dept.name, func.count(Employee.id).label("emp_count"))\
            .join(Employee, isouter=True)\
            .group_by(Dept.id)\
            .order_by(desc("emp_count"))

        result = session.execute(stmt)
        for obj in result:
            print(obj[0], obj[1])


