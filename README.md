微博实时监控脚本
===========================================

[![PyPI version](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)  [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/LICENSE) 

实时关注微博用户动态

特点
====

微博实时监控推送

使用
====

#### 安装方法

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
git clone https://github.com/RyanBrainNew/wbinfo.git
pip3 install requests yaml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### 使用方法

修改util目录下的config.yml配置文件，填入telegram推送id、微信推送id、需要屏蔽过滤的关键词、需要监控的微博用户的uid后，运行weibo.py即可

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
python3 weibo.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#### 定时重启

宝塔或者crontab设置定时任务

注意事项：

1.执行定时任务请把各py文件内的文件路径替换为绝对路径

2.根据实际使用情况，修改monitor.sh中的exec_path等参数

```
crontab -e
*/1 * * * * /root/monitor/monitor.sh
```

记得看日志验证结果

```
tail /var/log/cron
或者
tail /root/cron.log
```
