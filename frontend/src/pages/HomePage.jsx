import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
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
  Zap
} from 'lucide-react';
import { mockData } from '../data/mock';
import { apiService } from '../services/api';
import { toast } from 'sonner';

const HomePage = () => {
  const [hoveredService, setHoveredService] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

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
      
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-white to-cyan-50">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(6,182,212,0.1),transparent_50%)] pointer-events-none"></div>
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-24">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            
            {/* Content */}
            <div className="space-y-8">
              <div className="space-y-4">
                <Badge className="bg-cyan-100 text-cyan-700 hover:bg-cyan-200 transition-colors">
                  <Zap className="mr-1 h-3 w-3" />
                  Same-Day Delivery Available
                </Badge>
                <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight">
                  Premium
                  <span className="bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent"> Ice Delivery </span>
                  for Every Event
                </h1>
                <div className="text-2xl lg:text-3xl font-bold text-cyan-600 mb-4">
                  "More Ice = More Vibes"
                </div>
                <p className="text-xl text-gray-600 leading-relaxed">
                  Crystal-clear, restaurant-quality ice delivered fresh to your door. 
                  Perfect for parties, events, restaurants, and bars.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/quote">
                  <Button 
                    size="lg" 
                    className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                  >
                    <Truck className="mr-2 h-5 w-5" />
                    Order Ice Now
                  </Button>
                </Link>
                <Link to="/products">
                  <Button 
                    variant="outline" 
                    size="lg"
                    className="border-2 border-cyan-500 text-cyan-600 hover:bg-cyan-50 transition-all duration-300"
                  >
                    View Products
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-3 gap-4 pt-8 border-t border-gray-200">
                <div className="text-center">
                  <div className="text-2xl font-bold text-cyan-600">1000+</div>
                  <div className="text-sm text-gray-600">Happy Customers</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-cyan-600">2-Hour</div>
                  <div className="text-sm text-gray-600">Fast Delivery</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-cyan-600">4.9★</div>
                  <div className="text-sm text-gray-600">Customer Rating</div>
                </div>
              </div>
            </div>

            {/* Visual Element */}
            <div className="relative">
              <div className="relative z-10 bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold text-gray-900">Quick Order</h3>
                    <Badge className="bg-green-100 text-green-700">Available Now</Badge>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-cyan-100 to-blue-100 rounded-lg flex items-center justify-center">
                        <Package className="h-6 w-6 text-cyan-600" />
                      </div>
                      <div>
                        <div className="font-medium text-gray-900">10lb Party Ice Bag</div>
                        <div className="text-sm text-gray-600">Crystal clear, restaurant quality</div>
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
              
              {/* Decorative Elements */}
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full opacity-20 blur-xl"></div>
              <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-gradient-to-br from-blue-400 to-cyan-500 rounded-full opacity-15 blur-xl"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Why Choose Ice Solutions?
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
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

              return (
                <Card 
                  key={service.id}
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
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Products Preview */}
      <section className="py-16 bg-gradient-to-br from-gray-50 to-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Our Ice Products
            </h2>
            <p className="text-lg text-gray-600">
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
              <Card key={product.id} className="group hover:shadow-xl transition-all duration-300 border-0 shadow-md overflow-hidden">
                <div className="aspect-video bg-gradient-to-br from-gray-50 to-white flex items-center justify-center relative overflow-hidden">
                  {product.id === 'prod_10lb' ? (
                    <img 
                      src="https://customer-assets.emergentagent.com/job_cool-cubes/artifacts/gat89bkm_10lbs%20ice%20bags.png"
                      alt="10lb Ice Bags"
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
                    <span className="text-2xl font-bold text-cyan-600">${product.price}</span>
                  </div>
                  <p className="text-gray-600 mb-4">{product.description}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {product.features.slice(0, 2).map((feature, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {feature}
                      </Badge>
                    ))}
                  </div>
                  <Link to={product.inStock ? "/quote" : "/products"}>
                    <Button 
                      className={`w-full ${
                        product.inStock 
                          ? 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white'
                          : 'bg-gray-200 text-gray-500 cursor-not-allowed'
                      }`}
                      disabled={!product.inStock}
                    >
                      {product.inStock ? 'Order Now' : 'Notify When Available'}
                    </Button>
                  </Link>
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
    </div>
  );
};

export default HomePage;