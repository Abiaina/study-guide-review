---
title: Programming Languages & Tools
---

# Programming Languages & Tools

*Deep dive into Python, Node.js, Bash scripting, and React with advanced patterns, practical examples, and interview essentials.*

---

## Python Deep Dive

### Advanced Patterns

#### Decorators
```python
# Function decorator
def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done"

# Class decorator
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Creating database connection...")

# Parameterized decorator
def retry(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def unreliable_api_call():
    import random
    if random.random() < 0.7:
        raise Exception("API failed")
    return "Success"
```

#### Context Managers
```python
# Custom context manager
class DatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None
    
    def __enter__(self):
        print(f"Connecting to {self.host}:{self.port}")
        self.connection = f"Connection to {self.host}:{self.port}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing connection to {self.host}:{self.port}")
        self.connection = None
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False  # Don't suppress exceptions

# Usage
with DatabaseConnection("localhost", 5432) as conn:
    print(f"Using connection: {conn}")
    # Database operations here

# Context manager with contextlib
from contextlib import contextmanager

@contextmanager
def file_handler(filename, mode='r'):
    file = open(filename, mode)
    try:
        yield file
    finally:
        file.close()

# Usage
with file_handler('data.txt', 'w') as f:
    f.write('Hello, World!')
```

#### Async/Await Patterns
```python
import asyncio
import aiohttp
import time

# Basic async function
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Async context manager
class AsyncDatabasePool:
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.connections = asyncio.Queue(maxsize=max_connections)
    
    async def __aenter__(self):
        # Initialize connections
        for i in range(self.max_connections):
            await self.connections.put(f"Connection {i}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Clean up connections
        while not self.connections.empty():
            await self.connections.get()
    
    async def get_connection(self):
        return await self.connections.get()
    
    async def return_connection(self, conn):
        await self.connections.put(conn)

# Concurrent execution
async def process_multiple_urls(urls):
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Async generator
async def async_range(start, end):
    for i in range(start, end):
        await asyncio.sleep(0.1)  # Simulate async work
        yield i

# Usage
async def main():
    urls = ['http://example.com', 'http://example.org', 'http://example.net']
    results = await process_multiple_urls(urls)
    
    async with AsyncDatabasePool() as pool:
        conn = await pool.get_connection()
        # Use connection
        await pool.return_connection(conn)
    
    async for i in async_range(0, 10):
        print(f"Processing {i}")

# Run async function
asyncio.run(main())
```

#### Metaclasses and Descriptors
```python
# Metaclass for singleton pattern
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        print("Creating database...")

# Descriptor for property validation
class ValidatedProperty:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be <= {self.max_value}")
        instance.__dict__[self.name] = value

class User:
    age = ValidatedProperty(min_value=0, max_value=150)
    score = ValidatedProperty(min_value=0, max_value=100)
    
    def __init__(self, age, score):
        self.age = age
        self.score = score
```

### Python Interview Essentials

#### Common Patterns
```python
# Factory pattern
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        animals = {
            'dog': Dog,
            'cat': Cat
        }
        return animals.get(animal_type, Animal)()

# Observer pattern
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, data):
        for observer in self._observers:
            observer.update(data)

class Observer:
    def update(self, data):
        print(f"Received: {data}")

# Usage
subject = Subject()
observer1 = Observer()
observer2 = Observer()
subject.attach(observer1)
subject.attach(observer2)
subject.notify("Hello observers!")
```

#### Performance Optimization
```python
# Use __slots__ for memory optimization
class Point:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Use functools.lru_cache for memoization
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Use collections.defaultdict for cleaner code
from collections import defaultdict

# Instead of this:
word_count = {}
for word in words:
    if word not in word_count:
        word_count[word] = 0
    word_count[word] += 1

# Use this:
word_count = defaultdict(int)
for word in words:
    word_count[word] += 1
```

---

## Node.js Deep Dive

### Event Loop and Asynchronous Patterns

#### Understanding the Event Loop
```javascript
// Event loop phases
console.log('1. Start');

setTimeout(() => {
    console.log('2. Timer phase');
}, 0);

setImmediate(() => {
    console.log('3. Check phase');
});

process.nextTick(() => {
    console.log('4. Next tick queue');
});

Promise.resolve().then(() => {
    console.log('5. Microtask queue');
});

console.log('6. End');

// Output order: 1, 6, 4, 5, 2, 3
```

#### Streams and Backpressure
```javascript
const fs = require('fs');
const { Transform } = require('stream');

// Custom transform stream
class UpperCaseTransform extends Transform {
    constructor() {
        super({ objectMode: true });
    }
    
    _transform(chunk, encoding, callback) {
        const upperChunk = chunk.toString().toUpperCase();
        this.push(upperChunk);
        callback();
    }
}

// File processing with streams
const readStream = fs.createReadStream('input.txt', { 
    highWaterMark: 64 * 1024 // 64KB chunks
});

const writeStream = fs.createWriteStream('output.txt');

const transformStream = new UpperCaseTransform();

// Handle backpressure
readStream.on('data', (chunk) => {
    const canContinue = writeStream.write(chunk);
    if (!canContinue) {
        readStream.pause();
    }
});

writeStream.on('drain', () => {
    readStream.resume();
});

// Pipe with error handling
readStream
    .pipe(transformStream)
    .pipe(writeStream)
    .on('error', (err) => {
        console.error('Stream error:', err);
    })
    .on('finish', () => {
        console.log('Processing complete');
    });
```

#### Async Patterns
```javascript
// Promise patterns
class PromiseUtils {
    static delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    static timeout(promise, ms) {
        return Promise.race([
            promise,
            new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Timeout')), ms)
            )
        ]);
    }
    
    static retry(fn, maxAttempts = 3, delay = 1000) {
        return async function(...args) {
            let lastError;
            for (let attempt = 1; attempt <= maxAttempts; attempt++) {
                try {
                    return await fn(...args);
                } catch (error) {
                    lastError = error;
                    if (attempt === maxAttempts) break;
                    await PromiseUtils.delay(delay * attempt);
                }
            }
            throw lastError;
        };
    }
}

// Async generator
async function* asyncGenerator() {
    for (let i = 0; i < 5; i++) {
        await PromiseUtils.delay(100);
        yield i;
    }
}

// Usage
(async () => {
    for await (const value of asyncGenerator()) {
        console.log(value);
    }
})();

// Worker threads for CPU-intensive tasks
const { Worker, isMainThread, parentPort } = require('worker_threads');

if (isMainThread) {
    const worker = new Worker(__filename);
    
    worker.on('message', (result) => {
        console.log('Result:', result);
    });
    
    worker.postMessage({ data: [1, 2, 3, 4, 5] });
} else {
    parentPort.on('message', (message) => {
        const result = message.data.reduce((sum, num) => sum + num, 0);
        parentPort.postMessage(result);
    });
}
```

#### Express/Fastify Patterns
```javascript
// Express middleware pattern
const express = require('express');
const app = express();

// Authentication middleware
const authenticate = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
        return res.status(401).json({ error: 'No token provided' });
    }
    
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        res.status(401).json({ error: 'Invalid token' });
    }
};

// Error handling middleware
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ 
        error: 'Something went wrong!',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
};

// Rate limiting middleware
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP'
});

// Route organization
const userRoutes = require('./routes/users');
const productRoutes = require('./routes/products');

app.use('/api/users', authenticate, userRoutes);
app.use('/api/products', productRoutes);
app.use(errorHandler);

// Fastify example
const fastify = require('fastify')({ logger: true });

// Plugin system
fastify.register(require('fastify-jwt'), {
    secret: process.env.JWT_SECRET
});

fastify.register(require('fastify-cors'), {
    origin: true
});

// Route with validation
const userSchema = {
    type: 'object',
    properties: {
        name: { type: 'string', minLength: 1 },
        email: { type: 'string', format: 'email' }
    },
    required: ['name', 'email']
};

fastify.post('/users', {
    schema: {
        body: userSchema
    }
}, async (request, reply) => {
    const { name, email } = request.body;
    // Create user logic
    return { id: 1, name, email };
});
```

### NPM Ecosystem Best Practices
```javascript
// Package.json scripts
{
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "build": "webpack --mode production",
    "docker:build": "docker build -t myapp .",
    "docker:run": "docker run -p 3000:3000 myapp"
  }
}

// Environment configuration
require('dotenv').config();

const config = {
    port: process.env.PORT || 3000,
    database: {
        url: process.env.DATABASE_URL,
        pool: {
            min: parseInt(process.env.DB_POOL_MIN) || 5,
            max: parseInt(process.env.DB_POOL_MAX) || 20
        }
    },
    redis: {
        url: process.env.REDIS_URL
    }
};

// Dependency injection
class UserService {
    constructor(database, cache) {
        this.database = database;
        this.cache = cache;
    }
    
    async getUser(id) {
        // Check cache first
        const cached = await this.cache.get(`user:${id}`);
        if (cached) return JSON.parse(cached);
        
        // Fetch from database
        const user = await this.database.query('SELECT * FROM users WHERE id = ?', [id]);
        
        // Cache for 5 minutes
        await this.cache.setex(`user:${id}`, 300, JSON.stringify(user));
        
        return user;
    }
}
```

---

## Bash Scripting Deep Dive

### System Administration Scripts

#### Process Management
```bash
#!/bin/bash

# Process monitoring script
monitor_process() {
    local process_name="$1"
    local max_cpu="$2"
    local max_memory="$3"
    
    while true; do
        # Get process info
        local pid=$(pgrep "$process_name")
        if [ -z "$pid" ]; then
            echo "$(date): Process $process_name not found"
            sleep 30
            continue
        fi
        
        # Get CPU and memory usage
        local cpu_usage=$(ps -p "$pid" -o %cpu --no-headers)
        local memory_usage=$(ps -p "$pid" -o %mem --no-headers)
        
        # Check thresholds
        if (( $(echo "$cpu_usage > $max_cpu" | bc -l) )); then
            echo "$(date): High CPU usage: ${cpu_usage}%"
            # Send alert or restart process
        fi
        
        if (( $(echo "$memory_usage > $max_memory" | bc -l) )); then
            echo "$(date): High memory usage: ${memory_usage}%"
            # Send alert or restart process
        fi
        
        sleep 60
    done
}

# Usage
monitor_process "nginx" 80 90
```

#### Log Analysis
```bash
#!/bin/bash

# Log analyzer
analyze_logs() {
    local log_file="$1"
    local output_file="$2"
    
    echo "Log Analysis Report - $(date)" > "$output_file"
    echo "================================" >> "$output_file"
    
    # Top IP addresses
    echo "Top 10 IP Addresses:" >> "$output_file"
    grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" "$log_file" | \
        sort | uniq -c | sort -nr | head -10 >> "$output_file"
    
    echo "" >> "$output_file"
    
    # Top user agents
    echo "Top 10 User Agents:" >> "$output_file"
    grep -oE "Mozilla/[^ ]*" "$log_file" | \
        sort | uniq -c | sort -nr | head -10 >> "$output_file"
    
    echo "" >> "$output_file"
    
    # Error analysis
    echo "Error Analysis:" >> "$output_file"
    grep -i "error\|exception\|fail" "$log_file" | \
        wc -l | xargs echo "Total errors:" >> "$output_file"
    
    # Response time analysis
    echo "Response Time Analysis:" >> "$output_file"
    grep -oE "response_time=[0-9.]+" "$log_file" | \
        sed 's/response_time=//' | \
        awk '{sum+=$1; count++} END {print "Average response time: " sum/count "ms"}' >> "$output_file"
}

# Usage
analyze_logs "/var/log/nginx/access.log" "log_report.txt"
```

#### Backup and Automation
```bash
#!/bin/bash

# Automated backup script
backup_database() {
    local db_name="$1"
    local backup_dir="$2"
    local retention_days="$3"
    
    # Create backup directory
    mkdir -p "$backup_dir"
    
    # Generate backup filename with timestamp
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$backup_dir/${db_name}_${timestamp}.sql"
    
    # Create backup
    if mysqldump -u root -p "$db_name" > "$backup_file"; then
        echo "$(date): Backup created: $backup_file"
        
        # Compress backup
        gzip "$backup_file"
        echo "$(date): Backup compressed: ${backup_file}.gz"
        
        # Clean old backups
        find "$backup_dir" -name "${db_name}_*.sql.gz" -mtime +"$retention_days" -delete
        echo "$(date): Old backups cleaned"
    else
        echo "$(date): Backup failed for $db_name"
        return 1
    fi
}

# System health check
system_health_check() {
    echo "System Health Check - $(date)"
    echo "================================"
    
    # Disk usage
    echo "Disk Usage:"
    df -h | grep -E '^/dev/'
    
    echo ""
    
    # Memory usage
    echo "Memory Usage:"
    free -h
    
    echo ""
    
    # Load average
    echo "Load Average:"
    uptime
    
    echo ""
    
    # Top processes
    echo "Top 5 CPU Processes:"
    ps aux --sort=-%cpu | head -6
    
    echo ""
    
    # Network connections
    echo "Active Network Connections:"
    netstat -tuln | grep LISTEN
}

# Cron job setup
setup_cron_jobs() {
    # Add backup job (daily at 2 AM)
    (crontab -l 2>/dev/null; echo "0 2 * * * /path/to/backup_script.sh") | crontab -
    
    # Add health check job (every 5 minutes)
    (crontab -l 2>/dev/null; echo "*/5 * * * * /path/to/health_check.sh") | crontab -
    
    # Add log rotation job (weekly)
    (crontab -l 2>/dev/null; echo "0 3 * * 0 /path/to/log_rotation.sh") | crontab -
}
```

### DevOps Automation

#### Docker Management
```bash
#!/bin/bash

# Docker container management
docker_cleanup() {
    echo "Cleaning up Docker resources..."
    
    # Remove stopped containers
    docker container prune -f
    
    # Remove unused images
    docker image prune -a -f
    
    # Remove unused volumes
    docker volume prune -f
    
    # Remove unused networks
    docker network prune -f
    
    echo "Docker cleanup completed"
}

# Docker health check
docker_health_check() {
    echo "Docker Health Check"
    echo "=================="
    
    # Check running containers
    echo "Running Containers:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo ""
    
    # Check container resource usage
    echo "Container Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
    
    echo ""
    
    # Check for unhealthy containers
    echo "Unhealthy Containers:"
    docker ps --filter "health=unhealthy" --format "table {{.Names}}\t{{.Status}}"
}

# Kubernetes management
k8s_management() {
    # Scale deployment
    scale_deployment() {
        local deployment="$1"
        local replicas="$2"
        kubectl scale deployment "$deployment" --replicas="$replicas"
    }
    
    # Check pod status
    check_pods() {
        kubectl get pods --all-namespaces -o wide
    }
    
    # Check node status
    check_nodes() {
        kubectl get nodes -o wide
    }
    
    # Check resource usage
    check_resources() {
        kubectl top nodes
        kubectl top pods --all-namespaces
    }
}
```

---

## React Deep Dive

### Component Patterns

#### Higher-Order Components (HOC)
```jsx
// HOC for authentication
const withAuth = (WrappedComponent) => {
    return class extends React.Component {
        constructor(props) {
            super(props);
            this.state = {
                isAuthenticated: false,
                user: null,
                loading: true
            };
        }
        
        componentDidMount() {
            this.checkAuth();
        }
        
        checkAuth = async () => {
            try {
                const token = localStorage.getItem('token');
                if (token) {
                    const response = await fetch('/api/verify-token', {
                        headers: { Authorization: `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const user = await response.json();
                        this.setState({ 
                            isAuthenticated: true, 
                            user, 
                            loading: false 
                        });
                    } else {
                        this.setState({ loading: false });
                    }
                } else {
                    this.setState({ loading: false });
                }
            } catch (error) {
                console.error('Auth check failed:', error);
                this.setState({ loading: false });
            }
        };
        
        render() {
            const { isAuthenticated, user, loading } = this.state;
            
            if (loading) {
                return <div>Loading...</div>;
            }
            
            if (!isAuthenticated) {
                return <LoginPage />;
            }
            
            return <WrappedComponent {...this.props} user={user} />;
        }
    };
};

// Usage
const ProtectedDashboard = withAuth(Dashboard);
```

#### Render Props Pattern
```jsx
// Data fetcher with render props
class DataFetcher extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null,
            loading: false,
            error: null
        };
    }
    
    componentDidMount() {
        this.fetchData();
    }
    
    fetchData = async () => {
        this.setState({ loading: true, error: null });
        try {
            const response = await fetch(this.props.url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this.setState({ data, loading: false });
        } catch (error) {
            this.setState({ error: error.message, loading: false });
        }
    };
    
    render() {
        return this.props.children(this.state);
    }
}

// Usage
<DataFetcher url="/api/users">
    {({ data, loading, error }) => {
        if (loading) return <div>Loading...</div>;
        if (error) return <div>Error: {error}</div>;
        if (!data) return <div>No data</div>;
        
        return (
            <ul>
                {data.map(user => (
                    <li key={user.id}>{user.name}</li>
                ))}
            </ul>
        );
    }}
</DataFetcher>
```

#### Custom Hooks
```jsx
// Custom hook for API calls
const useApi = (url, options = {}) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    const fetchData = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            setData(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [url, JSON.stringify(options)]);
    
    useEffect(() => {
        fetchData();
    }, [fetchData]);
    
    const refetch = useCallback(() => {
        fetchData();
    }, [fetchData]);
    
    return { data, loading, error, refetch };
};

// Custom hook for local storage
const useLocalStorage = (key, initialValue) => {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error(error);
            return initialValue;
        }
    });
    
    const setValue = useCallback((value) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error(error);
        }
    }, [key, storedValue]);
    
    return [storedValue, setValue];
};

// Custom hook for form validation
const useFormValidation = (initialValues, validationSchema) => {
    const [values, setValues] = useState(initialValues);
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});
    
    const handleChange = useCallback((name, value) => {
        setValues(prev => ({ ...prev, [name]: value }));
        
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    }, [errors]);
    
    const handleBlur = useCallback((name) => {
        setTouched(prev => ({ ...prev, [name]: true }));
        
        // Validate on blur
        if (validationSchema[name]) {
            const error = validationSchema[name](values[name]);
            setErrors(prev => ({ ...prev, [name]: error }));
        }
    }, [values, validationSchema]);
    
    const validate = useCallback(() => {
        const newErrors = {};
        Object.keys(validationSchema).forEach(field => {
            const error = validationSchema[field](values[field]);
            if (error) newErrors[field] = error;
        });
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    }, [values, validationSchema]);
    
    return {
        values,
        errors,
        touched,
        handleChange,
        handleBlur,
        validate
    };
};
```

### Performance Optimization

#### React.memo and useMemo
```jsx
// Optimized component with React.memo
const ExpensiveComponent = React.memo(({ data, onAction }) => {
    // Expensive computation
    const processedData = useMemo(() => {
        console.log('Processing data...');
        return data.map(item => ({
            ...item,
            processed: item.value * 2 + Math.sqrt(item.value)
        }));
    }, [data]);
    
    return (
        <div>
            {processedData.map(item => (
                <div key={item.id}>
                    {item.name}: {item.processed}
                </div>
            ))}
        </div>
    );
});

// Virtual scrolling for large lists
const VirtualList = ({ items, itemHeight, containerHeight }) => {
    const [scrollTop, setScrollTop] = useState(0);
    
    const visibleItemCount = Math.ceil(containerHeight / itemHeight);
    const startIndex = Math.floor(scrollTop / itemHeight);
    const endIndex = Math.min(startIndex + visibleItemCount, items.length);
    
    const visibleItems = items.slice(startIndex, endIndex);
    const totalHeight = items.length * itemHeight;
    const offsetY = startIndex * itemHeight;
    
    return (
        <div 
            style={{ height: containerHeight, overflow: 'auto' }}
            onScroll={(e) => setScrollTop(e.target.scrollTop)}
        >
            <div style={{ height: totalHeight }}>
                <div style={{ transform: `translateY(${offsetY}px)` }}>
                    {visibleItems.map(item => (
                        <div key={item.id} style={{ height: itemHeight }}>
                            {item.content}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
```

#### Code Splitting and Lazy Loading
```jsx
// Lazy loading components
const LazyDashboard = React.lazy(() => import('./Dashboard'));
const LazySettings = React.lazy(() => import('./Settings'));
const LazyProfile = React.lazy(() => import('./Profile'));

// Route-based code splitting
const App = () => {
    return (
        <Router>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    <Route path="/dashboard" element={<LazyDashboard />} />
                    <Route path="/settings" element={<LazySettings />} />
                    <Route path="/profile" element={<LazyProfile />} />
                </Routes>
            </Suspense>
        </Router>
    );
};

// Dynamic imports for conditional loading
const useDynamicImport = (importFn, deps) => {
    const [Component, setComponent] = useState(null);
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {
        setLoading(true);
        importFn()
            .then(module => {
                setComponent(() => module.default);
            })
            .catch(error => {
                console.error('Dynamic import failed:', error);
            })
            .finally(() => {
                setLoading(false);
            });
    }, deps);
    
    return { Component, loading };
};

// Usage
const MyComponent = () => {
    const { Component, loading } = useDynamicImport(
        () => import('./HeavyComponent'),
        []
    );
    
    if (loading) return <div>Loading...</div>;
    if (!Component) return <div>Failed to load component</div>;
    
    return <Component />;
};
```

### State Management Patterns

#### Context API with useReducer
```jsx
// Global state management
const initialState = {
    user: null,
    theme: 'light',
    notifications: [],
    loading: false
};

const AppContext = React.createContext();

const appReducer = (state, action) => {
    switch (action.type) {
        case 'SET_USER':
            return { ...state, user: action.payload };
        case 'SET_THEME':
            return { ...state, theme: action.payload };
        case 'ADD_NOTIFICATION':
            return { 
                ...state, 
                notifications: [...state.notifications, action.payload] 
            };
        case 'REMOVE_NOTIFICATION':
            return { 
                ...state, 
                notifications: state.notifications.filter(
                    n => n.id !== action.payload 
                ) 
            };
        case 'SET_LOADING':
            return { ...state, loading: action.payload };
        default:
            return state;
    }
};

const AppProvider = ({ children }) => {
    const [state, dispatch] = useReducer(appReducer, initialState);
    
    const value = {
        ...state,
        setUser: (user) => dispatch({ type: 'SET_USER', payload: user }),
        setTheme: (theme) => dispatch({ type: 'SET_THEME', payload: theme }),
        addNotification: (notification) => 
            dispatch({ type: 'ADD_NOTIFICATION', payload: notification }),
        removeNotification: (id) => 
            dispatch({ type: 'REMOVE_NOTIFICATION', payload: id }),
        setLoading: (loading) => 
            dispatch({ type: 'SET_LOADING', payload: loading })
    };
    
    return (
        <AppContext.Provider value={value}>
            {children}
        </AppContext.Provider>
    );
};

const useApp = () => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error('useApp must be used within AppProvider');
    }
    return context;
};
```

---

## Key Takeaways

### **Python Mastery**
- **Decorators** for cross-cutting concerns and metaprogramming
- **Context managers** for resource management
- **Async/await** for concurrent programming
- **Metaclasses and descriptors** for advanced patterns

### **Node.js Expertise**
- **Event loop** understanding for performance optimization
- **Streams** for handling large data efficiently
- **Async patterns** for non-blocking operations
- **Express/Fastify** for building scalable APIs

### **Bash Scripting**
- **System administration** automation
- **Process monitoring** and management
- **Log analysis** and reporting
- **DevOps automation** with Docker and Kubernetes

### **React Patterns**
- **Component patterns** (HOC, render props, custom hooks)
- **Performance optimization** (memoization, code splitting)
- **State management** with Context API and useReducer
- **Advanced patterns** for scalable applications

*Master these patterns and you'll be well-prepared for any programming language or framework interview!*
