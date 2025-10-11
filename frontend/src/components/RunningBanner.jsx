import React from 'react';
import './RunningBanner.css';

const RunningBanner = () => {
  const messages = [
    "Premium Ice Delivery for Every Event",
    "Crystal-clear, restaurant-quality ice delivered fresh to your door",
    "Perfect for parties, events, restaurants, and bars",
    "FREE DELIVERY in Washington Gardens"
  ];

  return (
    <div className="running-banner-container">
      {/* Blurred background images */}
      <div className="banner-background">
        <img 
          src="https://images.unsplash.com/photo-1505009258427-29298f4dc5f6?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxpY2UlMjBjdWJlc3xlbnwwfHx8Ymx1ZXwxNzYwMjIzNjcxfDA&ixlib=rb-4.1.0&q=85" 
          alt="" 
          className="banner-bg-image"
        />
        <img 
          src="https://images.unsplash.com/photo-1654146218080-40d0ec9cce46?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwxfHxpY2UlMjBidWNrZXR8ZW58MHx8fGJsdWV8MTc2MDIyMzY4M3ww&ixlib=rb-4.1.0&q=85" 
          alt="" 
          className="banner-bg-image"
        />
        <img 
          src="https://images.unsplash.com/photo-1570564117549-f9cb65185db2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxpY2UlMjBjdWJlc3xlbnwwfHx8Ymx1ZXwxNzYwMjIzNjcxfDA&ixlib=rb-4.1.0&q=85" 
          alt="" 
          className="banner-bg-image"
        />
      </div>

      {/* Scrolling text */}
      <div className="banner-scroll-wrapper">
        <div className="banner-scroll-content">
          {/* Duplicate the messages for seamless infinite scroll */}
          {[...messages, ...messages, ...messages].map((message, index) => (
            <span key={index} className="banner-message">
              {message}
              <span className="banner-separator">•</span>
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RunningBanner;
