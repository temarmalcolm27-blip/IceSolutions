import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        'An unexpected error occurred';
    
    // Don't show toast for specific errors that should be handled by components
    if (!error.config?.skipErrorToast) {
      toast.error(`Error: ${errorMessage}`);
    }
    
    return Promise.reject(error);
  }
);

// API Service Functions
export const apiService = {
  // Products API
  async getProducts() {
    try {
      const response = await api.get('/products');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch products:', error);
      throw error;
    }
  },

  async getProduct(productId) {
    try {
      const response = await api.get(`/products/${productId}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch product ${productId}:`, error);
      throw error;
    }
  },

  // Quotes API
  async createQuote(quoteData) {
    try {
      const response = await api.post('/quotes', quoteData);
      toast.success('Quote request submitted successfully!');
      return response.data;
    } catch (error) {
      console.error('Failed to create quote:', error);
      throw error;
    }
  },

  async getQuote(quoteId) {
    try {
      const response = await api.get(`/quotes/${quoteId}`, {
        skipErrorToast: true // Handle errors in component
      });
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch quote ${quoteId}:`, error);
      throw error;
    }
  },

  // Contacts API
  async createContact(contactData) {
    try {
      const response = await api.post('/contacts', contactData);
      toast.success('Message sent successfully! We\'ll respond within 2 hours.');
      return response.data;
    } catch (error) {
      console.error('Failed to send contact message:', error);
      throw error;
    }
  },

  async getContacts() {
    try {
      const response = await api.get('/contacts');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch contacts:', error);
      throw error;
    }
  },

  // Delivery Areas API
  async getDeliveryAreas() {
    try {
      const response = await api.get('/delivery-areas');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch delivery areas:', error);
      throw error;
    }
  },

  // Helper function to calculate quote with real-time delivery fee calculation
  async calculateInstantQuote(guestCount, iceAmount, address = '') {
    const recommendedBags = Math.max(1, 
      guestCount ? Math.ceil(guestCount / 25) : Math.ceil(iceAmount / 10)
    );
    
    const basePrice = recommendedBags * 350.00;
    
    // Start with no delivery fee
    let deliveryFee = null;
    let deliveryArea = '';
    
    // Check if address is provided
    if (address && address.trim().length > 0) {
      const addressLower = address.toLowerCase();
      
      // Check for Washington Gardens
      if (addressLower.includes('washington gardens') || 
          addressLower.includes('washington garden')) {
        deliveryFee = 0;
        deliveryArea = 'Washington Gardens - FREE Delivery';
      } 
      // For other addresses, call the API
      else if (address.trim().length >= 15) {
        try {
          const response = await api.post('/calculate-delivery-fee', {
            destination_address: address.trim(),
            bags: recommendedBags
          });
          
          if (response.data) {
            deliveryFee = response.data.delivery_fee;
            
            if (response.data.is_washington_gardens) {
              deliveryArea = 'Washington Gardens - FREE Delivery';
            } else {
              deliveryArea = `Distance: ${response.data.distance_text}`;
            }
          }
        } catch (error) {
          console.error('Delivery fee calculation error:', error);
          deliveryFee = null;
          deliveryArea = 'Enter valid address';
        }
      } else {
        deliveryArea = 'Enter full address';
      }
    }
    
    // Calculate discount
    let savings = 0;
    let discountPercent = 0;
    if (recommendedBags >= 20) {
      discountPercent = 15;
      savings = basePrice * 0.15;
    } else if (recommendedBags >= 10) {
      discountPercent = 10;
      savings = basePrice * 0.10;
    } else if (recommendedBags >= 5) {
      discountPercent = 5;
      savings = basePrice * 0.05;
    }
    
    const total = basePrice + (deliveryFee !== null ? deliveryFee : 0) - savings;
    
    return {
      bags: recommendedBags,
      basePrice,
      deliveryFee,
      total,
      savings,
      discountPercent,
      deliveryArea
    };
  },

  // Payment/Checkout APIs
  async createCheckoutSession(checkoutData, originUrl) {
    try {
      const response = await api.post('/checkout/create-session', checkoutData, {
        params: { origin_url: originUrl }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to create checkout session:', error);
      throw error;
    }
  },

  async getCheckoutStatus(sessionId) {
    try {
      const response = await api.get(`/checkout/status/${sessionId}`, {
        skipErrorToast: true
      });
      return response.data;
    } catch (error) {
      console.error(`Failed to get checkout status:`, error);
      throw error;
    }
  },

  async createOrder(orderData) {
    try {
      const response = await api.post('/orders', orderData);
      return response.data;
    } catch (error) {
      console.error('Failed to create order:', error);
      throw error;
    }
  },

  async getOrder(orderId) {
    try {
      const response = await api.get(`/orders/${orderId}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch order ${orderId}:`, error);
      throw error;
    }
  },

  // Product Notification APIs
  async subscribeToNotification(notificationData) {
    try {
      const response = await api.post('/notifications/subscribe', notificationData);
      toast.success(response.data.message || 'Successfully subscribed to notifications!');
      return response.data;
    } catch (error) {
      console.error('Failed to subscribe to notification:', error);
      throw error;
    }
  }
};

export default apiService;