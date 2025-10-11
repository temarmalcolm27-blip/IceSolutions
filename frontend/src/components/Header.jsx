import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from './ui/button';
import { Sheet, SheetContent, SheetTrigger } from './ui/sheet';
import { Menu, Phone, Truck } from 'lucide-react';
import './Logo.css';

const Header = () => {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Products', href: '/products' },
    { name: 'About', href: '/about' },
    { name: 'Contact', href: '/contact' }
  ];

  const isActive = (href) => location.pathname === href;

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-lg">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <img 
              src="/IceSolution-Logo.png" 
              alt="Ice Solutions Logo" 
              className="h-12 w-auto logo-transparent logo-header"
            />
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`text-sm font-medium transition-colors hover:text-cyan-600 ${
                  isActive(item.href) 
                    ? 'text-cyan-600 border-b-2 border-cyan-600 pb-1' 
                    : 'text-gray-600'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Contact Info & CTA */}
          <div className="hidden lg:flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm">
              <Phone className="h-4 w-4 text-cyan-600" />
              <span className="text-gray-600">(876) 490-7208</span>
            </div>
            <Link to="/quote">
              <Button className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white">
                <Truck className="mr-2 h-4 w-4" />
                Get Quote
              </Button>
            </Link>
          </div>

          {/* Mobile Menu */}
          <div className="md:hidden">
            <Sheet open={isOpen} onOpenChange={setIsOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="sm">
                  <Menu className="h-6 w-6" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[280px]">
                <div className="flex flex-col space-y-4 mt-8">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      onClick={() => setIsOpen(false)}
                      className={`text-lg font-medium transition-colors hover:text-cyan-600 ${
                        isActive(item.href) ? 'text-cyan-600' : 'text-gray-600'
                      }`}
                    >
                      {item.name}
                    </Link>
                  ))}
                  <div className="pt-4 border-t border-gray-200">
                    <div className="flex items-center space-x-2 text-sm mb-4">
                      <Phone className="h-4 w-4 text-cyan-600" />
                      <span className="text-gray-600">(876) 490-7208</span>
                    </div>
                    <Link to="/quote" onClick={() => setIsOpen(false)}>
                      <Button className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white">
                        <Truck className="mr-2 h-4 w-4" />
                        Get Quote
                      </Button>
                    </Link>
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;