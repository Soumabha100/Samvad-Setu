import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { MapPin, Navigation } from 'lucide-react-native';
import * as Location from 'expo-location';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useTheme } from '../../../context/ThemeContext'; // Import theme hook

export default function LocationScreen() {
  const router = useRouter();
  const { theme, isDarkMode } = useTheme(); // Pull dynamic theme

  const [locationName, setLocationName] = useState('Detecting current GPS location...');
  const [coords, setCoords] = useState<{ latitude: number; longitude: number } | null>(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    getCurrentLocation();
  }, []);

  const getCurrentLocation = async () => {
    setLoading(true);
    try {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setErrorMsg('Permission to access location was denied');
        setLocationName('Howrah, West Bengal (Default)');
        setLoading(false);
        return;
      }

      let currentLocation = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.High,
      });
      
      const { latitude, longitude } = currentLocation.coords;
      setCoords({ latitude, longitude });

      let reverseGeocode = await Location.reverseGeocodeAsync({ latitude, longitude });
      if (reverseGeocode.length > 0) {
        const address = reverseGeocode[0];
        const formattedAddress = `${address.name || address.street || ''}, ${address.subregion || address.city || 'Howrah'}, ${address.region || 'West Bengal'}`;
        setLocationName(formattedAddress.replace(/^,\s/, ''));
      } else {
        setLocationName(`Lat: ${latitude.toFixed(4)}, Long: ${longitude.toFixed(4)}`);
      }
    } catch (error) {
      console.error('Error fetching location:', error);
      setErrorMsg('Could not fetch GPS coordinates.');
      setLocationName('Howrah, West Bengal');
    } finally {
      setLoading(false);
    }
  };

  const handleNext = async () => {
    try {
      const ticketData = {
        location: locationName,
        latitude: coords?.latitude || 22.5958,
        longitude: coords?.longitude || 88.2636,
      };
      await AsyncStorage.setItem('@temp_ticket_location', JSON.stringify(ticketData));
    } catch (e) {
      console.error('Failed to save location', e);
    }
    
    router.push('/(citizen)/submit-problem/review' as any);
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: theme.background, padding: 16, justifyContent: 'space-between' }}>
      <View>
        <View style={{ marginBottom: 24 }}>
          <Text style={{ fontSize: 24, fontWeight: 'bold', color: theme.text }}>Pin Incident Location</Text>
          <Text style={{ fontSize: 13, color: theme.subtext, marginTop: 2 }}>We use your GPS to pinpoint infrastructure issues</Text>
        </View>

        <View style={{ backgroundColor: theme.card, borderRadius: 16, padding: 24, borderWidth: 1, borderColor: theme.border, alignItems: 'center', marginBottom: 20 }}>
          <View style={{ width: 64, height: 64, borderRadius: 32, backgroundColor: isDarkMode ? 'rgba(47, 158, 143, 0.1)' : 'rgba(35, 122, 110, 0.15)', justifyContent: 'center', alignItems: 'center', marginBottom: 16, borderWidth: 1, borderColor: theme.authorityPrimary }}>
            <MapPin size={32} color={theme.authorityPrimary} />
          </View>

          {loading ? (
            <View style={{ alignItems: 'center', marginVertical: 10 }}>
              <ActivityIndicator size="small" color={theme.authorityPrimary} style={{ marginBottom: 8 }} />
              <Text style={{ color: theme.subtext, fontSize: 13 }}>Acquiring satellite lock...</Text>
            </View>
          ) : (
            <>
              <Text style={{ color: theme.text, fontWeight: 'bold', fontSize: 15, textAlign: 'center', marginBottom: 6 }}>
                {locationName}
              </Text>
              {errorMsg && <Text style={{ color: theme.citizenPrimary, fontSize: 11, marginTop: 4 }}>{errorMsg}</Text>}
            </>
          )}
        </View>

        <TouchableOpacity 
          onPress={getCurrentLocation}
          style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center', backgroundColor: theme.card, padding: 12, borderRadius: 12, borderWidth: 1, borderColor: theme.border }}
        >
          <Navigation size={16} color={theme.authorityPrimary} style={{ marginRight: 8 }} />
          <Text style={{ color: theme.authorityPrimary, fontWeight: '600', fontSize: 13 }}>Refresh GPS Location</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity 
        onPress={handleNext}
        style={{ backgroundColor: theme.authorityPrimary, padding: 16, borderRadius: 16, alignItems: 'center', marginBottom: 12 }}
      >
        <Text style={{ color: isDarkMode ? '#0F1B1E' : '#FFFFFF', fontWeight: 'bold', fontSize: 16 }}>Confirm Location & Proceed</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}