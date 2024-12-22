from typing import Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from app.database.db import DB
from app.models.error import NotFoundException
from app.models import AddDoctorRequest
from app.models.requests.appointment_request import AppointmentRequest
from app.models.requests.availability_request import AvailabilityRequest
from app.services.availability_service import AvailabilityService, AvailabilityServiceImpl
from app.services.doctor_service import DoctorService, InDatabaseDoctorService, InMemoryDoctorService
from app.settings import Settings


def create_app() -> FastAPI:
    doctor_service: DoctorService
    availablity_service: AvailabilityService
    db: Optional[DB] = None
    if Settings.in_database:
        db = DB()
        db.init_if_needed()
        doctor_service = InDatabaseDoctorService(db=db)
    else:
        doctor_service = InMemoryDoctorService()
        doctor_service.seed()

    availablity_service = AvailabilityServiceImpl(db=db)
    app = FastAPI(swagger_ui_parameters={'tryItOutEnabled': True})

    @app.get('/doctors')
    def list_doctors():
        return doctor_service.list_doctors()

    @app.get('/doctors/{id}')
    async def get_doctor(id: int):
        return doctor_service.get_doctor(id)

    @app.post('/doctors')
    def add_doctor(request: AddDoctorRequest):
        id = doctor_service.add_doctor(
            first_name=request.first_name,
            last_name=request.last_name
        )

        return {
            'id': id,
            "message": "Doctor added successfully."
        }

    @app.get('/doctors/{doctor_id}/locations')
    def get_doctor_locations(doctor_id: int):
        return doctor_service.list_doctor_locations(doctor_id=doctor_id)

    # Add new endpoints here! #
    @app.post('/availability/add')
    def add_availability(request: AvailabilityRequest):
        id = availablity_service.add_availability(
            doctor_id=request.doctor_id,
            availability=request
        )
        return id
    
    @app.get('/availability/{doctor_id}')
    async def get_availability(doctor_id: int):
        return availablity_service.get_availability(doctor_id)
    
    @app.post('/appointment/add')
    def add_appointment(request: AppointmentRequest):
        id = availablity_service.book_appointment(appointment=request)
        return id

    @app.get('/appointment/{doctor_id}')
    async def get_appointments(doctor_id: int):
        return availablity_service.get_appointments(doctor_id)

    @app.post('/appointment/{appointment_id}/cancel')
    def cancel_appointment(appointment_id: int):
        return availablity_service.cancel_appointment(appointment_id)



    @app.exception_handler(NotFoundException)
    async def not_found(request: Request, exc: NotFoundException):
        return Response(status_code=404)

    @app.on_event('shutdown')
    def shutdown():
        if db:
            db.close_db()

    @app.get('/', include_in_schema=False)
    def root():
        return RedirectResponse('/docs')

    return app


app = create_app()
