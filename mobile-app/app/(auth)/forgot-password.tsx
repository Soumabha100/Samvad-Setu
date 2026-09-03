import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Mail, KeyRound, Lock, ArrowRight, ArrowLeft } from 'lucide-react-native';
import { useTheme } from '../../context/ThemeContext'; // Import theme hook

export default function ForgotPasswordScreen() {
  const router = useRouter();
  const { theme, isDarkMode } = useTheme(); // Pull dynamic theme
  
  // Step 1: 'email', Step 2: 'otp', Step 3: 'reset'
  const [step, setStep] = useState('email'); 
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // 1. Check if user exists and "send" OTP
  const handleSendOTP = async () => {
    const trimmedEmail = email.trim().toLowerCase();
    if (!trimmedEmail) return setErrorMessage('Please enter your email.');

    try {
      const usersJson = await AsyncStorage.getItem('@app_users');
      const users = usersJson ? JSON.parse(usersJson) : {};

      if (!users[trimmedEmail]) {
        return setErrorMessage('No account found with this email.');
      }

      // In a real app, you would call your Node.js/Express API here to send the email.
      // For now, we simulate success and move to the OTP step.
      setErrorMessage('');
      setStep('otp');
      Alert.alert("OTP Sent", "For testing, your OTP is: 1234");
    } catch (error) {
      setErrorMessage('Failed to verify account.');
    }
  };

  // 2. Verify the OTP
  const handleVerifyOTP = () => {
    if (otp === '1234') { // Hardcoded mock OTP
      setErrorMessage('');
      setStep('reset');
    } else {
      setErrorMessage('Invalid OTP. Please try again.');
    }
  };

  // 3. Save the new password
  const handleResetPassword = async () => {
    if (newPassword.length < 6) return setErrorMessage('Password must be at least 6 characters.');

    try {
      const trimmedEmail = email.trim().toLowerCase();
      const usersJson = await AsyncStorage.getItem('@app_users');
      const users = usersJson ? JSON.parse(usersJson) : {};

      // Update the password in storage
      users[trimmedEmail].password = newPassword;
      await AsyncStorage.setItem('@app_users', JSON.stringify(users));

      Alert.alert("Success", "Password updated successfully!");
      router.replace('/(auth)/login');
    } catch (error) {
      setErrorMessage('Failed to reset password.');
    }
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: theme.background }}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <View style={{ flex: 1, paddingHorizontal: 24, paddingTop: 40, justifyContent: 'center' }}>
          
          <TouchableOpacity onPress={() => router.back()} style={{ marginBottom: 30 }}>
            <ArrowLeft size={24} color={theme.subtext} />
          </TouchableOpacity>

          <Text style={{ fontSize: 28, fontWeight: '800', color: theme.text, marginBottom: 10 }}>
            {step === 'email' ? 'Reset Password' : step === 'otp' ? 'Enter OTP' : 'New Password'}
          </Text>
          <Text style={{ fontSize: 14, color: theme.subtext, marginBottom: 30, lineHeight: 20 }}>
            {step === 'email' ? 'Enter your registered email address to receive a verification code.' : 
             step === 'otp' ? `We sent a 4-digit code to ${email}` : 
             'Create a new secure password for your account.'}
          </Text>

          <View style={{ backgroundColor: theme.card, borderRadius: 20, padding: 20, borderWidth: 1, borderColor: theme.border }}>
            
            {/* STEP 1: EMAIL INPUT */}
            {step === 'email' && (
              <View style={{ marginBottom: 20 }}>
                <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 12 }}>
                  <Mail size={18} color={theme.subtext} style={{ marginRight: 10 }} />
                  <TextInput
                    value={email}
                    onChangeText={(val) => { setEmail(val); setErrorMessage(''); }}
                    placeholder="Email address"
                    placeholderTextColor={theme.subtext}
                    keyboardType="email-address"
                    autoCapitalize="none"
                    style={{ flex: 1, color: theme.text, fontSize: 15 }}
                  />
                </View>
              </View>
            )}

            {/* STEP 2: OTP INPUT */}
            {step === 'otp' && (
              <View style={{ marginBottom: 20 }}>
                <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 12 }}>
                  <KeyRound size={18} color={theme.subtext} style={{ marginRight: 10 }} />
                  <TextInput
                    value={otp}
                    onChangeText={(val) => { setOtp(val); setErrorMessage(''); }}
                    placeholder="4-digit OTP (1234)"
                    placeholderTextColor={theme.subtext}
                    keyboardType="number-pad"
                    maxLength={4}
                    style={{ flex: 1, color: theme.text, fontSize: 15 }}
                  />
                </View>
              </View>
            )}

            {/* STEP 3: NEW PASSWORD INPUT */}
            {step === 'reset' && (
              <View style={{ marginBottom: 20 }}>
                <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 12 }}>
                  <Lock size={18} color={theme.subtext} style={{ marginRight: 10 }} />
                  <TextInput
                    value={newPassword}
                    onChangeText={(val) => { setNewPassword(val); setErrorMessage(''); }}
                    placeholder="New Password"
                    placeholderTextColor={theme.subtext}
                    secureTextEntry
                    style={{ flex: 1, color: theme.text, fontSize: 15 }}
                  />
                </View>
              </View>
            )}

            {errorMessage ? <Text style={{ color: theme.error, fontSize: 12, marginBottom: 12, textAlign: 'center' }}>{errorMessage}</Text> : null}

            <TouchableOpacity 
              onPress={step === 'email' ? handleSendOTP : step === 'otp' ? handleVerifyOTP : handleResetPassword} 
              style={{ backgroundColor: theme.authorityPrimary, borderRadius: 14, paddingVertical: 16, flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}>
              <Text style={{ color: isDarkMode ? '#0F1B1E' : '#FFFFFF', fontSize: 16, fontWeight: '800', marginRight: 8 }}>
                {step === 'email' ? 'Send OTP' : step === 'otp' ? 'Verify Code' : 'Update Password'}
              </Text>
              <ArrowRight size={18} color={isDarkMode ? '#0F1B1E' : '#FFFFFF'} />
            </TouchableOpacity>

          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}