from sqlalchemy import select, func, desc
from sqlalchemy.orm import sessionmaker

from a2_sqlalchemy.db_config import engine
from models import Dept, Employee

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


