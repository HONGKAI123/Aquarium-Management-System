from all_query import query


# select
def select_example(*args):
    """
    print out all data from a table by specific table name
    :param args: table name : str
    :return: list of column name with sql result set
    """
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query = "select * from {0};".format(args[0])

    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'lucifer') as cur:
        cur.execute(sql_query)
        # 获得返回结果
        res = cur.fetchall()

    # 返回 结果和对应的名称
    return ['list', 'all', 'column', 'name', 'from', '*'], res


# update
def update_example(*args):
    """
    update animal status in animal table by animal ID
    :param args: animal ID 'string'
    有其他 input 就继续描述其他变量
    :return: bool:  has any effected row
    """
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query = "UPDATE animal \
    SET status = true \
    WHERE an_ID = {};".format(args[0])

    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'lucifer') as cur:
        cur.execute(sql_query)

        # 提交修改后的语句到数据库
        q.conn.commit()

        # 获取被修改的行数
        res = cur.rowcount

    # 是否有任何数据被修改
    return True if res > 0 else False


# insert
def insert_example(*args):
    """
    insert animal information into animal table
    :param args: animal id:string,
    animal name:string,
    animal species:string,
    curator id:string,
    habitat id:string

    :return: bool: has any effected row
    """
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query = "INSERT INTO animal  \
                VALUES ('{}','{}','{}', 0, '{}','{}'); ".format(args[0],args[1],args[2],args[3],args[4])


    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'lucifer') as cur:
        cur.execute(sql_query)

        # 提交修改后的语句到数据库
        q.conn.commit()

        # 获取被修改的行数
        res = cur.rowcount

    # 是否有任何数据被修改
    return True if res > 0 else False


# delete
def delete_example(*args):
    """
    delete a row from animal by animal id
    :param args: animal id :str
    :return: bool: has any effected row
    """
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query = "DELETE FROM animal \
        WHERE an_ID = '{}';".format(args[0])


    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'lucifer') as cur:
        cur.execute(sql_query)

        # 提交修改后的语句到数据库
        q.conn.commit()

        # 获取被修改的行数
        res = cur.rowcount

    # 是否有任何数据被修改
    return True if res > 0 else False


if __name__ == '__main__':
    table_name = ['animal']
    data_from_select = select_example(*table_name)
    print(data_from_select)

    update_value = [101001]
    update_result = update_example(*update_value)
    print(update_result)

    # [an_ID, name, species, curator,habitat]
    insert_value = ['123456', 'hongkai', 'human', '736289249', '100005']
    insert_result = insert_example(*insert_value)
    print(insert_result)

    delete_value = ['123456']
    delete_result = delete_example(*delete_value)
    print(delete_result)