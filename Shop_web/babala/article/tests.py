import pymysql

# 连接数据库
conn = pymysql.connect(host='localhost', user='root',  database='test_shop', charset='utf8', port=3306)
cursor = conn.cursor()

# 构建 SQL 更新语句
update_query = "UPDATE article_goods SET name = REPLACE(name, '手机_', '数码_') WHERE name LIKE '手机_%%'"

try:
    # 执行 SQL 语句
    cursor.execute(update_query)
    # 提交事务
    conn.commit()
except pymysql.MySQLError as e:
    print(f'Error: {e}')
    # 如果发生错误，回滚事务
    conn.rollback()
finally:
    # 关闭数据库连接
    cursor.close()
    conn.close()