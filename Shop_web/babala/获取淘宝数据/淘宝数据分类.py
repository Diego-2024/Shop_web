import pymysql
connection = pymysql.connect(host='localhost', user='root', database='test_shop', port=3306)


new_subcat_id = 4  # 以实际 ID 值替换

try:
    # 执行原生 SQL 更新语句
    with connection.cursor() as cursor:
        # 替换 'your_subcat_table_name' 为实际的 SubCat 表名
        update_query = """
        UPDATE article_goods
        SET supercat_id = %s
        WHERE name LIKE CONCAT('家电', '%%');
        """
        cursor.execute(update_query, (new_subcat_id,))


    # 如果使用 Django 的事务管理，通常不需要手动提交，Django 会在事务结束时自动提交。
    # 但是，如果你直接使用 pymysql 并且需要确保事务被提交，可以使用以下命令：
    connection.commit()  # 请注意，这可能不适用于所有 Django 版本。


finally:
    # 关闭数据库连接
    connection.close()

