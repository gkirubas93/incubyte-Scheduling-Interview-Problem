from abc import ABC, abstractmethod
from typing import List
from app.database.db import DB
from app.models import Doctor, Location, DoctorLocation
from app.models.error import NotFoundException


class DoctorService(ABC):

    @abstractmethod
    def list_doctors(self) -> List[Doctor]:
        ...

    @abstractmethod
    def get_doctor(self, id: int) -> Doctor:
        ...

    @abstractmethod
    def add_doctor(self, first_name: str, last_name: str) -> int:
        """
        Returns the id of the new doctor
        """
        ...

    @abstractmethod
    def list_doctor_locations(self, doctor_id: int) -> List[Location]:
        ...


class InMemoryDoctorService(DoctorService):

    def __init__(self) -> None:
        self.doctors: List[Doctor] = []
        self.locations: List[Location] = []
        self.doctor_locations: List[DoctorLocation] = []

    def seed(self):
        self.doctors.extend([
            {'id': 0, 'first_name': 'Jane', 'last_name': 'Wright'},
            {'id': 1, 'first_name': 'Joseph', 'last_name': 'Lister'}
        ])

        self.locations.extend([
            {'id': 0, 'address': '1 Park St'},
            {'id': 1, 'address': '2 University Ave'}
        ])

        self.doctor_locations.extend([
            {'id': 0, 'doctor_id': 0, 'location_id': 0},
            {'id': 1, 'doctor_id': 1, 'location_id': 0},
            {'id': 2, 'doctor_id': 1, 'location_id': 1}
        ])

    def list_doctors(self) -> List[Doctor]:
        return self.doctors

    def get_doctor(self, id: int) -> Doctor:
        if id < 0 or id >= len(self.doctors):
            raise NotFoundException()

        return self.doctors[id]

    def add_doctor(self, first_name: str, last_name: str) -> int:
        new_doctor = Doctor(
            id=len(self.doctors),
            first_name=first_name,
            last_name=last_name
        )

        self.doctors.append(new_doctor)

        return new_doctor.id

    def list_doctor_locations(self, doctor_id: int) -> List[Location]:
        if doctor_id < 0 or doctor_id >= len(self.doctors):
            raise NotFoundException()

        location_ids = [
            doctor_loc.id
            for doctor_loc in self.doctor_locations
            if doctor_loc.id == doctor_id
        ]

        return [
            loc
            for loc in self.locations
            if loc.id in location_ids
        ]


class InDatabaseDoctorService(DoctorService):

    def __init__(self, db: DB):
        self.db = db

    def list_doctors(self) -> List[Doctor]:
        dict_result = self.db.execute(
            'SELECT id, first_name, last_name '
            'FROM doctors'
        )

        return [
            Doctor(**res) for res in dict_result
        ]

    def get_doctor(self, id: int) -> Doctor:
        dict_result = self.db.execute(
            'SELECT id, first_name, last_name '
            'FROM doctors '
            'WHERE id = ?',
            [id]
        )

        if not dict_result:
            raise NotFoundException()

        if len(dict_result) > 1:
            raise Exception('Found more than one doctor with that ID')

        return Doctor(**dict_result[0])

    def add_doctor(self, first_name: str, last_name: str) -> int:
        self.db.execute(
            'INSERT INTO doctors (first_name, last_name) '
            'VALUES (?, ?)',
            [first_name, last_name]
        )

        id = self.db.last_row_id

        assert id

        return id

    def list_doctor_locations(self, doctor_id: int) -> List[Location]:
        dict_result = self.db.execute(
            'SELECT l.id, l.address '
            'FROM doctor_locations dl '
            'INNER JOIN locations l ON dl.location_id = l.id '
            'WHERE dl.doctor_id = ?',
            [doctor_id]
        )

        return [
            Location(**res) for res in dict_result
        ]
