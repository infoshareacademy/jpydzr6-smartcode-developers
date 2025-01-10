import json
import os
from typing import Dict, Any

from datetime import timedelta, datetime
from ui_terminal import *
import datetime
from devices import *
import enum

class Task:
    def __init__(self, change_time, change_action, device):
        self.change_time = change_time
        self.change_action = change_action
        self.device = device

class Scheduler(Task):
    def __init__(self, change_time, change_action, device, tasks_list):
        super().__init__(change_time, change_action, device)

        self.tasks_list = tasks_list

    def add_task(self, change_time, change_action, device):
        self.tasks_list.append(Task(change_time, change_action, device))

    def remove_task(self, index):
        del self.tasks_list[index]

    def show_tasks(self):
        for task in self.tasks_list:
            print(task.change_time, task.change_action, task.device)

    def check_tasks(self, change_time, change_action, device):
        for task in self.tasks_list:
            if task.change_time < datetime.now():
                change_action(device)
            else:
                pass

