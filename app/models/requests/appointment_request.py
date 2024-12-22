from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AppointmentRequest(BaseModel):
    doctor_id: int
    location: str
    appointment_time: datetime
    patient_name: str