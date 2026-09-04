import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Building2, User, Lock, Mail, GraduationCap, ShieldAlert, ArrowRight } from 'lucide-react-native';
import { useTheme } from '../../context/ThemeContext';
import { useAuthStore } from '../../store/authStore';
import { useToastStore } from '../../store/toastStore';

export default function SignupScreen() {
  const router = useRouter();
  const { theme } = useTheme();
  const { signup, isLoading } = useAuthStore();
  const { showToast } = useToastStore();

  const [role, setRole] = useState<'citizen' | 'hei' | 'industry_csr'>('citizen');
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    institutionName: '',
    department: '',
  });

  const getPrimaryColor = () => {
    if (role === 'citizen') return theme.citizenPrimary;
    if (role === 'hei') return '#2F9E8F';
    return theme.authorityPrimary;
  };
  
  const primaryColor = getPrimaryColor();

  const handleSignup = async () => {
    const { name, email, password, institutionName, department } = formData;
    
    if (!name.trim() || !email.trim() || !password.trim()) {
      showToast('Name, Email, and Password are required.', 'error');
      return;
    }
    if (role !== 'citizen' && (!institutionName.trim() || !department.trim())) {
      showToast('Organisation Name and Registration ID are required.', 'error');
      return;
    }

    const payload = {
      name: name.trim(),
      email: email.trim().toLowerCase(),
      password: password.trim(),
      role,
      institutionName: institutionName.trim(),
      department: department.trim(),
    };

    const success = await signup(payload);

    if (success) {
      showToast('Account created successfully!', 'success');
      // Redirect based on role
      if (role === 'citizen') router.replace('/(citizen)/home');
      else if (role === 'hei') router.replace('/(hei)/home' as any);
      else router.replace('/(industry)/home' as any);
    } else {
      const errorMsg = useAuthStore.getState().error || 'Registration failed.';
      showToast(errorMsg, 'error');
    }
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: theme.background }}>
      <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView contentContainerStyle={{ padding: 24, paddingBottom: 40 }}>
          
          <View style={{ alignItems: 'center', marginBottom: 20 }}>
            <Text style={{ fontSize: 24, fontWeight: '800', color: theme.text, marginBottom: 4 }}>Create an Account</Text>
            <Text style={{ fontSize: 12, color: theme.subtext, textAlign: 'center' }}>Select your registration path below.</Text>
          </View>

          {/* Role Selection Tabs */}
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 16 }}>
            {[
              { id: 'citizen', label: 'Citizen', icon: User, color: theme.citizenPrimary },
              { id: 'hei', label: 'University', icon: GraduationCap, color: '#2F9E8F' },
              { id: 'industry_csr', label: 'Industry', icon: Building2, color: theme.authorityPrimary }
            ].map((tab) => {
              const isActive = role === tab.id;
              const Icon = tab.icon;
              return (
                <TouchableOpacity
                  key={tab.id}
                  onPress={() => setRole(tab.id as any)}
                  style={{
                    flex: 1,
                    marginHorizontal: 4,
                    paddingVertical: 12,
                    backgroundColor: isActive ? theme.card : theme.background,
                    borderWidth: 1,
                    borderColor: isActive ? tab.color : theme.border,
                    borderRadius: 12,
                    alignItems: 'center'
                  }}
                >
                  <Icon size={20} color={isActive ? tab.color : theme.subtext} style={{ marginBottom: 6 }} />
                  <Text style={{ fontSize: 11, fontWeight: '600', color: isActive ? tab.color : theme.subtext }}>{tab.label}</Text>
                </TouchableOpacity>
              );
            })}
          </View>

          {role !== 'citizen' && (
            <View style={{ backgroundColor: theme.card, borderColor: '#2F9E8F', borderWidth: 1, borderRadius: 12, padding: 12, flexDirection: 'row', marginBottom: 16 }}>
              <ShieldAlert size={16} color="#2F9E8F" style={{ marginRight: 8, marginTop: 2 }} />
              <Text style={{ flex: 1, color: theme.subtext, fontSize: 11, lineHeight: 16 }}>
                Institutional accounts require verification by administrators prior to claiming projects.
              </Text>
            </View>
          )}

          <View style={{ backgroundColor: theme.card, borderRadius: 20, padding: 18, borderWidth: 1, borderColor: theme.border }}>
            
            <View style={{ marginBottom: 12 }}>
              <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, marginBottom: 4, fontWeight: '700' }}>FULL NAME</Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 10 }}>
                <User size={16} color={theme.subtext} style={{ marginRight: 10 }} />
                <TextInput
                  value={formData.name}
                  onChangeText={(val) => setFormData({ ...formData, name: val })}
                  placeholder="Full Name"
                  placeholderTextColor={theme.subtext}
                  style={{ flex: 1, color: theme.text, fontSize: 14 }}
                />
              </View>
            </View>

            <View style={{ marginBottom: 12 }}>
              <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, marginBottom: 4, fontWeight: '700' }}>EMAIL ADDRESS</Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 10 }}>
                <Mail size={16} color={theme.subtext} style={{ marginRight: 10 }} />
                <TextInput
                  value={formData.email}
                  onChangeText={(val) => setFormData({ ...formData, email: val })}
                  placeholder="name@example.com"
                  placeholderTextColor={theme.subtext}
                  keyboardType="email-address"
                  autoCapitalize="none"
                  style={{ flex: 1, color: theme.text, fontSize: 14 }}
                />
              </View>
            </View>

            <View style={{ marginBottom: 12 }}>
              <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, marginBottom: 4, fontWeight: '700' }}>PASSWORD</Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 10 }}>
                <Lock size={16} color={theme.subtext} style={{ marginRight: 10 }} />
                <TextInput
                  value={formData.password}
                  onChangeText={(val) => setFormData({ ...formData, password: val })}
                  placeholder="Create a secure password"
                  placeholderTextColor={theme.subtext}
                  secureTextEntry
                  style={{ flex: 1, color: theme.text, fontSize: 14 }}
                />
              </View>
            </View>

            {role !== 'citizen' && (
              <>
                <View style={{ marginBottom: 12 }}>
                  <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, marginBottom: 4, fontWeight: '700' }}>ORGANISATION NAME</Text>
                  <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 10 }}>
                    <Building2 size={16} color={theme.subtext} style={{ marginRight: 10 }} />
                    <TextInput
                      value={formData.institutionName}
                      onChangeText={(val) => setFormData({ ...formData, institutionName: val })}
                      placeholder="Organisation Name"
                      placeholderTextColor={theme.subtext}
                      style={{ flex: 1, color: theme.text, fontSize: 14 }}
                    />
                  </View>
                </View>

                <View style={{ marginBottom: 12 }}>
                  <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, marginBottom: 4, fontWeight: '700' }}>REGISTRATION ID</Text>
                  <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: theme.background, borderRadius: 12, borderWidth: 1, borderColor: theme.border, paddingHorizontal: 12, paddingVertical: 10 }}>
                    <ShieldAlert size={16} color={theme.subtext} style={{ marginRight: 10 }} />
                    <TextInput
                      value={formData.department}
                      onChangeText={(val) => setFormData({ ...formData, department: val })}
                      placeholder="AISHE Code / CIN"
                      placeholderTextColor={theme.subtext}
                      style={{ flex: 1, color: theme.text, fontSize: 14 }}
                    />
                  </View>
                </View>
              </>
            )}

            <TouchableOpacity 
              onPress={handleSignup} 
              disabled={isLoading} 
              style={{ backgroundColor: primaryColor, borderRadius: 12, paddingVertical: 14, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', marginTop: 8, opacity: isLoading ? 0.7 : 1 }}
            >
              <Text style={{ color: '#0F1B1E', fontSize: 15, fontWeight: '800', marginRight: 8 }}>
                {isLoading ? 'Creating Account...' : 'Complete Registration'}
              </Text>
              {!isLoading && <ArrowRight size={16} color="#0F1B1E" />}
            </TouchableOpacity>

            <TouchableOpacity onPress={() => router.push('/(auth)/login')} style={{ marginTop: 16, alignItems: 'center' }}>
              <Text style={{ color: theme.subtext, fontSize: 12 }}>
                Already registered? <Text style={{ color: primaryColor, fontWeight: 'bold' }}>Sign In</Text>
              </Text>
            </TouchableOpacity>

          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}