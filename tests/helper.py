import requests
import json
import time

class netpalm_testhelper:

    def __init__(self):
        with open("../config.json") as json_file:
            data = json.load(json_file)
        self.apikey = data["api_key"]
        self.ip = data["listen_ip"]
        self.port = data["listen_port"]
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'x-api-key': self.apikey}
        # test devices go here
        self.test_device_ios_cli = "10.0.2.33"
        self.test_device_netconf = "10.0.2.39"
        self.test_device_restconf = "ios-xe-mgmt-latest.cisco.com"
        self.http_timeout=5

    def check_task(self, taskid):
        try:
            r = requests.get('http://'+self.ip+':'+str(self.port)+'/task/'+taskid,headers=self.headers, timeout=self.http_timeout)
            return r.json()
        except Exception as e:
            return False

    def poll_task(self, taskid):
        try:
            task_complete = False
            result = False
            while task_complete == False:
                task_res = self.check_task(taskid)
                if task_res["data"]["task_status"] == "finished":
                    result = task_res["data"]["task_result"]
                    task_complete = True
            return result
        except Exception as e:
            return False

    def poll_task_errors(self, taskid):
        try:
            task_complete = False
            result = False
            while task_complete == False:
                task_res = self.check_task(taskid)
                if task_res["data"]["task_status"] == "finished":
                    result = task_res["data"]["task_errors"]
                    task_complete = True
            return result
        except Exception as e:
            return False

    def post_and_check(self, url, payload):
        try:
            r = requests.post('http://'+self.ip+':'+str(self.port)+url, json=payload, headers=self.headers, timeout=self.http_timeout)
            task = r.json()["data"]["task_id"]
            result = self.poll_task(task)
            return result
        except Exception as e:
            return e

    def post_and_check_errors(self, url, payload):
        try:
            r = requests.post('http://'+self.ip+':'+str(self.port)+url, json=payload, headers=self.headers, timeout=self.http_timeout)
            task = r.json()["data"]["task_id"]
            result = self.poll_task_errors(task)
            return result
        except Exception as e:
            return e

    def check_many(self, payload):
        try:
            result = []
            for task in payload:
                res = self.poll_task(task["data"]["data"]["task_id"])
                result.append(res)
            return result
        except Exception as e:
            return e