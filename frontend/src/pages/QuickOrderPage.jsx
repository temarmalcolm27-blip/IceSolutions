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
import { Package, ShoppingCart, MapPin, User } from 'lucide-react';

const QuickOrderPage = () => {
  const navigate = useNavigate();
  
  const [step, setStep] = useState(1); // 1 = quantity, 2 = details
  const [quantity, setQuantity] = useState('');
  const [customerInfo, setCustomerInfo] = useState({
    name: '',
    address: ''
  });

  const pricePerPack = 350;
  const subtotal = parseInt(quantity) * pricePerPack || 0;
  
  // Calculate discount (10% for 15+ packs)
  const discount = parseInt(quantity) >= 15 ? subtotal * 0.10 : 0;
  const total = subtotal - discount;

  const handleQuantitySubmit = (e) => {
    e.preventDefault();
    if (quantity && parseInt(quantity) > 0) {
      setStep(2);
    }
  };

  const handleCheckout = (e) => {
    e.preventDefault();
    
    // Navigate to checkout with order data
    navigate('/checkout', {
      state: {
        bags: parseInt(quantity),
        deliveryAddress: customerInfo.address,
        totalAmount: total,
        discountPercent: discount > 0 ? 10 : 0,
        discountAmount: discount,
        pricePerBag: pricePerPack,
        customerName: customerInfo.name,
        productName: 'Quick Pack'
      }
    });
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-cyan-50 via-white to-blue-50 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Quick Order - Quick Pack
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Fast and simple ordering for our Quick Pack (single bag)
            </p>
            <Badge className="bg-cyan-100 text-cyan-700 px-4 py-2 text-lg">
              JMD $350 per pack
            </Badge>
          </div>
        </div>
      </section>

      <section className="py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            
            {/* Left Side - Order Form */}
            <div className="space-y-8">
              
              {/* Step 1: Quantity */}
              {step === 1 && (
                <Card className="border-0 shadow-xl">
                  <CardHeader>
                    <CardTitle className="text-2xl text-gray-900 flex items-center gap-2">
                      <Package className="h-6 w-6 text-cyan-600" />
                      Step 1: Select Quantity
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <form onSubmit={handleQuantitySubmit} className="space-y-6">
                      <div className="space-y-4 p-6 bg-cyan-50 rounded-lg border-2 border-cyan-200">
                        <Label htmlFor="quantity" className="text-xl font-semibold text-gray-900">
                          Number of Quick Packs Needed *
                        </Label>
                        <Input
                          id="quantity"
                          type="number"
                          min="1"
                          value={quantity}
                          onChange={(e) => setQuantity(e.target.value)}
                          placeholder="Enter number of packs"
                          className="text-2xl py-6 text-center font-bold"
                          required
                          autoFocus
                        />
                        <p className="text-sm text-gray-600 text-center">
                          💡 1 Quick Pack = 10 lbs (serves ~25 people for 1 hour)
                        </p>
                      </div>

                      <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                        <h4 className="font-semibold text-blue-900 mb-2">Quick Guide</h4>
                        <ul className="text-sm text-blue-700 space-y-1">
                          <li>• Small gathering (10-25 people): 1-2 packs</li>
                          <li>• Medium party (25-50 people): 3-5 packs</li>
                          <li>• Large event (50-100 people): 6-10 packs</li>
                          <li>• Major event (100+ people): 15+ packs (10% discount!)</li>
                        </ul>
                      </div>

                      <Button 
                        type="submit" 
                        className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white py-6 text-lg"
                        disabled={!quantity || parseInt(quantity) <= 0}
                      >
                        Continue to Details
                      </Button>
                    </form>
                  </CardContent>
                </Card>
              )}

              {/* Step 2: Customer Details */}
              {step === 2 && (
                <Card className="border-0 shadow-xl">
                  <CardHeader>
                    <CardTitle className="text-2xl text-gray-900 flex items-center gap-2">
                      <User className="h-6 w-6 text-cyan-600" />
                      Step 2: Your Details
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <form onSubmit={handleCheckout} className="space-y-6">
                      
                      {/* Quantity Summary */}
                      <div className="bg-cyan-50 p-4 rounded-lg border border-cyan-200">
                        <p className="text-sm text-cyan-700">
                          <strong>Order:</strong> {quantity} Quick Pack{parseInt(quantity) > 1 ? 's' : ''}
                        </p>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => setStep(1)}
                          className="mt-2 text-cyan-600"
                        >
                          ← Change Quantity
                        </Button>
                      </div>

                      <div className="space-y-4">
                        <div className="space-y-2">
                          <Label htmlFor="name" className="flex items-center gap-2">
                            <User className="h-4 w-4 text-gray-600" />
                            Full Name *
                          </Label>
                          <Input
                            id="name"
                            value={customerInfo.name}
                            onChange={(e) => setCustomerInfo({...customerInfo, name: e.target.value})}
                            placeholder="Enter your full name"
                            required
                            autoFocus
                          />
                        </div>

                        <div className="space-y-2">
                          <Label htmlFor="address" className="flex items-center gap-2">
                            <MapPin className="h-4 w-4 text-gray-600" />
                            Delivery Address *
                          </Label>
                          <Input
                            id="address"
                            value={customerInfo.address}
                            onChange={(e) => setCustomerInfo({...customerInfo, address: e.target.value})}
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
                      >
                        <ShoppingCart className="mr-2 h-5 w-5" />
                        Proceed to Checkout
                      </Button>
                    </form>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Right Side - Order Summary */}
            <div className="space-y-6">
              <Card className="border-0 shadow-xl sticky top-6">
                <CardHeader className="bg-gradient-to-br from-cyan-500 to-blue-600 text-white">
                  <CardTitle className="text-2xl">Order Summary</CardTitle>
                </CardHeader>
                <CardContent className="p-6">
                  {quantity && parseInt(quantity) > 0 ? (
                    <div className="space-y-6">
                      <div className="space-y-4">
                        <div className="flex justify-between items-center text-lg">
                          <span className="text-gray-700">Quick Packs</span>
                          <span className="font-semibold">{quantity} pack{parseInt(quantity) > 1 ? 's' : ''}</span>
                        </div>
                        
                        <div className="flex justify-between items-center">
                          <span className="text-gray-700">Price per pack</span>
                          <span>JMD ${pricePerPack.toFixed(2)}</span>
                        </div>
                        
                        <div className="flex justify-between items-center">
                          <span className="text-gray-700">Subtotal</span>
                          <span>JMD ${subtotal.toFixed(2)}</span>
                        </div>

                        {discount > 0 && (
                          <div className="flex justify-between items-center text-green-600">
                            <span className="font-medium">Discount (10%)</span>
                            <span className="font-semibold">-JMD ${discount.toFixed(2)}</span>
                          </div>
                        )}

                        <div className="pt-4 border-t-2 border-gray-300">
                          <div className="flex justify-between items-center text-2xl font-bold">
                            <span className="text-gray-900">Total</span>
                            <span className="text-cyan-600">JMD ${total.toFixed(2)}</span>
                          </div>
                          <p className="text-xs text-gray-500 mt-2">
                            * Delivery fee will be calculated at checkout based on your location
                          </p>
                        </div>
                      </div>

                      {parseInt(quantity) >= 15 && (
                        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
                          <p className="text-green-700 font-semibold text-center">
                            🎉 You're saving 10% on this order!
                          </p>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-12">
                      <Package className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                      <p className="text-gray-500 text-lg">
                        Enter quantity to see your total
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Info Card */}
              <Card className="bg-gradient-to-br from-cyan-50 to-blue-50 border-cyan-200">
                <CardContent className="p-6">
                  <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                    <Package className="h-5 w-5 text-cyan-600" />
                    About Quick Pack
                  </h3>
                  <ul className="space-y-2 text-sm text-gray-700">
                    <li>• <strong>Weight:</strong> 10 lbs per pack</li>
                    <li>• <strong>Quality:</strong> Crystal clear, restaurant-grade</li>
                    <li>• <strong>Delivery:</strong> Same-day available</li>
                    <li>• <strong>Discount:</strong> 10% off orders of 15+ packs</li>
                    <li>• <strong>Free Delivery:</strong> On orders of 20+ packs</li>
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

export default QuickOrderPage;
