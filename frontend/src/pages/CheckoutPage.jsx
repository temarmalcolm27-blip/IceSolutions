import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { ShoppingCart, CreditCard, Truck, CheckCircle } from 'lucide-react';
import { apiService } from '../services/api';
import { toast } from 'sonner';

const CheckoutPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  
  // Get URL parameters (for chat widget integration)
  const searchParams = new URLSearchParams(location.search);
  const urlBags = searchParams.get('bags');
  const urlName = searchParams.get('name');
  const urlEmail = searchParams.get('email');
  const urlPhone = searchParams.get('phone');
  const urlAddress = searchParams.get('address');
  const fromChat = searchParams.get('from_chat') === 'true';
  
  const { 
    bags: stateBags, 
    deliveryFee, 
    deliveryAddress, 
    totalAmount, 
    discountPercent, 
    discountAmount,
    pricePerBag: customPricePerBag,
    isBulkOrder,
    bulkOrderTier,
    customerName: preFilledName,
    customerEmail: preFilledEmail,
    customerPhone: preFilledPhone,
    businessName,
    deliveryDate,
    notes
  } = location.state || {};
  
  // Use URL params if coming from chat, otherwise use state
  const bags = fromChat ? parseInt(urlBags) : stateBags;
  const initialName = fromChat ? urlName : (preFilledName || '');
  const initialEmail = fromChat ? urlEmail : (preFilledEmail || '');
  const initialPhone = fromChat ? urlPhone : (preFilledPhone || '');
  const initialAddress = fromChat ? urlAddress : (deliveryAddress || '');
  
  const [formData, setFormData] = useState({
    customerName: initialName,
    customerEmail: initialEmail,
    customerPhone: initialPhone,
    deliveryAddress: initialAddress,
    deliveryInstructions: notes || ''
  });
  
  const [calculatedDelivery, setCalculatedDelivery] = useState(null);
  const [deliveryData, setDeliveryData] = useState(null); // Store full delivery calculation data
  const [calculatingDelivery, setCalculatingDelivery] = useState(false);
  const [hasCalculated, setHasCalculated] = useState(false);

  // Calculate delivery fee when address is available (only once automatically)
  useEffect(() => {
    if (formData.deliveryAddress && !hasCalculated && bags) {
      calculateDeliveryFee();
      setHasCalculated(true);
    }
  }, [formData.deliveryAddress, bags]);
  
  const calculateDeliveryFee = async () => {
    if (!formData.deliveryAddress) return;
    
    setCalculatingDelivery(true);
    console.log('Calculating delivery fee for address:', formData.deliveryAddress);
    
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/calculate-delivery-fee`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          destination_address: formData.deliveryAddress,
          bags: bags || 0
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Delivery fee calculated:', data);
        setCalculatedDelivery(data.delivery_fee);
        setDeliveryData(data); // Store full data including distance
      } else {
        console.error('Failed to calculate delivery fee:', response.status);
      }
    } catch (error) {
      console.error('Error calculating delivery fee:', error);
    } finally {
      setCalculatingDelivery(false);
    }
  };

  useEffect(() => {
    if (!bags || !totalAmount) {
      toast.error('Invalid checkout data. Redirecting to quote page...');
      navigate('/quote');
    }
  }, [bags, totalAmount, navigate]);

  const pricePerBag = customPricePerBag || 350.00;
  const subtotal = (bags || 0) * pricePerBag;
  
  // Calculate discount: 10% for 15+ bags only
  let autoDiscountPercent = 0;
  let autoDiscountAmount = 0;
  if (bags >= 15) {
    autoDiscountPercent = 10;
    autoDiscountAmount = subtotal * 0.10;
  }
  
  const discount = discountAmount || autoDiscountAmount;
  const delivery = calculatedDelivery !== null ? calculatedDelivery : (deliveryFee || 300);
  // Always recalculate total based on current delivery fee
  const total = subtotal - discount + delivery;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const originUrl = window.location.origin;
      
      // Create checkout session with bulk order info
      const response = await apiService.createCheckoutSession({
        bags,
        delivery_address: formData.deliveryAddress,
        delivery_fee: delivery,
        discount_percent: discountPercent || 0,
        discount_amount: discount,
        is_bulk_order: isBulkOrder || false,
        bulk_order_tier: bulkOrderTier || '',
        metadata: {
          customer_name: formData.customerName,
          customer_email: formData.customerEmail,
          customer_phone: formData.customerPhone,
          business_name: businessName || '',
          delivery_date: deliveryDate || '',
          delivery_instructions: formData.deliveryInstructions
        }
      }, originUrl);

      // Redirect to Stripe Checkout
      if (response.url) {
        window.location.href = response.url;
      }
    } catch (error) {
      console.error('Checkout error:', error);
      toast.error('Failed to process checkout. Please try again.');
      setLoading(false);
    }
  };

  if (!bags) {
    return null;
  }

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Checkout
            </h1>
            <p className="text-lg text-gray-600">
              Complete your order details and proceed to payment
            </p>
          </div>
        </div>
      </section>

      {/* Checkout Form */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Contact & Delivery Information */}
              <div className="lg:col-span-2">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Truck className="h-5 w-5 text-cyan-600" />
                      Contact & Delivery Information
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="customerName">Full Name *</Label>
                          <Input
                            id="customerName"
                            required
                            value={formData.customerName}
                            onChange={(e) => setFormData({...formData, customerName: e.target.value})}
                            placeholder="John Doe"
                          />
                        </div>

                        <div className="space-y-2">
                          <Label htmlFor="customerPhone">Phone Number *</Label>
                          <Input
                            id="customerPhone"
                            type="tel"
                            required
                            value={formData.customerPhone}
                            onChange={(e) => setFormData({...formData, customerPhone: e.target.value})}
                            placeholder="+1 (876) 490-7208"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="customerEmail">Email Address *</Label>
                        <Input
                          id="customerEmail"
                          type="email"
                          required
                          value={formData.customerEmail}
                          onChange={(e) => setFormData({...formData, customerEmail: e.target.value})}
                          placeholder="john@example.com"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="deliveryAddress">Delivery Address *</Label>
                        <div className="flex gap-2">
                          <Input
                            id="deliveryAddress"
                            required
                            value={formData.deliveryAddress}
                            onChange={(e) => setFormData({...formData, deliveryAddress: e.target.value})}
                            placeholder="123 Main St, Washington Gardens"
                            className="flex-1"
                          />
                          <Button
                            type="button"
                            onClick={calculateDeliveryFee}
                            disabled={calculatingDelivery || !formData.deliveryAddress}
                            variant="outline"
                            className="whitespace-nowrap"
                          >
                            {calculatingDelivery ? 'Calculating...' : 'Calculate Fee'}
                          </Button>
                        </div>
                        {calculatingDelivery && (
                          <p className="text-sm text-gray-500">Calculating delivery fee based on distance...</p>
                        )}
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="deliveryInstructions">Delivery Instructions (Optional)</Label>
                        <Textarea
                          id="deliveryInstructions"
                          value={formData.deliveryInstructions}
                          onChange={(e) => setFormData({...formData, deliveryInstructions: e.target.value})}
                          placeholder="Gate code, special instructions, etc."
                          rows={3}
                        />
                      </div>

                      <div className="pt-4">
                        <Button
                          type="submit"
                          disabled={loading}
                          className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white py-6"
                        >
                          {loading ? (
                            'Processing...'
                          ) : (
                            <>
                              <CreditCard className="mr-2 h-5 w-5" />
                              Proceed to Payment
                            </>
                          )}
                        </Button>
                      </div>
                    </form>
                  </CardContent>
                </Card>
              </div>

              {/* Order Summary */}
              <div>
                <Card className="sticky top-24">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <ShoppingCart className="h-5 w-5 text-cyan-600" />
                      Order Summary
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex justify-between items-center pb-3 border-b">
                        <span className="text-gray-600">Quick Fix (10lb bags)</span>
                        <span className="font-semibold">{bags} bags</span>
                      </div>

                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">Price per bag</span>
                        <span>JMD ${pricePerBag.toFixed(2)}</span>
                      </div>

                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">Subtotal</span>
                        <span>JMD ${subtotal.toFixed(2)}</span>
                      </div>

                      {discount > 0 && (
                        <div className="flex justify-between items-center text-green-600">
                          <span>Discount ({discountPercent}%)</span>
                          <span>-JMD ${discount.toFixed(2)}</span>
                        </div>
                      )}

                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">Delivery Fee</span>
                        <span>
                          {delivery === 0 ? (
                            <span className="text-green-600 font-semibold">FREE</span>
                          ) : (
                            `JMD $${delivery.toFixed(2)}`
                          )}
                        </span>
                      </div>
                      
                      {/* Delivery Fee Breakdown */}
                      {deliveryData && deliveryData.delivery_fee > 0 && (
                        <div className="ml-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
                          <div className="text-xs space-y-1">
                            <div className="font-semibold text-blue-900 mb-2">📍 Delivery Calculation:</div>
                            <div className="flex justify-between text-gray-700">
                              <span>Distance:</span>
                              <span className="font-medium">{deliveryData.distance_text} ({deliveryData.distance_miles.toFixed(2)} miles)</span>
                            </div>
                            <div className="flex justify-between text-gray-700">
                              <span>Base fee:</span>
                              <span className="font-medium">JMD $300</span>
                            </div>
                            <div className="flex justify-between text-gray-700">
                              <span>Distance fee:</span>
                              <span className="font-medium">JMD $35 × {deliveryData.distance_miles.toFixed(2)} miles</span>
                            </div>
                            <div className="flex justify-between text-gray-700">
                              <span>Est. time:</span>
                              <span className="font-medium">{deliveryData.duration_text}</span>
                            </div>
                            <div className="pt-2 mt-2 border-t border-blue-200 flex justify-between font-semibold text-blue-900">
                              <span>Total delivery:</span>
                              <span>JMD ${deliveryData.delivery_fee.toFixed(2)}</span>
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {deliveryData && deliveryData.free_delivery_reason && (
                        <div className="ml-4 p-2 bg-green-50 rounded-lg border border-green-200">
                          <div className="text-xs text-green-700">
                            ✨ {deliveryData.free_delivery_reason}
                          </div>
                        </div>
                      )}
                      
                      {calculatingDelivery && (
                        <div className="text-xs text-gray-500 italic">
                          Calculating delivery fee...
                        </div>
                      )}

                      <div className="flex justify-between items-center pt-3 border-t">
                        <span className="text-lg font-semibold">Total</span>
                        <span className="text-2xl font-bold text-cyan-600">JMD ${total.toFixed(2)}</span>
                      </div>
                    </div>

                    <div className="pt-4 space-y-3">
                      <div className="flex items-start gap-2 text-sm text-gray-600">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Secure payment processing</span>
                      </div>
                      <div className="flex items-start gap-2 text-sm text-gray-600">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Same-day delivery available</span>
                      </div>
                      <div className="flex items-start gap-2 text-sm text-gray-600">
                        <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span>Quality guarantee</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default CheckoutPage;
