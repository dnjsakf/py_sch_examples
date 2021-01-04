'''
    Basic Concepts
      - triggers
      - jobstores
      - executors
      - schedulers
      
      Triggers contain the scheduling logic. Each job has its own trigger which determines when the job should be run next. Beyond their initial configuration, triggers are completely stateless.

      Job stores house the scheduled jobs. The default job store simply keeps the jobs in memory, but others store them in various kinds of databases. A job’s data is serialized when it is saved to a persistent job store, and deserialized when it’s loaded back from it. Job stores (other than the default one) don’t keep the job data in memory, but act as middlemen for saving, loading, updating and searching jobs in the backend. Job stores must never be shared between schedulers.

      Executors are what handle the running of the jobs. They do this typically by submitting the designated callable in a job to a thread or process pool. When the job is done, the executor notifies the scheduler which then emits an appropriate event.

      Schedulers are what bind the rest together. You typically have only one scheduler running in your application. The application developer doesn’t normally deal with the job stores, executors or triggers directly. Instead, the scheduler provides the proper interface to handle all those. Configuring the job stores and executors is done through the scheduler, as is adding, modifying and removing jobs.
'''

'''  
  Scheduler
    jobstores ( Task 저장소 )
      - JOB이 등록되면 저장소에 기록하며, Schedule이 완료되면 저장소에서 제거
        - scheduler.remove_job() 또는 job.remove() 명령을 통해 임의로 제거가능
        - job_id는 UNIQUE하며, 지정하지 않으면 uuid4()로 생성됨
      - 작업이력은 Pickle을 통해 직력화되어 저장되며, 조회할 때는 역직렬화함
      - 기본적으로 Memory에 저장하며, MongoDB, SQLite, RabbitMQ 등 다양한 저장소를 지원
      - 주기적으로 실행되는 스케줄의 경우, 

    
    executors ( 실행자 )
      - JOB을 Thread Pool 또는 Process Pool에 보내서 처리
      - 처리가 완료되면 스케줄러에 알림
        - 스케줄러는 다음 실행시간을 계산하거나, 스케줄을 종료시키는 등 상황에 따른 적절한 처리를 함
        
  JOB
    execute
      - JOB이 처리할 작업
    
    trigger
      - JOB을 수행할 스케줄
      
    id
      - JOB 식별자 
  
'''