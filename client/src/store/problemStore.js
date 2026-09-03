import { create } from 'zustand';
import api from '../api/axios';

export const useProblemStore = create((set, get) => ({
  problems: [],
  isLoading: false,

  fetchProblems: async () => {
    set({ isLoading: true });
    try {
      const response = await api.get('/problems/public');
      set({ problems: response.data, isLoading: false });
    } catch (error) {
      console.error("Failed to fetch problems", error);
      set({ isLoading: false });
    }
  },

  addProblem: async (data) => {
    set({ isLoading: true });
    try {
      let payload = data;

      if (data.images && data.images.length > 0) {
        payload = new FormData();
        payload.append('title', data.title);
        payload.append('description', data.description);
        payload.append('category', data.category);
        payload.append('urgency', data.urgency);
        payload.append('location', JSON.stringify(data.location));
        
        data.images.forEach((image) => {
          payload.append('images', image);
        });
      }

      const response = await api.post('/problems', payload);
      set({ problems: [response.data, ...get().problems], isLoading: false });
      return response.data;
    } catch (error) {
      console.error("Failed to submit problem", error);
      set({ isLoading: false });
      return null;
    }
  },
  
  deleteProblem: async (id) => {
    set({ isLoading: true });
    try {
      await api.delete(`/problems/${id}`);
      set({ 
        problems: get().problems.filter(p => p.id !== id), 
        isLoading: false 
      });
      return true;
    } catch (error) {
      console.error("Failed to delete problem", error);
      set({ isLoading: false });
      return false;
    }
  }
}));