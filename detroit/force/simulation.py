from collections.abc import Callable
from .lcg import lcg
from math import pi, sqrt, isnan, cos, sin, inf, nan
from typing import TypeVar
from ..types import SimulationNode, Force

TForceSimulation = TypeVar("ForceSimulation", bound="ForceSimulation")

def x(d: SimulationNode) -> float:
    return d["x"]

def y(d: SimulationNode) -> float:
    return d["y"]

INITIAL_RADIUS = 10
INITIAL_ANGLE = pi * (3 - sqrt(5))

class ForceSimulation:

    def __init__(self, nodes: list[SimulationNode]):
        self._nodes = nodes
        self._alpha = 1
        self._alpha_min = 0.001
        self._alpha_decay = 1 - pow(self._alpha_min, 1 / 300)
        self._alpha_target = 0
        self._velocity_decay = 0.6
        self._forces = {}
        self._random = lcg()
        self._initialize_nodes()


    def tick(self, iterations: float | None = None) -> TForceSimulation:
        """
        Manually steps the simulation by the specified number of iterations,
        and returns the simulation. If :code:`iterations` is not specified, it
        defaults to 1 (single step).

        For each iteration, it increments the current alpha by
        :code:`(alpha_target - alpha) * alpha_decay`; then invokes each
        registered force, passing the new alpha; then decrements each node’s
        velocity by :code:`velocity * velocity_decay`; lastly increments each
        node’s position by velocity.

        This method does not dispatch events; events are only dispatched by the
        internal timer when the simulation is started automatically upon
        creation or by calling simulation.restart. The natural number of ticks
        when the simulation is started is :code:`\\lceil
        \\log(\\alpha_{\\text{min}}) / \\log(1 - \\alpha_{\\text{decay}})
        \\rceil`; by default, this is 300.

        This method can be used in conjunction with simulation.stop to compute
        a static force layout. For large graphs, static layouts should be
        computed in a web worker to avoid freezing the user interface.

        Parameters
        ----------
        iterations : float | None
            Number of iterations

        Returns
        -------
        ForceSimulation
            Itself
        """
        if iterations is None:
            iterations = 1

        for k in range(iterations):
            self._alpha += (self._alpha_target - self._alpha) * self._alpha_decay

            for force in self._forces.values():
                force(self._alpha)

            for node in self._nodes:
                if node.get("fx") is None:
                    node["vx"] *= self._velocity_decay
                    node["x"] += node["vx"]
                else:
                    node["x"] = node["fx"]
                    node["vx"] = 0

                if node.get("fy") is None:
                    node["vy"] *= self._velocity_decay
                    node["y"] += node["vy"]
                else:
                    node["y"] = node["fy"]
                    node["vy"] = 0

        return self

    def _initialize_nodes(self):
        for i, node in enumerate(self._nodes):
            node["index"] = i
            if fx := node.get("fx"):
                node["x"] = fx
            if fy := node.get("fy"):
                node["y"] = fy
            if isnan(node.get("x", nan)) or isnan(node.get("y", nan)):
                radius = INITIAL_RADIUS * sqrt(0.5 + i)
                angle = i * INITIAL_ANGLE
                node["x"] = radius * cos(angle)
                node["y"] = radius * sin(angle)
            if isnan(node.get("vx", nan)) or isnan(node.get("vy", nan)):
                node["vx"] = 0
                node["vy"] = 0

    def _initialize_force(self, force: Force) -> Force:
        if hasattr(force, "initialize"):
            force.initialize(self._nodes, self._random)
        return force

    def find(self, x: float, y: float, radius: float | None = None) -> SimulationNode:
        """
        Returns the node closest to the position :math:`(x,y)` with the given
        search radius.

        Parameters
        ----------
        x : float
            x-coordinate value of the position
        y : float
            y-coordinate value of the position
        radius : float | None
            Radius value

        Returns
        -------
        SimulationNode
            Closest node
        """
        if radius is None:
            radius = inf
        else:
            radius *= radius

        closest = None
        for node in self._nodes:
            dx = x - node["x"]
            dy = y - node["y"]
            d2 = dx * dx + dy * dy
            if d2 < radius:
                closest = node
                radius = d2

        return closest

    def set_nodes(self, nodes: list[SimulationNode]) -> TForceSimulation:
        """
        Sets the simulation's nodes to the specified array of objects,
        initializing their positions and velocities if necessary, and then
        re-initializes any bound forces; returns the simulation.

        Each node must be an dictionary (:code:`dict`). The following
        properties are assigned by the simulation:

        * **index** (:code:`int`) - the node's zero-based index into nodes
        * **x** (:code:`float`) - the node's current x-position
        * **y** (:code:`float`) - the node's current y-position
        * **vx** (:code:`float`) - the node's current x-velocity
        * **vy** (:code:`float`) - the node's current y-velocity
        * **fx** (:code:`float`) - the node's fixed x-position
        * **fy** (:code:`float`) - the node's fixed y-position

        The position :math:`(x,y)` and velocity :math:`(v_x,v_y)` may be
        subsequently modified by forces and by the simulation. If either
        :code:`vx` or :code:`vy` is :code:`nan`, the velocity is initialized to
        :math:`(0,0)`. If either :code:`x` or :code:`y` is :code:`nan`, the
        position is initialized in a `phyllotaxis arrangement
        <https://en.wikipedia.org/wiki/Phyllotaxis>`_, so chosen to ensure a
        deterministic, uniform distribution.

        At the end of each tick, after the application of any forces, a node
        with a defined :code:`node["fx"]` has :code:`node["x"]` reset to this
        value and :code:`node["vx"]` set to zero; likewise, a node with a
        defined :code:`node["fy"]` has :code:`node["y"]` reset to this value
        and :code:`node["vy"]` set to zero. To unfix a node that was previously
        fixed, set :code:`node["fx"]` and :code:`node["fy"]` to :code:`None`,
        or delete these properties.

        If the specified array of nodes is modified, such as when nodes are
        added to or removed from the simulation, this method must be called
        again with the new (or changed) array to notify the simulation and
        bound forces of the change; the simulation does not make a defensive
        copy of the specified array.

        Parameters
        ----------
        nodes : list[SimulationNode]
            Array of nodes

        Returns
        -------
        ForceSimulation
            Itself
        """
        self._nodes = nodes
        self._initialize_nodes()
        for force in self._forces.values():
            self._initialize_force(force)
        return self

    def set_alpha(self, alpha: float) -> TForceSimulation:
        """
        It decreases over time as the simulation "cools down".

        Parameters
        ----------
        alpha : float
            Alpha value

        Returns
        -------
        ForceSimulation
            Itself
        """
        self._alpha = alpha
        return self

    def set_alpha_min(self, alpha_min: float) -> TForceSimulation:
        """
        Sets the minimum alpha to the specified number in the range
        :math:`[0,1]` and returns this simulation. 

        The simulation's internal timer stops when the current alpha is less
        than the minimum alpha. The default alpha decay rate of ~0.0228
        corresponds to 300 iterations.

        Parameters
        ----------
        alpha_min : float
            Alpha minimum value

        Returns
        -------
        ForceSimulation
            Itself
        """
        self._alpha_min = alpha_min
        return self

    def set_alpha_decay(self, alpha_decay: float) -> TForceSimulation:
        """
        Sets the alpha decay rate to the specified number in the range
        :math:`[0,1]` and returns this simulation.

        The alpha decay rate determines how quickly the current alpha
        interpolates towards the desired target alpha; since the default target
        alpha is zero, by default this controls how quickly the simulation
        cools. Higher decay rates cause the simulation to stabilize more
        quickly, but risk getting stuck in a local minimum; lower values cause
        the simulation to take longer to run, but typically converge on a
        better layout. To have the simulation run forever at the current alpha,
        set the decay rate to zero; alternatively, set a target alpha greater
        than the minimum alpha.

        Parameters
        ----------
        alpha_decay : float
            Alpha decay value

        Returns
        -------
        ForceSimulation
            Itself
        """
        self._alpha_decay = alpha_decay
        return self

    def set_alpha_target(self, alpha_target: float) -> TForceSimulation:
        """
        Sets the current target alpha to the specified number in the range
        :math:`[0,1]` and returns this simulation.

        Parameters
        ----------
        alpha_target : float
            Alpha target value

        Returns
        -------
        ForceSimulation
            Itself
        """
        self._alpha_target = alpha_target
        return self

    def set_velocity_decay(self, velocity_decay: float) -> TForceSimulation:
        """
        Sets the velocity decay factor to the specified number in the range
        :math:`[0,1]` and returns this simulation.

        The decay factor is akin to atmospheric friction; after the application
        of any forces during a tick, each node's velocity is multiplied by
        :code:`1 - decay`. As with lowering the alpha decay rate, less velocity
        decay may converge on a better solution, but risks numerical
        instabilities and oscillation.

        Parameters
        ----------
        velocity_decay : float
            Velocity decay value

        Returns
        -------
        ForceSimulation
            Itself
        """
        self._velocity_decay = 1 - velocity_decay
        return self

    def set_random_source(self, random_source: Callable[[None], float]) -> TForceSimulation:
        """
        Sets the function used to generate random numbers; this should be a
        function that returns a number between 0 (inclusive) and 1 (exclusive).
        If source is not specified, returns this simulation's current random
        source which defaults to a fixed-seed `linear congruential generator
        <https://en.wikipedia.org/wiki/Linear_congruential_generator>`_.

        Parameters
        ----------
        random_source : Callable[[None], float]
            Random source function

        Returns
        -------
        ForceSimulation
            Itself
        """
        self._random = random_source
        for force in self._forces:
            self._initialize_force(force)
        return self

    def set_force(self, name: str, force: Force | None = None) -> TForceSimulation:
        """
        If :code:`force` is not :code:`None`, assigns the :code:`force` for the
        specified :code:`name` and returns this simulation. To remove the
        :code:`force` with the given :code:`name`, pass :code:`None` as the
        :code:`force`.

        Parameters
        ----------
        name : str
            Name of the force
        force : Force | None
            Force value

        Returns
        -------
        ForceSimulation
            Itself
        """
        if force is None:
            self._forces.pop(name)
        else:
            self._forces[name] = self._initialize_force(force)
        return self

    def get_alpha(self) -> float:
        return self._alpha

    def get_alpha_min(self) -> float:
        return self._alpha_min

    def get_alpha_decay(self) -> float:
        return self._alpha_decay

    def get_alpha_target(self) -> float:
        return self._alpha_target

    def get_velocity_decay(self) -> float:
        return 1 - self._velocity_decay
    
    def get_random_source(self) -> Callable[[None], float]:
        return self._random

    def get_force(self, name: str) -> Force:
        return self._forces.get(name)

    def get_nodes(self) -> list[SimulationNode]:
        return self._nodes

def force_simulation(nodes: list[SimulationNode] | None = None) -> ForceSimulation:
    """
    A force simulation implements a velocity Verlet numerical integrator for
    simulating physical forces on particles (nodes). The simulation assumes a
    constant unit time step :math:`\\Delta t = 1` for each step and a constant
    unit mass :math:`m = 1` for all particles. As a result, a force :math:`F`
    acting on a particle is equivalent to a constant acceleration a over the
    time interval :math:`\\Delta t`, and can be simulated simply by adding to
    the particle's velocity, which is then added to the particle's position.

    Parameters
    ----------
    nodes : list[SimulationNode] | None
        List of nodes

    Returns
    -------
    ForceSimulation
        Simulation object
    """
    if nodes is None:
        nodes = []
    return ForceSimulation(nodes)
