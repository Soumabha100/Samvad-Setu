import React, { createContext, useState, useEffect, useContext } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

// 1. Define your two color palettes
export const themes = {
  dark: {
    background: '#0F1B1E',
    card: '#16262A',
    text: '#F2EFE9',
    subtext: '#9BA8A6',
    border: '#1D3238',
    authorityPrimary: '#2F9E8F',
    citizenPrimary: '#E8A33D',
    error: '#FFB4B4',
  },
  light: {
    background: '#F4F7F6',
    card: '#FFFFFF',
    text: '#111D20',
    subtext: '#6B7A78',
    border: '#E2E8E7',
    authorityPrimary: '#237A6E', // Slightly darker for better contrast on light mode
    citizenPrimary: '#D48A22',   // Slightly darker for better contrast
    error: '#D93838',
  }
};

// 2. Create the Context
const ThemeContext = createContext<any>(null);

// 3. Create the Provider Wrapper
export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [isDarkMode, setIsDarkMode] = useState(true);

  // Load the saved theme on startup
  useEffect(() => {
    const loadTheme = async () => {
      const savedTheme = await AsyncStorage.getItem('@app_theme');
      if (savedTheme === 'light') setIsDarkMode(false);
    };
    loadTheme();
  }, []);

  // Function to toggle and save the theme
  const toggleTheme = async () => {
    const newTheme = !isDarkMode;
    setIsDarkMode(newTheme);
    await AsyncStorage.setItem('@app_theme', newTheme ? 'dark' : 'light');
  };

  const currentTheme = isDarkMode ? themes.dark : themes.light;

  return (
    <ThemeContext.Provider value={{ theme: currentTheme, isDarkMode, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// 4. Custom Hook for easy access in your screens
export const useTheme = () => useContext(ThemeContext);