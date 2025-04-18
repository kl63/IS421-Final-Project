import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // Increase timeout to 60 seconds for long-running operations
});

export const reviewCode = async (data) => {
  try {
    const response = await apiClient.post('/review', data);
    return response.data;
  } catch (error) {
    console.error('Error in reviewCode:', error.response?.data || error.message || error);
    throw error;
  }
};

export const exportReview = async (reviewData) => {
  try {
    const response = await apiClient.post('/export-review', reviewData);
    return response.data;
  } catch (error) {
    console.error('Error in exportReview:', error.response?.data || error.message || error);
    throw error;
  }
};

export default {
  reviewCode,
  exportReview,
};
