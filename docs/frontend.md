---
title: Frontend Development
---

# Frontend Development

*Master the fundamentals of modern web development, React best practices, and ace your frontend interviews.*

---

## DOM (Document Object Model)

### What is the DOM?
The DOM is a programming interface for HTML and XML documents. It represents the page as a tree structure where each node represents an object.

### DOM Manipulation Examples

#### Basic DOM Selection
```javascript
// Select elements
const element = document.getElementById('myId');
const elements = document.getElementsByClassName('myClass');
const elements = document.querySelectorAll('.myClass');
const element = document.querySelector('#myId');

// Traverse DOM
const parent = element.parentElement;
const children = element.children;
const nextSibling = element.nextElementSibling;
const prevSibling = element.previousElementSibling;
```

#### Creating and Modifying Elements
```javascript
// Create new element
const newDiv = document.createElement('div');
newDiv.textContent = 'Hello World';
newDiv.className = 'my-class';
newDiv.setAttribute('data-id', '123');

// Append to DOM
document.body.appendChild(newDiv);
element.appendChild(newDiv);

// Remove elements
element.remove();
element.parentNode.removeChild(element);

// Modify content
element.innerHTML = '<span>New content</span>';
element.textContent = 'Plain text content';
element.innerText = 'Text with formatting preserved';
```

#### Event Handling
```javascript
// Add event listener
element.addEventListener('click', function(event) {
    console.log('Clicked!', event);
});

// Remove event listener
const handler = function(event) { console.log('Clicked!'); };
element.addEventListener('click', handler);
element.removeEventListener('click', handler);

// Event delegation
document.addEventListener('click', function(event) {
    if (event.target.matches('.button')) {
        console.log('Button clicked:', event.target);
    }
});
```

### DOM Performance Best Practices
```javascript
// Batch DOM updates
const fragment = document.createDocumentFragment();
for (let i = 0; i < 1000; i++) {
    const div = document.createElement('div');
    div.textContent = `Item ${i}`;
    fragment.appendChild(div);
}
document.body.appendChild(fragment);

// Use requestAnimationFrame for animations
function animate() {
    element.style.left = (parseInt(element.style.left) + 1) + 'px';
    requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

---

## React Fundamentals

### Core Concepts

#### JSX
```jsx
{% raw %}
// JSX is syntactic sugar for React.createElement
const element = <h1>Hello, World!</h1>;

// JSX with expressions
const name = 'John';
const element = <h1>Hello, {name}!</h1>;

// JSX with attributes
const element = <div className="container" data-testid="main">Content</div>;

// JSX with children
const element = (
    <div>
        <h1>Title</h1>
        <p>Paragraph</p>
    </div>
);
{% endraw %}
```

#### Components
```jsx
{% raw %}
// Function Component
function Welcome(props) {
    return <h1>Hello, {props.name}!</h1>;
}

// Arrow Function Component
const Welcome = (props) => {
    return <h1>Hello, {props.name}!</h1>;
};

// Class Component
class Welcome extends React.Component {
    render() {
        return <h1>Hello, {this.props.name}!</h1>;
    }
}
{% endraw %}
```
{% raw %}

### React Hooks

#### useState
{% endraw %}
```jsx
{% raw %}
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    const [name, setName] = useState('John');

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Increment
            </button>
            <input 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
            />
        </div>
    );
}
{% endraw %}
```

**Advanced useState Patterns and Best Practices**:

**1. Functional Updates** (When new state depends on previous state):
```jsx
{% raw %}
function Counter() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Can lead to stale closures
    const increment = () => setCount(count + 1);
    
    // ✅ Good: Uses functional update
    const increment = () => setCount(prevCount => prevCount + 1);
    
    // ✅ Good: Multiple updates in sequence
    const incrementByThree = () => {
        setCount(prev => prev + 1);
        setCount(prev => prev + 1);
        setCount(prev => prev + 1);
    };
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={increment}>+1</button>
            <button onClick={incrementByThree}>+3</button>
        </div>
    );
}
{% endraw %}
```

**2. Object State Management** (Managing multiple related values):
```jsx
{% raw %}
function UserForm() {
    const [user, setUser] = useState({
        name: '',
        email: '',
        age: ''
    });
    
    // ❌ Bad: Mutating state directly
    const handleChange = (field, value) => {
        user[field] = value; // This mutates the original object!
        setUser(user); // React won't detect the change
    };
    
    // ✅ Good: Creating new object
    const handleChange = (field, value) => {
        setUser(prevUser => ({
            ...prevUser, // Spread previous state
            [field]: value // Update specific field
        }));
    };
    
    return (
        <form>
            <input
                value={user.name}
                onChange={(e) => handleChange('name', e.target.value)}
                placeholder="Name"
            />
            <input
                value={user.email}
                onChange={(e) => handleChange('email', e.target.value)}
                placeholder="Email"
            />
            <input
                value={user.age}
                onChange={(e) => handleChange('age', e.target.value)}
                placeholder="Age"
            />
        </form>
    );
}
{% endraw %}
```

**3. Lazy Initialization** (Expensive initial state):
```jsx
{% raw %}
function ExpensiveComponent() {
    // ❌ Bad: Expensive computation runs on every render
    const [data, setData] = useState(expensiveCalculation());
    
    // ✅ Good: Expensive computation only runs once
    const [data, setData] = useState(() => expensiveCalculation());
    
    function expensiveCalculation() {
        console.log('Running expensive calculation...');
        // Simulate expensive operation
        let result = 0;
        for (let i = 0; i < 1000000; i++) {
            result += Math.sqrt(i);
        }
        return result;
    }
    
    return <div>Result: {data}</div>;
}
{% endraw %}
```

**Common useState Mistakes and Solutions**:

**Mistake 1: Stale Closures in Event Handlers**
```jsx
{% raw %}
function StaleClosureExample() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Creates a new function on every render
    const handleClick = () => {
        setTimeout(() => {
            console.log(count); // Always logs the initial value!
        }, 1000);
    };
    
    // ✅ Good: Use functional update
    const handleClick = () => {
        setTimeout(() => {
            setCount(prevCount => {
                console.log(prevCount); // Logs current value
                return prevCount + 1;
            });
        }, 1000);
    };
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={handleClick}>Increment with Delay</button>
        </div>
    );
}
{% endraw %}
```

**Mistake 2: Mutating State Objects**
```jsx
{% raw %}
function MutatingStateExample() {
    const [items, setItems] = useState([1, 2, 3]);
    
    // ❌ Bad: Mutating the array directly
    const addItem = () => {
        items.push(4); // This mutates the original array!
        setItems(items); // React won't detect the change
    };
    
    // ✅ Good: Creating a new array
    const addItem = () => {
        setItems(prevItems => [...prevItems, 4]);
    };
    
    return (
        <div>
            <ul>
                {items.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ul>
            <button onClick={addItem}>Add Item</button>
        </div>
    );
}
{% endraw %}
```

**Real-world useState Examples**:

**1. Form Management**:
```jsx
{% raw %}
function ContactForm() {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        message: ''
    });
    
    const [errors, setErrors] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    
    const handleChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
        // Clear error when user starts typing
        if (errors[field]) {
            setErrors(prev => ({ ...prev, [field]: '' }));
        }
    };
    
    const validateForm = () => {
        const newErrors = {};
        if (!formData.firstName) newErrors.firstName = 'First name is required';
        if (!formData.lastName) newErrors.lastName = 'Last name is required';
        if (!formData.email) newErrors.email = 'Email is required';
        if (!formData.email.includes('@')) newErrors.email = 'Invalid email format';
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!validateForm()) return;
        
        setIsSubmitting(true);
        try {
            await submitForm(formData);
            // Reset form on success
            setFormData({ firstName: '', lastName: '', email: '', message: '' });
            setErrors({});
        } catch (error) {
            setErrors({ submit: 'Failed to submit form' });
        } finally {
            setIsSubmitting(false);
        }
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <div>
                <input
                    type="text"
                    value={formData.firstName}
                    onChange={(e) => handleChange('firstName', e.target.value)}
                    placeholder="First Name"
                    className={errors.firstName ? 'error' : ''}
                />
                {errors.firstName && <span className="error-text">{errors.firstName}</span>}
            </div>
            
            <div>
                <input
                    type="text"
                    value={formData.lastName}
                    onChange={(e) => handleChange('lastName', e.target.value)}
                    placeholder="Last Name"
                    className={errors.lastName ? 'error' : ''}
                />
                {errors.lastName && <span className="error-text">{errors.lastName}</span>}
            </div>
            
            <div>
                <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    placeholder="Email"
                    className={errors.email ? 'error' : ''}
                />
                {errors.email && <span className="error-text">{errors.email}</span>}
            </div>
            
            <div>
                <textarea
                    value={formData.message}
                    onChange={(e) => handleChange('message', e.target.value)}
                    placeholder="Message"
                />
            </div>
            
            {errors.submit && <div className="error-text">{errors.submit}</div>}
            
            <button type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Submitting...' : 'Submit'}
            </button>
        </form>
    );
}
{% endraw %}
```

**2. Shopping Cart State**:
```jsx
{% raw %}
function ShoppingCart() {
    const [cart, setCart] = useState([]);
    const [total, setTotal] = useState(0);
    
    const addToCart = (product) => {
        setCart(prevCart => {
            const existingItem = prevCart.find(item => item.id === product.id);
            
            if (existingItem) {
                // Update quantity of existing item
                return prevCart.map(item =>
                    item.id === product.id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            } else {
                // Add new item
                return [...prevCart, { ...product, quantity: 1 }];
            }
        });
    };
    
    const removeFromCart = (productId) => {
        setCart(prevCart => prevCart.filter(item => item.id !== productId));
    };
    
    const updateQuantity = (productId, newQuantity) => {
        if (newQuantity <= 0) {
            removeFromCart(productId);
            return;
        }
        
        setCart(prevCart =>
            prevCart.map(item =>
                item.id === productId
                    ? { ...item, quantity: newQuantity }
                    : item
            )
        );
    };
    
    // Calculate total whenever cart changes
    useEffect(() => {
        const newTotal = cart.reduce((sum, item) => 
            sum + (item.price * item.quantity), 0
        );
        setTotal(newTotal);
    }, [cart]);
    
    return (
        <div>
            <h2>Shopping Cart ({cart.length} items)</h2>
            {cart.map(item => (
                <div key={item.id} className="cart-item">
                    <span>{item.name}</span>
                    <span>${item.price}</span>
                    <input
                        type="number"
                        min="1"
                        value={item.quantity}
                        onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
                    />
                    <button onClick={() => removeFromCart(item.id)}>Remove</button>
                </div>
            ))}
            <div className="cart-total">
                <strong>Total: ${total.toFixed(2)}</strong>
            </div>
        </div>
    );
}
{% endraw %}
```

#### useEffect - Side Effects and Lifecycle Management

**What it does**: `useEffect` lets you perform side effects in function components. It's a combination of `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount` from class components.

**Key Concepts**:
- **Side Effects**: Operations like data fetching, subscriptions, manual DOM mutations, logging
- **Dependency Array**: Controls when the effect runs
- **Cleanup Function**: Runs before the component unmounts or before the effect runs again
- **Timing**: Runs after the browser has painted the DOM

**Basic Usage**:
```jsx
{% raw %}
import React, { useState, useEffect } from 'react';

function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // ComponentDidMount equivalent
        fetchUser(userId);
        
        // ComponentWillUnmount equivalent
        return () => {
            // Cleanup function
            console.log('Component unmounting');
        };
    }, [userId]); // Dependency array

    useEffect(() => {
        // Run on every render
        document.title = user ? `${user.name}'s Profile` : 'Loading...';
    });

    const fetchUser = async (id) => {
        try {
            const response = await fetch(`/api/users/${id}`);
            const userData = await response.json();
            setUser(userData);
        } catch (error) {
            console.error('Error fetching user:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (!user) return <div>User not found</div>;

    return (
        <div>
            <h1>{user.name}</h1>
            <p>{user.email}</p>
        </div>
    );
}
{% endraw %}
```

**useEffect Dependency Array Patterns**:

**1. No Dependencies** (Runs after every render):
```jsx
{% raw %}
function LoggingComponent() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Runs on every render, can cause infinite loops
    useEffect(() => {
        console.log('Component rendered');
        // This could trigger another render if it updates state!
    });
    
    // ✅ Good: Only for logging, no state updates
    useEffect(() => {
        console.log('Component rendered, count:', count);
    });
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>Increment</button>
        </div>
    );
}
{% endraw %}
```

**2. Empty Dependencies** (Runs only once on mount):
```jsx
{% raw %}
function SubscriptionComponent() {
    const [data, setData] = useState(null);
    
    useEffect(() => {
        // ✅ Good: Set up subscription only once
        const subscription = subscribeToData((newData) => {
            setData(newData);
        });
        
        // Cleanup: Remove subscription on unmount
        return () => {
            subscription.unsubscribe();
        };
    }, []); // Empty dependency array = run only once
    
    return <div>Data: {data}</div>;
}
{% endraw %}
```

**3. Specific Dependencies** (Runs when dependencies change):
```jsx
{% raw %}
function SearchComponent({ query, filters }) {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {
        // ✅ Good: Only search when query or filters change
        if (query.trim()) {
            setLoading(true);
            searchAPI(query, filters).then(setResults).finally(() => setLoading(false));
        }
    }, [query, filters]); // Re-run when query or filters change
    
    return (
        <div>
            {loading ? <div>Searching...</div> : (
                <ul>
                    {results.map(result => (
                        <li key={result.id}>{result.title}</li>
                    ))}
                </ul>
            )}
        </div>
    );
}
{% endraw %}
```

**4. Function Dependencies** (Handling function references):
```jsx
{% raw %}
function ParentComponent() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Function recreated on every render
    const handleIncrement = () => setCount(count + 1);
    
    // ✅ Good: Memoized function with useCallback
    const handleIncrement = useCallback(() => {
        setCount(prev => prev + 1);
    }, []); // No dependencies needed
    
    return <ChildComponent onIncrement={handleIncrement} />;
}

function ChildComponent({ onIncrement }) {
    useEffect(() => {
        // This effect will only run when onIncrement function reference changes
        console.log('Increment handler changed');
    }, [onIncrement]);
    
    return <button onClick={onIncrement}>Increment</button>;
}
{% endraw %}
```

**Advanced useEffect Patterns**:

**1. Multiple Effects for Different Concerns**:
```jsx
{% raw %}
function ComplexComponent({ userId, theme }) {
    const [user, setUser] = useState(null);
    const [posts, setPosts] = useState([]);
    const [notifications, setNotifications] = useState([]);
    
    // Effect 1: Fetch user data
    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, [userId]);
    
    // Effect 2: Fetch user posts
    useEffect(() => {
        if (user) {
            fetchUserPosts(user.id).then(setPosts);
        }
    }, [user]);
    
    // Effect 3: Set up real-time notifications
    useEffect(() => {
        if (user) {
            const subscription = subscribeToNotifications(user.id, setNotifications);
            return () => subscription.unsubscribe();
        }
    }, [user]);
    
    // Effect 4: Update document title
    useEffect(() => {
        if (user) {
            document.title = `${user.name}'s Dashboard`;
        }
    }, [user]);
    
    // Effect 5: Apply theme
    useEffect(() => {
        document.body.className = `theme-${theme}`;
    }, [theme]);
    
    return (
        <div>
            {/* Component JSX */}
        </div>
    );
}
{% endraw %}
```

**2. Cleanup Functions and AbortController**:
```jsx
{% raw %}
function DataFetchingComponent({ url }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        const abortController = new AbortController();
        
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await fetch(url, {
                    signal: abortController.signal
                });
                const result = await response.json();
                setData(result);
            } catch (error) {
                if (error.name === 'AbortError') {
                    console.log('Fetch aborted');
                } else {
                    console.error('Fetch error:', error);
                }
            } finally {
                setLoading(false);
            }
        };
        
        fetchData();
        
        // Cleanup: Abort fetch if component unmounts or URL changes
        return () => {
            abortController.abort();
        };
    }, [url]);
    
    if (loading) return <div>Loading...</div>;
    return <div>{JSON.stringify(data)}</div>;
}
{% endraw %}
```

**3. Custom Hook with useEffect**:
```jsx
{% raw %}
function useLocalStorage(key, initialValue) {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return initialValue;
        }
    });
    
    const setValue = (value) => {
        try {
            // Allow value to be a function so we have the same API as useState
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error('Error setting localStorage:', error);
        }
    };
    
    return [storedValue, setValue];
}

// Usage
function UserPreferences() {
    const [theme, setTheme] = useLocalStorage('theme', 'light');
    const [language, setLanguage] = useLocalStorage('language', 'en');
    
    return (
        <div>
            <select value={theme} onChange={(e) => setTheme(e.target.value)}>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
            </select>
            
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
            </select>
        </div>
    );
}
{% endraw %}
```

**Common useEffect Mistakes and Solutions**:

**Mistake 1: Missing Dependencies**:
```jsx
{% raw %}
function BuggyComponent({ userId }) {
    const [user, setUser] = useState(null);
    
    // ❌ Bad: Missing userId in dependencies
    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, []); // This will only fetch once, even if userId changes!
    
    // ✅ Good: Include all dependencies
    useEffect(() => {
        fetchUser(userId).then(setUser);
    }, [userId]);
    
    return <div>{user?.name}</div>;
}
{% endraw %}
```

**Mistake 2: Infinite Loops**:
```jsx
{% raw %}
function InfiniteLoopComponent() {
    const [count, setCount] = useState(0);
    
    // ❌ Bad: Updates state in effect with no dependencies
    useEffect(() => {
        setCount(count + 1); // This causes infinite re-renders!
    }); // No dependency array = runs after every render
    
    // ✅ Good: Only update when needed
    useEffect(() => {
        if (count < 10) {
            setCount(prev => prev + 1);
        }
    }, [count]); // Only run when count changes
    
    // ✅ Better: Use a ref to track if it's the first render
    const isFirstRender = useRef(true);
    useEffect(() => {
        if (isFirstRender.current) {
            isFirstRender.current = false;
            setCount(1); // Only set once on mount
        }
    }, []);
    
    return <div>Count: {count}</div>;
}
{% endraw %}
```

**Mistake 3: Forgetting Cleanup**:
```jsx
{% raw %}
function SubscriptionComponent() {
    const [data, setData] = useState(null);
    
    // ❌ Bad: No cleanup, can cause memory leaks
    useEffect(() => {
        const subscription = subscribeToData(setData);
        // Missing return statement for cleanup!
    }, []);
    
    // ✅ Good: Proper cleanup
    useEffect(() => {
        const subscription = subscribeToData(setData);
        return () => subscription.unsubscribe();
    }, []);
    
    return <div>{data}</div>;
}
{% endraw %}
```

**Real-world useEffect Examples**:

**1. API Data Fetching with Loading States**:
```jsx
{% raw %}
function UserDashboard({ userId }) {
    const [user, setUser] = useState(null);
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState({ user: true, posts: true });
    const [error, setError] = useState(null);
    
    // Fetch user data
    useEffect(() => {
        const fetchUser = async () => {
            try {
                setLoading(prev => ({ ...prev, user: true }));
                setError(null);
                
                const response = await fetch(`/api/users/${userId}`);
                if (!response.ok) throw new Error('Failed to fetch user');
                
                const userData = await response.json();
                setUser(userData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(prev => ({ ...prev, user: false }));
            }
        };
        
        fetchUser();
    }, [userId]);
    
    // Fetch user posts (only after user is loaded)
    useEffect(() => {
        if (!user) return;
        
        const fetchPosts = async () => {
            try {
                setLoading(prev => ({ ...prev, posts: true }));
                const response = await fetch(`/api/users/${userId}/posts`);
                const postsData = await response.json();
                setPosts(postsData);
            } catch (err) {
                console.error('Failed to fetch posts:', err);
            } finally {
                setLoading(prev => ({ ...prev, posts: false }));
            }
        };
        
        fetchPosts();
    }, [user, userId]);
    
    // Update document title
    useEffect(() => {
        if (user) {
            document.title = `${user.name}'s Dashboard`;
        }
    }, [user]);
    
    if (loading.user) return <div>Loading user...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!user) return <div>User not found</div>;
    
    return (
        <div>
            <h1>{user.name}'s Dashboard</h1>
            <p>Email: {user.email}</p>
            
            <h2>Posts</h2>
            {loading.posts ? (
                <div>Loading posts...</div>
            ) : (
                <div>
                    {posts.map(post => (
                        <div key={post.id}>
                            <h3>{post.title}</h3>
                            <p>{post.excerpt}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
{% endraw %}
```

**2. Real-time Updates with WebSocket**:
```jsx
{% raw %}
function ChatRoom({ roomId, userId }) {
    const [messages, setMessages] = useState([]);
    const [isConnected, setIsConnected] = useState(false);
    const [newMessage, setNewMessage] = useState('');
    
    // WebSocket connection
    useEffect(() => {
        const ws = new WebSocket(`wss://chat.example.com/room/${roomId}`);
        
        ws.onopen = () => {
            setIsConnected(true);
            console.log('Connected to chat room');
        };
        
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            setMessages(prev => [...prev, message]);
        };
        
        ws.onclose = () => {
            setIsConnected(false);
            console.log('Disconnected from chat room');
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            setIsConnected(false);
        };
        
        // Cleanup: Close connection on unmount
        return () => {
            ws.close();
        };
    }, [roomId]);
    
    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        const chatContainer = document.getElementById('chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }, [messages]);
    
    const sendMessage = () => {
        if (!newMessage.trim() || !isConnected) return;
        
        const message = {
            id: Date.now(),
            text: newMessage,
            userId,
            timestamp: new Date().toISOString()
        };
        
        // Optimistically add message to UI
        setMessages(prev => [...prev, message]);
        setNewMessage('');
        
        // Send to server (in real app, you'd send via WebSocket)
        console.log('Sending message:', message);
    };
    
    return (
        <div>
            <div className="connection-status">
                Status: {isConnected ? 'Connected' : 'Disconnected'}
            </div>
            
            <div id="chat-container" className="messages">
                {messages.map(message => (
                    <div key={message.id} className={`message ${message.userId === userId ? 'own' : 'other'}`}>
                        <span className="user">{message.userId}</span>
                        <span className="text">{message.text}</span>
                        <span className="time">{new Date(message.timestamp).toLocaleTimeString()}</span>
                    </div>
                ))}
            </div>
            
            <div className="input-area">
                <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Type a message..."
                    disabled={!isConnected}
                />
                <button onClick={sendMessage} disabled={!isConnected || !newMessage.trim()}>
                    Send
                </button>
            </div>
        </div>
    );
}
{% endraw %}
```

#### useRef
```jsx
{% raw %}
import React, { useRef, useEffect } from 'react';

function FocusInput() {
    const inputRef = useRef(null);

    useEffect(() => {
        // Focus input on mount
        inputRef.current.focus();
    }, []);

    return (
        <div>
            <input ref={inputRef} type="text" placeholder="Focus me!" />
            <button onClick={() => inputRef.current.focus()}>
                Focus Input
            </button>
        </div>
    );
}
{% endraw %}
```

#### Custom Hooks
```jsx
{% raw %}
// Custom hook for API calls
function useApi(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await fetch(url);
                const result = await response.json();
                setData(result);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [url]);

    return { data, loading, error };
}

// Usage
function UserList() {
    const { data: users, loading, error } = useApi('/api/users');

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <ul>
            {users.map(user => (
                <li key={user.id}>{user.name}</li>
            ))}
        </ul>
    );
}
{% endraw %}
```

---

## React Best Practices

### Component Design

#### Single Responsibility Principle
```jsx
{% raw %}
// ❌ Bad: Component doing too many things
function UserDashboard() {
    const [users, setUsers] = useState([]);
    const [posts, setPosts] = useState([]);
    const [comments, setComments] = useState([]);
    
    // Fetch logic, rendering logic, business logic all mixed
    return (
        <div>
            {/* Complex mixed content */}
        </div>
    );
}

// ✅ Good: Separated concerns
function UserDashboard() {
    return (
        <div>
            <UserList />
            <PostList />
            <CommentList />
        </div>
    );
}

function UserList() {
    const [users, setUsers] = useState([]);
    // Only user-related logic
    return <div>{/* User rendering */}</div>;
}
{% endraw %}
```

#### Props Design
```jsx
{% raw %}
// ❌ Bad: Too many props
function UserCard({ id, name, email, avatar, bio, location, website, twitter, github, linkedin, skills, experience, education, projects, followers, following, createdAt, updatedAt, status, role, permissions, settings, preferences, notifications, theme, language, timezone, currency, units, privacy, security, verification, badges, achievements, level, points, rank, tier, subscription, plan, billing, payment, history, logs, analytics, reports, exports, imports, backups, restores, migrations, updates, patches, hotfixes, releases, versions, builds, deployments, environments, configs, secrets, keys, tokens, sessions, cookies, cache, storage, database, api, endpoints, routes, middleware, validation, sanitization, encryption, hashing, compression, optimization, minification, bundling, transpilation, polyfills, shims, fallbacks, polyfills, shims, fallbacks }) {
    // Component with 100+ props
}

// ✅ Good: Grouped props
function UserCard({ user, actions, theme }) {
    const { name, email, avatar, bio } = user;
    const { onEdit, onDelete, onFollow } = actions;
    const { colors, spacing } = theme;
    
    return <div>{/* Clean component */}</div>;
}

// Usage
<UserCard 
    user={userData}
    actions={{ onEdit, onDelete, onFollow }}
    theme={{ colors: 'dark', spacing: 'compact' }}
/>
{% endraw %}
```

#### Conditional Rendering
```jsx
{% raw %}
// ❌ Bad: Complex nested ternaries
function UserStatus({ user }) {
    return (
        <div>
            {user.isActive ? (
                user.isPremium ? (
                    user.isVerified ? (
                        <span className="premium-verified">Premium Verified</span>
                    ) : (
                        <span className="premium">Premium</span>
                    )
                ) : (
                    user.isVerified ? (
                        <span className="verified">Verified</span>
                    ) : (
                        <span className="active">Active</span>
                    )
                )
            ) : (
                <span className="inactive">Inactive</span>
            )}
        </div>
    );
}

// ✅ Good: Clean conditional rendering
function UserStatus({ user }) {
    if (!user.isActive) {
        return <span className="inactive">Inactive</span>;
    }

    const statusClasses = ['active'];
    if (user.isPremium) statusClasses.push('premium');
    if (user.isVerified) statusClasses.push('verified');

    const statusText = [
        user.isPremium && 'Premium',
        user.isVerified && 'Verified'
    ].filter(Boolean).join(' ') || 'Active';

    return (
        <span className={statusClasses.join(' ')}>
            {statusText}
        </span>
    );
}
{% endraw %}
```

### Performance Optimization

#### React.memo
```jsx
{% raw %}
import React, { memo } from 'react';

const ExpensiveComponent = memo(function ExpensiveComponent({ data, onAction }) {
    // Expensive computation
    const processedData = data.map(item => ({
        ...item,
        processed: item.value * 2 + Math.sqrt(item.value)
    }));

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

// Only re-renders if props change
<ExpensiveComponent data={userData} onAction={handleAction} />
{% endraw %}
```

#### useMemo and useCallback
```jsx
{% raw %}
import React, { useState, useMemo, useCallback } from 'react';

function UserDashboard({ users, filters }) {
    const [sortBy, setSortBy] = useState('name');

    // Memoize expensive computation
    const filteredAndSortedUsers = useMemo(() => {
        console.log('Computing filtered users...');
        return users
            .filter(user => {
                if (filters.activeOnly && !user.isActive) return false;
                if (filters.role && user.role !== filters.role) return false;
                return true;
            })
            .sort((a, b) => {
                if (sortBy === 'name') return a.name.localeCompare(b.name);
                if (sortBy === 'email') return a.email.localeCompare(b.email);
                return 0;
            });
    }, [users, filters, sortBy]);

    // Memoize callback functions
    const handleUserAction = useCallback((userId, action) => {
        console.log(`Performing ${action} on user ${userId}`);
        // Action logic
    }, []);

    const handleSort = useCallback((field) => {
        setSortBy(field);
    }, []);

    return (
        <div>
            <div>
                <button onClick={() => handleSort('name')}>Sort by Name</button>
                <button onClick={() => handleSort('email')}>Sort by Email</button>
            </div>
            {filteredAndSortedUsers.map(user => (
                <UserCard 
                    key={user.id} 
                    user={user} 
                    onAction={handleUserAction}
                />
            ))}
        </div>
    );
}
{% endraw %}
```

#### Code Splitting
```jsx
{% raw %}
import React, { Suspense, lazy } from 'react';

// Lazy load components
const UserList = lazy(() => import('./UserList'));
const UserDetails = lazy(() => import('./UserDetails'));
const UserSettings = lazy(() => import('./UserSettings'));

function App() {
    return (
        <Router>
            <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                    <Route path="/users" element={<UserList />} />
                    <Route path="/users/:id" element={<UserDetails />} />
                    <Route path="/users/:id/settings" element={<UserSettings />} />
                </Routes>
            </Suspense>
        </Router>
    );
}
{% endraw %}
```

---

## Component Creation Examples

### Reusable Button Component
```jsx
{% raw %}
import React from 'react';
import PropTypes from 'prop-types';

const Button = React.memo(function Button({ 
    children, 
    variant = 'primary', 
    size = 'medium',
    disabled = false,
    loading = false,
    onClick,
    type = 'button',
    className = '',
    ...props 
}) {
    const baseClasses = 'btn';
    const variantClasses = {
        primary: 'btn-primary',
        secondary: 'btn-secondary',
        danger: 'btn-danger',
        success: 'btn-success',
        warning: 'btn-warning'
    };
    const sizeClasses = {
        small: 'btn-sm',
        medium: 'btn-md',
        large: 'btn-lg'
    };

    const classes = [
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        disabled && 'btn-disabled',
        loading && 'btn-loading',
        className
    ].filter(Boolean).join(' ');

    const handleClick = (event) => {
        if (!disabled && !loading && onClick) {
            onClick(event);
        }
    };

    return (
        <button
            type={type}
            className={classes}
            disabled={disabled || loading}
            onClick={handleClick}
            {...props}
        >
            {loading && <span className="spinner" />}
            {children}
        </button>
    );
});

Button.propTypes = {
    children: PropTypes.node.isRequired,
    variant: PropTypes.oneOf(['primary', 'secondary', 'danger', 'success', 'warning']),
    size: PropTypes.oneOf(['small', 'medium', 'large']),
    disabled: PropTypes.bool,
    loading: PropTypes.bool,
    onClick: PropTypes.func,
    type: PropTypes.oneOf(['button', 'submit', 'reset']),
    className: PropTypes.string
};

export default Button;
{% endraw %}
```

### Form Component with Validation
```jsx
{% raw %}
import React, { useState, useCallback } from 'react';

function useForm(initialValues, validationSchema) {
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

    const reset = useCallback(() => {
        setValues(initialValues);
        setErrors({});
        setTouched({});
    }, [initialValues]);

    return {
        values,
        errors,
        touched,
        handleChange,
        handleBlur,
        validate,
        reset
    };
}

function LoginForm() {
    const validationSchema = {
        email: (value) => {
            if (!value) return 'Email is required';
            if (!/\S+@\S+\.\S+/.test(value)) return 'Email is invalid';
            return '';
        },
        password: (value) => {
            if (!value) return 'Password is required';
            if (value.length < 6) return 'Password must be at least 6 characters';
            return '';
        }
    };

    const { values, errors, touched, handleChange, handleBlur, validate } = useForm(
        { email: '', password: '' },
        validationSchema
    );

    const handleSubmit = (e) => {
        e.preventDefault();
        if (validate()) {
            console.log('Form submitted:', values);
            // Submit logic
        }
    };

    return (
        <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                    id="email"
                    type="email"
                    value={values.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    onBlur={() => handleBlur('email')}
                    className={touched.email && errors.email ? 'error' : ''}
                />
                {touched.email && errors.email && (
                    <span className="error-message">{errors.email}</span>
                )}
            </div>

            <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                    id="password"
                    type="password"
                    value={values.password}
                    onChange={(e) => handleChange('password', e.target.value)}
                    onBlur={() => handleBlur('password')}
                    className={touched.password && errors.password ? 'error' : ''}
                />
                {touched.password && errors.password && (
                    <span className="error-message">{errors.password}</span>
                )}
            </div>

            <button type="submit" className="btn btn-primary">
                Login
            </button>
        </form>
    );
}
{% endraw %}
```

---

## Frontend Interview Essentials

### Common Questions & Answers

#### 1. What is the Virtual DOM?
```javascript
// Virtual DOM is a lightweight copy of the actual DOM
// React uses it to optimize rendering performance

// Without Virtual DOM (expensive)
function updateDOM() {
    // Directly manipulate DOM - causes reflows/repaints
    document.getElementById('user-list').innerHTML = newHTML;
}

// With Virtual DOM (efficient)
function ReactUpdate() {
    // React compares Virtual DOM with previous version
    // Only updates what changed
    return (
        <UserList users={updatedUsers} />
    );
}
```

#### 2. Explain React's Component Lifecycle
```jsx
{% raw %}
class ClassComponent extends React.Component {
    // Mounting Phase
    constructor(props) {
        super(props);
        this.state = { data: null };
    }

    static getDerivedStateFromProps(props, state) {
        // Called before render, can update state
        return null;
    }

    componentDidMount() {
        // Component mounted, safe to make API calls
        this.fetchData();
    }

    // Updating Phase
    shouldComponentUpdate(nextProps, nextState) {
        // Return false to prevent re-render
        return this.props.id !== nextProps.id;
    }

    getSnapshotBeforeUpdate(prevProps, prevState) {
        // Capture info before DOM updates
        return { scrollPosition: window.scrollY };
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        // Component updated, can access DOM
        if (snapshot.scrollPosition) {
            window.scrollTo(0, snapshot.scrollPosition);
        }
    }

    // Unmounting Phase
    componentWillUnmount() {
        // Cleanup: remove event listeners, cancel requests
        this.cancelRequest();
    }

    render() {
        return <div>{this.state.data}</div>;
    }
}

// Hooks equivalent
function FunctionalComponent({ id }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // componentDidMount
        fetchData();
        
        // componentWillUnmount
        return () => cleanup();
    }, [id]); // componentDidUpdate equivalent

    return <div>{data}</div>;
}
{% endraw %}
```

#### 3. State Management Patterns
```jsx
{% raw %}
// Local State
function LocalStateExample() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
}

// Lifted State
function Parent() {
    const [sharedState, setSharedState] = useState('');
    return (
        <div>
            <ChildA value={sharedState} onChange={setSharedState} />
            <ChildB value={sharedState} onChange={setSharedState} />
        </div>
    );
}

// Context API
const ThemeContext = React.createContext();

function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');
    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

function ThemedButton() {
    const { theme, setTheme } = useContext(ThemeContext);
    return (
        <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
            Current theme: {theme}
        </button>
    );
}

// Custom Hook for State
function useCounter(initialValue = 0) {
    const [count, setCount] = useState(initialValue);
    
    const increment = useCallback(() => setCount(c => c + 1), []);
    const decrement = useCallback(() => setCount(c => c - 1), []);
    const reset = useCallback(() => setCount(initialValue), [initialValue]);
    
    return { count, increment, decrement, reset };
}
{% endraw %}
```

#### 4. Performance Optimization Techniques
```jsx
{% raw %}
// 1. React.memo for expensive components
const ExpensiveComponent = React.memo(({ data }) => {
    // Only re-renders if props change
    return <div>{/* Expensive rendering */}</div>;
});

// 2. useMemo for expensive calculations
function DataTable({ data, filters }) {
    const filteredData = useMemo(() => {
        return data.filter(item => {
            // Expensive filtering logic
            return filters.every(filter => filter(item));
        });
    }, [data, filters]);

    return <table>{/* Render filtered data */}</table>;
}

// 3. useCallback for stable references
function ParentComponent() {
    const [count, setCount] = useState(0);
    
    const handleClick = useCallback(() => {
        setCount(c => c + 1);
    }, []); // Stable reference, won't cause child re-renders

    return <ChildComponent onClick={handleClick} />;
}

// 4. Lazy loading
const LazyComponent = React.lazy(() => import('./LazyComponent'));

function App() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <LazyComponent />
        </Suspense>
    );
}
{% endraw %}
```

#### 5. Error Boundaries
```jsx
{% raw %}
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        // Log error to service
        console.error('Error caught by boundary:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="error-boundary">
                    <h2>Something went wrong</h2>
                    <button onClick={() => window.location.reload()}>
                        Reload Page
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

// Usage
<ErrorBoundary>
    <ComponentThatMightError />
</ErrorBoundary>
{% endraw %}
```

### CSS-in-JS and Styling
```jsx
{% raw %}
// Styled Components
import styled from 'styled-components';

const Button = styled.button`
    background: ${props => props.primary ? 'blue' : 'white'};
    color: ${props => props.primary ? 'white' : 'blue'};
    padding: 10px 20px;
    border: 2px solid blue;
    border-radius: 4px;
    cursor: pointer;
    
    &:hover {
        background: ${props => props.primary ? 'darkblue' : 'lightblue'};
    }
    
    &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
`;

// CSS Modules
import styles from './Button.module.css';

function Button({ children, variant }) {
    const buttonClass = `${styles.button} ${styles[variant]}`;
    return <button className={buttonClass}>{children}</button>;
}

// CSS-in-JS with emotion
import { css } from '@emotion/react';

const buttonStyle = css`
    background: blue;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    
    &:hover {
        background: darkblue;
    }
`;

function Button({ children }) {
    return <button css={buttonStyle}>{children}</button>;
}
{% endraw %}
```

---

## Key Takeaways

### **DOM Mastery**
- Understand DOM tree structure and traversal
- Use event delegation for performance
- Batch DOM updates to minimize reflows

### **React Best Practices**
- Keep components small and focused
- Use hooks for state and side effects
- Implement proper error boundaries
- Optimize with React.memo, useMemo, useCallback

### **Component Design**
- Single responsibility principle
- Props design with object grouping
- Conditional rendering patterns
- Reusable component libraries

### **Performance**
- Virtual DOM understanding
- Code splitting and lazy loading
- Bundle optimization
- Memory leak prevention

### **Interview Success**
- Explain concepts clearly with examples
- Show understanding of trade-offs
- Demonstrate problem-solving approach
- Know when to use different patterns

*Frontend development is about creating intuitive, performant user experiences. Master these fundamentals and you'll be well-prepared for any frontend role!*
