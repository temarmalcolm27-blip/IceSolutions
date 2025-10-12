import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { 
  Package, 
  CheckCircle, 
  Clock, 
  Truck, 
  Shield,
  Star,
  ArrowRight,
  Bell,
  X
} from 'lucide-react';
import { mockData } from '../data/mock';
import { apiService } from '../services/api';
import { toast } from 'sonner';

const ProductsPage = () => {
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showNotifyDialog, setShowNotifyDialog] = useState(false);
  const [notifyProduct, setNotifyProduct] = useState(null);
  const [notifyEmail, setNotifyEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleNotifyClick = (product) => {
    setNotifyProduct(product);
    setShowNotifyDialog(true);
  };

  const handleNotifySubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      await apiService.subscribeToNotification({
        email: notifyEmail,
        product_name: notifyProduct.name,
        product_size: notifyProduct.weight
      });

      toast.success(`You'll be notified when ${notifyProduct.weight} bags are available!`);
      setShowNotifyDialog(false);
      setNotifyEmail('');
      setNotifyProduct(null);
    } catch (error) {
      console.error('Error subscribing:', error);
      toast.error('Failed to subscribe. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-6">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Premium Ice Products
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Crystal-clear, restaurant-quality ice delivered fresh to your door. 
              Choose from our range of premium ice products perfect for any event size.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Badge className="bg-green-100 text-green-700 px-4 py-2">
                <CheckCircle className="mr-1 h-4 w-4" />
                Same-Day Delivery
              </Badge>
              <Badge className="bg-blue-100 text-blue-700 px-4 py-2">
                <Shield className="mr-1 h-4 w-4" />
                Quality Guaranteed
              </Badge>
              <Badge className="bg-cyan-100 text-cyan-700 px-4 py-2">
                <Truck className="mr-1 h-4 w-4" />
                Free Local Delivery
              </Badge>
            </div>
          </div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {mockData.products.map((product) => (
              <Card 
                key={product.id} 
                className={`group hover:shadow-2xl transition-all duration-300 border-0 shadow-lg overflow-hidden cursor-pointer ${
                  selectedProduct === product.id ? 'ring-2 ring-cyan-500 shadow-2xl' : ''
                }`}
                onClick={() => setSelectedProduct(selectedProduct === product.id ? null : product.id)}
              >
                <div className="aspect-video bg-gradient-to-br from-gray-50 to-white flex items-center justify-center relative overflow-hidden">
                  {product.id === 'prod_10lb' ? (
                    <img 
                      src="https://customer-assets.emergentagent.com/job_cool-cubes/artifacts/gat89bkm_10lbs%20ice%20bags.png"
                      alt="10lb Ice Bags"
                      className="w-full h-full object-contain p-6 group-hover:scale-110 transition-transform duration-300"
                    />
                  ) : (
                    <Package className="h-20 w-20 text-cyan-600 group-hover:scale-110 transition-transform duration-300" />
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  
                  {product.comingSoon && (
                    <Badge className="absolute top-4 right-4 bg-amber-500 text-white shadow-lg">
                      Coming Soon
                    </Badge>
                  )}
                  {product.inStock && (
                    <Badge className="absolute top-4 right-4 bg-green-500 text-white shadow-lg">
                      In Stock
                    </Badge>
                  )}
                  
                  <div className="absolute bottom-4 left-4">
                    <Badge className="bg-white/90 text-gray-700 font-semibold">
                      {product.weight}
                    </Badge>
                  </div>
                </div>

                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-cyan-600 transition-colors">
                      {product.name}
                    </h3>
                    <div className="text-right">
                      <span className="text-2xl font-bold text-cyan-600">${product.price}</span>
                      <div className="text-sm text-gray-500">per bag</div>
                    </div>
                  </div>
                  
                  <p className="text-gray-600 mb-4 leading-relaxed">{product.description}</p>
                  
                  {/* Features */}
                  <div className="space-y-2 mb-6">
                    {product.features.map((feature, index) => (
                      <div key={index} className="flex items-center text-sm">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                        <span className="text-gray-700">{feature}</span>
                      </div>
                    ))}
                  </div>

                  {/* Action Buttons */}
                  <div className="space-y-3">
                    {product.inStock ? (
                      <>
                        <Link to="/quote" className="block">
                          <Button className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white shadow-lg">
                            Order Now
                            <ArrowRight className="ml-2 h-4 w-4" />
                          </Button>
                        </Link>
                        <Link to="/quote" className="block">
                          <Button variant="outline" className="w-full border-cyan-500 text-cyan-600 hover:bg-cyan-50">
                            Get Custom Quote
                          </Button>
                        </Link>
                      </>
                    ) : (
                      <Button 
                        className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white" 
                        onClick={() => handleNotifyClick(product)}
                      >
                        <Bell className="mr-2 h-4 w-4" />
                        Notify When Available
                      </Button>
                    )}
                  </div>
                </CardContent>

                {/* Expanded Details */}
                {selectedProduct === product.id && (
                  <div className="border-t border-gray-200 bg-gray-50 p-6">
                    <Tabs defaultValue="details" className="w-full">
                      <TabsList className="grid w-full grid-cols-2">
                        <TabsTrigger value="details">Details</TabsTrigger>
                        <TabsTrigger value="delivery">Delivery Info</TabsTrigger>
                      </TabsList>
                      
                      <TabsContent value="details" className="mt-4 space-y-4">
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Product Specifications</h4>
                          <ul className="space-y-1 text-sm text-gray-600">
                            <li>• Weight: {product.weight}</li>
                            <li>• Ice Type: Premium cube ice</li>
                            <li>• Temperature: -10°F to 0°F</li>
                            <li>• Shelf Life: 24-48 hours in cooler</li>
                          </ul>
                        </div>
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Perfect For</h4>
                          <ul className="space-y-1 text-sm text-gray-600">
                            <li>• Parties and events</li>
                            <li>• Restaurants and bars</li>
                            <li>• Catering services</li>
                            <li>• Emergency cooling needs</li>
                          </ul>
                        </div>
                      </TabsContent>
                      
                      <TabsContent value="delivery" className="mt-4 space-y-4">
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Delivery Options</h4>
                          <ul className="space-y-1 text-sm text-gray-600">
                            <li>• Same-day delivery available</li>
                            <li>• 2-hour delivery window</li>
                            <li>• Free delivery in downtown area</li>
                            <li>• Contactless delivery available</li>
                          </ul>
                        </div>
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Bulk Discounts</h4>
                          <ul className="space-y-1 text-sm text-gray-600">
                            <li>• 5+ bags: 5% discount</li>
                            <li>• 10+ bags: 10% discount</li>
                            <li>• 20+ bags: 15% discount</li>
                            <li>• Custom pricing for 50+ bags</li>
                          </ul>
                        </div>
                      </TabsContent>
                    </Tabs>
                  </div>
                )}
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Ice Calculator Section */}
      <section className="py-16 bg-gradient-to-br from-gray-50 to-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="max-w-2xl mx-auto border-0 shadow-xl">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-gray-900">How Much Ice Do You Need?</CardTitle>
              <p className="text-gray-600">Use our calculator to estimate the perfect amount for your event</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700">Number of Guests</label>
                  <select className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                    <option>10-25 guests</option>
                    <option>25-50 guests</option>
                    <option>50-100 guests</option>
                    <option>100+ guests</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700">Event Duration</label>
                  <select className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent">
                    <option>2-4 hours</option>
                    <option>4-6 hours</option>
                    <option>6-8 hours</option>
                    <option>8+ hours</option>
                  </select>
                </div>
              </div>
              
              <div className="bg-cyan-50 p-6 rounded-lg border border-cyan-200">
                <h4 className="font-semibold text-cyan-900 mb-2">Recommended Amount</h4>
                <p className="text-2xl font-bold text-cyan-600">3-4 bags (30-40 lbs)</p>
                <p className="text-sm text-cyan-700 mt-1">Based on your selections</p>
              </div>
              
              <Link to="/quote">
                <Button className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white">
                  Get Quote for This Amount
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose Our Ice?
            </h2>
            <p className="text-lg text-gray-600">
              Premium quality and service that sets us apart
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 mx-auto bg-gradient-to-br from-cyan-100 to-blue-100 rounded-full flex items-center justify-center">
                <Shield className="h-8 w-8 text-cyan-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Premium Quality</h3>
              <p className="text-gray-600">Crystal-clear ice made from filtered water, perfect cube size for optimal cooling and presentation.</p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 mx-auto bg-gradient-to-br from-cyan-100 to-blue-100 rounded-full flex items-center justify-center">
                <Truck className="h-8 w-8 text-cyan-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Fast Delivery</h3>
              <p className="text-gray-600">Same-day delivery available with 2-hour windows. We'll get your ice to you when you need it.</p>
            </div>
            
            <div className="text-center space-y-4">
              <div className="w-16 h-16 mx-auto bg-gradient-to-br from-cyan-100 to-blue-100 rounded-full flex items-center justify-center">
                <Star className="h-8 w-8 text-cyan-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Trusted Service</h3>
              <p className="text-gray-600">4.9/5 star rating from 1000+ satisfied customers. Reliable service you can count on.</p>
            </div>
          </div>
        </div>
      </section>

      <Footer />

      {/* Notification Dialog */}
      {showNotifyDialog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-md w-full">
            <CardHeader className="relative">
              <button
                onClick={() => setShowNotifyDialog(false)}
                className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5 text-cyan-600" />
                Get Notified
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleNotifySubmit} className="space-y-4">
                <p className="text-gray-600">
                  We'll send you an email when <strong>{notifyProduct?.weight} {notifyProduct?.name}</strong> become available.
                </p>
                
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="your.email@example.com"
                    value={notifyEmail}
                    onChange={(e) => setNotifyEmail(e.target.value)}
                    required
                  />
                </div>

                <div className="flex gap-3">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setShowNotifyDialog(false)}
                    className="flex-1"
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    disabled={isSubmitting}
                    className="flex-1 bg-gradient-to-r from-cyan-500 to-blue-600"
                  >
                    {isSubmitting ? 'Subscribing...' : 'Notify Me'}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default ProductsPage;