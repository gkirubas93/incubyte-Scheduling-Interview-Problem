
from abc import ABC, abstractmethod
from datetime import datetime
from http.client import HTTPException
import logging
import sqlite3
from typing import List

from app.database.db import DB
from app.models.doctor import Appointment, Availability
from app.models.error import NotFoundException
from app.models.requests.appointment_request import AppointmentRequest
from app.models.requests.availability_request import AvailabilityRequest


class AvailabilityService(ABC):
    
    @abstractmethod
    def get_availability(self, doctor_id: int) -> List[Availability]:
        ...
    
    @abstractmethod
    def add_availability(self, doctor_id: int, availability: AvailabilityRequest) -> Availability:
        ...
    
    @abstractmethod
    def book_appointment(self, appointment: AppointmentRequest) -> Appointment:
        ...
    
    @abstractmethod
    def get_appointments(self, doctor_id: int) -> List[Appointment]:
        ...
    
    @abstractmethod
    def cancel_appointment(self, appointment_id: int) -> int:
        ...


class AvailabilityServiceImpl(AvailabilityService):

    def __init__(self, db: DB):
        self.db = db
        logging.basicConfig(
            level=logging.DEBUG,  # Minimum log level
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger("fastapi-app")  # Create a logger for your app

    def add_availability(self, doctor_id: int, availability: AvailabilityRequest):
        """Add availability for a doctor."""
        if not self._is_doctor_exist(doctor_id):
            return {"message": "Doctor not found."}

        start_time_str = availability.start_time.strftime('%H:%M:%S')
        end_time_str = availability.end_time.strftime('%H:%M:%S')

        if self._is_availability_exists(doctor_id, start_time_str, end_time_str):
            return {"message": "The requested time is already available."}

        try:
            self.db.execute(
                "INSERT INTO availability (doctor_id, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?)",
                (doctor_id, availability.day_of_week, start_time_str, end_time_str),
            )
            availability_id = self.db.last_row_id
            return {"id": availability_id, "message": "Availability added successfully."}
        except sqlite3.IntegrityError as e:
            return {"status": 400, "message": f"Database error: {str(e)}"}

    def get_availability(self, doctor_id: int):
        """Retrieve all availability for a doctor."""
        if not self._is_doctor_exist(doctor_id):
            return {"message": "Doctor not found."}
        results = self.db.execute(
            "SELECT id, doctor_id, day_of_week, start_time, end_time FROM availability WHERE doctor_id = ?",
            (doctor_id,),
        )
        return [Availability(**result) for result in results]

    def book_appointment(self, appointment: AppointmentRequest):
        

        """Book an appointment for a doctor."""
        if not self._is_doctor_exist(appointment.doctor_id):
            return {"message": "Doctor not found."}

        day_of_week = appointment.appointment_time.strftime('%A')  # Full name of the day (e.g., 'Saturday')
        time_str = appointment.appointment_time.strftime('%H:%M:%S')  # Time in HH:MM:SS format
        self.logger.info(f"Day of week: {day_of_week}, Time: {time_str}")
        if not self._is_doctor_available(appointment.doctor_id,day_of_week,time_str):
            return {"message": "Doctor is not available at the requested time."}

        if self._is_appointment_exists(appointment.doctor_id, time_str):
            return {"message": "The requested time is already booked."}

        try:
            appointment_time_str = appointment.appointment_time.strftime('%Y-%m-%D %H:%M:%S')
            self.db.execute(
                "INSERT INTO appointments (doctor_id, location, appointment_time, patient_name) VALUES (?, ?, ?, ?)",
                (appointment.doctor_id, appointment.location, appointment_time_str, appointment.patient_name),
            )
            appointment_id = self.db.last_row_id
            return {"id": appointment_id, "message": "Appointment booked successfully."}
        except sqlite3.IntegrityError as e:
            return {"status": 400, "message": f"Database error: {str(e)}"}

    def get_appointments(self, doctor_id: int):
        """Retrieve all appointments for a doctor."""
        if not self._is_doctor_exist(doctor_id):
            return {"message": "Doctor not found."}
        results = self.db.execute(
            "SELECT id, doctor_id, location, appointment_time, patient_name FROM appointments WHERE doctor_id = ?",
            (doctor_id,),
        )
        return [Appointment(**result) for result in results]

    def cancel_appointment(self, appointment_id: int):
        """Cancel an appointment by its ID."""
        if not self._is_appointment_exists_by_id(appointment_id):
            return {"message": "No appointment found with the given ID."}

        self.db.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        return {"message": "Appointment canceled successfully."}

    # Helper Methods

    def _is_doctor_exist(self, doctor_id: int):
        result = self.db.execute("SELECT id FROM doctors WHERE id = ?", (doctor_id,))
        return bool(result)
        # if len(result) > 1:
        #     raise Exception('Found more than one doctor with that ID')

    def _is_availability_exists(self, doctor_id: int, start_time: str, end_time: str):
        """Check if availability already exists for the given time."""
        result = self.db.execute(
            "SELECT id FROM availability WHERE doctor_id = ? AND start_time = ? AND end_time = ?",
            (doctor_id, start_time, end_time),
        )
        return bool(result)

    def _is_doctor_available(self, doctor_id: int,day_of_week: str, time: str):
        """Check if a doctor is available at the given time."""
        result = self.db.execute(
            "SELECT id FROM availability WHERE doctor_id = ? AND day_of_week = ? AND ? BETWEEN start_time AND end_time",
            (doctor_id, day_of_week.lower(), time),
        )
        self.logger.debug(f"Checking availability for doctor_id={doctor_id}, day_of_week={day_of_week}, time={time}")
        self.logger.info(f"Doctor availability: {bool(result)}")
        return bool(result)

    def _is_appointment_exists(self, doctor_id: int,time: datetime):
        """Check if an appointment already exists for the given time."""
        result = self.db.execute(
            "SELECT id FROM appointments WHERE doctor_id = ? AND appointment_time = ?",
            (doctor_id, time),
        )
        return bool(result)

    def _is_appointment_exists_by_id(self, appointment_id: int):
        """Check if an appointment exists by its ID."""
        result = self.db.execute("SELECT id FROM appointments WHERE id = ?", (appointment_id,))
        return bool(result)