from abc import ABC, abstractmethod


class Context(ABC):
    """
    Context definition
    """

    @abstractmethod
    def arc(
        self,
        x: float,
        y: float,
        r: float,
        start_angle: float,
        end_angle: float,
    ):
        """
        Adds an arc

        Parameters
        ----------
        x : float
            x value of the end point
        y : float
            y value of the end point
        r : float
            radius value
        start_angle : float
            start angle value
        end_angle : float
            end angle value
        """
        ...

    @abstractmethod
    def rect(self, x: float, y: float, w: float, h: float):
        """
        Adds an rectangle

        Parameters
        ----------
        x : float
            x value of the top left corner of the rectangle
        y : float
            y value of the top left corner of the rectangle
        w : float
            width of the rectangle
        h : float
            height of the rectangle
        """
        ...

    @abstractmethod
    def move_to(self, x: float, y: float):
        """
        Moves to a specific point

        Parameters
        ----------
        x : float
            x value of the end point
        y : float
            y value of the end point
        """
        ...

    @abstractmethod
    def line_to(self, x: float, y: float):
        """
        Makes a line

        Parameters
        ----------
        x : float
            x value of the end point
        y : float
            y value of the end point
        """
        ...

    @abstractmethod
    def close_path(self):
        """
        Closes the path
        """
        ...
