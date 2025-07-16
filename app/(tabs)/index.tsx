import React from 'react';
import { View, Text, StyleSheet, ScrollView, SafeAreaView, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { MapPin, Star, Clock, RefreshCw } from 'lucide-react-native';
import { usePractitioners } from '../../hooks/usePractitioners';

export default function HomeScreen() {
  const router = useRouter();
  const { practitioners, loading, error, refetch } = usePractitioners({ limit: 10 });

  const handleRefresh = () => {
    refetch();
  };

  const showError = () => {
    Alert.alert(
      'Connection Error',
      error || 'Unable to load practitioners. Please check your connection and try again.',
      [
        { text: 'Retry', onPress: handleRefresh },
        { text: 'Cancel', style: 'cancel' }
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <View style={styles.headerContent}>
            <View style={styles.headerText}>
              <Text style={styles.welcomeText}>Welcome to</Text>
              <Text style={styles.appName}>Tangerine</Text>
              <Text style={styles.subtitle}>Find the perfect Ayurvedic practitioner for your wellness journey</Text>
            </View>
            {error && (
              <TouchableOpacity style={styles.refreshButton} onPress={handleRefresh}>
                <RefreshCw size={20} color="#FF8C42" />
              </TouchableOpacity>
            )}
          </View>
        </View>

        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Featured Practitioners</Text>
            {!loading && !error && (
              <TouchableOpacity style={styles.refreshIconButton} onPress={handleRefresh}>
                <RefreshCw size={18} color="#6B7280" />
              </TouchableOpacity>
            )}
          </View>
          
          {loading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#FF8C42" />
              <Text style={styles.loadingText}>Loading practitioners...</Text>
            </View>
          ) : error ? (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>Unable to load practitioners</Text>
              <TouchableOpacity style={styles.retryButton} onPress={showError}>
                <Text style={styles.retryButtonText}>Tap to retry</Text>
              </TouchableOpacity>
            </View>
          ) : practitioners.length === 0 ? (
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>No practitioners available</Text>
              <TouchableOpacity style={styles.retryButton} onPress={handleRefresh}>
                <Text style={styles.retryButtonText}>Refresh</Text>
              </TouchableOpacity>
            </View>
          ) : (
            practitioners.map((practitioner) => (
              <TouchableOpacity 
                key={practitioner.id} 
                style={styles.practitionerCard}
                onPress={() => router.push(`/book/${practitioner.id}`)}
              >
                <View style={styles.cardContent}>
                  <View style={styles.practitionerInfo}>
                    <Text style={styles.practitionerName}>{practitioner.name}</Text>
                    <Text style={styles.specialty}>{practitioner.specialty}</Text>
                    
                    <View style={styles.detailsRow}>
                      <View style={styles.ratingContainer}>
                        <Star size={16} color="#FFD700" fill="#FFD700" />
                        <Text style={styles.rating}>{practitioner.rating}</Text>
                      </View>
                      <Text style={styles.experience}>{practitioner.experience}</Text>
                    </View>
                    
                    <View style={styles.locationRow}>
                      <MapPin size={14} color="#6B7280" />
                      <Text style={styles.location}>{practitioner.location}</Text>
                    </View>
                    
                    <View style={styles.availabilityRow}>
                      <Clock size={14} color="#87A96B" />
                      <Text style={styles.nextAvailable}>{practitioner.nextAvailable}</Text>
                    </View>
                  </View>
                </View>
              </TouchableOpacity>
            ))
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8F9FA',
  },
  scrollView: {
    flex: 1,
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 30,
    backgroundColor: '#FFFFFF',
    borderBottomLeftRadius: 24,
    borderBottomRightRadius: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  headerText: {
    flex: 1,
  },
  refreshButton: {
    padding: 8,
    marginTop: 4,
  },
  welcomeText: {
    fontSize: 16,
    color: '#6B7280',
    marginBottom: 4,
  },
  appName: {
    fontSize: 32,
    fontWeight: '700',
    color: '#FF8C42',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: '#6B7280',
    lineHeight: 20,
  },
  section: {
    paddingHorizontal: 20,
    paddingTop: 24,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: '600',
    color: '#1F2937',
    marginBottom: 16,
  },
  practitionerCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  cardContent: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  practitionerInfo: {
    flex: 1,
  },
  practitionerName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1F2937',
    marginBottom: 4,
  },
  specialty: {
    fontSize: 14,
    color: '#87A96B',
    fontWeight: '500',
    marginBottom: 8,
  },
  detailsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 6,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 16,
  },
  rating: {
    fontSize: 14,
    color: '#1F2937',
    fontWeight: '500',
    marginLeft: 4,
  },
  experience: {
    fontSize: 14,
    color: '#6B7280',
  },
  locationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 6,
  },
  location: {
    fontSize: 14,
    color: '#6B7280',
    marginLeft: 4,
  },
  availabilityRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  nextAvailable: {
    fontSize: 14,
    color: '#87A96B',
    fontWeight: '500',
    marginLeft: 4,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  refreshIconButton: {
    padding: 4,
  },
  loadingContainer: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  loadingText: {
    fontSize: 16,
    color: '#6B7280',
    marginTop: 12,
  },
  errorContainer: {
    alignItems: 'center',
    paddingVertical: 40,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    marginBottom: 16,
  },
  errorText: {
    fontSize: 16,
    color: '#EF4444',
    marginBottom: 12,
    textAlign: 'center',
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 40,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    marginBottom: 16,
  },
  emptyText: {
    fontSize: 16,
    color: '#6B7280',
    marginBottom: 12,
    textAlign: 'center',
  },
  retryButton: {
    backgroundColor: '#FF8C42',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  retryButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
});