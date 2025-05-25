# Frontend Integration Guide for Ace Olympiads Authentication

This document provides comprehensive guidance for implementing authentication in the frontend application using Next.js and NextAuth.js, connecting to the Ace Olympiads backend.

## Table of Contents

1. [Overview](#overview)
2. [Backend API Endpoints](#backend-api-endpoints)
3. [Implementation Guide](#implementation-guide)
   - [Registration Page](#registration-page)
   - [Login Page](#login-page)
   - [Profile Page](#profile-page)
4. [NextAuth.js Configuration](#nextauth-configuration)
5. [Making Authenticated Requests](#making-authenticated-requests)
6. [Error Handling](#error-handling)

## Overview

The Ace Olympiads backend uses Firebase Authentication with JWT tokens for user authentication. The system supports:

- Email/password registration and login
- Google OAuth authentication
- Direct Firebase token authentication

The backend issues JWT tokens with the following configuration:
- Access token lifetime: 60 minutes
- Refresh token lifetime: 14 days

**Important Note**: While the backend doesn't enforce authentication checks on routes, it's recommended to include the authentication token in requests for future compatibility.

## Backend API Endpoints

### Authentication Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/users/auth/register/` | POST | Register with email/password | `{ email, password, username }` | `{ refresh, access, user }` |
| `/api/users/auth/login/` | POST | Login with email/password | `{ email, password }` | `{ refresh, access, user }` |
| `/api/users/auth/google/` | POST | Authenticate with Google | `{ auth_code }` | `{ refresh, access, user }` |
| `/api/users/auth/firebase/` | POST | Authenticate with Firebase token | `{ id_token }` | `{ refresh, access, user }` |

### User Profile Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/users/profile/` | GET | Get current user profile | N/A | User profile data |
| `/api/users/profile/` | PUT | Update user profile | Updated profile fields | Updated user data |
| `/api/users/profile/{user_id}/` | GET | Get specific user profile | N/A | User profile data |

## Implementation Guide

### Registration Page

#### UI Components

Create a registration form with the following fields:
- Email address (required)
- Password (required, min 8 characters)
- Username (required)
- Submit button

#### Implementation Steps

1. Create a registration form component:

```jsx
// components/RegisterForm.jsx
import { useState } from 'react';
import { useRouter } from 'next/router';

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('YOUR_BACKEND_URL/api/users/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Registration failed');
      }
      
      // Store tokens in localStorage or secure cookie
      localStorage.setItem('accessToken', data.access);
      localStorage.setItem('refreshToken', data.refresh);
      
      // Store user data in NextAuth session or context
      // This depends on your NextAuth configuration
      
      router.push('/dashboard'); // Redirect to dashboard or profile page
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      
      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          minLength={8}
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="username">Username</label>
        <input
          type="text"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />
      </div>
      
      <button type="submit" disabled={loading}>
        {loading ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
}
```

2. Create a registration page:

```jsx
// pages/register.jsx
import Head from 'next/head';
import Link from 'next/link';
import RegisterForm from '../components/RegisterForm';

export default function Register() {
  return (
    <div className="container">
      <Head>
        <title>Register - Ace Olympiads</title>
      </Head>
      
      <h1>Create an Account</h1>
      <RegisterForm />
      
      <p>
        Already have an account? <Link href="/login">Login</Link>
      </p>
    </div>
  );
}
```

### Login Page

#### UI Components

Create a login form with:
- Email address
- Password
- "Remember me" checkbox (optional)
- Login button
- "Forgot password" link (optional)
- Google login button

#### Implementation Steps

1. Create a login form component:

```jsx
// components/LoginForm.jsx
import { useState } from 'react';
import { useRouter } from 'next/router';
import { signIn } from 'next-auth/react';

export default function LoginForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // Using NextAuth to handle the login
      const result = await signIn('credentials', {
        redirect: false,
        email: formData.email,
        password: formData.password
      });
      
      if (result.error) {
        throw new Error(result.error);
      }
      
      router.push('/dashboard'); // Redirect to dashboard or profile page
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    try {
      await signIn('google', { callbackUrl: '/dashboard' });
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {error && <div className="error">{error}</div>}
        
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      
      <div className="social-login">
        <button onClick={handleGoogleLogin} className="google-button">
          Login with Google
        </button>
      </div>
    </div>
  );
}
```

2. Create a login page:

```jsx
// pages/login.jsx
import Head from 'next/head';
import Link from 'next/link';
import LoginForm from '../components/LoginForm';

export default function Login() {
  return (
    <div className="container">
      <Head>
        <title>Login - Ace Olympiads</title>
      </Head>
      
      <h1>Login to Your Account</h1>
      <LoginForm />
      
      <p>
        Don't have an account? <Link href="/register">Register</Link>
      </p>
    </div>
  );
}
```

### Profile Page

#### UI Components

Create a profile page with:
- User information display (username, email, etc.)
- Profile image
- Contact information
- Edit profile button/form

#### Implementation Steps

1. Create a profile page component:

```jsx
// pages/profile.jsx
import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/router';
import Head from 'next/head';

export default function Profile() {
  const { data: session, status } = useSession();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    contact_no: '',
    image: ''
  });
  const router = useRouter();

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/login');
      return;
    }

    if (status === 'authenticated') {
      fetchProfile();
    }
  }, [status]);

  const fetchProfile = async () => {
    try {
      const response = await fetch('YOUR_BACKEND_URL/api/users/profile/', {
        headers: {
          'Authorization': `Bearer ${session.accessToken}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch profile');
      }
      
      const data = await response.json();
      setProfile(data);
      setFormData({
        username: data.username || '',
        contact_no: data.contact_no || '',
        image: data.image || ''
      });
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('YOUR_BACKEND_URL/api/users/profile/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.accessToken}`
        },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        throw new Error('Failed to update profile');
      }
      
      const updatedProfile = await response.json();
      setProfile(updatedProfile);
      setIsEditing(false);
    } catch (error) {
      setError(error.message);
    }
  };

  if (loading) {
    return <div>Loading profile...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="container">
      <Head>
        <title>Your Profile - Ace Olympiads</title>
      </Head>
      
      <h1>Your Profile</h1>
      
      {isEditing ? (
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="contact_no">Contact Number</label>
            <input
              type="text"
              id="contact_no"
              name="contact_no"
              value={formData.contact_no}
              onChange={handleChange}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="image">Profile Image URL</label>
            <input
              type="text"
              id="image"
              name="image"
              value={formData.image}
              onChange={handleChange}
            />
          </div>
          
          <div className="button-group">
            <button type="submit">Save Changes</button>
            <button type="button" onClick={() => setIsEditing(false)}>Cancel</button>
          </div>
        </form>
      ) : (
        <div className="profile-info">
          {profile.image && (
            <div className="profile-image">
              <img src={profile.image} alt={profile.username} />
            </div>
          )}
          
          <div className="profile-details">
            <p><strong>Email:</strong> {profile.email}</p>
            <p><strong>Username:</strong> {profile.username}</p>
            <p><strong>Contact Number:</strong> {profile.contact_no || 'Not provided'}</p>
            <p><strong>Role:</strong> {profile.role}</p>
            <p><strong>Account Created:</strong> {new Date(profile.created_at).toLocaleDateString()}</p>
          </div>
          
          <button onClick={() => setIsEditing(true)}>Edit Profile</button>
        </div>
      )}
    </div>
  );
}
```

## NextAuth Configuration

Configure NextAuth.js to work with your backend authentication system:

```jsx
// pages/api/auth/[...nextauth].js
import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import CredentialsProvider from 'next-auth/providers/credentials';

export default NextAuth({
  providers: [
    // Email/Password authentication
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        try {
          const response = await fetch('YOUR_BACKEND_URL/api/users/auth/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          });
          
          const data = await response.json();
          
          if (!response.ok) {
            throw new Error(data.error || 'Invalid credentials');
          }
          
          // Return user data and tokens
          return {
            ...data.user,
            accessToken: data.access,
            refreshToken: data.refresh
          };
        } catch (error) {
          return null;
        }
      }
    }),
    
    // Google authentication
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      authorization: {
        params: {
          prompt: "consent",
          access_type: "offline",
          response_type: "code"
        }
      }
    })
  ],
  
  callbacks: {
    async jwt({ token, user, account }) {
      // Initial sign in
      if (account && user) {
        if (account.provider === 'google') {
          try {
            // Exchange Google auth code for Firebase tokens
            const response = await fetch('YOUR_BACKEND_URL/api/users/auth/google/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                auth_code: account.id_token,
              }),
            });
            
            const data = await response.json();
            
            if (!response.ok) {
              throw new Error(data.error || 'Google authentication failed');
            }
            
            return {
              ...token,
              accessToken: data.access,
              refreshToken: data.refresh,
              user: data.user
            };
          } catch (error) {
            return token;
          }
        }
        
        // For credentials login, user already contains tokens
        return {
          ...token,
          accessToken: user.accessToken,
          refreshToken: user.refreshToken,
          user: {
            id: user.id,
            email: user.email,
            username: user.username,
            role: user.role
          }
        };
      }
      
      // Return previous token if the access token has not expired yet
      if (Date.now() < token.accessTokenExpires) {
        return token;
      }
      
      // Access token has expired, try to refresh it
      return refreshAccessToken(token);
    },
    
    async session({ session, token }) {
      session.user = token.user;
      session.accessToken = token.accessToken;
      session.error = token.error;
      return session;
    },
  },
  
  pages: {
    signIn: '/login',
    signOut: '/logout',
    error: '/auth/error',
  },
  
  session: {
    strategy: 'jwt',
    maxAge: 60 * 60, // 1 hour
  },
  
  debug: process.env.NODE_ENV === 'development',
});

// Helper function to refresh access token
async function refreshAccessToken(token) {
  try {
    const response = await fetch('YOUR_BACKEND_URL/api/token/refresh/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        refresh: token.refreshToken,
      }),
    });
    
    const refreshedTokens = await response.json();
    
    if (!response.ok) {
      throw refreshedTokens;
    }
    
    return {
      ...token,
      accessToken: refreshedTokens.access,
      refreshToken: refreshedTokens.refresh || token.refreshToken,
      accessTokenExpires: Date.now() + 60 * 60 * 1000, // 1 hour
    };
  } catch (error) {
    return {
      ...token,
      error: 'RefreshAccessTokenError',
    };
  }
}
```

## Making Authenticated Requests

To make authenticated requests to your backend API, include the access token in the Authorization header:

```jsx
// utils/api.js
import { getSession } from 'next-auth/react';

export async function fetchWithAuth(url, options = {}) {
  const session = await getSession();
  
  if (!session?.accessToken) {
    throw new Error('No access token available');
  }
  
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${session.accessToken}`,
    ...options.headers,
  };
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  // Handle token expiration
  if (response.status === 401) {
    // Redirect to login or refresh token
    window.location.href = '/login';
    return;
  }
  
  return response;
}

// Example usage:
// const response = await fetchWithAuth('YOUR_BACKEND_URL/api/users/profile/');
// const data = await response.json();
```

## Error Handling

Implement consistent error handling across your authentication flows:

```jsx
// utils/errorHandler.js
export function handleAuthError(error) {
  // Common authentication errors
  const errorMessages = {
    'invalid_credentials': 'Invalid email or password',
    'user_exists': 'User with this email already exists',
    'token_expired': 'Your session has expired. Please login again.',
    'invalid_token': 'Authentication failed. Please login again.',
    'network_error': 'Network error. Please check your connection.',
  };
  
  // Extract error message or code from the error object
  let errorMessage = 'An unknown error occurred';
  
  if (typeof error === 'string') {
    errorMessage = error;
  } else if (error.message) {
    errorMessage = error.message;
  } else if (error.error) {
    errorMessage = errorMessages[error.error] || error.error;
  }
  
  return errorMessage;
}
```

This documentation provides a comprehensive guide for implementing authentication in your Next.js frontend application, connecting to your Ace Olympiads backend. The implementation follows best practices for Next.js and NextAuth.js while accommodating your specific backend API structure.
