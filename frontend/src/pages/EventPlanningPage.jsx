import React, { useState } from 'react';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Calculator, Users, Clock, Calendar, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const EventPlanningPage = () => {
  const [formData, setFormData] = useState({
    guests: '',
    duration: '',
    eventType: ''
  });
  
  const [result, setResult] = useState(null);

  const calculateIce = () => {
    const guests = parseInt(formData.guests) || 0;
    const duration = parseFloat(formData.duration) || 0;
    
    // Ice calculation formula (optimized for 10lb bags):
    // More conservative approach: 0.5 lb per guest per hour base
    // This accounts for: drinks, cooling, and wastage
    const baseLbsPerGuestPerHour = 0.5;
    
    // Event type multipliers (reduced to be more realistic)
    const multipliers = {
      'party': 0.8,      // Social events - moderate ice use
      'wedding': 1.0,    // Formal events - standard use
      'restaurant': 1.2, // Commercial - higher turnover
      'bar': 1.5,        // Bars - highest ice consumption
      'corporate': 0.7   // Corporate - lighter consumption
    };
    
    const multiplier = multipliers[formData.eventType] || 0.8;
    const totalIceLbs = guests * duration * baseLbsPerGuestPerHour * multiplier;
    
    // Calculate bags needed (10 lb bags), minimum 1 bag
    const bagsNeeded = Math.max(1, Math.ceil(totalIceLbs / 10));
    
    // Calculate price (JMD $350 per bag)
    const pricePerBag = 350.00;
    const totalPrice = bagsNeeded * pricePerBag;
    
    // Apply discount: 10% for 15+ bags only
    let discount = 0;
    if (bagsNeeded >= 15) {
      discount = 0.10;
    }
    
    const discountAmount = totalPrice * discount;
    const finalPrice = totalPrice - discountAmount;
    
    setResult({
      totalIceLbs: totalIceLbs.toFixed(1),
      bagsNeeded,
      pricePerBag,
      totalPrice: totalPrice.toFixed(2),
      discount: (discount * 100).toFixed(0),
      discountAmount: discountAmount.toFixed(2),
      finalPrice: finalPrice.toFixed(2)
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    calculateIce();
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
              Event Planning Calculator
            </h1>
            <p className="text-xl text-gray-600">
              Calculate the perfect amount of ice needed for your event based on guest count, duration, and event type.
            </p>
          </div>
        </div>
      </section>

      {/* Calculator Section */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Calculator Form */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calculator className="h-5 w-5 text-cyan-600" />
                  Enter Event Details
                </CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="guests" className="flex items-center gap-2">
                      <Users className="h-4 w-4 text-gray-500" />
                      Number of Guests
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
                      Event Duration (hours)
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
                      Event Type
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

                  <Button 
                    type="submit" 
                    className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700"
                  >
                    Calculate Ice Needed
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Results Display */}
            {result && (
              <Card className="bg-gradient-to-br from-cyan-50 to-blue-50">
                <CardHeader>
                  <CardTitle className="text-cyan-700">Your Ice Calculation</CardTitle>
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
                      <span className="text-gray-600">Price per Bag</span>
                      <span className="text-lg font-semibold text-gray-900">JMD ${result.pricePerBag}</span>
                    </div>

                    {result.discount > 0 && (
                      <>
                        <div className="flex justify-between items-center p-4 bg-white rounded-lg">
                          <span className="text-gray-600">Subtotal</span>
                          <span className="text-lg text-gray-900">JMD ${result.totalPrice}</span>
                        </div>
                        
                        <div className="flex justify-between items-center p-4 bg-green-100 rounded-lg border-2 border-green-300">
                          <span className="text-green-700 font-medium">Bulk Discount ({result.discount}%)</span>
                          <span className="text-lg font-semibold text-green-700">-JMD ${result.discountAmount}</span>
                        </div>
                      </>
                    )}
                    
                    <div className="flex justify-between items-center p-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg">
                      <span className="text-white font-semibold text-lg">Total Price</span>
                      <span className="text-3xl font-bold text-white">JMD ${result.finalPrice}</span>
                    </div>
                  </div>

                  <Link to="/quote" state={{ calculatedBags: result.bagsNeeded }}>
                    <Button className="w-full bg-white text-cyan-600 hover:bg-gray-50 border-2 border-cyan-600">
                      Proceed to Order
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>

                  <p className="text-sm text-gray-600 text-center">
                    Free delivery in Washington Gardens | JMD $300 delivery fee elsewhere
                  </p>
                </CardContent>
              </Card>
            )}

            {!result && (
              <Card className="bg-gradient-to-br from-gray-50 to-white flex items-center justify-center">
                <CardContent className="text-center py-12">
                  <Calculator className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Enter your event details to see ice calculations</p>
                </CardContent>
              </Card>
            )}
          </div>

          {/* How It Works */}
          <div className="mt-16 max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">How We Calculate</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card>
                <CardContent className="p-6 text-center">
                  <Users className="h-10 w-10 text-cyan-600 mx-auto mb-4" />
                  <h3 className="font-semibold mb-2">Guest Count</h3>
                  <p className="text-sm text-gray-600">Base calculation on number of attendees</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <Clock className="h-10 w-10 text-cyan-600 mx-auto mb-4" />
                  <h3 className="font-semibold mb-2">Event Duration</h3>
                  <p className="text-sm text-gray-600">Longer events need more ice</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-6 text-center">
                  <Calendar className="h-10 w-10 text-cyan-600 mx-auto mb-4" />
                  <h3 className="font-semibold mb-2">Event Type</h3>
                  <p className="text-sm text-gray-600">Different events have different ice needs</p>
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

export default EventPlanningPage;
