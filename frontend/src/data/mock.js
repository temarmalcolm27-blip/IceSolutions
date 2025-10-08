export const mockData = {
  // Company Information
  company: {
    name: "Ice Solutions",
    tagline: "Premium Party Ice Delivery",
    description: "Your trusted partner for all party ice needs. We deliver fresh, crystal-clear ice directly to your event, restaurant, or venue.",
    phone: "(555) 123-ICE1",
    email: "orders@icesolutions.com",
    address: "123 Ice Street, Cool City, CC 12345"
  },

  // Products
  products: [
    {
      id: 1,
      name: "10lb Party Ice Bags",
      description: "Perfect for parties, events, and small gatherings. Crystal-clear, restaurant-quality ice.",
      price: 8.99,
      weight: "10 lbs",
      image: "/api/placeholder/300/200",
      inStock: true,
      features: ["Crystal Clear", "Restaurant Quality", "Fast Melting", "Perfect Cube Size"]
    },
    {
      id: 2,
      name: "50lb Commercial Ice Bags",
      description: "Coming Soon! Perfect for larger events and commercial use.",
      price: 34.99,
      weight: "50 lbs",
      image: "/api/placeholder/300/200",
      inStock: false,
      comingSoon: true,
      features: ["Bulk Quantity", "Cost Effective", "Commercial Grade", "Extended Freshness"]
    },
    {
      id: 3,
      name: "100lb Industrial Ice Bags",
      description: "Coming Soon! Ideal for restaurants, bars, and large-scale events.",
      price: 64.99,
      weight: "100 lbs", 
      image: "/api/placeholder/300/200",
      inStock: false,
      comingSoon: true,
      features: ["Maximum Volume", "Professional Grade", "Bulk Pricing", "Commercial Delivery"]
    }
  ],

  // Services
  services: [
    {
      id: 1,
      title: "Same-Day Delivery",
      description: "Order before 2 PM for same-day delivery to your location.",
      icon: "Truck"
    },
    {
      id: 2,
      title: "Event Planning",
      description: "Let us help calculate the perfect amount of ice for your event size.",
      icon: "Calendar"
    },
    {
      id: 3,
      title: "Bulk Orders",
      description: "Special pricing available for large orders and recurring deliveries.",
      icon: "Package"
    },
    {
      id: 4,
      title: "Quality Guarantee",
      description: "100% satisfaction guaranteed with fresh, crystal-clear ice every time.",
      icon: "Shield"
    }
  ],

  // Delivery Areas
  deliveryAreas: [
    {
      id: 1,
      area: "Downtown Core",
      deliveryFee: "Free",
      timeSlots: ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"]
    },
    {
      id: 2,
      area: "West Side",
      deliveryFee: "$5.99",
      timeSlots: ["10 AM - 1 PM", "1 PM - 4 PM", "4 PM - 7 PM"]
    },
    {
      id: 3,
      area: "East Side",
      deliveryFee: "$5.99", 
      timeSlots: ["10 AM - 1 PM", "1 PM - 4 PM", "4 PM - 7 PM"]
    },
    {
      id: 4,
      area: "North Suburbs",
      deliveryFee: "$8.99",
      timeSlots: ["11 AM - 2 PM", "2 PM - 5 PM"]
    }
  ],

  // Testimonials
  testimonials: [
    {
      id: 1,
      name: "Sarah Martinez",
      title: "Event Planner",
      company: "Elite Events Co.",
      review: "Ice Solutions has been our go-to ice supplier for 3+ years. Always reliable, crystal-clear ice, and their delivery team is professional.",
      rating: 5
    },
    {
      id: 2,
      name: "Mike Thompson",
      title: "Restaurant Manager",
      company: "Blue Moon Bistro",
      review: "Consistent quality and on-time delivery. The bulk pricing helps our restaurant maintain profit margins while serving quality drinks.",
      rating: 5
    },
    {
      id: 3,
      name: "Jennifer Lee",
      title: "Private Customer",
      company: null,
      review: "Used them for my daughter's graduation party. Easy ordering process and the ice quality was perfect. Definitely using them again!",
      rating: 5
    }
  ],

  // Mock orders for testing
  orders: [],

  // Mock quotes
  quotes: []
};