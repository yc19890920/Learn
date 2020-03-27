1. 连表更新
    - 表间更新
    ```
    UPDATE table_a
    INNER JOIN table_b
    ON table_a.ref_id=table_b.ref_id
    SET table_a.is_show=table_b.is_show
    WHERE table_a.ref_id<6
    ```
    等同于：
    ```
    UPDATE  table_a, table_b
    SET table_a.is_show=table_b.is_show
    WHERE table_a.ref_id=table_b.ref_id AND table_a.ref_id<6
    ```
    - 表内更新
    ```
    UPDATE table_a t1, (
    SELECT address, ref_id, name FROM table_a WHERE ref_id = 1
    ) t2
    SET t1.name=t2.name
    WHERE t1.address=t2.address AND t1.ref_id = 21
    ```

2. 插入更新或者创建
    - INSERT INTO ON DUPLICATE KEY UPDATE 与 REPLACE INTO，两个命令可以处理重复键值问题
    - 前提条件是这个表必须有一个唯一索引或主键。
    #### 1、REPLACE发现重复的先删除再插入，如果记录有多个字段，在插入的时候如果有的字段没有赋值，那么新插入的记录这些字段为空。
    #### 2、INSERT发现重复的是更新操作。在原有记录基础上，更新指定字段内容，其它字段内容保留。
    ### 参考文档： 
    1) [ON DUPLICATE KEY UPDATE](http://www.cnblogs.com/rockee/archive/2012/06/11/2544903.html)
    2) [13.2.5.3 INSERT ... ON DUPLICATE KEY UPDATE Syntax](https://dev.mysql.com/doc/refman/5.7/en/insert-on-duplicate.html)
    ```
    sql = """
    INSERT INTO stat_task_real (customer_id, task_ident, domain, count_send, count_error, count_err_1, count_err_2, count_err_3, count_err_5, created, updated)
        VALUES (%d, '%s', '%s', %d, %d, %d, %d, %d, %d, '%s', '%s')
        ON DUPLICATE KEY UPDATE
                  count_send=count_send + VALUES(count_send),
                  count_error=count_error + VALUES(count_error),
                  count_err_1=count_err_1 + VALUES(count_err_1),
                  count_err_2=count_err_2 + VALUES(count_err_2),
                  count_err_3=count_err_3 + VALUES(count_err_3),
                  count_err_5=count_err_5 + VALUES(count_err_5),
                  updated=VALUES(updated);
    """ % (
        user_id, task_ident, recv_domain,
        count_success + count_error, count_error,
        detail_data['count_err_1'], detail_data['count_err_2'],
        detail_data['count_err_3'], detail_data['count_err_5'],
        now, now
    )
    ```

3. 随机取一行数据的设计
    - 表建索引（random字段建索引）
      `SELECT content FROM table WHERE random>=RAND() ORDER BY random limit 1;`
      
    - rand(), 效率非常低
      `SELECT * FROM table ORDER BY RAND() LIMIT 5`
      
    - 改进rand()
    ```
    SELECT * FROM table 
        WHERE id >= ( 
            SELECT floor( RAND() * ( ( SELECT MAX(id) FROM table )-( SELECT MIN(id) FROM table )) + ( SELECT MIN(id) FROM table ) ) 
        )  
    ORDER BY id LIMIT 1;
    ```
    ```
    SELECT * 
        FROM table AS t1 
    JOIN ( 
        SELECT ROUND( 
            RAND() * ( ( SELECT MAX(id) FROM table )-( SELECT MIN(id) FROM table )) + ( SELECT MIN(id) FROM table) 
        ) AS id
    ) AS t2 
    WHERE t1.id >= t2.id 
    ORDER BY t1.id 
    LIMIT 1;
    ```
    ```
    最后对这两个语句进行分别查询10次，
    前者花费时间 0.147433 秒
    后者花费时间 0.015130 秒
    看来采用JOIN的语法比直接在WHERE中使用函数效率还要高很多。 
    ```
    
4. 删除重复的记录
```
DELETE t1.* FROM table AS t1, (
     SELECT name, COUNT(*), MAX(id) AS id
       FROM table 
     WHERE ref_id=123
     GROUP BY name HAVING COUNT(*)>1
) AS t2
WHERE ref_id=123 AND t1.name = t2.name and t1.id < t2.id;
```
