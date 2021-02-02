from enum import Enum

import pytest
from pipelayer import Pipeline


@pytest.mark.unit
class TestSwitch:

    @pytest.mark.happy
    def test_switch(self):
        from pipelayer import Context, Switch

        class Color(Enum):
            Red = 1
            Green = 2
            Blue = 3

        class IsRed(Enum):
            DEFAULT: int = 0
            IS_TRUE: int = 1
            IS_FALSE: int = 2

        class Car:
            color: Color = Color.Red

        class CarColor:
            @staticmethod
            def run(car: Car, context: Context) -> IsRed:
                try:
                    return IsRed.IS_TRUE if car.color is Color.Red else IsRed.IS_FALSE
                except Exception:
                    return IsRed.DEFAULT

        def car_is_red(data: Car, context: Context) -> dict:
            return {"car": "Is red."}

        switch = Switch(
            CarColor, {
                IsRed.IS_TRUE:
                    car_is_red,
                IsRed.IS_FALSE:
                    lambda d, c: {"car": "Is not red."}
            }
        )

        pipeline = Pipeline([switch])

        data = pipeline.run(Car(), Context())

        assert data == {"car": "Is red."}

        car = Car()
        car.color = Color.Green

        data = pipeline.run(car, Context())

        assert data == {"car": "Is not red."}
