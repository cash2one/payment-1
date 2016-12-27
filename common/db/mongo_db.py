#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mongodb 工具类
"""

__author__ = 'swzs'

from setting import MONGO_DB_HOST, MONGO_DB_PORT, MONGO_DB_NAME
from pymongo import mongo_client, ASCENDING, DESCENDING
from bson import ObjectId



class MongodbUtilsHandler:

    def __init__(self):
        pass

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self.MONGO_DB_CONN = mongo_client.MongoClient(host=MONGO_DB_HOST, port=MONGO_DB_PORT)

        return self.MONGO_DB_CONN[MONGO_DB_NAME]

    def ensure_index(self, colle_name, indexes):
        """
        创建Index
        :param colle_name:
        :param indexes:
        :return:
        """

        if type(indexes) is not list:
            result = [indexes]
        else:
            result = indexes

        for idx in result:
            self.db[colle_name].create_index(idx)

    def find_collection_names(self):
        """
        查出所有文档的名字
        类似于 show collections
        :return: []
        """
        return self.db.collection_names()

    def create_collection(self, coll_name):
        """
        新建一个文档
        类似于   db.createCollection('XXX')
        :param coll_name:
        :return:
        """
        return self.db.create_collection(coll_name)


    #===================================save_data==================================================================================

    def db_insert_one(self, coll_name, data_dict={}):
        """
        保存一条数据
        类似于  db.collection.insert({xxx:yyy})
        :param coll_name: 集合名
        :param data_dict: 插入的数据字典
        :return: '_id'
        """
        if not data_dict or not coll_name:
            return

        result = self.db[coll_name].insert_one(data_dict)
        insert_id = result.inserted_id
        if isinstance(insert_id, ObjectId):
            return str(insert_id)

        return insert_id

    def save_many(self, coll_name, colums=[]):
        """
        批量保存
        :desc 此方法一般常用于批量插入处理
        :param coll_name:
        :param [row_dict]:
        :return: [id]
        """
        fidels = []
        if colums:
            for filed in colums:
                save_id = self.db[coll_name].save(filed)
                fidels.append(str(save_id))

        return fidels

    def inc_one(self, coll_name, object_id, data_dict={}, is_oid=False):
        """
        向文档新增列
        :param coll_name:
        :param object_id:
        :param data_dict:
        :param is_oid
        :return:
        """
        if is_oid:
            oid = ObjectId(object_id)
        else:
            oid = object_id

        return self.__db[coll_name].update({'_id': oid}, {'$inc': data_dict}, {'multi': True})

    #======================================update_data=================================================================

    def db_update_one(self, coll_name, object_id, data_dict={}, is_oid=False):
        """
        更新一条记录
        :param coll_name:
        :param object_id:
        :param data_dict:
        :return:
        """
        if is_oid:
            oid = ObjectId(object_id)
        else:
            oid = object_id

        res = self.db[coll_name].update_one({'_id': oid}, {'$set': data_dict})

        return res.matched_count

    def db_update_many(self, coll_name, condition={}, row_list_dict=[]):
        """
        批量更新
        :param coll_name:
        :param row_list_dict: [{a,b,c,d,e,f,g}]
        :return:
        """

        fildes = []

        for row_dict in row_list_dict:
            if condition:
                result = self.db[coll_name].update_many({'_id': row_dict['_id']}, {'$set': row_dict})
            else:
                result = self.db[coll_name].update({}, {'$set': row_dict})
            fildes.append(result)

        return fildes

    #======================================find_data====================================================================

    def db_find_one(self, coll_name, columns=[], condition={}, is_oid=False):
        """
        按条件查出单条数据的值
        :param coll_name:
        :param columns:
        :param condition:
        :return:
        """

        filed_list = {}

        for filed in columns:
            filed_list[filed] = 1

        if is_oid and '_id' in condition:
            condition['_id'] = ObjectId(condition['_id'])

        result = self.db[coll_name].find_one(condition, filed_list)

        if not result:
            return None
        return self.__check_id(result)

    def find_filed_value(self, coll_name, columns=[], condition={}, is_oid=False):
        """
        根据条件查出属性的值
        :param coll_name:
        :param condition:
        :param columns:
        :param is_oid:
        :return:
        """

        filed_list = {'_id': 0}
        for filed in columns:
            filed_list[filed] = 1

        condit_data = {}
        if '_id' in condition and is_oid is True:
            condit_data['_id'] = ObjectId(condition['_id'])

        result = self.db[coll_name].find_one(condit_data, filed_list) or {}
        if '_id' in result:
            result = self.__check_id(result)

        return result

    def find_exists(self, coll_name, condition={}, is_oid=False):
        """
        检查记录是否存在
        :param coll_name:
        :param condition:
        :return:
        """

        if is_oid is True and '_id' in condition:
            condition['_id'] = ObjectId(condition['_id'])

        return self.db[coll_name].find_one(condition)

    def get_by_id(self, coll_name, columns=None, condition={}, is_oid=False):
        """
        根据ID 查出记录
        :param coll_name:
        :param columns:
        :param condition:
        :param is_oid:
        :return:
        """
        if is_oid:
            oid = ObjectId(condition['_id'])
        else:
            oid = condition['_id']

        fields = {}
        if columns and isinstance(columns, list):
            for field in columns:
                fields[field] = 1
            result = self.db[coll_name].find_one(oid, fields)
        else:
            result = self.db[coll_name].find_one(oid)

        if '_id' in result:
            return self.__check_id(result)
        return result

    def find_count(self, coll_name, condition={}):
        """
        查出文档记录数,如果条件为空则查出全部
        类似于  db.getCollection('coll_name').find({})count()
        :param coll_name:
        :param condition:
        :return: int
        """
        if condition:
            return self.db[coll_name].find(condition).count()
        return self.db[coll_name].find().count()

    def query(self, coll_name, columns, condition={}, sort=None, skip_id=True, limit=0, page=0, page_size=10, trans=None):
        """
        db查询
        :param coll_name:
        :param columns: 列
        :param condition: 条件
        :param sort: 排序
        :param skip_id: 是否跳过
        :param limit: 限制
        :param page: 页码
        :param page_size:  大小
        :return:
        """

        fields = {}
        for c in columns:
            fields[c] = 1
        if skip_id:
            fields['_id'] = 0

        stupid_sort = []
        if sort is not None:
            if type(sort) == str:
                stupid_sort.append([sort, ASCENDING])
            else:
                for f in sort:
                    if sort[f] == -1:
                        stupid_sort.append([f, DESCENDING])
                    else:
                        stupid_sort.append([f, ASCENDING])

        skip = 0
        if page > 0 and page_size > 0:
            skip = page_size * (page - 1)
            limit = page_size

        c = self.db[coll_name].find(condition, projection=fields, sort=stupid_sort, limit=limit, skip=skip)

        result = []

        for r in c:
            if not skip_id:
                self.__json_id(r)
            if trans:
                trans(r)
            result.append(r)

        return result

    def find_all(self, coll_name):
        """
        查看文档全部数据
        :param coll_name:
        :return:
        """
        result = self.db[coll_name].find()
        if result:
            return self.__check_id(result)
        return result

#============================================delete data===================================================================

    def drop(self, coll_name):
        """
        删除一个文档
        :param coll_name:
        :return:
        """
        return self.db.drop_collection(coll_name)

    def db_remove(self, coll_name, object_id, is_oid=False):
        """
        按 object_id 删除数据
        :param coll_name:
        :param object_id:
        :param is_oid:
        :return: {u'ok': 1, u'n': 1}  n表示删除勒几条数据
        """
        condition = {}
        if is_oid:
            oid = ObjectId(object_id)
        else:
            oid = object_id
        condition['_id'] = oid

        return self.db[coll_name].remove(condition)

    def db_delete_one(self, coll_name, object_id, is_obj=False):
        """
        删除一行数据
        :param coll_name:
        :param object_id:
        :param is_obj:
        :return:
        """
        if is_obj:
            oid = ObjectId(object_id)
        else:
            oid = object_id
        res = self.db[coll_name].delete_one({'_id': oid})

        return res.deleted_count

    def delete_option(self, coll_name, object_id, condition={}, is_oid=False):
        """
        按条件删除属性
        :param coll_name:
        :param condition:
        :param is_oid:
        :return:
        """
        if is_oid:
            oid = ObjectId(object_id)
        else:
            oid = object_id

        return self.db[coll_name].update({'_id': oid}, {'$unset': condition}, multi=True)

    def pull_one(self, coll_name, object_id, condition={}, is_oid=False):
        """
        从数组field内删除一个等于value值。
        :param coll_name:
        :param condition:
        :param is_oid:
        :return:
        @author qiao
        """
        if is_oid:
            oid = ObjectId(object_id)
        else:
            oid = object_id

        return self.db[coll_name].update({'_id':oid}, {'$pull': condition}, multi=True)

    def push_one(self, coll_name, object_id, condition={}, is_oid=False):
        """
        把value追加到数组field里面去
        :param coll_name:
        :param condition:
        :param is_oid:
        :return:
        @author qiao
        """
        if is_oid:
            oid = ObjectId(object_id)
        else:
            oid = object_id

        return self.db[coll_name].update({'_id':oid}, {'$push': condition}, multi=True)

    def __check_id(self, list_or_doc):
        """
        检查并转换
        :param list_or_doc:
        :return:
        """

        if isinstance(list_or_doc, dict):
            list_or_doc["_id"] = str(list_or_doc["_id"])
            return list_or_doc
        else:
            result = []
            for row in list_or_doc:
                if isinstance(row['_id'], ObjectId):
                    row['_id'] = str(row['_id'])
                result.append(row)
            return result

    def __json_id(self, doc):
        """
        将结果中的ObjectId转换为json格式
        :param doc:
        :return:
        """

        if isinstance(doc, dict) and doc.has_key("_id") and isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])


    def auto_inc_id(self, coll_name=None):
        """
        获取文档(coll_name)一个自增的(int)ID
        :param coll_name:
        :return int
        @author qiao
        """
        if self.find_exists(coll_name=coll_name, condition={'_id': 'auto_id'}, is_oid=False) :
            return self.db[coll_name].find_and_modify( query={'_id': 'auto_id'}, \
                                    update={'$inc': {'seq': 1}}, new=True)['seq']
        else :
            self.db[coll_name].insert_one({'_id':'auto_id', 'seq':1})
            return 1

    #TODO  暂未实现
    def backup_db(self):
        """
        备份
        :return:
        """
        pass

    #TODO  暂未实现
    def slicing_db(self):
        """
        分片
        :return:
        """
        pass

mongo_manage = MongodbUtilsHandler()
