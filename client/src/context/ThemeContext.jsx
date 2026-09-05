import React, { createContext, useContext, useEffect, useState } from 'react';
import { Monitor, Moon, Sun } from 'lucide-react';

const ThemeContext = createContext(null);
const STORAGE_KEY = 'samvad-setu-theme';

function getSystemTheme() {
  return window.matchMedia?.('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
}

export function ThemeProvider({ children }) {
  const [mode, setMode] = useState(() => localStorage.getItem(STORAGE_KEY) || 'system');
  const [resolvedTheme, setResolvedTheme] = useState('dark');

  useEffect(() => {
    const mediaQuery = window.matchMedia?.('(prefers-color-scheme: light)');
    const applyTheme = () => {
      const nextTheme = mode === 'system' ? getSystemTheme() : mode;
      setResolvedTheme(nextTheme);
      document.documentElement.dataset.theme = nextTheme;
    };

    applyTheme();
    mediaQuery?.addEventListener('change', applyTheme);
    return () => mediaQuery?.removeEventListener('change', applyTheme);
  }, [mode]);

  const setThemeMode = (nextMode) => {
    setMode(nextMode);
    localStorage.setItem(STORAGE_KEY, nextMode);
  };

  return (
    <ThemeContext.Provider value={{ mode, resolvedTheme, setThemeMode }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}

export function ThemeSwitcher({ compact = false }) {
  const { mode, setThemeMode } = useTheme();
  const options = [
    { value: 'light', label: 'Light', icon: Sun },
    { value: 'dark', label: 'Dark', icon: Moon },
    { value: 'system', label: 'System', icon: Monitor },
  ];

  return (
    <div className={`theme-switcher ${compact ? 'theme-switcher-compact' : ''}`} role="group" aria-label="Theme mode">
      {options.map(({ value, label, icon: Icon }) => (
        <button
          key={value}
          type="button"
          title={`${label} theme`}
          aria-pressed={mode === value}
          onClick={() => setThemeMode(value)}
          className={mode === value ? 'theme-option active' : 'theme-option'}
        >
          <Icon size={14} />
          {!compact && <span>{label}</span>}
        </button>
      ))}
    </div>
  );
}