import React from 'react';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Card, CardContent } from '../components/ui/card';
import { FileText } from 'lucide-react';

const TermsConditionsPage = () => {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <div className="inline-block p-3 bg-cyan-100 rounded-full">
              <FileText className="h-8 w-8 text-cyan-600" />
            </div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Terms & Conditions
            </h1>
            <p className="text-lg text-gray-600">
              Last updated: {new Date().toLocaleDateString()}
            </p>
          </div>
        </div>
      </section>

      {/* Terms Content */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <Card>
              <CardContent className="p-8 space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Acceptance of Terms</h2>
                  <p className="text-gray-600">
                    By accessing and using Ice Solutions' website and services, you accept and agree to be bound by these Terms and Conditions. If you do not agree, please do not use our services.
                  </p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">2. Services</h2>
                  <p className="text-gray-600 mb-4">
                    Ice Solutions provides premium ice delivery services in Kingston, Jamaica and surrounding areas:
                  </p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>Quick Fix (10lb bags) - restaurant-quality ice (currently available)</li>
                    <li>Party Solution (50lb bags) - coming soon (notification list available)</li>
                    <li>Mega Solution (100lb bags) - coming soon (notification list available)</li>
                    <li>Same-day delivery (order at least 2 hours in advance)</li>
                    <li>FREE delivery in Washington Gardens area</li>
                    <li>JMD $300 delivery fee for other areas</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Orders and Payment</h2>
                  <p className="text-gray-600 mb-4"><strong>Order Placement:</strong></p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>Orders can be placed through our website or by phone</li>
                    <li>Order confirmation will be sent via email</li>
                    <li>We reserve the right to refuse or cancel orders</li>
                  </ul>
                  <p className="text-gray-600 mb-4 mt-4"><strong>Payment:</strong></p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>Payment is processed securely through Stripe</li>
                    <li>We accept major credit and debit cards</li>
                    <li>Payment must be completed before delivery</li>
                    <li>Prices are in Jamaican Dollars (JMD)</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Delivery</h2>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>Same-day delivery available for orders placed at least 2 hours in advance</li>
                    <li>Delivery times: Mon-Sun, 7AM - 9PM</li>
                    <li>FREE delivery in Washington Gardens</li>
                    <li>JMD $300 delivery fee for other Kingston areas</li>
                    <li>Delivery address must be provided at checkout</li>
                    <li>Customer must be available to receive delivery</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Pricing and Discounts</h2>
                  <p className="text-gray-600 mb-4"><strong>Standard Pricing:</strong></p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>Quick Fix (10lb): JMD $350 per bag</li>
                  </ul>
                  <p className="text-gray-600 mb-4 mt-4"><strong>Bulk Discounts (automatic):</strong></p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>5-9 bags: 5% discount</li>
                    <li>10-19 bags: 10% discount</li>
                    <li>20+ bags: 15% discount</li>
                  </ul>
                  <p className="text-gray-600 mt-4">
                    Prices are subject to change. The price at the time of order placement will apply.
                  </p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Product Quality</h2>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>We provide crystal-clear, restaurant-quality ice</li>
                    <li>Ice is made from purified water</li>
                    <li>Each bag contains 10 pounds of ice cubes</li>
                    <li>Quality is guaranteed at time of delivery</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Cancellation and Refunds</h2>
                  <p className="text-gray-600 mb-4">Please see our <a href="/refund-policy" className="text-cyan-600 hover:underline">Refund Policy</a> for detailed information.</p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>Cancellations accepted up to 1 hour before scheduled delivery</li>
                    <li>Refunds processed within 5-7 business days</li>
                    <li>Quality issues must be reported within 24 hours</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Limitation of Liability</h2>
                  <p className="text-gray-600">
                    Ice Solutions is not liable for any indirect, incidental, or consequential damages. Our liability is limited to the total amount paid for your order. We are not responsible for delays due to weather, traffic, or circumstances beyond our control.
                  </p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">9. Intellectual Property</h2>
                  <p className="text-gray-600">
                    All content on this website, including text, images, logos, and design, is the property of Ice Solutions and protected by copyright laws. You may not use our content without written permission.
                  </p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">10. Governing Law</h2>
                  <p className="text-gray-600">
                    These Terms and Conditions are governed by the laws of Jamaica. Any disputes will be resolved in the courts of Jamaica.
                  </p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">11. Changes to Terms</h2>
                  <p className="text-gray-600">
                    We reserve the right to modify these terms at any time. Changes will be posted on this page with an updated date. Continued use of our services after changes constitutes acceptance.
                  </p>
                </div>

                <div className="bg-cyan-50 border-l-4 border-cyan-600 p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Questions?</h3>
                  <p className="text-gray-600 mb-4">
                    If you have questions about these Terms and Conditions:
                  </p>
                  <div className="space-y-2 text-gray-600">
                    <p><strong>Email:</strong> <a href="mailto:icesolutions.mybusiness@gmail.com" className="text-cyan-600 hover:underline">icesolutions.mybusiness@gmail.com</a></p>
                    <p><strong>Phone:</strong> <a href="tel:+18764907208" className="text-cyan-600 hover:underline">(876) 490-7208</a></p>
                    <p><strong>Address:</strong> Rosend Avenue, Washington Gardens, Kingston 20, Jamaica</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default TermsConditionsPage;
