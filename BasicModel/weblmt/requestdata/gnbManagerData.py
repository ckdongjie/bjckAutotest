# coding = utf-8 
'''
Created on 2022年10月27日

@author: dj
'''
LMT_URL_DICT={
    'BntReboot':
        {
            'action': '/cgi-bin/BntReboot.py',
            'method': 'POST',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            },
            'body': {
            }
        },

    'Logout':
        {
            'action': '/',
            'method': 'GET',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            },
        },

    'GnbInfo':
        {
            'action': '/cgi-bin/queryBoardStatus.py',
            'method': 'POST',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            },
            'body': {
                'operationType': "query",
                'tableName': "boardStatus"
            }
        },

    'ClockMode':
        {
            'action': '/cgi-bin/CuDuBts.py',
            'method': 'POST',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            },
            'body': {
                'operationType': "update",
                'tableName': "t_clock_src"
            }
        },

    'OperatorInfo':
        {
            'action': '/cgi-bin/CuDuBts.py',
            'method': 'POST',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            },
            'body': {
                'operationType': "select",
                'pageIndex': 0,
                'pageSize': "25",
                'tableName': "t_operator"
            }
        },

    'OperatorCfg':
        {
            'action': '/cgi-bin/CuDuBts.py',
            'method': 'POST',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            },
            'body': {
                'operationType': "update",
                'tableName': "t_operator",
                'data': [
                    {'OperatorId': 0, 'OperatorName': "SonyWireless", 'Mcc': "460", 'Mnc': "00", 'OperatorType': 0}]
            }
        },

    'WIFILog':
        {
            'action': '/cgi-bin/extractLog.py?logType=1',
            'method': 'GET',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            }
        },

    'DeviceLog':
        {
            'action': '/cgi-bin/extractLog.py?logType=52',
            'method': 'GET',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            }
        },

    'CHRLog':
        {
            'action': '/cgi-bin/extractLog.py?logType=53',
            'method': 'GET',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            }
        },

    'BlackBoxLog':
        {
            'action': '/cgi-bin/extractLog.py?logType=54',
            'method': 'GET',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            }
        },

    'TestModeActivated':
        {
            'action': '/cgi-bin/AutoTestMode.py',
            'method': 'POST',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            },
            'body': {
                'IsAutoStart': 1,
                'optType': 8310
            }
        },

    'EnableSwitch':
        {
            'action': '/cgi-bin/CuDuBts.py',
            'method': 'POST',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            },
            'body': {
                'operationType': "update",
                'tableName': "t_ipStack",
                'data': [{'IPStackID': 1, 'IPv4Enable': "1", 'IPv6Enable': "0"}]
            }
        },

    'IPAddress':
        {
            'action': '/cgi-bin/CuDuBts.py',
            'method': 'POST',
            'header': {
                'content-type': "application/json; charset=UTF-8",
                'Cookie': 'LoginName=admin'
            },
            'body': {
                'operationType': "select",
                'pageIndex': 0,
                'pageSize': "25",
                'tableName': "t_ipv6"
            }
        }

}