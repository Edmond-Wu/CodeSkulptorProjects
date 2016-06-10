"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 100

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    _total_cookies = 0.0
    _current_amount = 0.0
    _current_time = 0.0
    _current_cps = 1.0
    _history = []
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_amount = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "\n" + "------------------------" + "\n" + "Total cookies: " + str(self._total_cookies) + "\n" + "Current amount: " + str(self._current_amount) + "\n" + "Current time: " + str(self._current_time) + "\n" + "Current CPS: " + str(self._current_cps) + "\n" + "History: " + str(self._history) + "\n" + "------------------------"
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_amount
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_amount >= cookies:
            return 0.0
        else:
            cookies_left = cookies - self._current_amount
            return math.ceil(cookies_left/self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._current_time += time
            self._current_amount += (self._current_cps * time)
            self._total_cookies += (self._current_cps * time)
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_amount:
            self._current_amount -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies))
            
            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    build_clone = build_info.clone()
    clicker = ClickerState()
    stop = False
    while clicker.get_time() <= duration and stop == False:
        time_left = duration - clicker.get_time()
        item = strategy(clicker.get_cookies(), clicker.get_cps(), time_left, build_clone)
        if item == None:
            clicker.wait(time_left)
            stop = True
        else:
            cost = build_clone.get_cost(item)
            if clicker.get_cookies() >= cost:
                clicker.buy_item(item, cost, build_clone.get_cps(item))
                build_clone.update_item(item)
            else:
                time_til_upgrade = clicker.time_until(cost)
                if time_til_upgrade <= time_left:
                    clicker.wait(time_til_upgrade)
                    clicker.buy_item(item, cost, build_clone.get_cps(item))
                    build_clone.update_item(item) 
                else:
                    clicker.wait(time_left)
                    stop = True
                    
    time_left = duration - clicker.get_time()
    clicker.wait(time_left)
    return clicker


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Returns the cheapest item you can afford
    """
    clone = build_info.clone()
    items = clone.build_items()
    affordability = cookies + cps * time_left
    min_item = None
    min_item_cost = float("inf")
    for element in items:
        if clone.get_cost(element) < min_item_cost and clone.get_cost(element) <= affordability:
            min_item = element
            min_item_cost = clone.get_cost(element)
    return min_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Returns the most expensive item you can afford
    """
    clone = build_info.clone()
    items = clone.build_items()
    affordability = cookies + cps * time_left
    max_item = None
    max_item_cost = float("-inf")
    for element in items:
        if clone.get_cost(element) > max_item_cost and clone.get_cost(element) <= affordability:
            max_item = element
            max_item_cost = clone.get_cost(element)
    return max_item

def strategy_best(cookies, cps, time_left, build_info):
    """
    Best strategy returning the item with the highest production
    per cost
    """
    clone = build_info.clone()
    items = clone.build_items()
    affordability = cookies + cps * time_left
    best_item = None
    max_cps_cost = float("-inf")
    for element in items:
        cps_cost = clone.get_cps(element)/clone.get_cost(element)
        if cps_cost > max_cps_cost and clone.get_cost(element) <= affordability:
            max_cps_cost = cps_cost
            best_item = element
    return best_item
        
    
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor)
    
    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

run()
