import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { CheckCircle, Package, Clock, Phone } from 'lucide-react';
import { apiService } from '../services/api';

const OrderConfirmationPage = () => {
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');
  const [loading, setLoading] = useState(true);
  const [paymentStatus, setPaymentStatus] = useState(null);
  const [pollCount, setPollCount] = useState(0);

  useEffect(() => {
    if (!sessionId) {
      setLoading(false);
      return;
    }

    // Poll for payment status
    const pollPaymentStatus = async (attempts = 0) => {
      const maxAttempts = 5;
      
      if (attempts >= maxAttempts) {
        setLoading(false);
        return;
      }

      try {
        const status = await apiService.getCheckoutStatus(sessionId);
        setPaymentStatus(status);

        if (status.payment_status === 'paid') {
          setLoading(false);
          return;
        } else if (status.status === 'expired') {
          setLoading(false);
          return;
        }

        // Continue polling
        setPollCount(attempts + 1);
        setTimeout(() => pollPaymentStatus(attempts + 1), 2000);
      } catch (error) {
        console.error('Error checking payment status:', error);
        setLoading(false);
      }
    };

    pollPaymentStatus();
  }, [sessionId]);

  if (!sessionId) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <RunningBanner />
        
        <section className="py-16">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-2xl mx-auto text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                No Order Found
              </h1>
              <p className="text-gray-600 mb-8">
                We couldn't find your order. Please try placing a new order.
              </p>
              <Link to="/quote">
                <Button className="bg-gradient-to-r from-cyan-500 to-blue-600">
                  Place New Order
                </Button>
              </Link>
            </div>
          </div>
        </section>

        <Footer />
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <RunningBanner />
        
        <section className="py-16">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-2xl mx-auto text-center">
              <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-cyan-600 mx-auto mb-6"></div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Processing Your Payment...
              </h2>
              <p className="text-gray-600">
                Please wait while we confirm your order
              </p>
            </div>
          </div>
        </section>

        <Footer />
      </div>
    );
  }

  const isSuccess = paymentStatus?.payment_status === 'paid';

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Success Section */}
      {isSuccess ? (
        <section className="py-16 bg-gradient-to-br from-green-50 via-white to-cyan-50">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
              <div className="text-center mb-12">
                <div className="inline-block p-4 bg-green-100 rounded-full mb-6">
                  <CheckCircle className="h-16 w-16 text-green-600" />
                </div>
                <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-4">
                  Order Confirmed!
                </h1>
                <p className="text-xl text-gray-600">
                  Thank you for your order. We'll deliver your ice soon!
                </p>
              </div>

              <Card className="mb-8">
                <CardContent className="p-8">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 mb-2">Order ID</h3>
                      <p className="text-lg font-semibold text-gray-900">{sessionId.substring(0, 16)}...</p>
                    </div>
                    <div>
                      <h3 className="text-sm font-medium text-gray-500 mb-2">Total Amount</h3>
                      <p className="text-lg font-semibold text-cyan-600">
                        JMD ${(paymentStatus?.amount_total / 100).toFixed(2)}
                      </p>
                    </div>
                  </div>

                  <div className="border-t border-gray-200 pt-8">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">What Happens Next?</h3>
                    <div className="space-y-4">
                      <div className="flex items-start gap-3">
                        <div className="flex-shrink-0 w-8 h-8 bg-cyan-100 rounded-full flex items-center justify-center">
                          <span className="text-cyan-600 font-semibold">1</span>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">Order Processing</h4>
                          <p className="text-sm text-gray-600">We're preparing your ice order right now</p>
                        </div>
                      </div>

                      <div className="flex items-start gap-3">
                        <div className="flex-shrink-0 w-8 h-8 bg-cyan-100 rounded-full flex items-center justify-center">
                          <span className="text-cyan-600 font-semibold">2</span>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">Quality Check</h4>
                          <p className="text-sm text-gray-600">Crystal-clear ice packed and ready for delivery</p>
                        </div>
                      </div>

                      <div className="flex items-start gap-3">
                        <div className="flex-shrink-0 w-8 h-8 bg-cyan-100 rounded-full flex items-center justify-center">
                          <span className="text-cyan-600 font-semibold">3</span>
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">Same-Day Delivery</h4>
                          <p className="text-sm text-gray-600">Your ice will arrive within 2-4 hours</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="text-center p-6">
                  <Package className="h-10 w-10 text-cyan-600 mx-auto mb-3" />
                  <h4 className="font-semibold mb-1">Quality Guarantee</h4>
                  <p className="text-sm text-gray-600">100% satisfaction guaranteed</p>
                </Card>

                <Card className="text-center p-6">
                  <Clock className="h-10 w-10 text-cyan-600 mx-auto mb-3" />
                  <h4 className="font-semibold mb-1">Fast Delivery</h4>
                  <p className="text-sm text-gray-600">Same-day service available</p>
                </Card>

                <Card className="text-center p-6">
                  <Phone className="h-10 w-10 text-cyan-600 mx-auto mb-3" />
                  <h4 className="font-semibold mb-1">Need Help?</h4>
                  <p className="text-sm text-gray-600">(876) 490-7208</p>
                </Card>
              </div>

              <div className="text-center mt-8">
                <Link to="/">
                  <Button variant="outline" className="mr-4">
                    Return Home
                  </Button>
                </Link>
                <Link to="/quote">
                  <Button className="bg-gradient-to-r from-cyan-500 to-blue-600">
                    Place Another Order
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </section>
      ) : (
        <section className="py-16 bg-gradient-to-br from-red-50 via-white to-orange-50">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-2xl mx-auto text-center">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Payment {paymentStatus?.status === 'expired' ? 'Expired' : 'Pending'}
              </h1>
              <p className="text-gray-600 mb-8">
                {paymentStatus?.status === 'expired' 
                  ? 'Your payment session has expired. Please try placing your order again.' 
                  : 'Your payment is still being processed. Please check back in a moment.'}
              </p>
              <Link to="/quote">
                <Button className="bg-gradient-to-r from-cyan-500 to-blue-600">
                  Try Again
                </Button>
              </Link>
            </div>
          </div>
        </section>
      )}

      <Footer />
    </div>
  );
};

export default OrderConfirmationPage;
