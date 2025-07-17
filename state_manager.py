# state_manager.py
"""
Manages game states using a stack-based approach.

The StateManager allows for pushing new states onto the stack, popping states off,
and accessing the current active state. It also delegates event processing,
updates, and drawing to the current state.
"""
import logging

logger = logging.getLogger(__name__)

class StateManager:
    """
    Manages a stack of game states.

    Attributes:
        states: A list representing the state stack. The last element is the current state.
    """
    def __init__(self, initial_state):
        """
        Initializes the StateManager with a starting state.

        Args:
            initial_state: The first state to be added to the state stack.
        """
        self.states = [initial_state] # Initialize state stack with the initial state
        logger.debug(f"State Manager initialized with initial state: {type(initial_state).__name__}")

    def push_state(self, state):
        """
        Pushes a new state onto the top of the state stack.

        The new state becomes the current active state.

        Args:
            state: The state object to push onto the stack.
        """
        if state is None:
            logger.warning("Attempted to push a None state. Ignoring push operation.")
            return
        self.states.append(state)
        logger.debug(f"Pushed state: {type(state).__name__}. Current state stack: {[type(s).__name__ for s in self.states]}")


    def pop_state(self):
        """
        Pops the current state off the top of the stack.

        If there is more than one state in the stack, the topmost state is removed,
        and the state below it becomes the current state.
        If only one state is left, this operation does nothing (to ensure there's always a current state).
        """
        if len(self.states) > 1:
            state = self.states.pop()
            logger.debug(f"Popped state: {type(state).__name__}. Current state stack: {[type(s).__name__ for s in self.states]}")
        else:
            logger.debug("Attempted to pop state with only one state left. Ignoring pop operation to maintain a current state.")

    def current_state(self):
        """
        Returns the current active state (the state at the top of the stack).

        Returns:
            The current game state object, or None if the state stack is empty (which should not happen in normal operation).
        """
        if not self.states:
            logger.error("State stack is empty! This should not happen.")
            return None  # Should ideally not reach here in normal game flow
        return self.states[-1]

    def process_events(self, events):
        """
        Delegates event processing to the current state.

        Args:
            events: A list of pygame.event.Event objects to process.
        """
        current_state = self.current_state()
        if current_state:
            return current_state.process_events(events)
        else:
            logger.warning("No current state to process events.")
            return None

    def update(self):
        """
        Delegates update logic to the current state.
        """
        current_state = self.current_state()
        if current_state:
            current_state.update()
        else:
            logger.warning("No current state to update.")

    def draw(self):
        """
        Delegates drawing to the current state.
        """
        current_state = self.current_state()
        if current_state:
            current_state.draw()
        else:
            logger.warning("No current state to draw.")