from service.model.domain_model import DomainModel


class User(DomainModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str
