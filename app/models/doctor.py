from datetime import datetime
from datetime import time
from pydantic import BaseModel


class Doctor(BaseModel):
    id: int
    first_name: str
    last_name: str


class Location(BaseModel):
    id: int
    address: str


class DoctorLocation(BaseModel):
    """
    This indicates that a doctor works at a location. Locations can have
    multiple doctors, and doctors can have multiple locations
    """
    id: int
    doctor_id: int
    location_id: int

class Appointment(BaseModel):
    id: int
    doctor_id: int 
    location: str 
    appointment_time: datetime 
    patient_name: str

class Availability(BaseModel):
    id: int
    doctor_id: int
    day_of_week: str 
    start_time: time
    end_time: time
