import React from 'react';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { 
  Shield, 
  Award, 
  Users, 
  Truck, 
  Clock, 
  Star,
  CheckCircle,
  Phone
} from 'lucide-react';
import { Link } from 'react-router-dom';

const AboutPage = () => {
  const stats = [
    { label: 'Happy Customers', value: '1,000+', icon: Users },
    { label: 'Ice Delivered', value: '50,000+ lbs', icon: Truck },
    { label: 'Since', value: '2023', icon: Award },
    { label: 'Average Rating', value: '4.9★', icon: Star }
  ];

  const values = [
    {
      icon: Shield,
      title: 'Quality First',
      description: 'Every bag of ice is made from filtered water and meets restaurant-grade standards. We never compromise on quality.'
    },
    {
      icon: Clock,
      title: 'Reliable Service',
      description: 'When you need ice, we deliver. Same-day service with precise timing you can count on for your events.'
    },
    {
      icon: Users,
      title: 'Customer Focus',
      description: 'Your success is our success. We work closely with event planners, restaurants, and individuals to exceed expectations.'
    },
    {
      icon: Truck,
      title: 'Fast Delivery',
      description: 'Professional delivery team with refrigerated vehicles ensuring your ice arrives fresh and on time.'
    }
  ];

  const team = [
    {
      name: 'Temar Malcolm',
      role: 'Founder & CEO',
      bio: 'Over a decade in customer service and customer relations. Founded Ice Solutions in 2023 to provide affordable, reliable ice delivery across Kingston.',
      image: '/api/placeholder/200/200'
    },
    {
      name: 'Shandale Campbell',
      role: 'Founder & Operations Manager',
      bio: 'Former restaurant and bar manager who understands the critical importance of reliable ice supply for hospitality and events.',
      image: '/api/placeholder/200/200'
    },
    {
      name: 'Marcus Thompson',
      role: 'Delivery Supervisor',
      bio: 'Logistics expert ensuring efficient routes and on-time deliveries across Kingston. Specializes in same-day delivery coordination.',
      image: '/api/placeholder/200/200'
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-6 max-w-4xl mx-auto">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              About Ice Solutions
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed">
              Founded in 2023, Ice Solutions was born from recognizing a real struggle in Washington Gardens, Jamaica — 
              finding party ice that's quick, reliable, and affordable. Based right here in Washington Gardens, we set 
              out to solve this problem by providing crystal-clear, restaurant-quality ice with fast, reliable delivery 
              and bulk discounts. Today, we're proud to serve over 1,000 happy customers across Kingston 20 and the wider 
              Kingston area, keeping vibes cool and celebrations flowing.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Badge className="bg-green-100 text-green-700 px-4 py-2">
                <CheckCircle className="mr-1 h-4 w-4" />
                Family Owned Business
              </Badge>
              <Badge className="bg-blue-100 text-blue-700 px-4 py-2">
                <Shield className="mr-1 h-4 w-4" />
                Licensed & Insured
              </Badge>
              <Badge className="bg-cyan-100 text-cyan-700 px-4 py-2">
                <Award className="mr-1 h-4 w-4" />
                Industry Leading Service
              </Badge>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const IconComponent = stat.icon;
              return (
                <Card key={index} className="text-center border-0 shadow-lg hover:shadow-xl transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-cyan-100 to-blue-100 rounded-full flex items-center justify-center">
                      <IconComponent className="h-8 w-8 text-cyan-600" />
                    </div>
                    <div className="text-3xl font-bold text-gray-900 mb-2">{stat.value}</div>
                    <div className="text-gray-600 font-medium">{stat.label}</div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Our Story */}
      <section className="py-16 bg-gradient-to-br from-gray-50 to-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h2 className="text-3xl lg:text-4xl font-bold text-gray-900">
                Our Story
              </h2>
              <div className="space-y-4 text-gray-600 leading-relaxed">
                <p>
                  In 2023, I realized a real issue in Washington Gardens, Jamaica — finding party ice that's quick, 
                  reliable, and affordable was a major struggle for many of us. Event planners, party hosts, restaurants, 
                  and bars were all facing the same headache: last-minute shortages, inconsistent suppliers, and overpriced 
                  ice making celebrations harder than they should be.
                </p>
                <p>
                  That's why we started IceSolutions, right here in Washington Gardens, Kingston. Our mission is simple: 
                  to make getting ice easy, fast, and affordable. We deliver crystal-clear, restaurant-quality ice, offer 
                  same-day delivery when you order at least two hours in advance, and provide bulk discounts to help you 
                  save more. Best of all, delivery is FREE within Washington Gardens!
                </p>
                <p>
                  Today, we're proud to serve over 1,000 happy customers across Kingston 20 and the wider Kingston area, 
                  from cozy backyard parties and street dances to major events, restaurants, and bars. Every 10lb bag we 
                  deliver is more than just ice; it's our promise to keep your vibes cool and your celebrations flowing.
                </p>
              </div>
              <Link to="/contact">
                <Button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white">
                  Get in Touch
                </Button>
              </Link>
            </div>
            
            {/* Visual Element */}
            <div className="relative">
              <Card className="border-0 shadow-2xl overflow-hidden">
                <div className="aspect-video bg-gradient-to-br from-cyan-200 to-blue-300 flex items-center justify-center">
                  <div className="text-center text-white">
                    <Truck className="h-20 w-20 mx-auto mb-4" />
                    <div className="text-lg font-semibold">Professional Ice Delivery</div>
                    <div className="text-sm opacity-90">Serving Kingston since 2023</div>
                  </div>
                </div>
              </Card>
              
              {/* Decorative Elements */}
              <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full opacity-20 blur-xl"></div>
              <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-gradient-to-br from-blue-400 to-cyan-500 rounded-full opacity-15 blur-xl"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Our Values */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Our Values
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              These core principles guide everything we do, from production to delivery
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {values.map((value, index) => {
              const IconComponent = value.icon;
              return (
                <Card key={index} className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 group">
                  <CardContent className="p-6">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-gradient-to-br from-cyan-100 to-blue-100 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:from-cyan-500 group-hover:to-blue-600 transition-all duration-300">
                        <IconComponent className="h-6 w-6 text-cyan-600 group-hover:text-white transition-colors duration-300" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">{value.title}</h3>
                        <p className="text-gray-600 leading-relaxed">{value.description}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Our Team */}
      <section className="py-16 bg-gradient-to-br from-gray-50 to-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Meet Our Team
            </h2>
            <p className="text-lg text-gray-600">
              The dedicated professionals behind your ice delivery experience
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <Card key={index} className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 text-center group">
                <CardContent className="p-6">
                  <div className="w-24 h-24 mx-auto mb-4 bg-gradient-to-br from-cyan-100 to-blue-100 rounded-full flex items-center justify-center group-hover:from-cyan-500 group-hover:to-blue-600 transition-all duration-300">
                    <Users className="h-12 w-12 text-cyan-600 group-hover:text-white transition-colors duration-300" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-1">{member.name}</h3>
                  <div className="text-cyan-600 font-medium mb-3">{member.role}</div>
                  <p className="text-gray-600 text-sm leading-relaxed">{member.bio}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Certifications & Quality */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Quality & Certifications
            </h2>
            <p className="text-lg text-gray-600">
              Meeting the highest standards in ice production and delivery
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="border-2 border-green-200 bg-green-50 hover:shadow-lg transition-all duration-300">
              <CardContent className="p-6 text-center">
                <Shield className="h-12 w-12 text-green-600 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">FDA Approved</h3>
                <p className="text-sm text-gray-600">All production meets FDA food safety standards</p>
              </CardContent>
            </Card>
            
            <Card className="border-2 border-blue-200 bg-blue-50 hover:shadow-lg transition-all duration-300">
              <CardContent className="p-6 text-center">
                <Award className="h-12 w-12 text-blue-600 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Health Certified</h3>
                <p className="text-sm text-gray-600">Regular health department inspections passed</p>
              </CardContent>
            </Card>
            
            <Card className="border-2 border-cyan-200 bg-cyan-50 hover:shadow-lg transition-all duration-300">
              <CardContent className="p-6 text-center">
                <CheckCircle className="h-12 w-12 text-cyan-600 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Quality Tested</h3>
                <p className="text-sm text-gray-600">Every batch tested for purity and clarity</p>
              </CardContent>
            </Card>
            
            <Card className="border-2 border-purple-200 bg-purple-50 hover:shadow-lg transition-all duration-300">
              <CardContent className="p-6 text-center">
                <Star className="h-12 w-12 text-purple-600 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Insured & Bonded</h3>
                <p className="text-sm text-gray-600">Full liability coverage for your peace of mind</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-br from-cyan-600 via-blue-600 to-slate-700 text-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <h2 className="text-3xl lg:text-4xl font-bold">
            Ready to Experience the Difference?
          </h2>
          <p className="text-xl opacity-90 max-w-2xl mx-auto">
            Join over 1,000 satisfied customers who trust Ice Solutions for their ice delivery needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/quote">
              <Button size="lg" className="bg-white text-cyan-600 hover:bg-gray-50 shadow-lg">
                <Truck className="mr-2 h-5 w-5" />
                Get Your Quote
              </Button>
            </Link>
            <Link to="/contact">
              <Button 
                variant="outline" 
                size="lg"
                className="border-2 border-white text-white hover:bg-white hover:text-cyan-600"
              >
                <Phone className="mr-2 h-5 w-5" />
                Contact Us
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default AboutPage;