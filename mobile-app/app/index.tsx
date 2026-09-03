import React from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { ShieldCheck, User, ArrowRight, Building2, Activity, Clock3, Sun, Moon } from 'lucide-react-native';
import { useTheme } from '../context/ThemeContext'; // Import the new ThemeContext

export default function RoleSelectionScreen() {
  const router = useRouter();
  
  // Pull all the dynamic values from our context!
  const { theme, isDarkMode, toggleTheme } = useTheme();

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: theme.background, padding: 20 }}>
      
      {/* --> THEME TOGGLE BUTTON (Top Right) <-- */}
      <View style={{ alignItems: 'flex-end', marginBottom: 10 }}>
        <TouchableOpacity 
          onPress={toggleTheme}
          style={{
            backgroundColor: theme.card,
            padding: 10,
            borderRadius: 20,
            borderWidth: 1,
            borderColor: theme.border,
            flexDirection: 'row',
            alignItems: 'center'
          }}
        >
          {isDarkMode ? <Sun size={18} color={theme.subtext} /> : <Moon size={18} color={theme.subtext} />}
        </TouchableOpacity>
      </View>

      <ScrollView contentContainerStyle={{ flexGrow: 1, justifyContent: 'center', paddingBottom: 40 }}>
        <View style={{ alignItems: 'center', marginBottom: 28 }}>
          <View style={{ width: 84, height: 84, borderRadius: 24, backgroundColor: theme.card, borderWidth: 1, borderColor: theme.authorityPrimary, alignItems: 'center', justifyContent: 'center', marginBottom: 16, shadowColor: theme.authorityPrimary, shadowOpacity: 0.22, shadowRadius: 18, shadowOffset: { width: 0, height: 10 } }}>
            <ShieldCheck size={38} color={theme.authorityPrimary} />
          </View>
          <Text style={{ fontSize: 30, fontWeight: '800', color: theme.text, textAlign: 'center', marginBottom: 8 }}>
            Samvad-Setu
          </Text>
          <Text style={{ fontSize: 14, color: theme.subtext, textAlign: 'center', paddingHorizontal: 24, lineHeight: 20 }}>
            Public issue reporting, municipal oversight, and transparent civic action in one place.
          </Text>
        </View>

        <View style={{ flexDirection: 'row', gap: 12, marginBottom: 20 }}>
          <View style={{ flex: 1, backgroundColor: theme.card, borderRadius: 14, padding: 14, borderWidth: 1, borderColor: theme.border }}>
            <Activity size={16} color={theme.authorityPrimary} style={{ marginBottom: 8 }} />
            <Text style={{ color: theme.subtext, fontSize: 10, marginBottom: 4, letterSpacing: 0.8 }}>LIVE NODES</Text>
            <Text style={{ color: theme.text, fontSize: 20, fontWeight: '700' }}>128</Text>
          </View>
          <View style={{ flex: 1, backgroundColor: theme.card, borderRadius: 14, padding: 14, borderWidth: 1, borderColor: theme.border }}>
            <Clock3 size={16} color={theme.citizenPrimary} style={{ marginBottom: 8 }} />
            <Text style={{ color: theme.subtext, fontSize: 10, marginBottom: 4, letterSpacing: 0.8 }}>AVG. SLA</Text>
            <Text style={{ color: theme.text, fontSize: 20, fontWeight: '700' }}>48h</Text>
          </View>
        </View>

        <Text style={{ fontSize: 16, fontWeight: '700', color: theme.text, marginBottom: 16 }}>
          Choose your portal
        </Text>

        <TouchableOpacity 
          onPress={() => router.push({ pathname: '/(auth)/login', params: { portal: 'citizen' } } as any)}
          style={{ 
            backgroundColor: theme.card, 
            borderRadius: 18,
            padding: 20,
            borderWidth: 1,
            borderColor: theme.border,
            marginBottom: 16,
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}
        >
          <View style={{ flexDirection: 'row', alignItems: 'center', flex: 1 }}>
            {/* Keeping the icon background slightly transparent based on the exact hex to maintain the design */}
            <View style={{ backgroundColor: isDarkMode ? 'rgba(232, 163, 61, 0.12)' : 'rgba(212, 138, 34, 0.12)', padding: 12, borderRadius: 12, marginRight: 16 }}>
              <User size={24} color={theme.citizenPrimary} />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={{ color: theme.text, fontSize: 18, fontWeight: '700', marginBottom: 4 }}>Citizen Portal</Text>
              <Text style={{ color: theme.subtext, fontSize: 13, lineHeight: 18 }}>Report civic issues, track progress, and get status updates in real time.</Text>
            </View>
          </View>
          <ArrowRight size={20} color={theme.citizenPrimary} />
        </TouchableOpacity>

        <TouchableOpacity 
          onPress={() => router.push({ pathname: '/(auth)/login', params: { portal: 'authority' } } as any)}
          style={{ 
            backgroundColor: theme.card, 
            borderRadius: 18,
            padding: 20,
            borderWidth: 1,
            borderColor: theme.border,
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}
        >
          <View style={{ flexDirection: 'row', alignItems: 'center', flex: 1 }}>
            <View style={{ backgroundColor: isDarkMode ? 'rgba(47, 158, 143, 0.12)' : 'rgba(35, 122, 110, 0.12)', padding: 12, borderRadius: 12, marginRight: 16 }}>
              <Building2 size={24} color={theme.authorityPrimary} />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={{ color: theme.text, fontSize: 18, fontWeight: '700', marginBottom: 4 }}>Authority Portal</Text>
              <Text style={{ color: theme.subtext, fontSize: 13, lineHeight: 18 }}>Review municipal queues, assign teams, and resolve infrastructure complaints.</Text>
            </View>
          </View>
          <ArrowRight size={20} color={theme.authorityPrimary} />
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}