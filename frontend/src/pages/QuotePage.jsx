import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Calendar } from '../components/ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from '../components/ui/popover';
import { 
  Package, 
  Calendar as CalendarIcon,
  Clock, 
  MapPin,
  Calculator,
  CheckCircle,
  Truck,
  DollarSign,
  Phone,
  Mail
} from 'lucide-react';
import { format } from 'date-fns';
import { mockData } from '../data/mock';
import { apiService } from '../services/api';
import { toast } from 'sonner';

const QuotePage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    eventDate: null,
    eventType: '',
    guestCount: '',
    iceAmount: '',
    specialRequests: '',
    deliveryTime: ''
  });
  const [calculatedQuote, setCalculatedQuote] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [deliveryAreas, setDeliveryAreas] = useState([]);
  const [deliveryAreasLoading, setDeliveryAreasLoading] = useState(true);

  const eventTypes = [
    'Private Party',
    'Wedding',
    'Corporate Event',
    'Restaurant/Bar',
    'Catering Service',
    'Emergency Supply',
    'Other'
  ];

  const timeSlots = [
    '8:00 AM - 10:00 AM',
    '10:00 AM - 12:00 PM',
    '12:00 PM - 2:00 PM',
    '2:00 PM - 4:00 PM',
    '4:00 PM - 6:00 PM',
    '6:00 PM - 8:00 PM'
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  useEffect(() => {
    const fetchDeliveryAreas = async () => {
      try {
        const areas = await apiService.getDeliveryAreas();
        setDeliveryAreas(areas);
      } catch (error) {
        console.error('Failed to load delivery areas:', error);
        // Fallback to mock data
        setDeliveryAreas(mockData.deliveryAreas);
      } finally {
        setDeliveryAreasLoading(false);
      }
    };

    fetchDeliveryAreas();
  }, []);

  // Real-time quote calculation whenever form data changes
  useEffect(() => {
    const guestCount = parseInt(formData.guestCount) || 0;
    const iceAmount = parseInt(formData.iceAmount) || 0;
    const address = formData.address || '';
    
    // Only calculate if we have meaningful data
    if (guestCount > 0 || iceAmount > 0) {
      const quote = apiService.calculateInstantQuote(guestCount, iceAmount, address);
      setCalculatedQuote(quote);
    } else {
      setCalculatedQuote(null);
    }
  }, [formData.guestCount, formData.iceAmount, formData.address]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Prepare quote data for API
      const quoteData = {
        customerInfo: {
          name: formData.name,
          email: formData.email,
          phone: formData.phone,
          address: formData.address
        },
        eventDetails: {
          eventDate: formData.eventDate ? formData.eventDate.toISOString() : new Date().toISOString(),
          eventType: formData.eventType || 'Other',
          guestCount: parseInt(formData.guestCount) || 0,
          iceAmount: parseInt(formData.iceAmount) || 0,
          deliveryTime: formData.deliveryTime || ''
        },
        specialRequests: formData.specialRequests
      };
      
      // Submit to API
      const newQuote = await apiService.createQuote(quoteData);
      
      toast.success(`Quote request submitted! Quote ID: ${newQuote.id}. We'll call you at (${formData.phone}) immediately!`);
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        address: '',
        eventDate: null,
        eventType: '',
        guestCount: '',
        iceAmount: '',
        specialRequests: '',
        deliveryTime: ''
      });
      setCalculatedQuote(null);
      
    } catch (error) {
      console.error('Failed to submit quote:', error);
      // Error handling is done in the API service
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlaceOrder = async () => {
    if (!calculatedQuote) {
      toast.error('Please calculate a quote first');
      return;
    }

    setIsLoading(true);
    try {
      // First create the quote
      const quoteData = {
        customerInfo: {
          name: formData.name,
          email: formData.email,
          phone: formData.phone,
          address: formData.address
        },
        eventDetails: {
          eventDate: formData.eventDate ? formData.eventDate.toISOString() : new Date().toISOString(),
          eventType: formData.eventType || 'Other',
          guestCount: parseInt(formData.guestCount) || 0,
          iceAmount: parseInt(formData.iceAmount) || 0,
          deliveryTime: formData.deliveryTime || ''
        },
        specialRequests: formData.specialRequests
      };
      
      const newQuote = await apiService.createQuote(quoteData);
      
      // Show success message with order details
      toast.success(`🎉 Order placed successfully! 
      Order Total: JMD $${(calculatedQuote.total - (calculatedQuote.savings || 0)).toFixed(0)}
      Order ID: ${newQuote.id}
      
      Our team will call you at (${formData.phone}) within 2-3 minutes to confirm delivery details and arrange payment.`, {
        duration: 8000,
      });

      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        address: '',
        eventDate: null,
        eventType: '',
        guestCount: '',
        iceAmount: '',
        specialRequests: '',
        deliveryTime: ''
      });
      setCalculatedQuote(null);

    } catch (error) {
      console.error('Failed to place order:', error);
      toast.error('Failed to place order. Please try again or call us directly.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Get Your Ice Quote
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Tell us about your event and get an instant quote for premium ice delivery
            </p>
            <Badge className="bg-green-100 text-green-700 px-4 py-2">
              <CheckCircle className="mr-1 h-4 w-4" />
              Instant Quote & Fast Response
            </Badge>
          </div>
        </div>
      </section>

      <section className="py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            
            {/* Quote Form */}
            <div className="space-y-8">
              <Card className="border-0 shadow-xl">
                <CardHeader>
                  <CardTitle className="text-2xl text-gray-900 flex items-center">
                    <Calculator className="mr-2 h-6 w-6 text-cyan-600" />
                    Quote Request Form
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    
                    {/* Contact Information */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold text-gray-900">Contact Information</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="name">Full Name *</Label>
                          <Input
                            id="name"
                            value={formData.name}
                            onChange={(e) => handleInputChange('name', e.target.value)}
                            placeholder="Your full name"
                            required
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="phone">Phone Number *</Label>
                          <Input
                            id="phone"
                            type="tel"
                            value={formData.phone}
                            onChange={(e) => handleInputChange('phone', e.target.value)}
                            placeholder="(555) 123-4567"
                            required
                          />
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="email">Email Address *</Label>
                        <Input
                          id="email"
                          type="email"
                          value={formData.email}
                          onChange={(e) => handleInputChange('email', e.target.value)}
                          placeholder="your@email.com"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="address">Delivery Address *</Label>
                        <Input
                          id="address"
                          value={formData.address}
                          onChange={(e) => handleInputChange('address', e.target.value)}
                          placeholder="Full delivery address"
                          required
                        />
                      </div>
                    </div>

                    {/* Event Details */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold text-gray-900">Event Details</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label>Event Date *</Label>
                          <Popover>
                            <PopoverTrigger asChild>
                              <Button
                                variant="outline"
                                className="w-full justify-start text-left font-normal"
                              >
                                <CalendarIcon className="mr-2 h-4 w-4" />
                                {formData.eventDate ? format(formData.eventDate, "PPP") : "Select date"}
                              </Button>
                            </PopoverTrigger>
                            <PopoverContent className="w-auto p-0" align="start">
                              <Calendar
                                mode="single"
                                selected={formData.eventDate}
                                onSelect={(date) => handleInputChange('eventDate', date)}
                                initialFocus
                                disabled={(date) => date < new Date()}
                              />
                            </PopoverContent>
                          </Popover>
                        </div>
                        <div className="space-y-2">
                          <Label>Preferred Delivery Time</Label>
                          <Select onValueChange={(value) => handleInputChange('deliveryTime', value)}>
                            <SelectTrigger>
                              <SelectValue placeholder="Select time slot" />
                            </SelectTrigger>
                            <SelectContent>
                              {timeSlots.map((slot) => (
                                <SelectItem key={slot} value={slot}>
                                  {slot}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <Label>Event Type</Label>
                        <Select onValueChange={(value) => handleInputChange('eventType', value)}>
                          <SelectTrigger>
                            <SelectValue placeholder="Select event type" />
                          </SelectTrigger>
                          <SelectContent>
                            {eventTypes.map((type) => (
                              <SelectItem key={type} value={type}>
                                {type}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="guests">Number of Guests</Label>
                          <Input
                            id="guests"
                            type="number"
                            value={formData.guestCount}
                            onChange={(e) => handleInputChange('guestCount', e.target.value)}
                            placeholder="e.g., 50"
                            min="1"
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="iceAmount">Ice Amount (lbs)</Label>
                          <Input
                            id="iceAmount"
                            type="number"
                            value={formData.iceAmount}
                            onChange={(e) => handleInputChange('iceAmount', e.target.value)}
                            placeholder="e.g., 30"
                            min="10"
                            step="10"
                          />
                        </div>
                      </div>
                    </div>

                    {/* Special Requests */}
                    <div className="space-y-2">
                      <Label htmlFor="requests">Special Requests</Label>
                      <Textarea
                        id="requests"
                        value={formData.specialRequests}
                        onChange={(e) => handleInputChange('specialRequests', e.target.value)}
                        placeholder="Any special delivery instructions, timing requirements, or other requests..."
                        rows={3}
                      />
                    </div>

                    <div className="flex space-x-4">
                      <Button
                        type="button"
                        variant="outline"
                        onClick={calculateQuote}
                        className="flex-1"
                        disabled={!formData.guestCount && !formData.iceAmount}
                      >
                        <Calculator className="mr-2 h-4 w-4" />
                        Calculate Quote
                      </Button>
                      <Button
                        type="submit"
                        className="flex-1 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white"
                        disabled={isLoading || !formData.name || !formData.phone || !formData.email}
                      >
                        {isLoading ? 'Submitting...' : 'Request Quote'}
                      </Button>
                    </div>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Quote Summary & Info */}
            <div className="space-y-8">
              
              {/* Instant Quote */}
              {calculatedQuote && (
                <Card className="border-0 shadow-xl bg-gradient-to-br from-cyan-50 to-blue-50">
                  <CardHeader>
                    <CardTitle className="text-2xl text-gray-900 flex items-center">
                      <DollarSign className="mr-2 h-6 w-6 text-cyan-600" />
                      Instant Quote
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-700">Ice Bags ({calculatedQuote.bags} x 10lbs)</span>
                        <span className="font-semibold">${calculatedQuote.basePrice.toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-700">Delivery Fee</span>
                        <span className="font-semibold">
                          {calculatedQuote.deliveryFee === 0 ? 'FREE' : `$${calculatedQuote.deliveryFee.toFixed(2)}`}
                        </span>
                      </div>
                      {calculatedQuote.savings > 0 && (
                        <div className="flex justify-between items-center text-green-600">
                          <span>Bulk Discount (5+ bags)</span>
                          <span className="font-semibold">-${calculatedQuote.savings.toFixed(2)}</span>
                        </div>
                      )}
                      <div className="border-t border-gray-300 pt-3">
                        <div className="flex justify-between items-center text-lg font-bold">
                          <span className="text-gray-900">Total Estimate</span>
                          <span className="text-cyan-600">${(calculatedQuote.total - (calculatedQuote.savings || 0)).toFixed(2)}</span>
                        </div>
                      </div>
                    </div>
                    <div className="bg-white p-4 rounded-lg border border-cyan-200">
                      <p className="text-sm text-gray-600 text-center">
                        This is an estimate. Final pricing may vary based on delivery location and special requirements.
                      </p>
                    </div>
                    
                    {/* Order Placement Buttons */}
                    <div className="space-y-3 pt-4 border-t border-gray-200">
                      <Button 
                        className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white shadow-lg"
                        onClick={() => handlePlaceOrder()}
                        disabled={!formData.name || !formData.phone || !formData.email}
                      >
                        <CheckCircle className="mr-2 h-5 w-5" />
                        Place Order Now (JMD ${(calculatedQuote.total - (calculatedQuote.savings || 0)).toFixed(0)})
                      </Button>
                      <p className="text-xs text-gray-500 text-center">
                        By placing this order, you agree to our terms. You'll receive a call within 2-3 minutes to confirm delivery details.
                      </p>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Delivery Areas */}
              <Card className="border-0 shadow-xl">
                <CardHeader>
                  <CardTitle className="text-xl text-gray-900 flex items-center">
                    <MapPin className="mr-2 h-5 w-5 text-cyan-600" />
                    Delivery Areas & Fees
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {deliveryAreasLoading ? (
                      // Loading skeleton for delivery areas
                      Array.from({ length: 4 }, (_, index) => (
                        <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg animate-pulse">
                          <div className="flex-1">
                            <div className="h-4 bg-gray-200 rounded mb-2"></div>
                            <div className="h-3 bg-gray-200 rounded w-3/4"></div>
                          </div>
                          <div className="h-6 w-16 bg-gray-200 rounded"></div>
                        </div>
                      ))
                    ) : (
                      deliveryAreas.map((area) => (
                        <div key={area.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                          <div>
                            <div className="font-medium text-gray-900">{area.area}</div>
                            <div className="text-sm text-gray-600">
                              Available: {area.timeSlots.join(', ')}
                            </div>
                          </div>
                          <Badge className={area.deliveryFee === 0 ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'}>
                            {area.deliveryFee === 0 ? 'Free' : `JMD $${area.deliveryFee.toFixed(0)}`}
                          </Badge>
                        </div>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Quick Info */}
              <Card className="border-0 shadow-xl">
                <CardHeader>
                  <CardTitle className="text-xl text-gray-900 flex items-center">
                    <Clock className="mr-2 h-5 w-5 text-cyan-600" />
                    What Happens Next?
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-start space-x-3">
                      <div className="w-6 h-6 bg-cyan-600 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
                      <div>
                        <div className="font-medium text-gray-900">Request Saved</div>
                        <div className="text-sm text-gray-600">Your quote/order is saved in our system with a unique ID</div>
                      </div>
                    </div>
                    <div className="flex items-start space-x-3">
                      <div className="w-6 h-6 bg-cyan-600 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
                      <div>
                        <div className="font-medium text-gray-900">Personal Call</div>
                        <div className="text-sm text-gray-600">Our AI agent will call you within 2-3 minutes to confirm details and arrange payment</div>
                      </div>
                    </div>
                    <div className="flex items-start space-x-3">
                      <div className="w-6 h-6 bg-cyan-600 text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
                      <div>
                        <div className="font-medium text-gray-900">Scheduled Delivery</div>
                        <div className="text-sm text-gray-600">Fresh ice delivered to your address at your preferred time</div>
                      </div>
                    </div>
                    
                    <div className="bg-amber-50 p-4 rounded-lg border border-amber-200 mt-4">
                      <p className="text-sm text-amber-800">
                        <strong>Note:</strong> Currently, quotes and orders are stored in our database. Our team reviews them manually and contacts customers by phone. Email notifications will be added in a future update.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Contact */}
              <Card className="border-0 shadow-xl bg-gradient-to-br from-slate-900 to-blue-900 text-white">
                <CardContent className="p-6 text-center space-y-4">
                  <h3 className="text-xl font-semibold">Need Help?</h3>
                  <p className="text-gray-300">
                    Have questions or need a custom quote? Our ice experts are here to help!
                  </p>
                  <div className="flex flex-col sm:flex-row gap-3 justify-center">
                    <Button 
                      className="bg-white text-gray-900 hover:bg-gray-100"
                      onClick={() => window.open('tel:(876)490-7208')}
                    >
                      <Phone className="mr-2 h-4 w-4" />
                      Call (876) 490-7208
                    </Button>
                    <Button 
                      variant="outline" 
                      className="border-white text-white hover:bg-white hover:text-gray-900"
                      onClick={() => window.open('mailto:orders@icesolutions.com')}
                    >
                      Email Us
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default QuotePage;