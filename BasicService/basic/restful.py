# coding = utf-8 
'''
Created on 2022年9月6日

@author: dj
'''
import requests

class HttpClient(object):
    
    #发送url get请求
    def get_request(self, url, data=None, json=None, **kwargs):
        return self._url_request('get', url, data, json, **kwargs)
    #发送url post请求   
    def post_request(self, url, data=None, json=None, **kwargs):
        return self._url_request('post', url, data, json, **kwargs)    
        
    def _url_request(self, method, url, data=None, json=None, **kwargs):
        method = method.upper()
    
        if method == 'GET':
            res = requests.get(url, timeout=5, **kwargs)
        elif method == 'POST':
            res = requests.post(url, data=data, json=json, timeout=5, **kwargs)
        elif method == 'PUT':
            res = requests.put(url, data=data, timeout=5, **kwargs)
        elif method == 'DELETE':
            res = requests.delete(url, timeout=5,)
        else:
            print('请求方法未定义，请检查！')
        return res

