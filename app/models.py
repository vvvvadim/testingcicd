from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, unique=True, nullable=False)


class Coffee(Base):
    __tablename__ = "coffee"

    title = Column(String(200), nullable=False)
    origin = Column(String(200))
    intensifier = Column(String(100))
    notes = Column(ARRAY(String(100)))

    def __repr__(self):
        return f"Coffee(id={self.id}),title={self.title}, origin={self.origin}, intensifier={self.intensifier}, notes={self.notes}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = "users"

    name = Column(String(50), nullable=False)
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey("coffee.id"))

    coffee = relationship("Coffee", backref="users")

    def __repr__(self):
        return f"User(id={self.id}),name={self.name},address={self.address}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
