import os
import glob

app_name = "soso"
dir_name = os.getcwd() + "/"
build_dir_name = os.getcwd() + "/build/lib.linux-x86_64-3.6/"
useless_files = []

app_path = dir_name + app_name
# 如果源码为客户私有部署的，可以把.git文件也清理了
useless_files += glob.glob(app_path + "/*.py")
useless_files += glob.glob(app_path + "/*.c")
useless_files += glob.glob(app_path + "/*.so")
for useless_file in useless_files:
    try:
        os.remove(useless_file)
        print("Delete: " + useless_file)
    except BaseException:
        print(useless_file + "not exsit")

builded_app_path = build_dir_name + app_name
os.system("cp " + builded_app_path + "/* " + app_path)
print("Copy: " + builded_app_path + "/* TO " + app_path)

print("All done!")
