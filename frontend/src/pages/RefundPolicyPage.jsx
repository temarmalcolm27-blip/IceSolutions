import React from 'react';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Card, CardContent } from '../components/ui/card';
import { RefreshCw } from 'lucide-react';

const RefundPolicyPage = () => {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <div className="inline-block p-3 bg-cyan-100 rounded-full">
              <RefreshCw className="h-8 w-8 text-cyan-600" />
            </div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">Refund Policy</h1>
            <p className="text-lg text-gray-600">Last updated: {new Date().toLocaleDateString()}</p>
          </div>
        </div>
      </section>

      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <Card>
              <CardContent className="p-8 space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">100% Satisfaction Guarantee</h2>
                  <p className="text-gray-600">At Ice Solutions, we're committed to delivering the highest quality ice. If you're not completely satisfied, we'll make it right.</p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Cancellation Policy</h2>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li><strong>Before Delivery:</strong> Cancel up to 1 hour before scheduled delivery for a full refund</li>
                    <li><strong>How to Cancel:</strong> Call (876) 490-7208 or email icesolutions.mybusiness@gmail.com</li>
                    <li><strong>Refund Timeline:</strong> Refunds processed within 5-7 business days to original payment method</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Quality Issues</h2>
                  <p className="text-gray-600 mb-4">If there's an issue with your ice quality:</p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li><strong>Report Within:</strong> 24 hours of delivery</li>
                    <li><strong>Contact Method:</strong> Call (876) 490-7208 with your order number</li>
                    <li><strong>Resolution:</strong> We'll offer a replacement delivery or full refund</li>
                    <li><strong>No Returns Needed:</strong> Keep the ice, we trust your feedback</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Delivery Issues</h2>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li><strong>Late Delivery:</strong> If we're more than 30 minutes late, contact us for compensation</li>
                    <li><strong>Wrong Amount:</strong> We'll deliver the difference immediately at no charge</li>
                    <li><strong>Wrong Product:</strong> If we delivered the wrong product size (e.g., different bag size than ordered)</li>
                    <li><strong>Non-Delivery:</strong> Full refund if we fail to deliver</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Non-Refundable Items</h2>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>Orders cancelled less than 1 hour before delivery</li>
                    <li>Customer unavailable at delivery address (reschedule fee may apply)</li>
                    <li>Ice that has melted due to improper storage after delivery</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Refund Process</h2>
                  <ol className="list-decimal pl-6 space-y-2 text-gray-600">
                    <li>Contact us via phone or email</li>
                    <li>Provide your order number and reason for refund</li>
                    <li>We'll review and approve eligible refunds within 24 hours</li>
                    <li>Refund processed to original payment method</li>
                    <li>Bank processing may take 5-7 business days</li>
                  </ol>
                </div>

                <div className="bg-cyan-50 border-l-4 border-cyan-600 p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Need a Refund?</h3>
                  <p className="text-gray-600 mb-4">Contact us immediately:</p>
                  <div className="space-y-2 text-gray-600">
                    <p><strong>Phone:</strong> <a href="tel:+18764907208" className="text-cyan-600 hover:underline">(876) 490-7208</a> (Fastest)</p>
                    <p><strong>Email:</strong> <a href="mailto:icesolutions.mybusiness@gmail.com" className="text-cyan-600 hover:underline">icesolutions.mybusiness@gmail.com</a></p>
                    <p className="text-sm mt-4">We're here to help! Your satisfaction is our priority.</p>
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

export default RefundPolicyPage;