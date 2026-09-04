import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ScrollView, ActivityIndicator, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Send, MapPin, FileText, AlertTriangle, Image as ImageIcon } from 'lucide-react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Location from 'expo-location';
import { useProblemStore } from '../../../store/problemStore';
import { useTheme } from '../../../context/ThemeContext'; // Import theme hook

export default function ReviewScreen() {
  const router = useRouter();
  const { theme, isDarkMode } = useTheme(); // Pull dynamic theme
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const department = useProblemStore((state: any) => state.department);
  const description = useProblemStore((state: any) => state.description);

  const [reportLocation, setReportLocation] = useState('Fetching GPS location...');
  const [coords, setCoords] = useState<{ latitude: number; longitude: number } | null>(null);
  const [isLocLoading, setIsLocLoading] = useState(true);
  const [attachedImage, setAttachedImage] = useState<string | null>(null);

  useEffect(() => {
    fetchCurrentGPSLocation();
    fetchAttachedImage();
  }, []);

  const fetchAttachedImage = async () => {
    try {
      const img = await AsyncStorage.getItem('@temp_ticket_image');
      if (img) setAttachedImage(img);
    } catch (e) {
      console.error('Error fetching image for review', e);
    }
  };

  const fetchCurrentGPSLocation = async () => {
    setIsLocLoading(true);
    try {
      const servicesEnabled = await Location.hasServicesEnabledAsync();
      if (!servicesEnabled) {
        setReportLocation('Location services disabled on device');
        setIsLocLoading(false);
        return;
      }

      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setReportLocation('Location permission denied');
        setIsLocLoading(false);
        return;
      }

      let location = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.Balanced,
      }).catch(async () => {
        return await Location.getLastKnownPositionAsync();
      });

      if (!location) {
        location = await Location.getLastKnownPositionAsync();
      }

      if (location) {
        const { latitude, longitude } = location.coords;
        setCoords({ latitude, longitude });

        const reverseGeocode = await Location.reverseGeocodeAsync({ latitude, longitude });
        if (reverseGeocode && reverseGeocode.length > 0) {
          const place = reverseGeocode[0];
          const parts = [
            place.name || place.street,
            place.subregion || place.district || place.city,
            place.region,
            place.country,
          ].filter(Boolean);

          setReportLocation(parts.length > 0 ? parts.join(', ') : `Lat: ${latitude.toFixed(4)}, Long: ${longitude.toFixed(4)}`);
        } else {
          setReportLocation(`Lat: ${latitude.toFixed(4)}, Long: ${longitude.toFixed(4)}`);
        }
      } else {
        setReportLocation('Unable to pinpoint location');
      }
    } catch (error) {
      console.error('Error acquiring location:', error);
      setReportLocation('Location unavailable');
    } finally {
      setIsLocLoading(false);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const ticketId = `CHAL-${Math.floor(1000 + Math.random() * 9000)}`;
      const newTicket = {
        id: ticketId,
        title: description ? (description.length > 35 ? `${description.substring(0, 35)}...` : description) : 'Grassroots Innovation Challenge',
        domain: department,
        description: description,
        stage: 'Submitted',
        status: 'Open for HEI Claim',
        assignedDept: 'Pending AI Routing',
        suggestedHEI: 'Pending Allocation',
        industryPledge: null,
        location: reportLocation,
        latitude: coords?.latitude || 23.3441,
        longitude: coords?.longitude || 85.3096,
        imageUri: attachedImage,
        date: 'Just now',
      };

      const existingTicketsJson = await AsyncStorage.getItem('@citizen_tickets');
      const existingTickets = existingTicketsJson ? JSON.parse(existingTicketsJson) : [];

      const updatedTickets = [newTicket, ...existingTickets];
      await AsyncStorage.setItem('@citizen_tickets', JSON.stringify(updatedTickets));

      await AsyncStorage.removeItem('@temp_ticket_image');

      setTimeout(() => {
        setIsSubmitting(false);
        router.push('/(citizen)/home' as any);
      }, 800);
    } catch (error) {
      console.error('Failed to save ticket locally', error);
      setIsSubmitting(false);
    }
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: theme.background, padding: 16 }}>
      <ScrollView contentContainerStyle={{ paddingBottom: 40, flexGrow: 1 }} showsVerticalScrollIndicator={false}>
        
        <View style={{ marginBottom: 24, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
          <Text style={{ fontSize: 14, fontWeight: '600', color: theme.citizenPrimary }}>STEP 4 OF 4</Text>
          <Text style={{ fontSize: 12, color: theme.subtext }}>Review & Submit</Text>
        </View>

        <Text style={{ fontSize: 24, fontWeight: 'bold', color: theme.text, marginBottom: 8 }}>Review your report</Text>
        <Text style={{ fontSize: 14, color: theme.subtext, marginBottom: 24 }}>
          Please verify the details below before submitting to the innovation portal.
        </Text>

        <View style={{ backgroundColor: theme.card, borderRadius: 16, padding: 20, borderWidth: 1, borderColor: theme.border, marginBottom: 24 }}>
          
          <View style={{ flexDirection: 'row', alignItems: 'flex-start', marginBottom: 20 }}>
            <AlertTriangle size={20} color={theme.citizenPrimary} style={{ marginTop: 2, marginRight: 12 }} />
            <View style={{ flex: 1 }}>
              <Text style={{ color: theme.subtext, fontSize: 12, marginBottom: 4 }}>THEMATIC DOMAIN</Text>
              <Text style={{ color: theme.text, fontSize: 16, fontWeight: '500' }}>{department}</Text>
            </View>
          </View>

          <View style={{ flexDirection: 'row', alignItems: 'flex-start', marginBottom: 20 }}>
            <FileText size={20} color={theme.citizenPrimary} style={{ marginTop: 2, marginRight: 12 }} />
            <View style={{ flex: 1 }}>
              <Text style={{ color: theme.subtext, fontSize: 12, marginBottom: 4 }}>DESCRIPTION</Text>
              <Text style={{ color: theme.text, fontSize: 14, lineHeight: 20 }}>
                {description || 'No description provided.'}
              </Text>
            </View>
          </View>

          <View style={{ flexDirection: 'row', alignItems: 'flex-start', marginBottom: 20 }}>
            <MapPin size={20} color={theme.citizenPrimary} style={{ marginTop: 2, marginRight: 12 }} />
            <View style={{ flex: 1 }}>
              <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                <Text style={{ color: theme.subtext, fontSize: 12 }}>GPS LOCATION</Text>
                <TouchableOpacity onPress={fetchCurrentGPSLocation} disabled={isLocLoading}>
                  <Text style={{ color: theme.authorityPrimary, fontSize: 11, fontWeight: '600' }}>
                    {isLocLoading ? 'Locating...' : 'Refresh GPS'}
                  </Text>
                </TouchableOpacity>
              </View>
              {isLocLoading ? (
                <View style={{ flexDirection: 'row', alignItems: 'center', marginTop: 4 }}>
                  <ActivityIndicator size="small" color={theme.authorityPrimary} style={{ marginRight: 8 }} />
                  <Text style={{ color: theme.subtext, fontSize: 13 }}>Acquiring satellite fix...</Text>
                </View>
              ) : (
                <Text style={{ color: theme.text, fontSize: 14, lineHeight: 20 }}>{reportLocation}</Text>
              )}
            </View>
          </View>

          <View style={{ flexDirection: 'row', alignItems: 'flex-start' }}>
            <ImageIcon size={20} color={theme.citizenPrimary} style={{ marginTop: 2, marginRight: 12 }} />
            <View style={{ flex: 1 }}>
              <Text style={{ color: theme.subtext, fontSize: 12, marginBottom: 8 }}>EVIDENCE</Text>
              {attachedImage ? (
                <Image 
                  source={{ uri: attachedImage }} 
                  style={{ width: 100, height: 100, borderRadius: 8, borderWidth: 1, borderColor: theme.authorityPrimary }} 
                />
              ) : (
                <Text style={{ color: theme.citizenPrimary, fontSize: 14, fontWeight: '500' }}>No image attached</Text>
              )}
            </View>
          </View>

        </View>

        <View style={{ flex: 1 }} />

        <TouchableOpacity 
          onPress={handleSubmit}
          disabled={isSubmitting || isLocLoading}
          style={{ 
            backgroundColor: theme.authorityPrimary, 
            paddingVertical: 16, 
            borderRadius: 12, 
            flexDirection: 'row', 
            alignItems: 'center', 
            justifyContent: 'center',
            opacity: isLocLoading ? 0.7 : 1
          }}
        >
          {isSubmitting ? (
            <ActivityIndicator color={isDarkMode ? '#0F1B1E' : '#FFFFFF'} />
          ) : (
            <>
              <Text style={{ color: isDarkMode ? '#0F1B1E' : '#FFFFFF', fontWeight: 'bold', fontSize: 16, marginRight: 8 }}>
                Submit Challenge
              </Text>
              <Send size={18} color={isDarkMode ? '#0F1B1E' : '#FFFFFF'} />
            </>
          )}
        </TouchableOpacity>

      </ScrollView>
    </SafeAreaView>
  );
}