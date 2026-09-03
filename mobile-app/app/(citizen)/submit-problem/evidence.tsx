import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView, Image } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { ArrowRight, Camera, Image as ImageIcon, CheckCircle, AlertTriangle } from 'lucide-react-native';
import * as ImagePicker from 'expo-image-picker';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useTheme } from '../../../context/ThemeContext'; // Import theme hook

export default function EvidenceScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const { theme, isDarkMode } = useTheme(); // Pull theme variables
  
  const [imageUri, setImageUri] = useState<string | null>(null);
  
  // New state to control the visibility of the red error message
  const [showError, setShowError] = useState(false);

  const handleOpenCamera = async () => {
    setShowError(false); // Clear error when trying to add photo
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
    if (!permissionResult.granted) {
      alert('Camera permission is required to take a photo!');
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled && result.assets && result.assets.length > 0) {
      setImageUri(result.assets[0].uri);
    }
  };

  const handleOpenGallery = async () => {
    setShowError(false); // Clear error when trying to add photo
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permissionResult.granted) {
      alert('Media library permission is required to select a photo!');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });

    if (!result.canceled && result.assets && result.assets.length > 0) {
      setImageUri(result.assets[0].uri);
    }
  };

  const handleNext = async () => {
    // 1. Mandatory Validation Check
    if (!imageUri) {
      setShowError(true);
      return; // Stop execution, do not navigate
    }

    try {
      // Securely store the image URI locally so the Review screen can pick it up
      await AsyncStorage.setItem('@temp_ticket_image', imageUri);
    } catch (e) {
      console.error('Failed to save image locally', e);
    }

    // Route to the location screen next, since validation passed
    router.push({
      pathname: '/(citizen)/submit-problem/location',
      params: params
    } as any);
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: theme.background, padding: 16 }}>
      <ScrollView contentContainerStyle={{ paddingBottom: 40, flexGrow: 1 }}>
        
        <View style={{ marginBottom: 24, flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
          <Text style={{ fontSize: 14, fontWeight: '600', color: theme.citizenPrimary }}>STEP 2 OF 4</Text>
          <Text style={{ fontSize: 12, color: theme.subtext }}>Evidence Capture</Text>
        </View>

        <Text style={{ fontSize: 24, fontWeight: 'bold', color: theme.text, marginBottom: 8 }}>Attach Photo Evidence</Text>
        <Text style={{ fontSize: 14, color: theme.subtext, marginBottom: 24 }}>
          Take a live photo or upload an existing image from your gallery to help municipal field agents.
        </Text>

        {imageUri && (
          <View style={{ marginBottom: 20, alignItems: 'center', backgroundColor: theme.card, padding: 12, borderRadius: 16, borderWidth: 1, borderColor: theme.authorityPrimary }}>
            <Image source={{ uri: imageUri }} style={{ width: '100%', height: 180, borderRadius: 12, marginBottom: 8 }} />
            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <CheckCircle size={16} color={theme.authorityPrimary} style={{ marginRight: 6 }} />
              <Text style={{ color: theme.authorityPrimary, fontWeight: 'bold', fontSize: 13 }}>Photo Attached Successfully</Text>
            </View>
          </View>
        )}

        <View style={{ flexDirection: 'row', gap: 12, marginBottom: 24 }}>
          <TouchableOpacity 
            onPress={handleOpenCamera}
            style={{ 
              flex: 1, backgroundColor: theme.card, height: 180, borderRadius: 16, 
              borderWidth: 1, borderColor: theme.border, justifyContent: 'center', 
              alignItems: 'center', padding: 12
            }}
          >
            <Camera size={36} color={theme.authorityPrimary} style={{ marginBottom: 12 }} />
            <Text style={{ color: theme.text, fontWeight: 'bold', fontSize: 13, textAlign: 'center' }}>Take Photo</Text>
            <Text style={{ color: theme.subtext, fontSize: 11, marginTop: 4, textAlign: 'center' }}>Open Camera</Text>
          </TouchableOpacity>

          <TouchableOpacity 
            onPress={handleOpenGallery}
            style={{ 
              flex: 1, backgroundColor: theme.card, height: 180, borderRadius: 16, 
              borderWidth: 1, borderColor: theme.border, justifyContent: 'center', 
              alignItems: 'center', padding: 12
            }}
          >
            <ImageIcon size={36} color={theme.authorityPrimary} style={{ marginBottom: 12 }} />
            <Text style={{ color: theme.text, fontWeight: 'bold', fontSize: 13, textAlign: 'center' }}>Upload Photo</Text>
            <Text style={{ color: theme.subtext, fontSize: 11, marginTop: 4, textAlign: 'center' }}>From Gallery</Text>
          </TouchableOpacity>
        </View>

        <View style={{ flex: 1 }} />

        {/* Dynamic Error Message Pop-up */}
        {showError && (
          <View style={{ 
            backgroundColor: isDarkMode ? 'rgba(239, 68, 68, 0.15)' : 'rgba(217, 56, 56, 0.1)', 
            padding: 14, 
            borderRadius: 12, 
            marginBottom: 16,
            borderWidth: 1,
            borderColor: theme.error,
            flexDirection: 'row',
            alignItems: 'center'
          }}>
            <AlertTriangle size={18} color={theme.error} style={{ marginRight: 10 }} />
            <Text style={{ color: theme.error, fontWeight: '700', fontSize: 13, flex: 1 }}>
              Image required! Please attach evidence to proceed.
            </Text>
          </View>
        )}

        <TouchableOpacity 
          onPress={handleNext}
          style={{ 
            backgroundColor: theme.citizenPrimary, paddingVertical: 16, borderRadius: 12, 
            flexDirection: 'row', alignItems: 'center', justifyContent: 'center',
            opacity: (!imageUri && showError) ? 0.7 : 1 // Dim button slightly if error is showing
          }}
        >
          <Text style={{ color: isDarkMode ? '#0F1B1E' : '#FFFFFF', fontWeight: 'bold', fontSize: 16, marginRight: 8 }}>Next: Location Pin</Text>
          <ArrowRight size={18} color={isDarkMode ? '#0F1B1E' : '#FFFFFF'} />
        </TouchableOpacity>

      </ScrollView>
    </SafeAreaView>
  );
}