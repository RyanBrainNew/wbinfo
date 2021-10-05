# import watchdog
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1.看门狗配置 创建事件处理对象
# patterns = ["*.yml"]   # 监控文件的模式 如果你想监控所有文件，那么设置成"*" 即可
# ignore_patterns = ""       # 设置忽略的文件模式，我这里没有忽略任何文件
# ignore_directories = True  # 是否忽略文件夹变化 设置为True表示忽略文件夹的变化
# case_sensitive = True      # 是否对大小写敏感 如果设置为True，那么修改文件名称时，如果只是大小写发生变化，那么则不会被监控
# event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
event_handler = PatternMatchingEventHandler(patterns=["config.yml"], ignore_patterns="",
                                            ignore_directories=True, case_sensitive=True)


# 2.处理事件 一共有四种事件需要处理，对应的，编写4个函数
# def on_created(event):
#     print(f"{event.src_path}被创建")
#
#
# def on_deleted(event):
#     print(f"{event.src_path}被删除")


def on_modified(event):
    print(f"{event.src_path} 被修改")


# def on_moved(event):
#     print(f"{event.src_path}被移动到{event.dest_path}")


# event_handler.on_created = on_created
#
# event_handler.on_deleted = on_deleted

event_handler.on_modified = on_modified

# event_handler.on_moved = on_moved

# 3.创建观察者，来负责启动监控任务

watch_path = BASE_DIR  # 监控目录

go_recursively = True  # 是否监控子文件夹

my_observer = Observer()

my_observer.schedule(event_handler, watch_path, recursive=go_recursively)

my_observer.start()

try:

    while True:

        time.sleep(1)

except KeyboardInterrupt:

    my_observer.stop()

    my_observer.join()
