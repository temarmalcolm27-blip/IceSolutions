import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Badge } from '../components/ui/badge';
import { Package, MapPin, ShoppingCart } from 'lucide-react';
import apiService from '../services/api';

const QuotePage = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    bags: '',
    name: '',
    email: '',
    phone: '',
    address: ''
  });
  
  const [calculatedQuote, setCalculatedQuote] = useState(null);

  // Real-time quote calculation with debounce
  useEffect(() => {
    const timeoutId = setTimeout(async () => {
      const bags = parseInt(formData.bags) || 0;
      const address = formData.address || '';
      
      if (bags > 0) {
        const quote = await apiService.calculateInstantQuote(bags, 0, address);
        setCalculatedQuote(quote);
      } else {
        setCalculatedQuote(null);
      }
    }, 800);
    
    return () => clearTimeout(timeoutId);
  }, [formData.bags, formData.address]);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleContinueToCheckout = (e) => {
    e.preventDefault();
    
    if (!calculatedQuote) {
      alert('Please enter number of bags');
      return;
    }
    
    // Navigate to checkout with quote data
    navigate('/checkout', {
      state: {
        bags: calculatedQuote.bags,
        deliveryFee: calculatedQuote.deliveryFee,
        deliveryAddress: formData.address,
        totalAmount: calculatedQuote.total,
        discountPercent: calculatedQuote.discountPercent,
        discountAmount: calculatedQuote.savings,
        pricePerBag: 350,
        customerName: formData.name,
        customerEmail: formData.email,
        customerPhone: formData.phone
      }
    });
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Get Your Ice Quote
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Tell us how many bags you need and we'll calculate your total instantly
            </p>
            <div className="flex items-center justify-center gap-2">
              <Badge className="bg-cyan-100 text-cyan-700 px-4 py-2">
                <Package className="mr-1 h-4 w-4" />
                Quick Fix - JMD $350/bag
              </Badge>
              <Badge className="bg-green-100 text-green-700 px-4 py-2">
                10% OFF 15+ bags
              </Badge>
            </div>
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
                  <CardTitle className="text-2xl text-gray-900">
                    Order Details
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleContinueToCheckout} className="space-y-6">
                    
                    {/* Number of Bags - Main Question */}
                    <div className="space-y-4 p-6 bg-cyan-50 rounded-lg border-2 border-cyan-200">
                      <Label htmlFor="bags" className="text-xl font-semibold text-gray-900">
                        How many Quick Fix (10lb) bags do you need? *
                      </Label>
                      <Input
                        id="bags"
                        type="number"
                        min="1"
                        value={formData.bags}
                        onChange={(e) => handleInputChange('bags', e.target.value)}
                        placeholder="Enter number of bags"
                        className="text-2xl py-6 text-center font-bold"
                        required
                      />
                      <p className="text-sm text-gray-600 text-center">
                        💡 Not sure? 1 bag serves ~25 people for 1 hour
                      </p>
                    </div>

                    {/* Contact Information */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold text-gray-900">Contact Information</h3>
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
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                          <Label htmlFor="phone">Phone Number *</Label>
                          <Input
                            id="phone"
                            type="tel"
                            value={formData.phone}
                            onChange={(e) => handleInputChange('phone', e.target.value)}
                            placeholder="(876) 123-4567"
                            required
                          />
                        </div>
                      </div>
                    </div>

                    {/* Delivery Address */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                        <MapPin className="mr-2 h-5 w-5 text-cyan-600" />
                        Delivery Address
                      </h3>
                      <div className="space-y-2">
                        <Label htmlFor="address">Full Delivery Address *</Label>
                        <Input
                          id="address"
                          value={formData.address}
                          onChange={(e) => handleInputChange('address', e.target.value)}
                          placeholder="123 Main St, Washington Gardens, Kingston"
                          required
                        />
                        <p className="text-xs text-gray-500">
                          Include street address, area, and any landmarks
                        </p>
                      </div>
                    </div>

                    <Button 
                      type="submit" 
                      className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white py-6 text-lg"
                      disabled={!calculatedQuote}
                    >
                      <ShoppingCart className="mr-2 h-5 w-5" />
                      Continue to Payment
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Instant Quote Display */}
            <div className="space-y-6">
              {calculatedQuote ? (
                <Card className="border-0 shadow-xl sticky top-6">
                  <CardHeader className="bg-gradient-to-br from-cyan-500 to-blue-600 text-white">
                    <CardTitle className="text-2xl">Your Instant Quote</CardTitle>
                  </CardHeader>
                  <CardContent className="p-6 space-y-6">
                    <div className="space-y-4">
                      <div className="flex justify-between items-center text-lg">
                        <span className="text-gray-700">Quick Fix Bags</span>
                        <span className="font-semibold">{calculatedQuote.bags} bags</span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-gray-700">Price per bag</span>
                        <span>JMD $350.00</span>
                      </div>
                      
                      <div className="flex justify-between items-center">
                        <span className="text-gray-700">Subtotal</span>
                        <span>JMD ${calculatedQuote.basePrice.toFixed(2)}</span>
                      </div>

                      {calculatedQuote.savings > 0 && (
                        <div className="flex justify-between items-center text-green-600">
                          <span className="font-medium">Discount ({calculatedQuote.discountPercent}%)</span>
                          <span className="font-semibold">-JMD ${calculatedQuote.savings.toFixed(2)}</span>
                        </div>
                      )}

                      <div className="flex justify-between items-center">
                        <span className="text-gray-700">Delivery Fee</span>
                        <span className="font-semibold">
                          {calculatedQuote.deliveryFee === null ? (
                            <span className="text-gray-400 text-sm">{calculatedQuote.deliveryArea || '--'}</span>
                          ) : calculatedQuote.deliveryFee === 0 ? (
                            <span className="text-green-600">FREE</span>
                          ) : (
                            `JMD $${calculatedQuote.deliveryFee.toFixed(2)}`
                          )}
                        </span>
                      </div>
                      
                      {/* Delivery Fee Breakdown */}
                      {calculatedQuote.deliveryDetails && calculatedQuote.deliveryFee > 0 && (
                        <div className="ml-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
                          <div className="text-xs space-y-1">
                            <div className="font-semibold text-blue-900 mb-2">📍 Delivery Calculation:</div>
                            <div className="flex justify-between text-gray-700">
                              <span>Distance:</span>
                              <span className="font-medium">{calculatedQuote.deliveryDetails.distance_text} ({calculatedQuote.deliveryDetails.distance_miles.toFixed(2)} miles)</span>
                            </div>
                            <div className="flex justify-between text-gray-700">
                              <span>Base fee:</span>
                              <span className="font-medium">JMD $300</span>
                            </div>
                            <div className="flex justify-between text-gray-700">
                              <span>Distance fee:</span>
                              <span className="font-medium">JMD $35 × {calculatedQuote.deliveryDetails.distance_miles.toFixed(2)} miles</span>
                            </div>
                            <div className="flex justify-between text-gray-700">
                              <span>Est. time:</span>
                              <span className="font-medium">{calculatedQuote.deliveryDetails.duration_text}</span>
                            </div>
                          </div>
                        </div>
                      )}

                      <div className="pt-4 border-t-2 border-gray-300">
                        <div className="flex justify-between items-center text-2xl font-bold">
                          <span className="text-gray-900">Total</span>
                          <span className="text-cyan-600">JMD ${calculatedQuote.total.toFixed(2)}</span>
                        </div>
                      </div>
                    </div>

                    {calculatedQuote.bags >= 20 && (
                      <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
                        <p className="text-green-700 font-semibold text-center">
                          🎉 You qualify for FREE delivery!
                        </p>
                      </div>
                    )}

                    {calculatedQuote.bags >= 15 && calculatedQuote.bags < 20 && (
                      <div className="bg-cyan-50 border-2 border-cyan-200 rounded-lg p-4">
                        <p className="text-cyan-700 font-semibold text-center">
                          💰 You're saving 10% on this order!
                        </p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ) : (
                <Card className="border-0 shadow-xl">
                  <CardContent className="p-12 text-center">
                    <Package className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500 text-lg">
                      Enter number of bags to see your instant quote
                    </p>
                  </CardContent>
                </Card>
              )}

              {/* Info Cards */}
              <Card className="bg-gradient-to-br from-cyan-50 to-blue-50 border-cyan-200">
                <CardContent className="p-6">
                  <h3 className="font-semibold text-gray-900 mb-3">Quick Guide</h3>
                  <ul className="space-y-2 text-sm text-gray-700">
                    <li>• <strong>Small party (10-25 people):</strong> 1-2 bags</li>
                    <li>• <strong>Medium event (25-50 people):</strong> 3-5 bags</li>
                    <li>• <strong>Large gathering (50-100 people):</strong> 6-10 bags</li>
                    <li>• <strong>Major event (100+ people):</strong> 15+ bags</li>
                  </ul>
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
