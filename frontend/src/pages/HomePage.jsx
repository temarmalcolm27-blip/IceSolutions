import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { 
  Truck, 
  Shield, 
  Clock, 
  Star, 
  Phone, 
  MapPin,
  Calendar,
  Package,
  ArrowRight,
  CheckCircle,
  Zap,
  Bell,
  X
} from 'lucide-react';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { mockData } from '../data/mock';
import { apiService } from '../services/api';
import { toast } from 'sonner';

const HomePage = () => {
  const [hoveredService, setHoveredService] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
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

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const productsData = await apiService.getProducts();
        setProducts(productsData);
      } catch (error) {
        console.error('Failed to load products:', error);
        // Fallback to mock data if API fails
        setProducts(mockData.products);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleQuickOrder = () => {
    toast.success("Redirecting to quote page...");
    // Will navigate to quote page
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-cyan-500 via-blue-500 to-indigo-600">
        {/* Ice Image Background - Fills entire blue area */}
        <div 
          className="absolute inset-0 w-full h-full"
          style={{
            backgroundImage: 'url(https://customer-assets.emergentagent.com/job_icesolutions/artifacts/7a482py7_ice%20image%20-%20%202025-10-18%20174632.png)',
            backgroundSize: 'cover',
            backgroundPosition: 'center right',
            backgroundRepeat: 'no-repeat',
            opacity: '0.4',
            mixBlendMode: 'overlay'
          }}
        ></div>
        
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.2),transparent_50%)] pointer-events-none"></div>
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(6,182,212,0.3),transparent_50%)] pointer-events-none"></div>
        
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-24 relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            
            {/* Quick Order - Left Side */}
            <div className="relative">
              <div 
                className="relative z-10 bg-white rounded-2xl shadow-2xl p-8 border-4 border-cyan-300 hover:border-cyan-500 transition-all duration-500 hover:scale-105"
                style={{
                  boxShadow: '0 25px 50px -12px rgba(6, 182, 212, 0.4), 0 0 80px rgba(6, 182, 212, 0.2), inset 0 2px 20px rgba(255, 255, 255, 0.8)',
                  background: 'linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(224, 242, 254, 0.5) 100%)'
                }}
              >
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-gray-900">Quick Order</h3>
                    <Badge className="bg-green-100 text-green-700">Available Now</Badge>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-16 h-16 bg-gray-50 rounded-lg flex items-center justify-center p-1">
                        <img 
                          src="https://customer-assets.emergentagent.com/job_iceflow-system/artifacts/yoj6u8t5_10lb%20Quick%20Pack.jpg"
                          alt="Quick Pack Ice Bag"
                          className="w-full h-full object-contain"
                        />
                      </div>
                      <div>
                        <div className="font-medium text-gray-900">Quick Pack</div>
                        <div className="text-sm text-gray-600">Single bag solution</div>
                      </div>
                      <div className="text-lg font-bold text-cyan-600">$350.00</div>
                    </div>
                    
                    <Link to="/quote" className="block">
                      <Button className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white">
                        Order Now - Same Day Delivery
                      </Button>
                    </Link>
                  </div>
                </div>
              </div>
              
              {/* Decorative Elements - Enhanced Godly Glow */}
              <div className="absolute -top-8 -right-8 w-40 h-40 bg-gradient-to-br from-cyan-400 via-blue-400 to-blue-500 rounded-full opacity-30 blur-2xl animate-pulse"></div>
              <div className="absolute -bottom-8 -left-8 w-48 h-48 bg-gradient-to-br from-blue-400 via-cyan-400 to-cyan-500 rounded-full opacity-25 blur-2xl animate-pulse" style={{animationDelay: '1s'}}></div>
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full h-full bg-gradient-radial from-cyan-200/20 to-transparent rounded-2xl blur-xl"></div>
            </div>

            {/* Empty right column for spacing on large screens */}
            <div className="hidden lg:block"></div>
          </div>
        </div>
      </section>

      {/* Products Preview - Moved up after Hero */}
      <section className="py-16 bg-gradient-to-br from-blue-50 via-cyan-50 to-indigo-50 relative overflow-hidden">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-cyan-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
              Why Choose Ice Solutions?
            </h2>
            <p className="text-lg text-gray-700 max-w-2xl mx-auto font-medium">
              We're committed to delivering the highest quality ice with exceptional service for all your needs.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {mockData.services.map((service, index) => {
              const IconComponent = {
                Truck,
                Calendar,
                Package,
                Shield
              }[service.icon];

              // Determine link for clickable cards
              const getServiceLink = (id) => {
                if (id === 2) return '/event-planning';
                if (id === 3) return '/bulk-orders';
                return null;
              };

              const serviceLink = getServiceLink(service.id);
              const CardWrapper = serviceLink ? Link : 'div';
              const wrapperProps = serviceLink ? { to: serviceLink } : {};

              return (
                <CardWrapper key={service.id} {...wrapperProps}>
                  <Card 
                    className={`group cursor-pointer transition-all duration-300 border-2 hover:border-cyan-200 hover:shadow-lg ${
                      hoveredService === index ? 'shadow-lg border-cyan-200 scale-105' : 'shadow-sm border-gray-200'
                    }`}
                    onMouseEnter={() => setHoveredService(index)}
                    onMouseLeave={() => setHoveredService(null)}
                  >
                    <CardContent className="p-6 text-center">
                      <div className={`w-16 h-16 mx-auto mb-4 rounded-lg flex items-center justify-center transition-colors ${
                        hoveredService === index 
                          ? 'bg-gradient-to-br from-cyan-500 to-blue-600' 
                          : 'bg-gradient-to-br from-cyan-100 to-blue-100'
                      }`}>
                        <IconComponent className={`h-8 w-8 ${
                          hoveredService === index ? 'text-white' : 'text-cyan-600'
                        }`} />
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">{service.title}</h3>
                      <p className="text-gray-600 text-sm leading-relaxed">{service.description}</p>
                      {serviceLink && (
                        <div className="mt-4 flex items-center justify-center text-cyan-600 group-hover:text-cyan-700">
                          <ArrowRight className="h-4 w-4" />
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </CardWrapper>
              );
            })}
          </div>
        </div>
      </section>

      {/* Services Section - Why Choose Ice Solutions */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-cyan-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
              Our Ice Products
            </h2>
            <p className="text-lg text-gray-700 font-medium">
              Premium quality ice for every occasion and event size
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {loading ? (
              // Loading skeleton
              Array.from({ length: 3 }, (_, index) => (
                <Card key={index} className="border-0 shadow-md overflow-hidden animate-pulse">
                  <div className="aspect-video bg-gray-200"></div>
                  <CardContent className="p-6">
                    <div className="h-6 bg-gray-200 rounded mb-3"></div>
                    <div className="h-4 bg-gray-200 rounded mb-4"></div>
                    <div className="h-10 bg-gray-200 rounded"></div>
                  </CardContent>
                </Card>
              ))
            ) : (
              products.map((product) => (
              <Card key={product.id} className="group hover:shadow-2xl transition-all duration-300 border-2 border-cyan-100 shadow-lg overflow-hidden transform hover:scale-105">
                <div className="aspect-video bg-gradient-to-br from-cyan-50 via-blue-50 to-indigo-50 flex items-center justify-center relative overflow-hidden">
                  {product.id === 'prod_10lb' ? (
                    <img 
                      src="https://customer-assets.emergentagent.com/job_cool-cubes/artifacts/gat89bkm_10lbs%20ice%20bags.png"
                      alt="Quick Fix Ice Bags"
                      className="w-full h-full object-contain p-4 group-hover:scale-105 transition-transform duration-300"
                    />
                  ) : (
                    <Package className="h-16 w-16 text-cyan-600" />
                  )}
                  {product.comingSoon && (
                    <Badge className="absolute top-4 right-4 bg-amber-100 text-amber-700">
                      Coming Soon
                    </Badge>
                  )}
                  {product.inStock && (
                    <Badge className="absolute top-4 right-4 bg-green-100 text-green-700">
                      In Stock
                    </Badge>
                  )}
                </div>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-xl font-semibold text-gray-900">{product.name}</h3>
                    {product.inStock && (
                      <span className="text-2xl font-bold text-cyan-600">${product.price}</span>
                    )}
                  </div>
                  <p className="text-gray-600 mb-4">{product.description}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {product.features.slice(0, 2).map((feature, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {feature}
                      </Badge>
                    ))}
                  </div>
                  {product.inStock ? (
                    <Link to="/quote">
                      <Button 
                        className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white"
                    >
                      Order Now
                    </Button>
                    </Link>
                  ) : (
                    <Button 
                      className="w-full bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white"
                      onClick={() => handleNotifyClick(product)}
                    >
                      <Bell className="mr-2 h-4 w-4" />
                      Notify When Available
                    </Button>
                  )}
                </CardContent>
              </Card>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              What Our Customers Say
            </h2>
            <p className="text-lg text-gray-600">
              Don't just take our word for it - hear from our satisfied customers
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {mockData.testimonials.map((testimonial) => (
              <Card key={testimonial.id} className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
                <CardContent className="p-6">
                  <div className="flex items-center mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <p className="text-gray-600 italic mb-4 leading-relaxed">"{testimonial.review}"</p>
                  <div className="border-t border-gray-100 pt-4">
                    <div className="font-semibold text-gray-900">{testimonial.name}</div>
                    <div className="text-sm text-gray-600">
                      {testimonial.title}
                      {testimonial.company && (
                        <span>, {testimonial.company}</span>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section - Happy Customers, Fast Delivery, Customer Rating */}
      <section className="py-16 bg-gradient-to-br from-gray-50 to-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-cyan-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
              Our Track Record
            </h2>
            <p className="text-lg text-gray-700 max-w-2xl mx-auto font-medium">
              Numbers that speak for themselves
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center p-8 bg-gradient-to-br from-white to-cyan-50 rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 border-2 border-cyan-200">
              <div className="text-5xl font-bold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent mb-2">1000+</div>
              <div className="text-lg text-gray-700 font-medium">Happy Customers</div>
              <p className="text-sm text-gray-600 mt-2">Serving businesses across Kingston</p>
            </div>
            <div className="text-center p-8 bg-gradient-to-br from-white to-blue-50 rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 border-2 border-blue-200">
              <div className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2">2-Hour</div>
              <div className="text-lg text-gray-700 font-medium">Fast Delivery</div>
              <p className="text-sm text-gray-600 mt-2">Same-day service available</p>
            </div>
            <div className="text-center p-8 bg-gradient-to-br from-white to-yellow-50 rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 border-2 border-yellow-200">
              <div className="text-5xl font-bold bg-gradient-to-r from-yellow-600 to-orange-600 bg-clip-text text-transparent mb-2">4.9★</div>
              <div className="text-lg text-gray-700 font-medium">Customer Rating</div>
              <p className="text-sm text-gray-600 mt-2">Based on 500+ reviews</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-br from-cyan-600 via-blue-600 to-slate-700 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_30%,rgba(255,255,255,0.1),transparent_50%)] pointer-events-none"></div>
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center space-y-6">
            <h2 className="text-3xl lg:text-4xl font-bold">
              Ready to Cool Down Your Event?
            </h2>
            <p className="text-xl opacity-90 max-w-2xl mx-auto">
              Get crystal-clear ice delivered to your door today. Same-day delivery available for orders placed before 2 PM.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/quote">
                <Button 
                  size="lg" 
                  className="bg-white text-cyan-600 hover:bg-gray-50 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                >
                  <Truck className="mr-2 h-5 w-5" />
                  Get Your Quote Now
                </Button>
              </Link>
              <Link to="tel:(876)490-7208">
                <Button 
                  variant="outline" 
                  size="lg"
                  className="border-2 border-white text-white hover:bg-white hover:text-cyan-600 transition-all duration-300"
                >
                  <Phone className="mr-2 h-5 w-5" />
                  Call (876) 490-7208
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      <Footer />

      {/* Notification Dialog */}
      {showNotifyDialog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-md w-full">
            <CardContent className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-2">
                  <Bell className="h-5 w-5 text-cyan-600" />
                  <h3 className="text-lg font-semibold">Get Notified</h3>
                </div>
                <button
                  onClick={() => setShowNotifyDialog(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              <form onSubmit={handleNotifySubmit} className="space-y-4">
                <p className="text-gray-600">
                  We'll send you an email when the <strong>{notifyProduct?.name}</strong> become available.
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

export default HomePage;