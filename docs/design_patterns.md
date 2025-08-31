---
title: Design Patterns
---

# Design Patterns

Design patterns are reusable solutions to common software design problems. They provide a shared vocabulary and help create maintainable, scalable code.

---

## 1. Creational Patterns

### Singleton Pattern

**What it is**: Ensures a class has only one instance and provides global access to it.

**Why Singleton is NOT just a constant**:
- **Constants are static values** that don't change and don't have behavior
- **Singleton is a class instance** that can have state, methods, and complex behavior
- **Constants are created at compile time** and exist throughout program execution
- **Singleton can be lazy-initialized** (only created when first needed)
- **Constants don't maintain state** between operations
- **Singleton can have mutable state** that changes over time
- **Constants can't be mocked** or replaced for testing
- **Singleton can implement interfaces** and be polymorphic

**Real-world analogy**: Think of a **constant** as a street sign (fixed, unchanging) vs. a **Singleton** as a traffic light controller (has state, behavior, and can change over time).

**When to use**: 
- Database connections (needs connection pooling, state management)
- Logger instances (needs to maintain log levels, handlers, state)
- Configuration managers (needs to load config, cache values, handle updates)
- Cache managers (needs to maintain cache state, eviction policies)
- Service locators (needs to manage service instances, lifecycle)
- Thread pools (needs to manage worker threads, queue state)

**Implementation**:
```python
class Singleton:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Prevent multiple initializations
        if not self._initialized:
            self._initialized = True
            self._data = {}
            self._counter = 0
    
    def set_data(self, key, value):
        self._data[key] = value
        self._counter += 1
    
    def get_data(self, key):
        return self._data.get(key)
    
    def get_counter(self):
        return self._counter

# Alternative with decorator
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self):
        self.connection_string = "db://localhost:5432"
        self.connection_pool = []
        self.active_connections = 0
    
    def get_connection(self):
        if not self.connection_pool:
            # Create new connection
            self.active_connections += 1
            return f"Connection_{self.active_connections}"
        return self.connection_pool.pop()
    
    def return_connection(self, connection):
        self.connection_pool.append(connection)
    
    def get_stats(self):
        return {
            'pool_size': len(self.connection_pool),
            'active_connections': self.active_connections
        }

# Thread-safe Singleton (Python 3.7+)
import threading
from typing import Optional

class ThreadSafeSingleton:
    _instance: Optional['ThreadSafeSingleton'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'ThreadSafeSingleton':
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking pattern
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**Advanced Singleton Patterns**:

**1. Monostate Pattern** (Shared State):
```python
class Monostate:
    _shared_state = {}
    
    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self._shared_state['data'] = {}
            self._shared_state['counter'] = 0
    
    def set_data(self, key, value):
        self._shared_state['data'][key] = value
        self._shared_state['counter'] += 1
    
    def get_data(self, key):
        return self._shared_state['data'].get(key)
```

**2. Borg Pattern** (Python-specific):
```python
class Borg:
    _shared_state = {}
    
    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self._shared_state['data'] = {}
            self._shared_state['counter'] = 0
```

**3. Singleton Registry** (Multiple Singletons):
```python
class SingletonRegistry:
    _instances = {}
    
    @classmethod
    def get_instance(cls, class_name):
        if class_name not in cls._instances:
            cls._instances[class_name] = type(class_name, (), {})()
        return cls._instances[class_name]
    
    @classmethod
    def clear(cls):
        cls._instances.clear()

# Usage
logger = SingletonRegistry.get_instance('Logger')
cache = SingletonRegistry.get_instance('Cache')
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - ✅ **Guarantees single instance** across the entire application
  - ✅ **Lazy initialization** (only created when first needed)
  - ✅ **Global access point** for shared resources
  - ✅ **Resource management** (connection pooling, caching)
  - ✅ **State persistence** across multiple calls
  - ✅ **Configuration management** (load once, use everywhere)
- **Costs**: 
  - ❌ **Global state** (hard to test and debug)
  - ❌ **Violates single responsibility principle** (manages both creation and behavior)
  - ❌ **Can be difficult to mock** in unit tests
  - ❌ **Tight coupling** (hard to replace or extend)
  - ❌ **Memory leaks** if not properly managed
  - ❌ **Thread safety issues** in multi-threaded environments
- **Use when**: 
  - You need exactly one instance and global access
  - The instance needs to maintain state over time
  - Resource management is critical (connections, caches)
  - Configuration needs to be shared across the application

**Anti-patterns to avoid**:
- **God Object**: Don't make the Singleton do everything
- **Tight Coupling**: Don't force other classes to depend on the Singleton
- **Global Mutable State**: Be careful with shared state that can change
- **Overuse**: Don't use Singleton for every class that should have one instance

**Testing Strategies**:
```python
# Reset Singleton for testing
class TestableSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset the singleton instance (for testing)"""
        cls._instance = None

# In tests
def test_singleton():
    # Reset before each test
    TestableSingleton.reset()
    instance1 = TestableSingleton()
    instance2 = TestableSingleton()
    assert instance1 is instance2
```

**Real-world Examples**:

**1. Database Connection Pool**:
```python
@singleton
class DatabasePool:
    def __init__(self):
        self.connections = []
        self.max_connections = 10
        self.active_connections = 0
    
    def get_connection(self):
        if self.connections:
            return self.connections.pop()
        elif self.active_connections < self.max_connections:
            self.active_connections += 1
            return self._create_connection()
        else:
            raise Exception("No available connections")
    
    def return_connection(self, connection):
        self.connections.append(connection)
    
    def _create_connection(self):
        # Create new database connection
        return f"DB_Connection_{self.active_connections}"
```

**2. Configuration Manager**:
```python
@singleton
class ConfigManager:
    def __init__(self):
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        # Load from file, environment, etc.
        self._config = {
            'database_url': 'postgresql://localhost:5432/mydb',
            'redis_url': 'redis://localhost:6379',
            'log_level': 'INFO',
            'max_workers': 4
        }
    
    def get(self, key, default=None):
        return self._config.get(key, default)
    
    def set(self, key, value):
        self._config[key] = value
        # Could also persist to file/database
    
    def reload(self):
        self._load_config()
```

**3. Logger with State**:
```python
@singleton
class Logger:
    def __init__(self):
        self.log_level = 'INFO'
        self.handlers = []
        self.log_history = []
    
    def set_level(self, level):
        self.log_level = level
    
    def add_handler(self, handler):
        self.handlers.append(handler)
    
    def log(self, level, message):
        if self._should_log(level):
            timestamp = datetime.now()
            log_entry = {'level': level, 'message': message, 'timestamp': timestamp}
            self.log_history.append(log_entry)
            
            for handler in self.handlers:
                handler.handle(log_entry)
    
    def _should_log(self, level):
        levels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4}
        return levels.get(level, 0) >= levels.get(self.log_level, 0)
    
    def get_history(self):
        return self.log_history.copy()
```

**When NOT to use Singleton**:
- **Simple configuration**: Use environment variables or config files
- **Stateless utilities**: Use static methods or utility classes
- **Testable code**: Prefer dependency injection
- **Multiple instances needed**: Use factory pattern instead
- **Temporary state**: Use regular objects with proper lifecycle management

---

### Factory Pattern

**What it is**: Creates objects without specifying their exact class.

**When to use**:
- Object creation depends on runtime conditions
- You want to delegate object creation to subclasses
- You want to create families of related objects

**Implementation**:
```python
from abc import ABC, abstractmethod

# Abstract product
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

# Concrete products
class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

# Factory
class AnimalFactory:
    def create_animal(self, animal_type):
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

# Usage
factory = AnimalFactory()
dog = factory.create_animal("dog")
print(dog.speak())  # Output: Woof!
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Encapsulates object creation logic
  - Easy to add new product types
  - Follows open/closed principle
- **Costs**: 
  - Adds complexity
  - Can lead to many small classes
- **Use when**: Object creation logic is complex or varies

---

### Builder Pattern

**What it is**: Constructs complex objects step by step.

**When to use**:
- Objects with many optional parameters
- Objects that require different construction steps
- Immutable objects

**Implementation**:
```python
class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
    
    def __str__(self):
        return f"Computer(CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}, GPU: {self.gpu})"

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()
    
    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self
    
    def set_ram(self, ram):
        self.computer.ram = ram
        return self
    
    def set_storage(self, storage):
        self.computer.storage = storage
        return self
    
    def set_gpu(self, gpu):
        self.computer.gpu = gpu
        return self
    
    def build(self):
        return self.computer

# Usage
computer = (ComputerBuilder()
           .set_cpu("Intel i7")
           .set_ram("16GB")
           .set_storage("1TB SSD")
           .set_gpu("RTX 3080")
           .build())
print(computer)
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Fluent interface
  - Immutable objects
  - Clear construction process
- **Costs**: 
  - More code
  - Can be overkill for simple objects
- **Use when**: Objects have many optional parameters or complex construction

---

## 2. Structural Patterns

### Adapter Pattern

**What it is**: Allows incompatible interfaces to work together.

**When to use**:
- Integrating third-party libraries
- Making old code work with new interfaces
- Supporting multiple data formats

**Implementation**:
```python
# Old interface
class OldPaymentSystem:
    def make_payment(self, amount, currency):
        print(f"Paid {amount} {currency} using old system")

# New interface
class PaymentProcessor:
    def process_payment(self, payment_data):
        pass

# Adapter
class PaymentAdapter(PaymentProcessor):
    def __init__(self, old_system):
        self.old_system = old_system
    
    def process_payment(self, payment_data):
        amount = payment_data.get('amount')
        currency = payment_data.get('currency', 'USD')
        self.old_system.make_payment(amount, currency)

# Usage
old_system = OldPaymentSystem()
adapter = PaymentAdapter(old_system)
payment_data = {'amount': 100, 'currency': 'USD'}
adapter.process_payment(payment_data)
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Integrates incompatible systems
  - Reuses existing code
  - Follows open/closed principle
- **Costs**: 
  - Adds complexity
  - Can create tight coupling
- **Use when**: You need to integrate incompatible interfaces

---

### Decorator Pattern

**What it is**: Adds behavior to objects dynamically without changing their class.

**When to use**:
- Adding features to objects at runtime
- Avoiding subclass explosion
- Implementing cross-cutting concerns

**Implementation**:
```python
from abc import ABC, abstractmethod

# Component interface
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

# Concrete component
class SimpleCoffee(Coffee):
    def cost(self):
        return 2.0
    
    def description(self):
        return "Simple coffee"

# Base decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee
    
    def cost(self):
        return self._coffee.cost()
    
    def description(self):
        return self._coffee.description()

# Concrete decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 0.5
    
    def description(self):
        return self._coffee.description() + ", milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 0.2
    
    def description(self):
        return self._coffee.description() + ", sugar"

# Usage
coffee = SimpleCoffee()
coffee_with_milk = MilkDecorator(coffee)
coffee_with_milk_and_sugar = SugarDecorator(coffee_with_milk)

print(f"{coffee_with_milk_and_sugar.description()}: ${coffee_with_milk_and_sugar.cost()}")
# Output: Simple coffee, milk, sugar: $2.7
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Flexible behavior composition
  - Follows single responsibility principle
  - Easy to add new behaviors
- **Costs**: 
  - Can create many small objects
  - Complex object hierarchies
- **Use when**: You need to add behavior dynamically

---

### Facade Pattern

**What it is**: Provides a simplified interface to a complex subsystem.

**When to use**:
- Simplifying complex APIs
- Providing a unified interface to multiple subsystems
- Reducing dependencies between client and subsystem

**Implementation**:
```python
# Complex subsystems
class AudioSystem:
    def turn_on(self):
        print("Audio system on")
    
    def set_volume(self, level):
        print(f"Volume set to {level}")

class VideoSystem:
    def turn_on(self):
        print("Video system on")
    
    def set_resolution(self, resolution):
        print(f"Resolution set to {resolution}")

class LightingSystem:
    def dim_lights(self):
        print("Lights dimmed")

# Facade
class HomeTheaterFacade:
    def __init__(self):
        self.audio = AudioSystem()
        self.video = VideoSystem()
        self.lighting = LightingSystem()
    
    def watch_movie(self):
        print("=== Starting Movie Mode ===")
        self.lighting.dim_lights()
        self.video.turn_on()
        self.video.set_resolution("4K")
        self.audio.turn_on()
        self.audio.set_volume(8)
        print("Movie mode ready!")
    
    def end_movie(self):
        print("=== Ending Movie Mode ===")
        # Turn off systems...

# Usage
theater = HomeTheaterFacade()
theater.watch_movie()
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Simplifies complex interfaces
  - Reduces coupling
  - Easy to use
- **Costs**: 
  - Can become a "god object"
  - Hides complexity
- **Use when**: You need to simplify complex subsystem interactions

---

## 3. Behavioral Patterns

### Observer Pattern

**What it is**: Defines a one-to-many dependency between objects.

**When to use**:
- Event handling systems
- Model-View architectures
- Publish-subscribe systems

**Implementation**:
```python
from abc import ABC, abstractmethod

# Subject interface
class Subject(ABC):
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self, data):
        for observer in self._observers:
            observer.update(data)

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass

# Concrete subject
class NewsAgency(Subject):
    def publish_news(self, news):
        print(f"Publishing: {news}")
        self.notify(news)

# Concrete observers
class NewsChannel(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, news):
        print(f"{self.name} received: {news}")

class NewsWebsite(Observer):
    def __init__(self, url):
        self.url = url
    
    def update(self, news):
        print(f"{self.url} updated with: {news}")

# Usage
agency = NewsAgency()
channel1 = NewsChannel("CNN")
channel2 = NewsChannel("BBC")
website = NewsWebsite("news.com")

agency.attach(channel1)
agency.attach(channel2)
agency.attach(website)

agency.publish_news("Breaking: AI solves all problems!")
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Loose coupling
  - Easy to add/remove observers
  - Supports broadcast communication
- **Costs**: 
  - Can cause memory leaks
  - Order of notifications not guaranteed
  - Can lead to complex update chains
- **Use when**: You need loose coupling between objects

---

### Strategy Pattern

**What it is**: Defines a family of algorithms and makes them interchangeable.

**When to use**:
- Multiple algorithms for the same task
- Algorithm selection at runtime
- Avoiding complex conditional statements

**Implementation**:
```python
from abc import ABC, abstractmethod

# Strategy interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# Concrete strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number):
        self.card_number = card_number
    
    def pay(self, amount):
        print(f"Paid ${amount} using credit card ending in {self.card_number[-4:]}")

class PayPalPayment(PaymentStrategy):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        print(f"Paid ${amount} using PayPal account {self.email}")

class BitcoinPayment(PaymentStrategy):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def pay(self, amount):
        print(f"Paid ${amount} using Bitcoin wallet {self.wallet_address[:8]}...")

# Context
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item, price):
        self.items.append((item, price))
    
    def set_payment_strategy(self, strategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        total = sum(price for _, price in self.items)
        if self.payment_strategy:
            self.payment_strategy.pay(total)
            self.items.clear()
        else:
            print("Please select a payment method")

# Usage
cart = ShoppingCart()
cart.add_item("Laptop", 999)
cart.add_item("Mouse", 25)

# Choose payment strategy
cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456"))
cart.checkout()

cart.add_item("Keyboard", 75)
cart.set_payment_strategy(PayPalPayment("user@example.com"))
cart.checkout()
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Easy to add new algorithms
  - Eliminates conditional statements
  - Follows open/closed principle
- **Costs**: 
  - More classes
  - Can be overkill for simple cases
- **Use when**: You have multiple algorithms for the same task

---

### Command Pattern

**What it is**: Encapsulates a request as an object.

**When to use**:
- Undo/redo functionality
- Queue operations
- Logging requests
- Remote procedure calls

**Implementation**:
```python
from abc import ABC, abstractmethod

# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

# Concrete commands
class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()

class LightOffCommand(Command):
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()
    
    def undo(self):
        self.light.turn_on()

# Receiver
class Light:
    def __init__(self, location):
        self.location = location
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print(f"{self.location} light is ON")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.location} light is OFF")

# Invoker
class RemoteControl:
    def __init__(self):
        self.commands = {}
        self.undo_stack = []
    
    def set_command(self, button, command):
        self.commands[button] = command
    
    def press_button(self, button):
        if button in self.commands:
            command = self.commands[button]
            command.execute()
            self.undo_stack.append(command)
    
    def press_undo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.undo()

# Usage
living_room_light = Light("Living Room")
kitchen_light = Light("Kitchen")

remote = RemoteControl()
remote.set_command("1", LightOnCommand(living_room_light))
remote.set_command("2", LightOffCommand(living_room_light))
remote.set_command("3", LightOnCommand(kitchen_light))

remote.press_button("1")  # Turn on living room light
remote.press_button("3")  # Turn on kitchen light
remote.press_undo()       # Undo last command
```

**Cost-Benefit Analysis**:
- **Benefits**: 
  - Supports undo/redo
  - Easy to queue operations
  - Decouples request from execution
- **Costs**: 
  - More classes
  - Can be complex for simple operations
- **Use when**: You need undo/redo or command queuing

---

## 4. Pattern Selection Guidelines

### When to Use Each Pattern

| Pattern | Use When | Avoid When |
|---------|----------|------------|
| **Singleton** | Need single instance, global access | Want testable, flexible code |
| **Factory** | Object creation varies, complex logic | Simple object creation |
| **Builder** | Many optional parameters, immutable objects | Simple objects with few parameters |
| **Adapter** | Integrating incompatible interfaces | Can modify existing code |
| **Decorator** | Adding behavior dynamically | Behavior is fixed |
| **Facade** | Simplifying complex subsystems | Simple, direct interactions |
| **Observer** | Loose coupling, event handling | Tight coupling is acceptable |
| **Strategy** | Multiple algorithms, runtime selection | Single algorithm, compile-time selection |
| **Command** | Undo/redo, queuing, logging | Simple, direct method calls |

### Cost-Benefit Summary

| Pattern | Complexity Cost | Flexibility Benefit | Maintainability Benefit |
|---------|----------------|-------------------|------------------------|
| **Singleton** | Low | Low | Low |
| **Factory** | Medium | High | High |
| **Builder** | Medium | High | Medium |
| **Adapter** | Low | Medium | Medium |
| **Decorator** | Medium | High | High |
| **Facade** | Low | Medium | High |
| **Observer** | Medium | High | Medium |
| **Strategy** | Medium | High | High |
| **Command** | High | High | High |

---

## 5. Anti-Patterns to Avoid

### God Object
- **Problem**: One class does everything
- **Solution**: Break into smaller, focused classes
- **Use**: Single responsibility principle

### Singleton Abuse
- **Problem**: Using singleton for everything
- **Solution**: Consider dependency injection
- **Use**: Only when you truly need one instance

### Over-Engineering
- **Problem**: Using patterns when not needed
- **Solution**: Start simple, add patterns as needed
- **Use**: YAGNI principle (You Aren't Gonna Need It)

---

*Design patterns are tools, not rules. Use them when they solve real problems, not just because they exist. The best pattern is often the simplest one that works.*
