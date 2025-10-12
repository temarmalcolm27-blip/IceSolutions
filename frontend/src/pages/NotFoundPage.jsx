import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Home, Search } from 'lucide-react';

const NotFoundPage = () => {
  return (
    <div className="min-h-screen bg-white flex flex-col">
      <Header />
      <RunningBanner />
      
      <section className="flex-grow flex items-center justify-center py-16 bg-gradient-to-br from-blue-50 via-white to-cyan-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-8 max-w-2xl mx-auto">
            <div className="text-9xl font-bold bg-gradient-to-r from-cyan-500 to-blue-600 bg-clip-text text-transparent">
              404
            </div>
            
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Oops! Page Not Found
            </h1>
            
            <p className="text-xl text-gray-600">
              The page you're looking for has melted away... just like ice on a hot day!
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
              <Link to="/">
                <Button size="lg" className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white">
                  <Home className="mr-2 h-5 w-5" />
                  Go Home
                </Button>
              </Link>
              
              <Link to="/products">
                <Button size="lg" variant="outline" className="border-cyan-600 text-cyan-600 hover:bg-cyan-50">
                  <Search className="mr-2 h-5 w-5" />
                  View Products
                </Button>
              </Link>
            </div>

            <div className="pt-8">
              <p className="text-gray-500">Need help? Contact us at:</p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center mt-4">
                <a href="tel:+18764907208" className="text-cyan-600 hover:underline font-medium">(876) 490-7208</a>
                <span className="hidden sm:inline text-gray-300">|</span>
                <a href="mailto:temarmalcolm27@gmail.com" className="text-cyan-600 hover:underline font-medium">temarmalcolm27@gmail.com</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default NotFoundPage;