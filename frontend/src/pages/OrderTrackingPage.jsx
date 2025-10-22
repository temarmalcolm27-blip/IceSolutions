import React, { useState } from 'react';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Package, Search, CheckCircle, Clock, Truck } from 'lucide-react';
import { apiService } from '../services/api';
import { toast } from 'sonner';

const OrderTrackingPage = () => {
  const [orderId, setOrderId] = useState('');
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const orderData = await apiService.getOrder(orderId);
      setOrder(orderData);
    } catch (error) {
      console.error('Error fetching order:', error);
      toast.error('Order not found. Please check your order ID.');
      setOrder(null);
    } finally {
      setLoading(false);
    }
  };

  const getStatusInfo = (status) => {
    const normalizedStatus = status?.toLowerCase() || '';
    const statuses = {
      planning: { color: 'text-blue-600', bg: 'bg-blue-100', icon: Clock, text: 'Planning' },
      'in transit': { color: 'text-purple-600', bg: 'bg-purple-100', icon: Truck, text: 'In Transit' },
      delivered: { color: 'text-green-600', bg: 'bg-green-100', icon: CheckCircle, text: 'Delivered' },
      pending: { color: 'text-yellow-600', bg: 'bg-yellow-100', icon: Clock, text: 'Pending' },
      confirmed: { color: 'text-blue-600', bg: 'bg-blue-100', icon: CheckCircle, text: 'Confirmed' },
      in_delivery: { color: 'text-purple-600', bg: 'bg-purple-100', icon: Truck, text: 'Out for Delivery' },
      cancelled: { color: 'text-red-600', bg: 'bg-red-100', icon: Clock, text: 'Cancelled' }
    };
    return statuses[normalizedStatus] || statuses.planning;
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <div className="inline-block p-3 bg-cyan-100 rounded-full">
              <Package className="h-8 w-8 text-cyan-600" />
            </div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">Track Your Order</h1>
            <p className="text-lg text-gray-600">Enter your order ID to check delivery status</p>
          </div>
        </div>
      </section>

      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto">
            <Card>
              <CardContent className="p-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-2">
                    <Label htmlFor="orderId">Order ID</Label>
                    <div className="flex gap-3">
                      <Input
                        id="orderId"
                        type="text"
                        placeholder="Enter your order ID (found in confirmation email)"
                        value={orderId}
                        onChange={(e) => setOrderId(e.target.value)}
                        required
                        className="flex-1"
                      />
                      <Button type="submit" disabled={loading} className="bg-gradient-to-r from-cyan-500 to-blue-600">
                        <Search className="h-4 w-4 mr-2" />
                        {loading ? 'Searching...' : 'Track'}
                      </Button>
                    </div>
                  </div>
                </form>

                {order && (
                  <div className="mt-8 space-y-6">
                    <div className="border-t pt-6">
                      <div className="flex items-center justify-between mb-6">
                        <h3 className="text-2xl font-bold text-gray-900">Order Details</h3>
                        {(() => {
                          const statusInfo = getStatusInfo(order.status || order.order_status);
                          const StatusIcon = statusInfo.icon;
                          return (
                            <div className={`flex items-center gap-2 px-4 py-2 rounded-full ${statusInfo.bg}`}>
                              <StatusIcon className={`h-5 w-5 ${statusInfo.color}`} />
                              <span className={`font-semibold ${statusInfo.color}`}>{statusInfo.text}</span>
                            </div>
                          );
                        })()}
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                        <div>
                          <p className="text-sm text-gray-500">Order ID</p>
                          <p className="font-medium text-gray-900">{order.order_id || order.id}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Order Date</p>
                          <p className="font-medium text-gray-900">{order.order_date || (order.created_at && new Date(order.created_at).toLocaleDateString())}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Customer Name</p>
                          <p className="font-medium text-gray-900">{order.customer_name}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Phone</p>
                          <p className="font-medium text-gray-900">{order.customer_phone}</p>
                        </div>
                      </div>

                      <div className="mb-6">
                        <p className="text-sm text-gray-500">Delivery Address</p>
                        <p className="font-medium text-gray-900">{order.delivery_address}</p>
                      </div>

                      <div className="bg-gray-50 rounded-lg p-4 space-y-3">
                        <div className="flex justify-between">
                          <span className="text-gray-600">{order.quantity || order.bags} x Quick Fix (10lb bags)</span>
                          <span className="font-medium">{order.subtotal}</span>
                        </div>
                        {order.discount && order.discount !== "$0.00" && (
                          <div className="flex justify-between text-green-600">
                            <span>Discount</span>
                            <span>-{order.discount}</span>
                          </div>
                        )}
                        <div className="flex justify-between text-lg font-bold border-t pt-3">
                          <span>Total</span>
                          <span className="text-cyan-600">{order.total}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            <div className="mt-8">
              <Card className="bg-gradient-to-br from-cyan-50 to-blue-50">
                <CardContent className="p-6">
                  <h4 className="font-semibold text-gray-900 mb-3">Need Help?</h4>
                  <p className="text-gray-600 text-sm mb-4">If you have questions about your order:</p>
                  <div className="flex flex-col sm:flex-row gap-3">
                    <a href="tel:+18764907208" className="text-cyan-600 hover:underline font-medium">(876) 490-7208</a>
                    <span className="hidden sm:inline text-gray-300">|</span>
                    <a href="mailto:temarmalcolm27@gmail.com" className="text-cyan-600 hover:underline font-medium">temarmalcolm27@gmail.com</a>
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

export default OrderTrackingPage;
