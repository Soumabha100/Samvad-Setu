import React from 'react';
import { Stack } from 'expo-router';
import OfflineBanner from '../components/OfflineBanner'; // Import the banner
import { ThemeProvider } from '../context/ThemeContext'; // Import the ThemeProvider

export default function RootLayout() {
  return (
    <ThemeProvider>
      {/* The banner sits at the very top of the app */}
      <OfflineBanner />
      
      {/* Your existing navigation stack */}
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" />
        <Stack.Screen name="(auth)" />
        <Stack.Screen name="(citizen)" />
        <Stack.Screen name="(government)" />
        <Stack.Screen name="(hei)" />
        <Stack.Screen name="(industry)" />
      </Stack>
    </ThemeProvider>
  );
}