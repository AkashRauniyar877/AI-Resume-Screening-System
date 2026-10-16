import React, { createContext, useContext, useState, useEffect } from 'react';
import { getToken, setToken, removeToken } from '../utils/auth';
import { loginApi, registerApi, getMeApi } from '../api/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setTokenState] = useState(getToken());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCurrentUser = async () => {
    const storedToken = getToken();
    if (!storedToken) {
      setUser(null);
      setTokenState(null);
      setLoading(false);
      return;
    }

    try {
      const userData = await getMeApi();
      setUser(userData);
      setTokenState(storedToken);
    } catch (err) {
      console.warn('Failed to validate session token:', err.message);
      removeToken();
      setUser(null);
      setTokenState(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  const login = async (email, password) => {
    setError(null);
    try {
      const tokenRes = await loginApi({ email, password });
      const accessToken = tokenRes.access_token;
      setToken(accessToken);
      setTokenState(accessToken);

      // Fetch user profile
      const userData = await getMeApi();
      setUser(userData);
      return userData;
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
      throw err;
    }
  };

  const register = async (name, email, password) => {
    setError(null);
    try {
      const newUser = await registerApi({ name, email, password });
      // Automatically attempt login after successful registration
      await login(email, password);
      return newUser;
    } catch (err) {
      setError(err.message || 'Registration failed.');
      throw err;
    }
  };

  const logout = () => {
    removeToken();
    setUser(null);
    setTokenState(null);
    setError(null);
  };

  const value = {
    user,
    token,
    loading,
    isAuthenticated: Boolean(user && token),
    error,
    login,
    register,
    logout,
    refreshUser: fetchCurrentUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
