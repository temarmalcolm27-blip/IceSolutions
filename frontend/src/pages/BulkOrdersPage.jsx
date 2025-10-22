import React from 'react';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Package, CheckCircle, TrendingDown, Phone, Mail } from 'lucide-react';
import { Link } from 'react-router-dom';

const BulkOrdersPage = () => {
  const pricingTiers = [
    {
      range: "1-14 Bags",
      rangeParam: "1-14",
      quantity: 14,
      discount: "0%",
      discountPercent: 0,
      pricePerBag: "JMD $350.00",
      totalExample: "JMD $4,900.00 (14 bags)",
      badgeColor: "bg-gray-100 text-gray-700",
      recommended: false
    },
    {
      range: "15+ Bags",
      rangeParam: "15+",
      quantity: 20,
      discount: "10%",
      discountPercent: 10,
      pricePerBag: "JMD $315.00",
      totalExample: "JMD $6,300.00 (20 bags)",
      savings: "Save JMD $700.00",
      badgeColor: "bg-cyan-100 text-cyan-700",
      recommended: true,
      freeDelivery: true
    }
  ];

  const benefits = [
    "Automatic discounts applied at checkout",
    "Priority delivery scheduling",
    "Dedicated account manager for 20+ bag orders",
    "Flexible payment terms for recurring orders",
    "Same-day delivery for orders placed before 2PM",
    "Quality guarantee on all ice products"
  ];

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-6 max-w-3xl mx-auto">
            <div className="inline-block p-3 bg-cyan-100 rounded-full">
              <Package className="h-8 w-8 text-cyan-600" />
            </div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Bulk Order Pricing
            </h1>
            <p className="text-xl text-gray-600">
              Save more when you order more! Special pricing for large orders and recurring deliveries.
            </p>
          </div>
        </div>
      </section>

      {/* Pricing Tiers */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Volume Discount Pricing</h2>
            <p className="text-lg text-gray-600">The more you order, the more you save</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {pricingTiers.map((tier, index) => (
              <Card 
                key={index}
                className={`relative hover:shadow-xl transition-all duration-300 ${
                  tier.recommended ? 'border-2 border-cyan-500 shadow-lg scale-105' : 'border-gray-200'
                }`}
              >
                {tier.recommended && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <Badge className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-4 py-1">
                      Most Popular
                    </Badge>
                  </div>
                )}
                
                <CardHeader className="text-center pb-4">
                  <div className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${tier.badgeColor} mb-3`}>
                    {tier.discount} OFF
                  </div>
                  <CardTitle className="text-2xl mb-2">{tier.range}</CardTitle>
                  <div className="text-3xl font-bold text-cyan-600">{tier.pricePerBag}</div>
                  <div className="text-sm text-gray-500">per bag</div>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div className="pt-4 border-t border-gray-100">
                    <div className="text-sm text-gray-600 mb-1">Example Total:</div>
                    <div className="text-lg font-semibold text-gray-900">{tier.totalExample}</div>
                  </div>

                  {tier.savings && (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                      <div className="flex items-center gap-2 text-green-700">
                        <TrendingDown className="h-4 w-4" />
                        <span className="text-sm font-medium">{tier.savings}</span>
                      </div>
                    </div>
                  )}

                  <Link to={`/bulk-order-form?tier=${tier.rangeParam}&quantity=${tier.quantity}&discount=${tier.discountPercent}`}>
                    <Button 
                      className={`w-full ${
                        tier.recommended 
                          ? 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700' 
                          : 'bg-gray-900 hover:bg-gray-800'
                      }`}
                    >
                      Order Now
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Benefits Section */}
          <div className="mt-16">
            <Card className="bg-gradient-to-br from-cyan-50 to-blue-50">
              <CardHeader>
                <CardTitle className="text-center text-2xl">Bulk Order Benefits</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {benefits.map((benefit, index) => (
                    <div key={index} className="flex items-start gap-3">
                      <CheckCircle className="h-5 w-5 text-cyan-600 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{benefit}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Calculation Example */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Savings Breakdown</h2>
            
            <Card>
              <CardContent className="p-8">
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
                    <div>
                      <div className="text-4xl font-bold text-gray-900 mb-2">5-9</div>
                      <div className="text-sm text-gray-600 mb-3">Bags</div>
                      <Badge className="bg-blue-100 text-blue-700">5% Discount</Badge>
                      <div className="mt-4 text-2xl font-bold text-blue-600">Save $17.50+</div>
                    </div>
                    
                    <div className="md:border-x border-gray-200">
                      <div className="text-4xl font-bold text-gray-900 mb-2">10-19</div>
                      <div className="text-sm text-gray-600 mb-3">Bags</div>
                      <Badge className="bg-cyan-100 text-cyan-700">10% Discount</Badge>
                      <div className="mt-4 text-2xl font-bold text-cyan-600">Save $350+</div>
                    </div>
                    
                    <div>
                      <div className="text-4xl font-bold text-gray-900 mb-2">20+</div>
                      <div className="text-sm text-gray-600 mb-3">Bags</div>
                      <Badge className="bg-green-100 text-green-700">15% Discount</Badge>
                      <div className="mt-4 text-2xl font-bold text-green-600">Save $1,050+</div>
                    </div>
                  </div>

                  <div className="pt-6 border-t border-gray-200">
                    <p className="text-center text-gray-600">
                      Discounts automatically applied at checkout. No coupon code needed!
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-br from-cyan-500 to-blue-600">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto text-center text-white space-y-6">
            <h2 className="text-3xl lg:text-4xl font-bold">Ready to Place Your Bulk Order?</h2>
            <p className="text-xl text-cyan-50">
              Get started now or contact us for custom pricing on recurring orders
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
              <Link to="/quote">
                <Button size="lg" className="bg-white text-cyan-600 hover:bg-gray-50">
                  <Package className="mr-2 h-5 w-5" />
                  Place Order Now
                </Button>
              </Link>
              
              <a href="tel:+18764907208">
                <Button size="lg" variant="outline" className="border-2 border-white text-white hover:bg-white/10">
                  <Phone className="mr-2 h-5 w-5" />
                  Call (876) 490-7208
                </Button>
              </a>
            </div>

            <div className="pt-6">
              <div className="flex items-center justify-center gap-2 text-cyan-50">
                <Mail className="h-4 w-4" />
                <span>orders@icesolutions.com</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default BulkOrdersPage;
