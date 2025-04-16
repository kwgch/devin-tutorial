import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

interface User {
  id: string;
  email: string;
  name: string | null;
  picture: string | null;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      try {
        const decoded: any = jwtDecode(token);
        
        const currentTime = Date.now() / 1000;
        if (decoded.exp && decoded.exp < currentTime) {
          localStorage.removeItem('auth_token');
          setUser(null);
        } else {
          setUser({
            id: decoded.sub,
            email: decoded.email,
            name: decoded.name || null,
            picture: decoded.picture || null
          });
        }
      } catch (error) {
        console.error('Invalid token:', error);
        localStorage.removeItem('auth_token');
      }
    }
    setIsLoading(false);
  }, []);

  const login = (token: string) => {
    localStorage.setItem('auth_token', token);
    
    try {
      const decoded: any = jwtDecode(token);
      setUser({
        id: decoded.sub,
        email: decoded.email,
        name: decoded.name || null,
        picture: decoded.picture || null
      });
      navigate('/');
    } catch (error) {
      console.error('Error decoding token:', error);
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setUser(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
