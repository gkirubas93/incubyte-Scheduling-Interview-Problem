from pydantic import BaseModel

class AddDoctorRequest(BaseModel):
    first_name: str
    last_name: str