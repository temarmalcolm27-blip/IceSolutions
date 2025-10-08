import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { 
  Phone, 
  Mail, 
  MapPin, 
  Clock, 
  MessageCircle,
  Truck,
  Calendar,
  Star
} from 'lucide-react';
import { mockData } from '../data/mock';
import { toast } from 'sonner';

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: '',
    contactMethod: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const contactMethods = [
    'General Inquiry',
    'Quote Request', 
    'Order Support',
    'Delivery Issue',
    'Partnership Opportunity',
    'Other'
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Mock submission
    setTimeout(() => {
      toast.success("Message sent successfully! We'll respond within 2 hours.");
      setIsLoading(false);
      setFormData({
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: '',
        contactMethod: ''
      });
    }, 1000);
  };

  const contactInfo = [
    {
      icon: Phone,
      title: 'Phone',
      details: '(876) 490-7208',
      description: 'Mon-Sun: 7AM - 9PM',
      action: () => window.open('tel:(555)123-ICE1')
    },
    {
      icon: Mail,
      title: 'Email',
      details: 'orders@icesolutions.com',
      description: 'We respond within 2 hours',
      action: () => window.open('mailto:orders@icesolutions.com')
    },
    {
      icon: MapPin,
      title: 'Location',
      details: '123 Ice Street, Cool City, CC 12345',
      description: 'Delivery & pickup available',
      action: () => window.open('https://maps.google.com/?q=123+Ice+Street+Cool+City+CC+12345')
    }
  ];

  const businessHours = [
    { day: 'Monday - Friday', hours: '7:00 AM - 9:00 PM', available: true },
    { day: 'Saturday', hours: '8:00 AM - 8:00 PM', available: true },
    { day: 'Sunday', hours: '9:00 AM - 7:00 PM', available: true }
  ];

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-6">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Contact Ice Solutions
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Have questions about our ice delivery service? Need a custom quote? 
              Our friendly team is here to help make your event a success.
            </p>
            <div className="flex flex-wrap justify-center gap-6 pt-4">
              <div className="flex items-center text-gray-600">
                <Clock className="h-5 w-5 mr-2 text-cyan-600" />
                <span>Response within 2 hours</span>
              </div>
              <div className="flex items-center text-gray-600">
                <Truck className="h-5 w-5 mr-2 text-cyan-600" />
                <span>Same-day delivery available</span>
              </div>
              <div className="flex items-center text-gray-600">
                <Star className="h-5 w-5 mr-2 text-cyan-600" />
                <span>4.9/5 customer rating</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            
            {/* Contact Form */}
            <div className="space-y-8">
              <Card className="border-0 shadow-xl">
                <CardHeader>
                  <CardTitle className="text-2xl text-gray-900 flex items-center">
                    <MessageCircle className="mr-2 h-6 w-6 text-cyan-600" />
                    Send Us a Message
                  </CardTitle>
                  <p className="text-gray-600">
                    Fill out the form below and we'll get back to you as soon as possible.
                  </p>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    
                    {/* Contact Details */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="name">Full Name *</Label>
                        <Input
                          id="name"
                          value={formData.name}
                          onChange={(e) => handleInputChange('name', e.target.value)}
                          placeholder="Your full name"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="phone">Phone Number</Label>
                        <Input
                          id="phone"
                          type="tel"
                          value={formData.phone}
                          onChange={(e) => handleInputChange('phone', e.target.value)}
                          placeholder="(555) 123-4567"
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="email">Email Address *</Label>
                      <Input
                        id="email"
                        type="email"
                        value={formData.email}
                        onChange={(e) => handleInputChange('email', e.target.value)}
                        placeholder="your@email.com"
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label>Inquiry Type</Label>
                      <Select onValueChange={(value) => handleInputChange('contactMethod', value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="What can we help you with?" />
                        </SelectTrigger>
                        <SelectContent>
                          {contactMethods.map((method) => (
                            <SelectItem key={method} value={method}>
                              {method}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="subject">Subject *</Label>
                      <Input
                        id="subject"
                        value={formData.subject}
                        onChange={(e) => handleInputChange('subject', e.target.value)}
                        placeholder="Brief description of your inquiry"
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="message">Message *</Label>
                      <Textarea
                        id="message"
                        value={formData.message}
                        onChange={(e) => handleInputChange('message', e.target.value)}
                        placeholder="Tell us more about your ice delivery needs, event details, or any questions you have..."
                        rows={5}
                        required
                      />
                    </div>

                    <Button
                      type="submit"
                      className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white"
                      disabled={isLoading || !formData.name || !formData.email || !formData.subject || !formData.message}
                    >
                      {isLoading ? 'Sending Message...' : 'Send Message'}
                    </Button>

                    <p className="text-sm text-gray-600 text-center">
                      By submitting this form, you agree to be contacted by our team regarding your inquiry.
                    </p>
                  </form>
                </CardContent>
              </Card>
            </div>

            {/* Contact Information */}
            <div className="space-y-8">
              
              {/* Contact Methods */}
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900">Get in Touch</h2>
                {contactInfo.map((contact, index) => {
                  const IconComponent = contact.icon;
                  return (
                    <Card 
                      key={index}
                      className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer group"
                      onClick={contact.action}
                    >
                      <CardContent className="p-6">
                        <div className="flex items-start space-x-4">
                          <div className="w-12 h-12 bg-gradient-to-br from-cyan-100 to-blue-100 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:from-cyan-500 group-hover:to-blue-600 transition-all duration-300">
                            <IconComponent className="h-6 w-6 text-cyan-600 group-hover:text-white transition-colors duration-300" />
                          </div>
                          <div className="flex-1">
                            <h3 className="text-lg font-semibold text-gray-900 mb-1">{contact.title}</h3>
                            <div className="text-cyan-600 font-medium mb-1">{contact.details}</div>
                            <p className="text-gray-600 text-sm">{contact.description}</p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>

              {/* Business Hours */}
              <Card className="border-0 shadow-xl">
                <CardHeader>
                  <CardTitle className="text-xl text-gray-900 flex items-center">
                    <Clock className="mr-2 h-5 w-5 text-cyan-600" />
                    Business Hours
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {businessHours.map((schedule, index) => (
                      <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                        <span className="font-medium text-gray-900">{schedule.day}</span>
                        <div className="text-right">
                          <div className="text-gray-600">{schedule.hours}</div>
                          {schedule.available && (
                            <div className="text-xs text-green-600 font-medium">Available for delivery</div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 p-3 bg-cyan-50 rounded-lg border border-cyan-200">
                    <p className="text-sm text-cyan-700">
                      <strong>Emergency Orders:</strong> Call us anytime for urgent ice delivery needs. 
                      Additional fees may apply for after-hours service.
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Quick Actions */}
              <Card className="border-0 shadow-xl bg-gradient-to-br from-slate-900 to-blue-900 text-white">
                <CardContent className="p-6 space-y-6">
                  <div className="text-center space-y-2">
                    <h3 className="text-xl font-semibold">Need Ice Right Now?</h3>
                    <p className="text-gray-300">
                      For immediate assistance or same-day delivery requests
                    </p>
                  </div>
                  
                  <div className="space-y-3">
                    <Button 
                      className="w-full bg-white text-gray-900 hover:bg-gray-100"
                      onClick={() => window.open('tel:(555)123-ICE1')}
                    >
                      <Phone className="mr-2 h-4 w-4" />
                      Call (876) 490-7208
                    </Button>
                    
                    <Button 
                      variant="outline" 
                      className="w-full border-white text-white hover:bg-white hover:text-gray-900"
                      onClick={() => window.location.href = '/quote'}
                    >
                      <Calendar className="mr-2 h-4 w-4" />
                      Get Quick Quote
                    </Button>
                  </div>

                  <div className="text-center pt-4 border-t border-gray-600">
                    <p className="text-sm text-gray-300">
                      Average response time: <strong className="text-white">Under 30 minutes</strong>
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* FAQ Preview */}
              <Card className="border-0 shadow-xl">
                <CardHeader>
                  <CardTitle className="text-xl text-gray-900">Quick Answers</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium text-gray-900 mb-1">How far in advance should I order?</h4>
                      <p className="text-sm text-gray-600">Same-day delivery available if ordered before 2 PM. We recommend 24-48 hours notice for large events.</p>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-1">What's your delivery area?</h4>
                      <p className="text-sm text-gray-600">We serve downtown and surrounding areas. Free delivery within 5 miles, delivery fees apply beyond.</p>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 mb-1">Do you offer bulk discounts?</h4>
                      <p className="text-sm text-gray-600">Yes! 5% off orders of 5+ bags, 10% off 10+ bags, and custom pricing for 20+ bags.</p>
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

export default ContactPage;