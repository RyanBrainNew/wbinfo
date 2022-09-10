#! /bin/sh

host_dir=`echo ~`                                       # 当前用户根目录
proc_name="weibo.py"                                    # 进程名
file_name="/cron.log"                                   # 日志文件
exec_path="/home/pi/weibo"                              # 执行路径
pid=0

proc_num()                                              # 计算进程数
{
	num=`ps -ef | grep $proc_name | grep -v grep | wc -l`
	return $num
}

proc_id()                                               # 进程号
{
	pid=`ps -ef | grep $proc_name | grep -v grep | awk '{print $2}'`
}

proc_num
number=$?
if [ $number -eq 0 ]                                    # 判断进程是否存在
then 
	cd $host_dir;nohup python3 $exec_path/$proc_name &          # 重启进程的命令，请相应修改
	proc_id                                                     # 获取新进程号
	echo ${pid}, $proc_name, `date` >> $host_dir$file_name      # 将新进程号和重启时间记录
fi

#crontab -e 中添加
#*/1 * * * * /root/weibo/monitor.sh
#如果不能生效，可能是没有读取的环境变量
#*/1 * * * * source /etc/profile;/bin/bash /root/monitor/monitor2.sh
#每周一早上九点清除文件内容
#0 9 * * 1 > /home/pi/weibo/util/wbIds.txt
