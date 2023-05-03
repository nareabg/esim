# import re
# import logging
# import threading
# from datetime import datetime
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from .tables import  Facts 
# from .config import db_uri
# import os

# LOGS = Facts.LOGS

# class LogFileHandler(FileSystemEventHandler):
#     def __init__(self):
 
#         self.pattern = re.compile(r'(?P<level>\w+)\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3}\s+-\s+(?P<file_name>\w+)\.py\s+-\s+(?P<message>.+)\s+\((?P<func_name>\w+)\.py:(?P<line_number>\d+)\)')
#         self.engine = create_engine(db_uri)
#         self.Session = sessionmaker(bind=self.engine)
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(logging.INFO)

#     def on_modified(self, event):
#         if event.is_directory:
#             return

#         with open(event.src_path, 'r') as f:
#             for line in f:
#                 match = self.pattern.match(line.strip())
#                 if match:
#                     level = match.group('level')
#                     file_name = match.group('file_name')
#                     func_name = match.group('func_name')
#                     message = match.group('message')
#                     line_number = match.group('line_number')
#                     load_time = datetime.now()

#                     log = LOGS(FILE_NAME=file_name, FUNC_NAME=func_name, MESSAGE=message, LOAD_TIME=load_time)

#                     if level == 'INFO':
#                         log_level = logging.INFO
#                     elif level == 'WARNING':
#                         log_level = logging.WARNING
#                     elif level == 'ERROR':
#                         log_level = logging.ERROR
#                     elif level == 'CRITICAL':
#                         log_level = logging.CRITICAL
#                     else:
#                         log_level = logging.INFO

#                     self.logger.setLevel(log_level)
#                     self.logger.log(log_level, message)

#                     session = self.Session()
#                     session.add(log)
#                     session.commit()
#                     session.close()

# # def start_log_watcher(log_file_path='logs.log'):
# #     log_dir_path = os.path.dirname(log_file_path)
# #     handler = LogFileHandler()
# #     observer = Observer()
# #     observer.schedule(handler, log_dir_path, recursive=False)
# #     observer.start()

# #     try:
# #         while True:
# #             threading.Thread(target=observer.join()).start()
# #     except KeyboardInterrupt:
# #         observer.stop()

# #     observer.join()
# import os

# def start_log_watcher(log_file_path='logs.log'):
#     log_dir_path = os.path.dirname(log_file_path)
#     handler = LogFileHandler()
#     observer = Observer()
#     observer.schedule(handler, log_dir_path, recursive=False)
#     observer.start()

#     try:
#         while True:
#             threading.Thread(target=observer.join()).start()
#     except KeyboardInterrupt:
#         observer.stop()

#     observer.join()
