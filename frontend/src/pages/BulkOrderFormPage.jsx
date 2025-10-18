import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Badge } from '../components/ui/badge';
import { Package, CheckCircle, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

const BulkOrderFormPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  // Get tier info from URL parameters
  const tierParam = searchParams.get('tier'); // e.g., "10-19"
  const quantityParam = searchParams.get('quantity'); // e.g., "19"
  const discountParam = searchParams.get('discount'); // e.g., "10"
  
  // Parse tier range
  const parseTierRange = (tier) => {
    if (!tier) return { min: 1, max: 999 };
    const parts = tier.split('-');
    if (parts.length === 1 && parts[0].endsWith('+')) {
      return { min: parseInt(parts[0]), max: 999 };
    }
    return { 
      min: parseInt(parts[0]) || 1, 
      max: parseInt(parts[1]) || 999 
    };
  };
  
  const tierRange = parseTierRange(tierParam);
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    businessName: '',
    quantity: parseInt(quantityParam) || tierRange.max,
    deliveryAddress: '',
    deliveryDate: '',
    notes: ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // Calculate pricing
  const basePrice = 350;
  const discount = parseInt(discountParam) || 0;
  const pricePerBag = basePrice * (1 - discount / 100);
  const subtotal = pricePerBag * formData.quantity;
  const totalSavings = (basePrice - pricePerBag) * formData.quantity;
  
  // Validate quantity is within tier range
  const isValidQuantity = formData.quantity >= tierRange.min && formData.quantity <= tierRange.max;
  
  const handleQuantityChange = (e) => {
    const value = parseInt(e.target.value) || tierRange.min;
    setFormData({ ...formData, quantity: value });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!isValidQuantity) {
      toast.error(`Quantity must be between ${tierRange.min} and ${tierRange.max} bags for this discount tier`);
      return;
    }
    
    // Navigate to checkout with bulk order data
    navigate('/checkout', {
      state: {
        bags: formData.quantity,
        deliveryAddress: formData.deliveryAddress,
        deliveryFee: 0, // Free delivery will be calculated at checkout
        discountPercent: discount,
        discountAmount: totalSavings,
        pricePerBag: pricePerBag,
        totalAmount: subtotal,
        isBulkOrder: true,
        bulkOrderTier: tierParam,
        customerName: formData.name,
        customerEmail: formData.email,
        customerPhone: formData.phone,
        businessName: formData.businessName,
        deliveryDate: formData.deliveryDate,
        notes: formData.notes
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
          <div className="text-center space-y-4 max-w-3xl mx-auto">
            <div className="inline-block p-3 bg-cyan-100 rounded-full">
              <Package className="h-8 w-8 text-cyan-600" />
            </div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Bulk Order Form
            </h1>
            <p className="text-xl text-gray-600">
              Complete your order details and we'll follow up to confirm delivery
            </p>
            {tierParam && (
              <Badge className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white text-lg px-6 py-2">
                {tierParam} Bags - {discount}% Discount
              </Badge>
            )}
          </div>
        </div>
      </section>
      
      {/* Order Form */}
      <section className="py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            
            {/* Form - Left Side */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Order Information</CardTitle>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Contact Information */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold text-gray-900">Contact Details</h3>
                      
                      <div>
                        <Label htmlFor="name">Full Name *</Label>
                        <Input
                          id="name"
                          type="text"
                          value={formData.name}
                          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                          required
                          placeholder="John Smith"
                        />
                      </div>
                      
                      <div>
                        <Label htmlFor="phone">Phone Number *</Label>
                        <Input
                          id="phone"
                          type="tel"
                          value={formData.phone}
                          onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                          required
                          placeholder="(876) 555-1234"
                        />
                      </div>
                      
                      <div>
                        <Label htmlFor="email">Email Address *</Label>
                        <Input
                          id="email"
                          type="email"
                          value={formData.email}
                          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                          required
                          placeholder="john@example.com"
                        />
                      </div>
                      
                      <div>
                        <Label htmlFor="businessName">Business Name (Optional)</Label>
                        <Input
                          id="businessName"
                          type="text"
                          value={formData.businessName}
                          onChange={(e) => setFormData({ ...formData, businessName: e.target.value })}
                          placeholder="Your Business Name"
                        />
                      </div>
                    </div>
                    
                    {/* Order Details */}
                    <div className="space-y-4 pt-6 border-t">
                      <h3 className="text-lg font-semibold text-gray-900">Order Details</h3>
                      
                      <div>
                        <Label htmlFor="quantity">
                          Number of Bags * 
                          {tierParam && (
                            <span className="text-sm text-gray-500 ml-2">
                              (Range: {tierRange.min}-{tierRange.max > 900 ? '∞' : tierRange.max})
                            </span>
                          )}
                        </Label>
                        <Input
                          id="quantity"
                          type="number"
                          value={formData.quantity}
                          onChange={handleQuantityChange}
                          min={tierRange.min}
                          max={tierRange.max > 900 ? undefined : tierRange.max}
                          required
                        />
                        {!isValidQuantity && (
                          <div className="flex items-center gap-2 mt-2 text-red-600 text-sm">
                            <AlertCircle className="h-4 w-4" />
                            <span>Quantity must be between {tierRange.min} and {tierRange.max > 900 ? 'unlimited' : tierRange.max} for this discount tier</span>
                          </div>
                        )}
                      </div>
                      
                      <div>
                        <Label htmlFor="deliveryAddress">Delivery Address *</Label>
                        <Input
                          id="deliveryAddress"
                          type="text"
                          value={formData.deliveryAddress}
                          onChange={(e) => setFormData({ ...formData, deliveryAddress: e.target.value })}
                          required
                          placeholder="123 Main St, Washington Gardens"
                        />
                      </div>
                      
                      <div>
                        <Label htmlFor="deliveryDate">Preferred Delivery Date *</Label>
                        <Input
                          id="deliveryDate"
                          type="date"
                          value={formData.deliveryDate}
                          onChange={(e) => setFormData({ ...formData, deliveryDate: e.target.value })}
                          required
                          min={new Date().toISOString().split('T')[0]}
                        />
                      </div>
                      
                      <div>
                        <Label htmlFor="notes">Special Instructions (Optional)</Label>
                        <textarea
                          id="notes"
                          value={formData.notes}
                          onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                          rows={4}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
                          placeholder="Any special delivery instructions or requirements..."
                        />
                      </div>
                    </div>
                    
                    <Button 
                      type="submit" 
                      className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white text-lg py-6"
                      disabled={isSubmitting || !isValidQuantity}
                    >
                      {isSubmitting ? 'Submitting...' : 'Submit Pre-Order Request'}
                    </Button>
                    
                    <p className="text-sm text-gray-600 text-center">
                      By submitting, you agree to be contacted to confirm your order details and delivery schedule.
                    </p>
                  </form>
                </CardContent>
              </Card>
            </div>
            
            {/* Order Summary - Right Side */}
            <div className="lg:col-span-1">
              <Card className="sticky top-4">
                <CardHeader>
                  <CardTitle>Order Summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex justify-between text-gray-600">
                      <span>Quantity:</span>
                      <span className="font-semibold text-gray-900">{formData.quantity} bags</span>
                    </div>
                    
                    <div className="flex justify-between text-gray-600">
                      <span>Base Price:</span>
                      <span>JMD ${basePrice.toFixed(2)}</span>
                    </div>
                    
                    {discount > 0 && (
                      <div className="flex justify-between text-green-600">
                        <span>Discount ({discount}%):</span>
                        <span>-JMD ${(basePrice - pricePerBag).toFixed(2)}</span>
                      </div>
                    )}
                    
                    <div className="flex justify-between text-gray-900 font-semibold">
                      <span>Price per Bag:</span>
                      <span>JMD ${pricePerBag.toFixed(2)}</span>
                    </div>
                    
                    <div className="pt-4 border-t border-gray-200">
                      <div className="flex justify-between text-xl font-bold text-gray-900">
                        <span>Total:</span>
                        <span>JMD ${subtotal.toFixed(2)}</span>
                      </div>
                    </div>
                    
                    {totalSavings > 0 && (
                      <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                        <div className="flex items-center justify-between text-green-700">
                          <span className="text-sm font-medium">Your Savings:</span>
                          <span className="text-lg font-bold">JMD ${totalSavings.toFixed(2)}</span>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="pt-4 border-t border-gray-200 space-y-2">
                    <div className="flex items-start gap-2 text-sm text-gray-600">
                      <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                      <span>Same-day delivery available</span>
                    </div>
                    <div className="flex items-start gap-2 text-sm text-gray-600">
                      <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                      <span>FREE delivery in Washington Gardens</span>
                    </div>
                    <div className="flex items-start gap-2 text-sm text-gray-600">
                      <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                      <span>Restaurant-quality ice guaranteed</span>
                    </div>
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

export default BulkOrderFormPage;
