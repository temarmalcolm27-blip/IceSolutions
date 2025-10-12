import React from 'react';
import { Link } from 'react-router-dom';
import { Phone, Mail, MapPin, Clock, Truck, Shield, Star } from 'lucide-react';
import './Logo.css';

const Footer = () => {
  return (
    <footer className="bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          {/* Company Info */}
          <div className="space-y-4">
            <img 
              src="/IceSolution-Logo.png" 
              alt="Ice Solutions" 
              className="h-12 w-auto logo-transparent logo-footer"
            />
            <p className="text-gray-300 text-sm leading-relaxed">
              Your trusted partner for premium party ice delivery. 
              Crystal-clear quality, reliable service, and fast delivery to your door.
            </p>
            <div className="flex space-x-4">
              <div className="flex items-center text-cyan-400">
                <Star className="h-4 w-4 mr-1" />
                <span className="text-sm">4.9/5 Rating</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Quick Links</h3>
            <nav className="flex flex-col space-y-2">
              <Link to="/" className="text-gray-300 hover:text-cyan-400 transition-colors text-sm">
                Home
              </Link>
              <Link to="/products" className="text-gray-300 hover:text-cyan-400 transition-colors text-sm">
                Products
              </Link>
              <Link to="/about" className="text-gray-300 hover:text-cyan-400 transition-colors text-sm">
                About Us
              </Link>
              <Link to="/quote" className="text-gray-300 hover:text-cyan-400 transition-colors text-sm">
                Get Quote
              </Link>
              <Link to="/contact" className="text-gray-300 hover:text-cyan-400 transition-colors text-sm">
                Contact
              </Link>
            </nav>
          </div>

          {/* Services */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Our Services</h3>
            <ul className="space-y-2 text-sm">
              <li className="flex items-center text-gray-300">
                <Truck className="h-4 w-4 mr-2 text-cyan-400" />
                Same-Day Delivery
              </li>
              <li className="flex items-center text-gray-300">
                <Shield className="h-4 w-4 mr-2 text-cyan-400" />
                Quality Guarantee
              </li>
              <li className="flex items-center text-gray-300">
                <Clock className="h-4 w-4 mr-2 text-cyan-400" />
                Flexible Time Slots
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-white">Contact Info</h3>
            <div className="space-y-3">
              <div className="flex items-center text-gray-300">
                <Phone className="h-4 w-4 mr-3 text-cyan-400" />
                <span className="text-sm">(876) 490-7208</span>
              </div>
              <a href="mailto:temarmalcolm27@gmail.com" className="flex items-center text-gray-300 hover:text-cyan-400 transition-colors">
                <Mail className="h-4 w-4 mr-3 text-cyan-400" />
                <span className="text-sm">temarmalcolm27@gmail.com</span>
              </a>
              <div className="flex items-start text-gray-300">
                <MapPin className="h-4 w-4 mr-3 text-cyan-400 mt-0.5 flex-shrink-0" />
                <span className="text-sm">Rosend Avenue, Washington Gardens,<br />Kingston 20, Jamaica</span>
              </div>
              <div className="flex items-center text-gray-300">
                <Clock className="h-4 w-4 mr-3 text-cyan-400" />
                <span className="text-sm">Mon-Sun: 7AM - 9PM</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-700 mt-12 pt-8 flex flex-col sm:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
            © 2025 Ice Solutions. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 sm:mt-0">
            <Link to="#" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">
              Privacy Policy
            </Link>
            <Link to="#" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">
              Terms of Service
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;