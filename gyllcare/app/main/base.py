from .gpio import ToggleSwitch, alarm_on
from .models import Schedule
from .extensions import db
from gyllcare import create_logger
from apscheduler.schedulers.background import BackgroundScheduler
import threading

log = create_logger(__name__)

class AlarmMode():      
    def start(self):
        AlarmMode.stop_thread = False
        self.id = threading.Thread(target=alarm_on, args=(lambda : AlarmMode.stop_thread,))
        self.id.start()
    
    def stop(self):
        AlarmMode.stop_thread = True
        self.id.join()


class Scheduler():
    def __init__(self, id, schedule_id):
        self.id = id
        self.schedule_id = schedule_id
       
    def return_status(self):
        self.state = Schedule.query.filter_by(id=self.id).first().active
        return self.state

    def pause_schedule(self):
        schedule.pause_job(job_id=self.schedule_id + '_on')
        schedule.pause_job(job_id=self.schedule_id + '_off')
        log.info(f'{self.schedule_id} schedule is paused')
    
    def resume_schedule(self):
        schedule.resume_job(job_id=self.schedule_id + '_on')
        schedule.resume_job(job_id=self.schedule_id + '_off')
        log.info(f'{self.schedule_id} schedule is resumed')

    def toggle_state(self):

        status = self.return_status()

        if status:
            Schedule.query.filter_by(id=self.id).first().active = False
            self.pause_schedule()
        else:
            Schedule.query.filter_by(id=self.id).first().active = True
            self.resume_schedule()
        
        db.session.commit()

CO2 = ToggleSwitch(25, "CO2")
O2 = ToggleSwitch(8, "O2")
Light = ToggleSwitch(7, "Light")
Therm = ToggleSwitch(1, "Therm")

CO2_scheduler = Scheduler(1, "toggle_CO2")
O2_scheduler = Scheduler(2, "toggle_O2")
Light_scheduler = Scheduler(3, "toggle_light")
Therm_scheduler = Scheduler(4, "toggle_temp")

alarm = AlarmMode()
schedule = BackgroundScheduler(daemon=True)