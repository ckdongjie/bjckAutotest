# coding = utf-8 
'''
Created on 2022年9月6日

@author: dj
'''
import logging
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
        requests.DEFAULT_RETRIES = 5
        req = requests.session()
        req.keep_alive = False
        res = None
        for i in range(3):
            try:
                if method == 'GET':
                    res = req.get(url, timeout=60, **kwargs)
                elif method == 'POST':
                    res = req.post(url, data=data, json=json, timeout=240, **kwargs)
                elif method == 'PUT':
                    res = req.put(url, data=data, timeout=240, **kwargs)
                elif method == 'DELETE':
                    res = req.delete(url)
                else:
                    print('请求方法未定义，请检查！')
                if res != None:
                    if res.json().get('socketTimeout') != None:
                        logging.warning('=========[HTTP Connect Timeout]=========')
                        continue
                    if res.status_code == 404:
                        logging.warning('=========[HTTP Request Error--404]=========')
                        continue
                    return res
            except Exception:
                if res != None and hasattr(res, 'json'):
                    return res
                    logging.warning('=========[HTTP Request Error, Error Code:'+str(res.status_code)+']=========')
                else:
                    logging.warning('=========[HTTP Request Error, try again]=========')
                    continue

