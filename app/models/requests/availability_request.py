from pydantic import BaseModel, validator
from datetime import time

class AvailabilityRequest(BaseModel):
    doctor_id: int 
    day_of_week: str 
    start_time: time 
    end_time: time
    
@validator("day_of_week")
def validate_day(cls, value):
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if value not in valid_days:
        raise ValueError(f"'{value}' is not a valid day of the week.")
    return value

@validator("end_time")
def validate_time(cls, end_time, values):
    start_time = values.get("start_time")
    if start_time and end_time <= start_time:
        raise ValueError("End time must be after start time.")
    return end_time