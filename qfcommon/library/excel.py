#coding: utf-8
import os
import types
import datetime
import logging
import traceback

import xlrd
import xlwt
from xlutils import copy as xlcopy  # as一下，与copy库区分

log = logging.getLogger()

class ExcelErr(Exception):
    pass

# 当成枚举来用吧
# xlrd支持的单元格式类型: 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error 
class CellType:
    # xlwt好像只支持num和str，bool是转换成num
    # 所以最好只使用NUM和STR
    T_EMPTY = 0     # 不知道干什么用, 先保留吧
    T_STR   = 1
    T_NUM   = 2
    T_DATE  = 3     # xlwt好像不支持, 先保留吧
    T_BOOL  = 4     # xlwt把BOOL转成了num或str
    T_ERR   = 5     # 不知道干什么用, 先保留吧

class Cell:
    '''
        excel的单元格式信息, 以unicode保存
        定义单元格的数据，类型及格式
    '''

    def __init__(self, value, ctype = CellType.T_STR, xf = 0, charset = 'utf-8'):
        '''
            value: 单元格数据
            ctype:  单元格式类型，默认是字符串
            xf:    扩展的格式化 # 不知道有什么用
        '''
        # XXX: 未验证value与type是否匹配
        # 如果value是字符串，且不是
        if not self._validate(value, ctype):
            raise ExcelErr, 'value and ctype is not match. type(value):%s ctype:%d' % (type(value), ctype)
        if ctype == CellType.T_STR:
            if not isinstance(value, types.UnicodeType):
                value = value.decode(charset)
        self.value = value
        self.ctype = ctype
        self.xf    = xf

    def __str__(self):
        return 'value:%s ctype:%d xf:%d' % (self.value, self.ctype, self.xf)

    def _validate(self, value, ctype):
        '''验证value与ctype是否匹配'''
        if ctype == CellType.T_STR:
            if not isinstance(value, basestring):
                return False
        elif ctype == CellType.T_NUM:
            if not (isinstance(value, types.IntType) or \
                    isinstance(value, types.LongType) or \
                    isinstance(value, types.FloatType)):
                return False
        #elif ctype == CellType.T_DATE:
        #    if not (isinstance(value, datetime.date) or \
        #            isinstance(value, datetime.datetime)):
        #        return False
        elif ctype == CellType.T_BOOL:
            if not isinstance(value, types.BooleanType):
                return False
        else:
            log.warn('donot support ctype:%s', ctype)
            return False
        return True

class Excel:
    '''
        excel读写时，统一使用unicode
        读时，会将读出来的每个单元格式的信息转成unicode
        写时，会将行中每个成功的信息写成unicode
    '''

    def __init__(self, xls_file, charset = 'utf-8'):
        # 打开失败，直接抛出异常
        self._file = xls_file
        self._table = xlrd.open_workbook(xls_file)
        self.curr_sheet = None  # 当前处理的sheet, 可能不存在
        self.charset = 'utf-8'
        log.debug('open excel:%s', self._file)

    def __del__(self):
        '''
            重载析构函数，保存Excel数据
            python的析构函数，不像C++，所以不保证靠谱，尽量自己调用save保存数据
        '''
        self.save()

    def sheet_count(self):
        '''获取excel的sheet数'''
        return len(self._table.sheets())

    def curr_sheet_name(self):
        '''获取当前处理的sheet的名'''
        if self.curr_sheet:
            return self.curr_sheet.name
        else:
            return None

    def curr_sheet_index(self):
        '''获取当前处理的sheet的index'''
        if self.curr_sheet:
            return self.curr_sheet.number
        else:
            return -1

    def save(self):
        '''
            保存excel
            如果在释放Excel对象时，未保存excel，则会导致数据丢失
            因为xlrd不能保存，xlwt不能添加，所以通过xlrd添加，完了后按原文件名保存
        '''
        new_table = xlcopy.copy(self._table)
        new_table.save(self._file)
        log.debug('save excel:%s', self._file)

    def open_sheet(self, sheet_id = 0, sheet_name = ''):
        '''根据sheet_id或sheet_name打开sheet'''
        # 根据sheet_id或sheet_name打开excel的sheet
        sheet = None
        if sheet_name:
            # 根据sheet_name打开sheet
            # 如果sheet_name不存在，则会抛异常
            try:
                sheet = self._table.sheet_by_name(sheet_name)
            except:
                log.warn('open %s %s sheet exception:[[%s]]',
                    self._file, sheet_name, traceback.format_exc())
        else:
            # 根据sheet_id打开sheet
            # 如果sheet_id太大，则会抛异常
            if sheet_id >= len(self._table.sheets()):
                log.warn('sheet_id is too large. sheet_id:%d sheet_count:%d',
                        sheet_id, len(self._table.sheets()))
            else:
                sheet = self._table.sheets()[sheet_id]
                # sheet = self._table.sheet_by_index(sheet_id)
        return sheet


    def read_row(self, sheet_id = 0, sheet_name = ''):
        '''打开sheet_id，并读取每一行'''
        # 打开sheet
        sheet = self.open_sheet(sheet_id, sheet_name)
        if not sheet:
            # 打开sheet失败，抛出异常
            raise
            #raise StopIteration
        # 保存当前处理的sheet
        self.curr_sheet = sheet
        # 读sheet中的数据
        for rownum in xrange(0, sheet.nrows):
            row = sheet.row_values(rownum)
            #yield row
            xl_row = []
            for cell in row:
                # 将每个单元格中的数据都转成unicode
                if isinstance(cell, basestring) and (not isinstance(cell, types.UnicodeType)):
                    cell = cell.decode(self.charset)
                xl_row.append(cell)
            yield xl_row
    
    def write_row(self, sheet_id = 0, sheet_name = '', row = None, row_num = -1):
        '''
            根据sheet_id或sheet_name打开excel的sheet，并写到表格中
            row: 行信息, row的成员是Cell对象
            row_num: 写到row_num行，如果row_num < 0: 则追加，否则替换
            charset: excel的编码，统一使用unicode
        '''
        log.debug('write_row...')
        if not row:
            # row不存在，直接成功
            return True
        sheet = self.open_sheet(sheet_id, sheet_name)
        if not sheet:
            # 打开sheet失败
            return False
        # 保存当前处理sheet
        self.curr_sheet = sheet
        # 获取row写到的行
        if row_num < 0:
            row_num = sheet.nrows   # 追加
            log.debug('excel sheet:%d row num:%d', sheet_id, row_num)
        # 判断需要写入的字段数是否与表格的列数相同
        #if sheet.ncols != 0 and len(row) != sheet.ncols:
        #    log.debug('row info is not valid. row:%s len(row):%d sheet_cols:%d', row, len(row), sheet.ncols)
        #for i in xrange(sheet.ncols):
        for i in xrange(len(row)):
            log.debug('cell:%s', row[i])
            sheet.put_cell(row_num, i, row[i].ctype, row[i].value, row[i].xf)
        return True

    @classmethod
    def create(cls, xls_file, rows = None):
        '''
            创建excel，并把rows添加到excel文件中
            rows: 行信息, rows的成员是list,list的成员是Cell,格式:[[cell, cell, cell], [cell, cell, cell]]
                 如果rows为空，则只创建excel文件，并在excel中添加一个Sheet1的sheet
        '''
        # 创建excel文件
        table = xlwt.Workbook()             # 创建一个工作簿
        sheet = table.add_sheet('Sheet1')       # 创建一个工作表
        if rows:
            # rows存在，将rows添加到excel中
            # 不存在，直接保存excel
            for rownum in xrange(0, len(rows)):
                for colnum in xrange(0, len(rows[rownum])):
                    #在rownum行rolnum列写入cell
                    cell = rows[rownum][colnum]
                    log.debug('cell:%s', cell)
                    sheet.write(rownum, colnum, cell.value)    # 保存单元格式数据
        table.save(xls_file)     # 保存
        # 返回Excel的实例
        excel = cls(xls_file)
        return excel
       

def xls2csv(xls_file, csv_file):
    '''
        excel转csv
        xls_file: excel文件
        csv_file: csv文件
    '''
    excel = Excel(xls_file)     # 打开excel文件
    fp = open(csv_file, 'w')    # 打开csv文件
    for row in excel.read_row():
        new_row = []
        # 列可能不为字符串
        for col in row:
            # 将excel行的数据转字符串
            if not isinstance(col, basestring):
                new_row.append(str(col))
            else:
                new_row.append(col)
        str_row = ','.join(new_row) # 将数据以逗号连接
        # 以utf-8的方式保存
        if isinstance(str_row, types.UnicodeType):
            str_row = str_row.encode('utf-8')
        fp.write(str_row)
        fp.write('\n')
    fp.close()

def csv2xls(xls_file, csv_file, charset = 'utf-8'):
    '''
        将csv转excel
        xls_file: excel文件
        csv_file: csv文件
        charset:  csv文件的编码
    '''
    # 如果xls_file文件存在，则删除
    # 如果xls_file是目录，则失败
    if os.path.exists(xls_file):
        if os.path.isfile(xls_file):
            os.remove(xls_file)
            log.debug('%s file exist. remove', xls_file)
        else:
            log.debug('%s is directory', xls_file)
            return False
    excel  = Excel.create(xls_file) # 创建xls文件
    # 打开csv文件
    csv_fp = open(csv_file, 'r')
    for row in csv_fp:
        cells = row.split(',')
        xl_row = []
        for cell in cells: 
            xl_cell = Cell(cell.decode(charset)) # 没办法，不知道类型，所以直接全部都是字符串了
            log.debug('cell:%s', xl_cell)
            xl_row.append(xl_cell)
        excel.write_row(row = xl_row)
    excel.save()
    csv_fp.close()
    return True



def create_xls(xls_file):
    # 如果xls_file文件存在，则删除
    # 如果xls_file是目录，则失败
    if os.path.exists(xls_file):
        if os.path.isfile(xls_file):
            os.remove(xls_file)
            log.debug('%s file exist. remove', xls_file)
        else:
            log.debug('%s is directory', xls_file)
            return False
    info  = [
        [Cell(u'张三'), Cell(18, CellType.T_NUM), Cell(u'女'), Cell('1988-12-12 00:00:00')],
        [Cell(u'李四'), Cell(19, CellType.T_NUM), Cell(u'男'), Cell('1989-12-12 00:00:00')],
        [Cell(u'五五'), Cell(18, CellType.T_NUM), Cell(u'女'), Cell('1985-12-12 00:00:00')],
    ]
    excel = Excel.create(xls_file, info)
    xls2csv(xls_file, 'test.csv')   # 将xls转csv
    return True

def create_xls2(xls_file):
    # 如果xls_file文件存在，则删除
    # 如果xls_file是目录，则失败
    if os.path.exists(xls_file):
        if os.path.isfile(xls_file):
            os.remove(xls_file)
            log.debug('%s file exist. remove', xls_file)
        else:
            log.debug('%s is directory', xls_file)
            return False
    info  = [
        [Cell('张三'), Cell(18, CellType.T_NUM), Cell('女'), Cell('1988-12-12 00:00:00')],
        [Cell('李四'), Cell(19, CellType.T_NUM), Cell('男'), Cell('1989-12-12 00:00:00')],
        [Cell('五五'), Cell(18, CellType.T_NUM), Cell('女'), Cell('1985-12-12 00:00:00')],
    ]
    excel = Excel.create(xls_file)
    for row in info:
        excel.write_row(row = row)
    excel.save()
    xls2csv(xls_file, 'test.csv')   # 将xls转csv
    return True

def create_xls3(xls_file):
    # 如果xls_file文件存在，则删除
    # 如果xls_file是目录，则失败
    if os.path.exists(xls_file):
        if os.path.isfile(xls_file):
            os.remove(xls_file)
            log.debug('%s file exist. remove', xls_file)
        else:
            log.debug('%s is directory', xls_file)
            return False
    info  = [
        [Cell('张三'), Cell(18, CellType.T_NUM), Cell(True, CellType.T_NUM), Cell('1988-12-12 00:00:00')],
        [Cell('李四'), Cell(19, CellType.T_NUM), Cell(False, CellType.T_NUM), Cell('1989-12-12 00:00:00')],
        [Cell('五五'), Cell(18, CellType.T_NUM), Cell(True, CellType.T_NUM), Cell('1990-12-12 00:00:00')],
    ]
    excel = Excel.create(xls_file)
    for row in info:
        excel.write_row(row = row)
    excel.save()
    xls2csv(xls_file, 'test.csv')   # 将xls转csv
    return True

def append_xls(xls_file):
    info  = [
        [Cell(u'张三1'), Cell(18, CellType.T_NUM), Cell(u'女'), Cell('1988-12-12 00:00:00')],
        [Cell(u'李四1'), Cell(19, CellType.T_NUM), Cell(u'男'), Cell('1989-12-12 00:00:00')],
        [Cell(u'五五1'), Cell(18, CellType.T_NUM), Cell(u'女'), Cell('1985-12-12 00:00:00')],
    ]
    excel = Excel(xls_file)
    for row in info:
        excel.write_row(row = row)
    excel.save()
    xls2csv(xls_file, 'test.csv')

def append_xls2(xls_file):
    info  = [
        # 多一列或少一列
        [Cell(u'张三1'), Cell(18, CellType.T_NUM), Cell(u'女'), Cell('1988-12-12 00:00:00'), Cell('test')],
        [Cell(u'李四1'), Cell(19, CellType.T_NUM), Cell(u'男'), ],
        [Cell(u'五五1'), Cell(18, CellType.T_NUM), Cell(u'女'), Cell('1985-12-12 00:00:00')],
    ]
    excel = Excel(xls_file)
    for row in info:
        excel.write_row(row = row)
    excel.save()
    xls2csv(xls_file, 'test.csv')



def update_xls(xls_file, row_num = 3):
    info  = [
        [Cell(u'张三3'), Cell(18, CellType.T_NUM), Cell(u'女'), Cell('1988-12-12 00:00:00')],
        [Cell(u'李四3'), Cell(19, CellType.T_NUM), Cell(u'男'), Cell('1989-12-12 00:00:00')],
        [Cell(u'五五3'), Cell(18, CellType.T_NUM), Cell(u'女'), Cell('1985-12-12 00:00:00')],
    ]
    excel = Excel(xls_file)
    row_num = row_num
    for row in info:
        excel.write_row(row = row, row_num = row_num)
        row_num += 1
    excel.save()
    # excel = None   # 强制析构
    xls2csv(xls_file, 'test.csv')

def test(xls_file):
    excel = Excel(xls_file)
    for row in excel.read_row():
        for col in row:
            print col,
        print 

def test_main():
    import logger
    logger.install('stdout')

    #test('test.xls')
    #xls2csv('test.xls', 'test.csv')
    #csv2xls('test3.xls', 'test.csv')
    #test('test3.xls')
    #create_xls('test1.xls')
    #create_xls2('test2.xls')
    create_xls3('test4.xls')
    #append_xls('test2.xls')
    #append_xls2('test2.xls')
    #update_xls('test2.xls')
    #update_xls('test2.xls', row_num = 15)

if __name__ == '__main__':
    test_main()

