from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker

from a2_sqlalchemy.db_config import engine
from models import Employee, SexValue, Dept, IdCard, User, Role


if __name__ == '__main__':
    # 创建表
    # Base.metadata.create_all(engine)

    with sessionmaker(engine).begin() as session:

        # # 新增数据（一）
        # emp1 = Employee(name='张三', sal=2000, bonus=300, gender=SexValue.MALE, entry_date=date(2019, 10, 23))
        # emp2 = Employee(name='李四', sal=3000, bonus=400, gender=SexValue.MALE, entry_date=date(2019, 10, 24))
        #
        # # session.add(emp1)
        # session.add_all([emp1, emp2])

        # # 新增数据（二）
        # insert_stmt = insert(Employee).values(name="老六", sal=500)
        # session.execute(insert_stmt)


        # # get返回一条数据
        # emp = session.get(Employee, 3)
        # print(emp)

        # # scalars返回的是模型对象
        # stmt = select(Employee)
        # print(type(stmt))
        # list_map = session.scalars(stmt).all()
        # for emp in list_map:
        #     print(type(emp))
        #     print(emp)

        # # 指定返回字段。execute返回的是row对象，row对象相当于是一个字典
        # # key是属性名，value是对应的字段的值
        # stmt = select(Employee.name, Employee.sal, Employee.gender)
        # result = session.execute(stmt).all()
        # for obj in result:
        #     print(type(obj))
        #     print(obj)

        # # 采用原生SQL来查询
        # # 返回指定字段的数据，execute返回的是row对象，row对象相当于是一个字典
        # # key是属性名，value是对应的字段的值
        # sql = text("select id, emp_name, sal, gender from t_emp")
        # result = session.execute(sql).all()
        # for obj in result:
        #     print(type(obj))
        #     print(obj.id, obj.emp_name, obj.sal, obj.gender)

        # # 修改：第一种
        # emp = session.get(Employee, 4)
        # emp.name = "更更高"

        # # 修改：第二种
        # stmt = update(Employee).where(Employee.id == 2).values(name="再找找", sal=111)
        # session.execute(stmt)

        # # 批量修改
        # session.execute(update(Employee), [
        #     {"id": 2, "bonus": 1222},
        #     {"id": 3, "bonus": 1333},
        # ])

        # # 删除：第一种
        # emp = session.get(Employee, 5)
        # session.delete(emp)

        # # 删除：第二种
        # stmt = delete(Employee).where(Employee.id==5)
        # session.execute(stmt)

        # 查询
        # stmt = select(Employee).where(Employee.name == "张三")
        # stmt = select(Employee).where(Employee.name.is_(None))

        # stmt = select(Employee).where(Employee.id.in_([1,2,3,4]))

        # stmt = select(Employee).where(Employee.name.like("%四%"), Employee.sal >= 3000)
        # stmt = select(Employee).where(or_(Employee.name.like("%四%"), Employee.sal <= 3000))
        # result = session.execute(stmt).scalars()
        # for o in result:
        #     print(o)

        # 聚合函数
        # stmt = select(func.avg(Employee.sal))
        # stmt = select(func.count(Employee.id))
        #
        # result = session.execute(stmt).first()
        # print(result)

        # 分页
        # stmt = select(Employee).offset(2).limit(3)
        # stmt = select(Employee).order_by(Employee.sal.desc()).offset(2).limit(3)
        # result = session.execute(stmt).scalars()
        # for o in result:
        #     print(o)

        stmt = select(Employee.gender, func.count(Employee.id)).group_by(Employee.gender)
        result = session.execute(stmt).all()
        for o in result:
            print(o.gender.value, o.count)








