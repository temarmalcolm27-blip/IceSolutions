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
              <a href="mailto:icesolutions.mybusiness@gmail.com" className="flex items-center text-gray-300 hover:text-cyan-400 transition-colors">
                <Mail className="h-4 w-4 mr-3 text-cyan-400" />
                <span className="text-sm">icesolutions.mybusiness@gmail.com</span>
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
        <div className="border-t border-gray-700 mt-12 pt-8">
          <div className="flex flex-col sm:flex-row justify-between items-center mb-6">
            <p className="text-gray-400 text-sm">
              © 2025 Ice Solutions. All rights reserved.
            </p>
            <div className="flex flex-wrap justify-center gap-4 mt-4 sm:mt-0">
              <Link to="/privacy-policy" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">
                Privacy Policy
              </Link>
              <Link to="/terms" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">
                Terms & Conditions
              </Link>
              <Link to="/refund-policy" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">
                Refund Policy
              </Link>
              <Link to="/faq" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">
                FAQ
              </Link>
              <Link to="/track-order" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">
                Track Order
              </Link>
            </div>
          </div>
          
          {/* Social Media Links */}
          <div className="flex justify-center gap-6 pt-4 border-t border-gray-700">
            <a href="https://facebook.com/icesolutionsja" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-cyan-400 transition-colors">
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a href="https://instagram.com/icesolutionsja" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-cyan-400 transition-colors">
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
              </svg>
            </a>
            <a href="https://wa.me/18764907208" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-cyan-400 transition-colors">
              <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.890-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;