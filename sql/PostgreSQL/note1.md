
1. distinct 和group by的去重逻辑浅析

> - count(distinct col)
>> select count(distinct col) from A;

> - group+count
>> select count(1) from (select 1 from A group by col) alias;

> - 两中方法实现有什么不同呢？
>> 其实上述两中方法分别是在运算和存储上的权衡。
>> `distinct需要将col列中的全部内容都存储在一个内存中，可以理解为一个hash结构，key为col的值，最后计算hash结构中有多少个key即可得到结果。
很明显，需要将所有不同的值都存起来。内存消耗可能较大。`
`而group by的方式是先将col排序。而数据库中的group一般使用sort的方法，即数据库会先对col进行排序。而排序的基本理论是，时间复杂为nlogn，空间为1.，然后只要单纯的计数就可以了。优点是空间复杂度小，缺点是要进行一次排序，执行时间会较长。`

> - 两中方法各有优劣，具体情况可参考如下法则：

>> | 数据分布	| 去重方式	|  原因 | 
>> | ---	    | ---    	|  ---  | 
>> | 离散	    |  group	| distinct空间占用较大，在时间复杂度允许的情况下，group 可以发挥空间复杂度优势 | 
>> | 集中	    | distinct	| distinct空间占用较小，可以发挥时间复杂度优势 | 

> - 两个极端：
>> 1.数据列的所有数据都一样，即去重计数的结果为1时，用distinct最佳
>> 2.如果数据列唯一，没有相同数值，用group 最好
> 当然，在group by时，某些数据库产品会根据数据列的情况智能地选择是使用排序去重还是hash去重，例如postgresql。


2. INNER JOIN 和 INTERSECT 区别
> INNER JOIN can simulate with INTERSECT when used with DISTINCT. (与 DISTINCT 一起使用时，INNER JOIN 可以与 INTERSECT 达到一样的效果。)
> INNER JOIN 没去重。 INTERSECT 去重。
>> ` SELECT ref_id FROM A INTERSECT SELECT ref_id FROM B `
>> ` SELECT DISTINCT A.ref_id FROM A INNER JOIN B ON A.ref_id=B.ref_id `
> 使用 INTERSECT 时， 会消除运算所产生的重复列。 INTERSECT ALL 回传所有列，包括重复列。


3. in 和 any (values|array)
> - [PostgreSQL in & = any (values|array)  ](http://blog.163.com/digoal@126/blog/static/16387704020149163535754/)

4. 更新或者创建操作
> - INSERT INTO core_address(email, fullname, updated) VALUES (%s, %s, %s) ON conflict (email) do UPDATE SET fullname=excluded.fullname, updated=excluded.updated;
> - args = ( addr, name, now )

5. 查询正在执行的SQL
```
SELECT
    procpid,
    START,
    now() - START AS lap,
    current_query
FROM
    (
        SELECT
            backendid,
            pg_stat_get_backend_pid (S.backendid) AS procpid,
            pg_stat_get_backend_activity_start (S.backendid) AS START,
            pg_stat_get_backend_activity (S.backendid) AS current_query
        FROM
            (
                SELECT
                    pg_stat_get_backend_idset () AS backendid
            ) AS S
    ) AS S
WHERE
    current_query <> '<IDLE>'
ORDER BY
    lap DESC;
```
procpid：进程id
start：进程开始时间
lap：经过时间
current_query：执行中的sql
怎样停止正在执行的sql
SELECT pg_cancel_backend(进程id);
或者用系统函数
kill -9 进程id;