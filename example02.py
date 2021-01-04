import logging
from tzlocal import get_localzone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import (
  ThreadPoolExecutor,
  ProcessPoolExecutor
)
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

# Logging Level 설정
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.INFO)

# 스케줄러 생성
#   - Foreground로 실행
scheduler = BlockingScheduler() # 

# 스케줄러 설정
scheduler.configure(
  # 저장소 설정
  jobstores={
    "default": MemoryJobStore()
  },
  # 실행자 설정
  executors={
    "default": ThreadPoolExecutor(20),
    "processpool": ProcessPoolExecutor(5)
  },
  # JOB 기본설정
  job_defaults={
    "coalesce": False, # 기본값은 True이며, Scheduler에 의해 작업이 여러번 실행되야하는 경우 통합하여 한번만 실행.
    "max_instances": 3 
  },
  # Timezone 설정
  timezone=get_localzone(), # "Asia/Seoul"
  daemon=True
)

# JOB Task 생성
#   - 입력받은 텍스트를 출력
def execute(text):
  print(text)

# JOB Schedule 등록
#   - task      : 입력받은 텍스트를 출력
#   - trigger   : date
#   - jobstore  : default
scheduler.add_job(
  execute,
  DateTrigger(),
  args=["[DateTrigger] Hello, Apscheduler!!!"]
)

# JOB Schedule 등록
#   - task      : 5초마다 반복하며, 입력받은 텍스트를 출력
#   - trigger   : interval
#   - jobstore  : default
scheduler.add_job(
  execute,
  IntervalTrigger(seconds=5),
  args=["[IntervalTrigger] Hello, Apscheduler!!!"]
)

# JOB Schedule 등록
#   - task      : 3초마다 반복하며, 입력받은 텍스트를 출력
#   - trigger   : cron
#   - jobstore  : default
scheduler.add_job(
  execute,
  CronTrigger.from_crontab("*/3 * * * *"),
  args=["[CronTrigger] Hello, Apscheduler!!!"]
)

# JOB 목록 출력
scheduler.print_jobs()

# 스케줄러 실행
#   - BlockingScheduler는 모든 상태를 설정한 후 마지막에 Scheduler를 실행
scheduler.start()

print("이 부분은 실행되지않음")