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

#### useEffect
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
