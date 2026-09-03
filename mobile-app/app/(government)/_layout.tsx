import { Tabs, useRouter } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { LayoutDashboard, Map as MapIcon, UserCircle } from 'lucide-react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function GovernmentTabLayout() {
  const router = useRouter();
  const insets = useSafeAreaInsets();
  
  // Strict login: Add a loading state to prevent the portal from flashing
  const [isAuthorized, setIsAuthorized] = useState(false);

  useEffect(() => {
    const checkAccess = async () => {
      try {
        const role = await AsyncStorage.getItem('@app_user_role');
        const token = await AsyncStorage.getItem('@app_user_token'); // Strict token check

        // Strict Check: Must have BOTH the official role AND an active token
        if (role !== 'official' || !token) {
          router.replace({ pathname: '/(auth)/login', params: { portal: 'authority' } } as any);
        } else {
          setIsAuthorized(true); // Reveal tabs only if fully verified
        }
      } catch (error) {
        // If storage fails to read, boot them out to be safe
        console.error("Auth check failed:", error);
        router.replace({ pathname: '/(auth)/login', params: { portal: 'authority' } } as any);
      }
    };

    checkAccess();
  }, [router]);

  // Show a blank screen (or loading spinner) while checking credentials
  if (!isAuthorized) {
    return (
      <View style={{ flex: 1, backgroundColor: '#16262A', justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#2F9E8F" />
      </View>
    );
  }

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#2F9E8F',
        tabBarInactiveTintColor: '#9BA8A6',
        headerShown: false,
        tabBarStyle: {
          backgroundColor: '#16262A',
          borderTopColor: '#1D3238',
          // Dynamically adjust height and bottom padding based on the phone's nav bar:
          height: 60 + insets.bottom,
          paddingBottom: 8 + insets.bottom,
          paddingTop: 8,
        },
      }}>
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
          title: 'Official',
          tabBarIcon: ({ color }) => <UserCircle size={22} color={color} />,
        }}
      />
      
      {/* Hide dynamic ticket detail page */}
      <Tabs.Screen 
        name="ticket/[id]" 
        options={{ 
          href: null,
          tabBarStyle: { display: 'none' } 
        }} 
      />

      {/* Hide analytics dashboard */}
      <Tabs.Screen 
        name="analytics" 
        options={{ 
          href: null,
          tabBarStyle: { display: 'none' }
        }} 
      />
    </Tabs>
  );
}