## 1、主从复制节点规划->搭建一主两从三哨兵
容器名称                容器IP地址           映射端口号                 服务运行模式
Redis-master           172.60.0.2         6382 -> 6379              Master
Redis-slave-1          172.60.0.3         6383 -> 6379              Slave1
Redis-slave-2          172.60.0.4         6384 -> 6379              Slave2
Redis-sentinel-1        172.60.0.5         26382 -> 26379            Sentinel1
Redis-sentinel-2        172.60.0.6         26383 -> 26379            Sentinel2
Redis-sentinel-3        172.60.0.7         26384 -> 26379            Sentinel3


## 查看主从信息
$ redis-cli -p 6382
```
127.0.0.1:6382> info
# Server
redis_version:5.0.3
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:8c0bf22bfba82c8f
redis_mode:standalone
os:Linux 4.4.0-139-generic x86_64
arch_bits:64
multiplexing_api:epoll
atomicvar_api:atomic-builtin
gcc_version:8.2.1
process_id:1
run_id:672472ff84b9770612eb8f59007aa292b49dfd8f
tcp_port:6379
uptime_in_seconds:116
uptime_in_days:0
hz:10
configured_hz:10
lru_clock:11624676
executable:/redis-server
config_file:/etc/redis.conf

# Clients
connected_clients:7
client_recent_max_input_buffer:2
client_recent_max_output_buffer:0
blocked_clients:0

# Memory
used_memory:13604696
used_memory_human:12.97M
used_memory_rss:5177344
used_memory_rss_human:4.94M
used_memory_peak:13726512
used_memory_peak_human:13.09M
used_memory_peak_perc:99.11%
used_memory_overhead:13558862
used_memory_startup:790880
used_memory_dataset:45834
used_memory_dataset_perc:0.36%
allocator_allocated:13808392
allocator_active:14196736
allocator_resident:17166336
total_system_memory:8370429952
total_system_memory_human:7.80G
used_memory_lua:37888
used_memory_lua_human:37.00K
used_memory_scripts:0
used_memory_scripts_human:0B
number_of_cached_scripts:0
maxmemory:0
maxmemory_human:0B
maxmemory_policy:noeviction
allocator_frag_ratio:1.03
allocator_frag_bytes:388344
allocator_rss_ratio:1.21
allocator_rss_bytes:2969600
rss_overhead_ratio:0.30
rss_overhead_bytes:-11988992
mem_fragmentation_ratio:0.38
mem_fragmentation_bytes:-8426312
mem_not_counted_for_evict:0
mem_replication_backlog:12582912
mem_clients_slaves:33844
mem_clients_normal:151226
mem_aof_buffer:0
mem_allocator:jemalloc-5.1.0
active_defrag_running:0
lazyfree_pending_objects:0

# Persistence
loading:0
rdb_changes_since_last_save:0
rdb_bgsave_in_progress:0
rdb_last_save_time:1571905649
rdb_last_bgsave_status:ok
rdb_last_bgsave_time_sec:0
rdb_current_bgsave_time_sec:-1
rdb_last_cow_size:430080
aof_enabled:1
aof_rewrite_in_progress:0
aof_rewrite_scheduled:0
aof_last_rewrite_time_sec:-1
aof_current_rewrite_time_sec:-1
aof_last_bgrewrite_status:ok
aof_last_write_status:ok
aof_last_cow_size:0
aof_current_size:0
aof_base_size:0
aof_pending_rewrite:0
aof_buffer_length:0
aof_rewrite_buffer_length:0
aof_pending_bio_fsync:0
aof_delayed_fsync:0

# Stats
total_connections_received:9
total_commands_processed:773
instantaneous_ops_per_sec:7
total_net_input_bytes:36588
total_net_output_bytes:246845
instantaneous_input_kbps:0.31
instantaneous_output_kbps:3.02
rejected_connections:0
sync_full:2
sync_partial_ok:0
sync_partial_err:0
expired_keys:0
expired_stale_perc:0.00
expired_time_cap_reached_count:0
evicted_keys:0
keyspace_hits:0
keyspace_misses:0
pubsub_channels:1
pubsub_patterns:0
latest_fork_usec:177
migrate_cached_sockets:0
slave_expires_tracked_keys:0
active_defrag_hits:0
active_defrag_misses:0
active_defrag_key_hits:0
active_defrag_key_misses:0

# Replication
role:master
connected_slaves:2
slave0:ip=172.60.0.3,port=6379,state=online,offset=22182,lag=1
slave1:ip=172.60.0.4,port=6379,state=online,offset=22317,lag=0
master_replid:67ce2cdc323989eb0b76e14cb8e50a23b5a9d427
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:22317
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:12582912
repl_backlog_first_byte_offset:1
repl_backlog_histlen:22317

# CPU
used_cpu_sys:0.300000
used_cpu_user:0.200000
used_cpu_sys_children:0.000000
used_cpu_user_children:0.000000

# Cluster
cluster_enabled:0

# Keyspace



127.0.0.1:6382> info Replication
# Replication
role:master
connected_slaves:2
slave0:ip=172.60.0.3,port=6379,state=online,offset=12797,lag=0
slave1:ip=172.60.0.4,port=6379,state=online,offset=12797,lag=1
master_replid:67ce2cdc323989eb0b76e14cb8e50a23b5a9d427
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:12797
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:12582912
repl_backlog_first_byte_offset:1
repl_backlog_histlen:12797
```