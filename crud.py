import math
from sqlalchemy.orm import Session
from models import Address
from schemas import AddressCreate, AddressUpdate

def create_address(db: Session, address: AddressCreate):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def update_address(db: Session, address_id: int, address: AddressUpdate):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if not db_address:
        return None
    for key, value in address.dict().items():
        setattr(db_address, key, value)
    db.commit()
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if not db_address:
        return None
    db.delete(db_address)
    db.commit()
    return db_address

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_addresses_within_distance(db: Session, lat, lon, distance_km):
    addresses = db.query(Address).all()
    return [
        a for a in addresses
        if haversine(lat, lon, a.latitude, a.longitude) <= distance_km
    ]

