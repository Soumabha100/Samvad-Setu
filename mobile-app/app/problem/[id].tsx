import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, Image, Share, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { 
  ArrowLeft, 
  MapPin, 
  Share2, 
  CheckCircle2, 
  Sparkles, 
  GraduationCap, 
  Briefcase, 
  Layers, 
  Calendar,
  AlertCircle
} from 'lucide-react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useTheme } from '../../context/ThemeContext'; // Import theme hook

const LIFECYCLE_STAGES = [
  { key: 'Submitted', label: '1. Grassroots Crowdsourced', desc: 'Reported with geo-tag and multimedia evidence by citizen.' },
  { key: 'AI Validated', label: '2. AI Categorized & Routed', desc: 'Thematic domain matched and mapped to target university departments.' },
  { key: 'Claimed by University', label: '3. HEI Project Team Formed', desc: 'Faculty mentor and student multidisciplinary research team actively working on prototype.' },
  { key: 'Industry Pledged', label: '4. CSR & Industry Mentorship', desc: 'Corporate grant, lab testing, or domain mentorship linked.' },
  { key: 'Deployed Solution', label: '5. Field Deployment & Social Impact', desc: 'Solution successfully piloted and operational in the community.' }
];

export default function ProblemTimelineScreen() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const { theme, isDarkMode } = useTheme(); // Pull dynamic theme

  const [problem, setProblem] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProblemDetails();
  }, [id]);

  const loadProblemDetails = async () => {
    try {
      const stored = await AsyncStorage.getItem('@citizen_tickets');
      if (stored) {
        const list = JSON.parse(stored);
        const match = list.find((item: any) => item.id === id);
        if (match) {
          setProblem(match);
        } else {
          setProblem({
            id: id || 'CHAL-2026-8432',
            title: 'Solar-Powered Cold Storage for Tribal Farmers',
            domain: 'Agriculture & Rural Livelihoods',
            description: 'Low-cost decentralized preservation units needed for minor forest produce in Khunti district.',
            stage: 'Claimed by University',
            status: 'Team Formed',
            assignedDept: 'AgriTech & Bioengineering',
            suggestedHEI: 'Birsa Agricultural University',
            industryPledge: 'Tata Steel CSR (Mentorship + ₹75,000 Grant)',
            location: 'Khunti, Jharkhand',
            date: 'Just now'
          });
        }
      }
    } catch (e) {
      console.error('Failed to load challenge details', e);
    } finally {
      setLoading(false);
    }
  };

  const handleShare = async () => {
    if (!problem) return;
    try {
      await Share.share({
        message: `SICP Challenge [${problem.id}]: ${problem.title || problem.description}\nDomain: ${problem.domain}\nTracking collaborative innovation progress on Jharkhand SICP Portal.`
      });
    } catch (error) {
      console.error('Error sharing challenge', error);
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={{ flex: 1, backgroundColor: theme.background, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color={theme.citizenPrimary} />
        <Text style={{ color: theme.subtext, marginTop: 12, fontSize: 13 }}>Loading innovation lifecycle...</Text>
      </SafeAreaView>
    );
  }

  if (!problem) {
    return (
      <SafeAreaView style={{ flex: 1, backgroundColor: theme.background, justifyContent: 'center', alignItems: 'center', padding: 20 }}>
        <AlertCircle size={36} color={theme.error} style={{ marginBottom: 12 }} />
        <Text style={{ color: theme.text, fontSize: 16, fontWeight: '700' }}>Challenge not found</Text>
        <TouchableOpacity onPress={() => router.back()} style={{ marginTop: 16, backgroundColor: theme.card, paddingHorizontal: 16, paddingVertical: 10, borderRadius: 10 }}>
          <Text style={{ color: theme.citizenPrimary, fontWeight: '700' }}>Go Back</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  const stageIndexMap: Record<string, number> = {
    'Submitted': 0, 'AI Validated': 1, 'Claimed by University': 2, 'Industry Pledged': 3, 'Deployed Solution': 4
  };
  const currentStageIndex = stageIndexMap[problem.stage] ?? 1;

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: theme.background, padding: 16 }}>
      <ScrollView contentContainerStyle={{ paddingBottom: 40 }} showsVerticalScrollIndicator={false}>
        
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
          <TouchableOpacity 
            onPress={() => router.back()}
            style={{ backgroundColor: theme.card, padding: 10, borderRadius: 12, borderWidth: 1, borderColor: theme.border }}
          >
            <ArrowLeft size={20} color={theme.text} />
          </TouchableOpacity>
          <View style={{ alignItems: 'center' }}>
            <Text style={{ color: theme.subtext, fontSize: 10, letterSpacing: 1, fontWeight: '700' }}>SICP LIFECYCLE</Text>
            <Text style={{ color: theme.citizenPrimary, fontWeight: '800', fontSize: 14 }}>{problem.id}</Text>
          </View>
          <TouchableOpacity 
            onPress={handleShare}
            style={{ backgroundColor: theme.card, padding: 10, borderRadius: 12, borderWidth: 1, borderColor: theme.border }}
          >
            <Share2 size={20} color={theme.authorityPrimary} />
          </TouchableOpacity>
        </View>

        <View style={{ backgroundColor: theme.card, borderRadius: 18, padding: 18, borderWidth: 1, borderColor: theme.border, marginBottom: 16 }}>
          <View style={{ backgroundColor: isDarkMode ? 'rgba(232, 163, 61, 0.12)' : 'rgba(212, 138, 34, 0.12)', alignSelf: 'flex-start', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8, borderWidth: 1, borderColor: theme.citizenPrimary, marginBottom: 10 }}>
            <Text style={{ color: theme.citizenPrimary, fontSize: 11, fontWeight: '800', textTransform: 'uppercase' }}>
              {problem.domain || 'Thematic Innovation Challenge'}
            </Text>
          </View>
          
          <Text style={{ color: theme.text, fontSize: 20, fontWeight: '800', marginBottom: 10, lineHeight: 26 }}>
            {problem.title || problem.description}
          </Text>

          <View style={{ flexDirection: 'row', alignItems: 'center', gap: 14 }}>
            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <MapPin size={13} color={theme.subtext} style={{ marginRight: 4 }} />
              <Text style={{ color: theme.subtext, fontSize: 12 }}>{problem.location || 'Jharkhand Region'}</Text>
            </View>
            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <Calendar size={13} color={theme.subtext} style={{ marginRight: 4 }} />
              <Text style={{ color: theme.subtext, fontSize: 12 }}>{problem.date || 'Active'}</Text>
            </View>
          </View>
        </View>

        {problem.imageUri && (
          <Image 
            source={{ uri: problem.imageUri }} 
            style={{ width: '100%', height: 200, borderRadius: 16, marginBottom: 16, borderWidth: 1, borderColor: theme.border }} 
          />
        )}

        <View style={{ backgroundColor: theme.card, borderRadius: 16, padding: 16, borderWidth: 1, borderColor: theme.border, marginBottom: 16 }}>
          <Text style={{ color: theme.text, fontSize: 14, fontWeight: '700', marginBottom: 6 }}>Grassroots Challenge Statement</Text>
          <Text style={{ color: theme.subtext, fontSize: 13, lineHeight: 20 }}>
            {problem.description}
          </Text>
        </View>

        <View style={{ backgroundColor: theme.card, borderRadius: 16, padding: 16, borderWidth: 1, borderColor: theme.border, marginBottom: 20 }}>
          <Text style={{ color: theme.text, fontSize: 14, fontWeight: '700', marginBottom: 12 }}>Assigned Innovation Ecosystem</Text>
          
          <View style={{ gap: 12 }}>
            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <View style={{ backgroundColor: theme.background, padding: 8, borderRadius: 10, marginRight: 10, borderWidth: 1, borderColor: theme.border }}>
                <GraduationCap size={16} color={theme.authorityPrimary} />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={{ color: theme.text, fontSize: 12, fontWeight: '700' }}>Leading Academic HEI</Text>
                <Text style={{ color: theme.subtext, fontSize: 11 }}>{problem.suggestedHEI || 'Birsa Agricultural University'}</Text>
              </View>
            </View>

            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <View style={{ backgroundColor: theme.background, padding: 8, borderRadius: 10, marginRight: 10, borderWidth: 1, borderColor: theme.border }}>
                <Sparkles size={16} color={theme.citizenPrimary} />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={{ color: theme.text, fontSize: 12, fontWeight: '700' }}>Academic Specialization</Text>
                <Text style={{ color: theme.subtext, fontSize: 11 }}>{problem.assignedDept || 'AgriTech & Bioengineering'}</Text>
              </View>
            </View>

            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              <View style={{ backgroundColor: theme.background, padding: 8, borderRadius: 10, marginRight: 10, borderWidth: 1, borderColor: theme.border }}>
                <Briefcase size={16} color="#A855F7" />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={{ color: theme.text, fontSize: 12, fontWeight: '700' }}>Industry / CSR Partnership</Text>
                <Text style={{ color: theme.subtext, fontSize: 11 }}>{problem.industryPledge || 'Open for CSR funding & mentorship'}</Text>
              </View>
            </View>
          </View>
        </View>

        <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 12 }}>
          <Layers size={16} color={theme.citizenPrimary} style={{ marginRight: 6 }} />
          <Text style={{ color: theme.text, fontSize: 16, fontWeight: '700' }}>
            NEP-2020 Innovation Lifecycle
          </Text>
        </View>

        <View style={{ backgroundColor: theme.card, borderRadius: 18, padding: 18, borderWidth: 1, borderColor: theme.border }}>
          {LIFECYCLE_STAGES.map((stg, idx) => {
            const isCompleted = idx <= currentStageIndex;
            const isCurrent = idx === currentStageIndex;

            return (
              <View key={stg.key} style={{ flexDirection: 'row', marginBottom: idx < LIFECYCLE_STAGES.length - 1 ? 20 : 0 }}>
                <View style={{ alignItems: 'center', marginRight: 14, width: 24 }}>
                  <View style={{
                    width: 24, height: 24, borderRadius: 12,
                    backgroundColor: isCompleted ? theme.authorityPrimary : theme.background,
                    borderWidth: 2,
                    borderColor: isCompleted ? theme.authorityPrimary : theme.border,
                    alignItems: 'center', justifyContent: 'center'
                  }}>
                    {isCompleted ? (
                      <CheckCircle2 size={14} color={isDarkMode ? '#0F1B1E' : '#FFFFFF'} />
                    ) : (
                      <View style={{ width: 6, height: 6, borderRadius: 3, backgroundColor: theme.subtext }} />
                    )}
                  </View>
                  {idx < LIFECYCLE_STAGES.length - 1 && (
                    <View style={{
                      width: 2, flex: 1,
                      backgroundColor: idx < currentStageIndex ? theme.authorityPrimary : theme.border,
                      marginTop: 4
                    }} />
                  )}
                </View>

                <View style={{ flex: 1 }}>
                  <Text style={{ 
                    color: isCompleted ? theme.text : theme.subtext, 
                    fontSize: 14, 
                    fontWeight: isCurrent ? '800' : '600',
                    marginBottom: 2
                  }}>
                    {stg.label}
                  </Text>
                  <Text style={{ color: theme.subtext, fontSize: 11, lineHeight: 16 }}>
                    {stg.desc}
                  </Text>
                </View>
              </View>
            );
          })}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}