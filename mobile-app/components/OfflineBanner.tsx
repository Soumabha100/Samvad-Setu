import React, { useEffect, useState } from 'react';
import { View, Text, Animated } from 'react-native';
import NetInfo from '@react-native-community/netinfo';
import { WifiOff } from 'lucide-react-native';

export default function OfflineBanner() {
  const [isConnected, setIsConnected] = useState(true);
  const slideAnim = useState(new Animated.Value(-100))[0];

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      const connected = state.isConnected === true;
      setIsConnected(connected);
      
      Animated.timing(slideAnim, {
        toValue: connected ? -100 : 0,
        duration: 300,
        useNativeDriver: true,
      }).start();
    });

    return () => unsubscribe();
  }, []);

  if (isConnected) return null;

  return (
    <Animated.View style={{
      transform: [{ translateY: slideAnim }],
      position: 'absolute',
      top: 0,
      left: 0,
      right: 0,
      backgroundColor: '#C1443B', // Red alert color
      padding: 10,
      paddingTop: 45, // Account for safe area notch
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 9999,
      elevation: 10,
    }}>
      <WifiOff size={16} color="#FFF" style={{ marginRight: 8 }} />
      <Text style={{ color: '#FFF', fontSize: 13, fontWeight: '700' }}>
        No Internet Connection. Operating in offline mode.
      </Text>
    </Animated.View>
  );
}