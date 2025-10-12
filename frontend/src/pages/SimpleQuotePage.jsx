import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Calculator, Users, Clock, Calendar, ArrowRight, TrendingDown } from 'lucide-react';

const SimpleQuotePage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const calculatedBagsFromPlanner = location.state?.calculatedBags;
  
  const [formData, setFormData] = useState({
    guests: calculatedBagsFromPlanner ? '' : '',
    duration: '',
    eventType: '',
    deliveryAddress: ''
  });
  
  const [result, setResult] = useState(null);

  useEffect(() => {
    // If coming from event planner, pre-fill with calculated bags
    if (calculatedBagsFromPlanner) {
      // Calculate equivalent guests for the bags
      const equivalentGuests = calculatedBagsFromPlanner * 10;
      setFormData(prev => ({
        ...prev,
        guests: equivalentGuests,
        duration: '4', // Default 4 hours
        eventType: 'party'
      }));
    }
  }, [calculatedBagsFromPlanner]);

  useEffect(() => {
    // Auto-calculate when form data changes
    const guests = parseInt(formData.guests) || 0;
    const duration = parseFloat(formData.duration) || 0;
    const eventType = formData.eventType;
    const address = formData.deliveryAddress || '';
    
    if (guests > 0 && duration > 0 && eventType) {
      calculateIce();
    } else {
      setResult(null);
    }
  }, [formData.guests, formData.duration, formData.eventType, formData.deliveryAddress]);

  const calculateIce = () => {
    const guests = parseInt(formData.guests) || 0;
    const duration = parseFloat(formData.duration) || 0;
    
    // Ice calculation formula:
    // Base: 1 lb per guest per hour
    const multipliers = {
      'party': 1.2,
      'wedding': 1.5,
      'restaurant': 1.8,
      'bar': 2.0,
      'corporate': 1.0
    };
    
    const multiplier = multipliers[formData.eventType] || 1.0;
    const totalIceLbs = guests * duration * multiplier;
    
    // Calculate bags needed (10 lb bags)
    const bagsNeeded = Math.ceil(totalIceLbs / 10);
    
    // Calculate price (JMD $350 per bag)
    const pricePerBag = 350.00;
    const subtotal = bagsNeeded * pricePerBag;
    
    // Apply bulk discounts
    let discountPercent = 0;
    if (bagsNeeded >= 20) {
      discountPercent = 15;
    } else if (bagsNeeded >= 10) {
      discountPercent = 10;
    } else if (bagsNeeded >= 5) {
      discountPercent = 5;
    }
    
    const discountAmount = subtotal * (discountPercent / 100);
    const totalAfterDiscount = subtotal - discountAmount;
    
    // Calculate delivery fee based on address
    const addressLower = formData.deliveryAddress.toLowerCase();
    const isWashingtonGardens = addressLower.includes('washington gardens') || 
                               addressLower.includes('washington garden');
    const deliveryFee = isWashingtonGardens ? 0 : 300.00;
    
    const finalTotal = totalAfterDiscount + deliveryFee;
    
    setResult({
      totalIceLbs: totalIceLbs.toFixed(1),
      bagsNeeded,
      pricePerBag,
      subtotal: subtotal.toFixed(2),
      discountPercent,
      discountAmount: discountAmount.toFixed(2),
      totalAfterDiscount: totalAfterDiscount.toFixed(2),
      deliveryFee: deliveryFee.toFixed(2),
      finalTotal: finalTotal.toFixed(2),
      deliveryArea: isWashingtonGardens ? 'Washington Gardens' : 'Outside Washington Gardens'
    });
  };

  const handleContinueToPayment = () => {
    if (!result) return;
    
    navigate('/checkout', {
      state: {
        bags: result.bagsNeeded,
        deliveryFee: parseFloat(result.deliveryFee),
        deliveryAddress: formData.deliveryAddress,
        totalAmount: parseFloat(result.finalTotal),
        discountPercent: result.discountPercent,
        discountAmount: parseFloat(result.discountAmount)
      }
    });
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-6 max-w-3xl mx-auto">
            <div className="inline-block p-3 bg-cyan-100 rounded-full">
              <Calculator className="h-8 w-8 text-cyan-600" />
            </div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Get Your Ice Quote
            </h1>
            <p className="text-xl text-gray-600">
              Tell us about your event and get an instant price quote
            </p>
          </div>
        </div>
      </section>

      {/* Quote Form */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Form */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Users className="h-5 w-5 text-cyan-600" />
                    Event Details
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div className="space-y-2">
                      <Label htmlFor="guests" className="flex items-center gap-2">
                        <Users className="h-4 w-4 text-gray-500" />
                        Number of Guests *
                      </Label>
                      <Input
                        id="guests"
                        type="number"
                        placeholder="e.g., 50"
                        min="1"
                        required
                        value={formData.guests}
                        onChange={(e) => setFormData({...formData, guests: e.target.value})}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="duration" className="flex items-center gap-2">
                        <Clock className="h-4 w-4 text-gray-500" />
                        Event Duration (hours) *
                      </Label>
                      <Input
                        id="duration"
                        type="number"
                        step="0.5"
                        placeholder="e.g., 4"
                        min="0.5"
                        required
                        value={formData.duration}
                        onChange={(e) => setFormData({...formData, duration: e.target.value})}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="eventType" className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-gray-500" />
                        Event Type *
                      </Label>
                      <Select 
                        value={formData.eventType} 
                        onValueChange={(value) => setFormData({...formData, eventType: value})}
                        required
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Select event type" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="party">Party/Celebration</SelectItem>
                          <SelectItem value="wedding">Wedding/Reception</SelectItem>
                          <SelectItem value="restaurant">Restaurant Service</SelectItem>
                          <SelectItem value="bar">Bar/Nightclub</SelectItem>
                          <SelectItem value="corporate">Corporate Event</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="deliveryAddress">
                        Delivery Address *
                      </Label>
                      <Input
                        id="deliveryAddress"
                        required
                        value={formData.deliveryAddress}
                        onChange={(e) => setFormData({...formData, deliveryAddress: e.target.value})}
                        placeholder="e.g., 123 Main St, Washington Gardens"
                      />
                      <p className="text-xs text-gray-500">
                        Free delivery in Washington Gardens
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Results */}
              {result ? (
                <Card className="bg-gradient-to-br from-cyan-50 to-blue-50">
                  <CardHeader>
                    <CardTitle className="text-cyan-700">Your Quote</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="space-y-4">
                      <div className="flex justify-between items-center p-4 bg-white rounded-lg">
                        <span className="text-gray-600">Total Ice Needed</span>
                        <span className="text-2xl font-bold text-gray-900">{result.totalIceLbs} lbs</span>
                      </div>
                      
                      <div className="flex justify-between items-center p-4 bg-white rounded-lg">
                        <span className="text-gray-600">10lb Bags Required</span>
                        <span className="text-2xl font-bold text-cyan-600">{result.bagsNeeded} bags</span>
                      </div>
                      
                      <div className="flex justify-between items-center p-4 bg-white rounded-lg">
                        <span className="text-gray-600">Subtotal</span>
                        <span className="text-lg text-gray-900">JMD ${result.subtotal}</span>
                      </div>

                      {result.discountPercent > 0 && (
                        <div className="flex justify-between items-center p-4 bg-green-100 rounded-lg border-2 border-green-300">
                          <div className="flex items-center gap-2">
                            <TrendingDown className="h-4 w-4 text-green-700" />
                            <span className="text-green-700 font-medium">Bulk Discount ({result.discountPercent}%)</span>
                          </div>
                          <span className="text-lg font-semibold text-green-700">-JMD ${result.discountAmount}</span>
                        </div>
                      )}

                      <div className="flex justify-between items-center p-4 bg-white rounded-lg">
                        <span className="text-gray-600">Delivery Fee</span>
                        <span>{result.deliveryFee === '0.00' ? 'FREE' : `JMD $${result.deliveryFee}`}</span>
                      </div>
                      
                      <div className="flex justify-between items-center p-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg">
                        <span className="text-white font-semibold text-lg">Total Amount</span>
                        <span className="text-3xl font-bold text-white">JMD ${result.finalTotal}</span>
                      </div>
                    </div>

                    <Button 
                      onClick={handleContinueToPayment}
                      className="w-full bg-white text-cyan-600 hover:bg-gray-50 border-2 border-cyan-600 py-6"
                    >
                      Continue to Payment
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>

                    <p className="text-sm text-gray-600 text-center">
                      {result.deliveryArea} • Order at least 2 hours before needed
                    </p>
                  </CardContent>
                </Card>
              ) : (
                <Card className="bg-gradient-to-br from-gray-50 to-white flex items-center justify-center">
                  <CardContent className="text-center py-12">
                    <Calculator className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500">Enter event details to see your quote</p>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default SimpleQuotePage;
