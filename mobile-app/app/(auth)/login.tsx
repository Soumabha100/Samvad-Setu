import React, { useMemo, useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Building2, ShieldCheck, User, Lock, Mail, Phone, ArrowRight } from 'lucide-react-native';
import { useTheme } from '../../context/ThemeContext';

const isOfficialAccount = (email: string) => {
  const normalized = email.trim().toLowerCase();
  if (!normalized) return false;
  return (
    /@(?:[a-z0-9-]+\.)*(?:gov(?:\.in)?|municipal|municipality|authority|official)(?:\.[a-z]{2,})?$/i.test(normalized) ||
    /^(official|authority|municipality|admin)[.@]/i.test(normalized) ||
    /(official|authority|municipality|admin)/i.test(normalized.split('@')[0])
  );
};

export default function AuthScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{ portal?: string }>();
  const portal = params.portal === 'authority' ? 'Authority' : 'Citizen';
  
  const { theme } = useTheme();
  const primaryColor = portal === 'Authority' ? theme.authorityPrimary : theme.citizenPrimary;
  
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const destination = useMemo(
    () => (portal === 'Authority' ? '/(government)/home' : '/(citizen)/home'),
    [portal]
  );

  const handleLogin = async () => {
    const trimmedName = name.trim();
    const trimmedEmail = email.trim().toLowerCase();
    const trimmedPhone = phone.trim();
    const trimmedPassword = password.trim();

    if (!trimmedName || !trimmedEmail || !trimmedPhone || !trimmedPassword) {
      setErrorMessage('Please fill in all fields (Name, Email, Phone, Password).');
      return;
    }

    if (trimmedPhone.length < 10) {
      setErrorMessage('Please enter a valid 10-digit mobile number.');
      return;
    }

    if (portal === 'Authority') {
      const isTestAdmin = trimmedEmail === 'admin@hmc.gov' && trimmedPassword === 'admin123';

      if (!isTestAdmin && !isOfficialAccount(trimmedEmail)) {
        setErrorMessage('Access denied: Restricted to verified official accounts.');
        return;
      }
      if (!isTestAdmin && trimmedPassword.length < 6) {
        setErrorMessage('Official password is invalid.');
        return;
      }
    } else {
      if (trimmedPassword.length < 6) {
        setErrorMessage('Password must be at least 6 characters long.');
        return;
      }

      try {
        const usersJson = await AsyncStorage.getItem('@app_users');
        const users = usersJson ? JSON.parse(usersJson) : {};

        if (users[trimmedEmail]) {
          if (users[trimmedEmail].password !== trimmedPassword) {
            setErrorMessage('Incorrect password for this account.');
            return;
          }
          users[trimmedEmail].phone = trimmedPhone;
          users[trimmedEmail].name = trimmedName;
          await AsyncStorage.setItem('@app_users', JSON.stringify(users));
        } else {
          users[trimmedEmail] = { password: trimmedPassword, phone: trimmedPhone, name: trimmedName };
          await AsyncStorage.setItem('@app_users', JSON.stringify(users));
        }
      } catch (error) {
        console.error("Auth Error:", error);
        setErrorMessage('An error occurred during authentication.');
        return;
      }
    }

    setErrorMessage('');

    // Save session containing user's entered name
    const sessionData = {
      email: trimmedEmail,
      phone: trimmedPhone,
      name: trimmedName,
      role: portal === 'Authority' ? 'official' : 'citizen'
    };
    
    await AsyncStorage.setItem('@app_current_session', JSON.stringify(sessionData));
    await AsyncStorage.setItem('@app_user_role', sessionData.role);
    await AsyncStorage.setItem('@app_user_token', 'dummy-auth-token-123'); 
    
    router.replace(destination as any);
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: theme.background }}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <View style={{ flex: 1, paddingHorizontal: 24, paddingTop: 20, paddingBottom: 20, justifyContent: 'center' }}>
          
          <View style={{ alignItems: 'center', marginBottom: 16 }}>
            <View style={{
                width: 68, height: 68, borderRadius: 20, backgroundColor: theme.card, borderWidth: 1,
                borderColor: primaryColor, alignItems: 'center',
                justifyContent: 'center', marginBottom: 10,
              }}>
              {portal === 'Authority' ? <ShieldCheck size={32} color={primaryColor} /> : <User size={32} color={primaryColor} />}
            </View>
            <Text style={{ fontSize: 24, fontWeight: '800', color: theme.text, marginBottom: 2 }}>{portal} Portal</Text>
            <Text style={{ fontSize: 12, color: theme.subtext, textAlign: 'center', lineHeight: 16 }}>
              {portal === 'Citizen' ? 'Sign in or register a new civic account.' : 'Sign in to your civic workspace.'}
            </Text>
          </View>

          <View style={{ backgroundColor: theme.card, borderRadius: 20, padding: 18, borderWidth: 1, borderColor: theme.border }}>
            
            {/* Full Name Field */}
            <View style={{ marginBottom: 12 }}>
              <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, marginBottom: 4, fontWeight: '700' }}>
                FULL NAME
              </Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 10 }}>
                <User size={16} color={theme.subtext} style={{ marginRight: 10 }} />
                <TextInput
                  value={name}
                  onChangeText={(val) => { setName(val); setErrorMessage(''); }}
                  placeholder="Enter your name"
                  placeholderTextColor={theme.subtext}
                  style={{ flex: 1, color: theme.text, fontSize: 14 }}
                />
              </View>
            </View>

            {/* Email Field */}
            <View style={{ marginBottom: 12 }}>
              <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, marginBottom: 4, fontWeight: '700' }}>
                {portal.toUpperCase()} EMAIL
              </Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 10 }}>
                <Mail size={16} color={theme.subtext} style={{ marginRight: 10 }} />
                <TextInput
                  value={email}
                  onChangeText={(val) => { setEmail(val); setErrorMessage(''); }}
                  placeholder={portal === 'Authority' ? 'admin@hmc.gov' : 'name@example.com'}
                  placeholderTextColor={theme.subtext}
                  keyboardType="email-address"
                  autoCapitalize="none"
                  style={{ flex: 1, color: theme.text, fontSize: 14 }}
                />
              </View>
            </View>

            {/* Phone Number Field */}
            <View style={{ marginBottom: 12 }}>
              <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, marginBottom: 4, fontWeight: '700' }}>
                CONTACT NUMBER
              </Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 10 }}>
                <Phone size={16} color={theme.subtext} style={{ marginRight: 10 }} />
                <TextInput
                  value={phone}
                  onChangeText={(val) => { setPhone(val); setErrorMessage(''); }}
                  placeholder="10-digit Mobile Number"
                  placeholderTextColor={theme.subtext}
                  keyboardType="phone-pad"
                  maxLength={10}
                  style={{ flex: 1, color: theme.text, fontSize: 14 }}
                />
              </View>
            </View>

            {/* Password Field */}
            <View style={{ marginBottom: 6 }}>
              <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, marginBottom: 4, fontWeight: '700' }}>
                PASSWORD
              </Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 10 }}>
                <Lock size={16} color={theme.subtext} style={{ marginRight: 10 }} />
                <TextInput
                  value={password}
                  onChangeText={(val) => { setPassword(val); setErrorMessage(''); }}
                  placeholder={portal === 'Authority' ? 'Official password' : 'Password'}
                  placeholderTextColor={theme.subtext}
                  secureTextEntry
                  style={{ flex: 1, color: theme.text, fontSize: 14 }}
                />
              </View>
            </View>

            <TouchableOpacity onPress={() => router.push('/(auth)/forgot-password')} style={{ marginBottom: 14, alignSelf: 'flex-end' }}>
              <Text style={{ color: primaryColor, fontSize: 12, fontWeight: '600' }}>
                Forgot Password?
              </Text>
            </TouchableOpacity>

            {errorMessage ? <Text style={{ color: theme.error, fontSize: 11, marginBottom: 10, textAlign: 'center' }}>{errorMessage}</Text> : null}

            <TouchableOpacity onPress={handleLogin} style={{ backgroundColor: primaryColor, borderRadius: 12, paddingVertical: 14, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', marginBottom: 8 }}>
              <Text style={{ color: '#0F1B1E', fontSize: 15, fontWeight: '800', marginRight: 8 }}>Sign in</Text>
              <ArrowRight size={16} color="#0F1B1E" />
            </TouchableOpacity>

            {portal === 'Authority' && (
              <Text style={{ color: theme.authorityPrimary, fontSize: 11, textAlign: 'center', marginTop: 8, fontWeight: '600' }}>
                Test: admin@hmc.gov / admin123
              </Text>
            )}
          </View>

        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}