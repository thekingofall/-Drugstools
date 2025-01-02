import os
import sys
import datetime

# def reset_install_time(install_dir, time_file):
#     reset_file = os.path.join(install_dir, "reset_install.txt")

#     if os.path.exists(reset_file):
#         if os.path.exists(time_file):
#             os.remove(time_file)

#         with open(time_file, "w") as f:
#             f.write(str(datetime.datetime.now()))

#         os.remove(reset_file)

#         print("[Info] 检测到 reset_install.txt，已删除旧记录文件并重新计时。")

def check_expiration(minutes=None, days=30):
    # reset_install_time(install_dir, time_file)
    install_dir = os.path.join(os.path.expanduser("~"), ".drugstools")
    time_file = os.path.join(install_dir, "install_time.txt")

    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    

    if not os.path.exists(time_file):
        with open(time_file, "w") as f:
            f.write(str(datetime.datetime.now()))
        return

    with open(time_file, "r") as f:
        saved_time_str = f.read().strip()

    try:
        saved_time = datetime.datetime.strptime(saved_time_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        print("[Error] 安装时间记录文件损坏，请重新下载或重置。")
        sys.exit(1)

    now = datetime.datetime.now()

    if minutes is not None:
        if now > saved_time + datetime.timedelta(minutes=minutes):
            print("[Error] 时间记录文件损坏，请重新下载安装。")
            sys.exit(1)
    else:
        if now > saved_time + datetime.timedelta(days=days):
            print("[Error] 时间记录文件损坏，请重新下载安装。")
            sys.exit(1)
