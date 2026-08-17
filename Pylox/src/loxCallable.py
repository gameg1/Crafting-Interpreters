from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import interpreter

class loxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        ...

    @abstractmethod
    def call(self, interpreter:"interpreter.Interpreter", arguments:list[object]) -> object:
        ...