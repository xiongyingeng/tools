import datetime
import time
import calendar


class TimeManage:
    ''' 时间管理类 '''

    @staticmethod
    def SecondsOfADay():
        # 一天的秒数
        return 86400  # 24 * 60 * 60

    @staticmethod
    def timestampTostr(timestamp, format='%Y-%m-%d %H:%M:%S'):
        '''时间戳转字符串'''
        # format = '%Y-%m-%d %H:%M:%S'
        # value为传入的值为时间戳(整形)，如：1332888820
        value = time.localtime(timestamp)
        return time.strftime(format, value)

    @staticmethod
    def strTotimestamp(str, format='%Y-%m-%d %H:%M:%S'):
        '''日期字符串转成时间戳'''
        # dt为字符串
        # 中间过程，一般都需要将字符串转化为时间数组
        time.strptime(str, format)
        s = time.mktime(time.strptime(str, format))
        return int(s)

    @staticmethod
    def timestampToHour(timestamp, format):
        '''根据时间戳得到日期对象'''
        timestr = TimeManage.timestampTostr(timestamp, format)
        return datetime.datetime.strptime(timestr, format).hour

    @staticmethod
    def timestampTotimestamp(timestamp, format):
        '''得到timestamp当天00:00:00的时间戳'''
        date = TimeManage.timestampTostr(timestamp, format)
        return TimeManage.strTotimestamp(date, format)

    @staticmethod
    def timestampToDiff(rtc1, rtc2, format):
        '''求两个时间的间隔,单位秒。format如跨天'%Y-%m-%d',跨小时'%Y-%m-%d %H'等'''
        h1 = TimeManage.timestampTotimestamp(rtc1, format)
        h2 = TimeManage.timestampTotimestamp(rtc2, format)
        return int(h2 - h1)

    @staticmethod
    def strToDiff(strDate, strDate2, format):
        '''求两个时间的间隔,单位秒。format如跨天'%Y-%m-%d',跨小时'%Y-%m-%d %H'等'''
        h1 = TimeManage.strTotimestamp(strDate, format)
        h2 = TimeManage.strTotimestamp(strDate2, format)
        return int(h2 - h1)

    @staticmethod
    def timestampToDatetime(timestamp, format):
        '''根据时间戳得到日期对象'''
        timestr = TimeManage.timestampTostr(timestamp, format)
        return datetime.datetime.strptime(timestr, format)

    @staticmethod
    def strToDatetime(strDate, format):
        '''根据日期得到日期对象'''
        return datetime.datetime.strptime(strDate, format)

    # 开始和结束的天数集合
    @staticmethod
    def dateRange(beginDate, endDate):
        dates = []
        dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
        date = beginDate[:]
        while date <= endDate:
            dates.append(date)
            dt = dt + datetime.timedelta(1)
            date = dt.strftime("%Y-%m-%d")
        return dates

    @staticmethod
    def week_no(date_str, format):
        index = int(datetime.datetime.strptime(date_str, format).strftime("%W"))
        return index

    @staticmethod
    def diff_now(strDate, format):
        a = datetime.datetime.now()
        b = datetime.datetime.strptime(strDate, format)
        c = a - b
        return c

    @staticmethod
    def date_interval(str_date1, str_date2, format='%Y-%m-%d'):
        '''求两个时间的间隔天数'''
        datetime1 = TimeManage.strToDatetime(str_date1, format)
        datetime2 = TimeManage.strToDatetime(str_date2, format)
        interval = datetime2 - datetime1
        return interval

    @staticmethod
    def date_interval_days(str_date1, str_date2, format='%Y-%m-%d'):
        '''求两个时间的间隔天数'''
        interval = TimeManage.date_interval(str_date1, str_date2, format)
        return interval.days

    @staticmethod
    def yyyy_mm_dd(str_date, format='%Y-%m-%d %H:%M:%S'):
        dt = TimeManage.strToDatetime(str_date, format)
        return '{}-{}-{}'.format(dt.year, dt.month, dt.day)

    @staticmethod
    def previous_date(days, date_str=None, format=None):
        """
        以前的日期
        :param days:        间隔的天数
        :param date_str:    基准日期
        :param format:      日期格式, date_str不为None，则format必须填充相应格式
        :return:
        """
        if date_str is None:
            ago_date = str(datetime.date.today() - datetime.timedelta(days))
        else:
            t = time.strptime(date_str, format)
            y, m, d = t[0:3]
            split_date = str(datetime.datetime(y, m, d) - datetime.timedelta(days)).split()
            ago_date = split_date[0]

        return ago_date

    @staticmethod
    def timedelta_date(date, format, days):
        """时间间隔"""
        if isinstance(date, str):
            t = datetime.datetime.strptime(date, format)
            dst_date = str(t + datetime.timedelta(days))
        elif isinstance(date, datetime.datetime):
            dst_date = str(date + datetime.timedelta(days))
        else:
            raise ValueError("date 类型错误!!")
        return dst_date

    @staticmethod
    def year_days(year):
        """一年有多少天"""
        return 366 if calendar.isleap(int(str(year))) else 365

    @staticmethod
    def after_date_of_year(cur_date: str, format="%Y-%m-%d %H:%M:%S"):
        """当前日期的后一年时间"""
        dt = TimeManage.strToDatetime(cur_date, format)

        cur_year_days = TimeManage.year_days(dt.year)
        after_year_days = TimeManage.year_days(dt.year + 1)
        if dt.month > 2:
            days = after_year_days
        else:
            days = cur_year_days
        return TimeManage.timedelta_date(cur_date, format, days - 1)

    @staticmethod
    def timedelta_month(cur_date: str, format="%Y-%m-%d %H:%M:%S", month=1):
        from dateutil.relativedelta import relativedelta
        dt = TimeManage.strToDatetime(cur_date, format) + relativedelta(months=month)

        return str(dt)


if __name__ == '__main__':
    print(TimeManage.previous_date(1, "20190724", "%Y%m%d"))
    print(TimeManage.after_date_of_year("2018/05/24 00:10:20", "%Y/%m/%d %H:%M:%S"))
    print(TimeManage.timedelta_date("2018-05-24 21:10:20", "%Y-%m-%d %H:%M:%S", -0.8))
    print(TimeManage.timedelta_month("2018-05-24", "%Y-%m-%d", 1)[0:10])

    end_date = TimeManage.previous_date(1, "20190724", "%Y%m%d").replace("-", "")
    start_date = TimeManage.previous_date(60, end_date, "%Y%m%d").replace("-", "")
    print(end_date, start_date)
