from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4


# Como administrador del sistema quiero poder visualizar las métricas de usuarios para medir el uso de la plataforma y sus servicios
# Criterios de aceptación

# CA 1: Métricas de nuevos usuarios utilizando mail y contraseña
# CA 2: Métricas de nuevos usuarios utilizando identidad federada
# CA 3: Métricas de login de usuarios utilizando mail y contraseña
# CA 4: Métricas de login de usuarios utilizando identidad federada
# CA 5: Métricas de usuarios bloqueados
# CA 6: Métricas de recupero de contraseña
# CA 7: Métricas de usuarios por zona geográfica


class MetricType(str, Enum):
    standard_user = "standard_user"
    federated_user = "federated_user"
    standard_user_login = "standard_user_login"
    federated_user_login = "federated_user_login"
    blocked_user = "blocked_user"
    password_recover = "password_recover"


class UserMetric(BaseModel):
    metric = MetricType

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "metric": "standard_user",
            }
        }
