import { Tabs } from 'expo-router';
import React from 'react';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { LayoutDashboard, Map as MapIcon, UserCircle } from 'lucide-react-native';

export default function CitizenTabLayout() {
  // 1. Get the safe margins of the specific Android device
  const insets = useSafeAreaInsets();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#E8A33D', // Accent color for the Citizen portal
        tabBarInactiveTintColor: '#9BA8A6',
        headerShown: false,
        tabBarStyle: {
          backgroundColor: '#16262A',
          borderTopColor: '#1D3238',
          // 2. Dynamically add the Android system bar height to our custom height
          height: 60 + insets.bottom,
          // 3. Push the clickable icons up above the system buttons
          paddingBottom: Math.max(insets.bottom, 8),
          paddingTop: 8,
        },
      }}>
      
      {/* 🟢 VISIBLE TABS */}
      <Tabs.Screen
        name="home"
        options={{
          title: 'Dashboard',
          tabBarIcon: ({ color }) => <LayoutDashboard size={22} color={color} />,
        }}
      />
      
      <Tabs.Screen
        name="map"
        options={{
          title: 'Heatmap',
          tabBarIcon: ({ color }) => <MapIcon size={22} color={color} />,
        }}
      />
      
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color }) => <UserCircle size={22} color={color} />,
        }}
      />

      {/* 🔴 HIDDEN TABS (These can be navigated to, but won't show on the bottom bar) */}
      <Tabs.Screen 
        name="submit-problem" 
        options={{ href: null }} 
      />
      
      <Tabs.Screen 
        name="ticket/[id]" 
        options={{ href: null }} 
      />
      
      <Tabs.Screen 
        name="notifications" 
        options={{ href: null }} 
      />
      
    </Tabs>
  );
}