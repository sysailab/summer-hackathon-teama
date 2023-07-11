from work_queue import WorkQueue

class SaveThread:    
    def work(self):
        while True:
            saveData = WorkQueue.saveQueue.get()            # queue 모니터링(bloking)
            
            # TODO: excel에 saveData 저장하기