import React, { useEffect, useState } from 'react';
import './FallingIce.css';

const FallingIce = () => {
  const [iceElements, setIceElements] = useState([]);

  useEffect(() => {
    // Create ice cubes and circular molds
    const elements = [];
    
    // Generate 20 ice elements (mix of cubes and circles)
    for (let i = 0; i < 20; i++) {
      elements.push({
        id: i,
        type: Math.random() > 0.5 ? 'cube' : 'circle',
        left: Math.random() * 100, // Random horizontal position (%)
        delay: Math.random() * 5, // Random delay (0-5s)
        duration: 3 + Math.random() * 2, // Random fall duration (3-5s)
        size: 30 + Math.random() * 40, // Random size (30-70px)
        rotation: Math.random() * 360, // Random initial rotation
        bounceHeight: 20 + Math.random() * 30 // Random bounce height
      });
    }
    
    setIceElements(elements);
  }, []);

  return (
    <div className="falling-ice-container">
      {iceElements.map((ice) => (
        <div
          key={ice.id}
          className={`ice-element ${ice.type}`}
          style={{
            left: `${ice.left}%`,
            animationDelay: `${ice.delay}s`,
            animationDuration: `${ice.duration}s`,
            width: `${ice.size}px`,
            height: `${ice.size}px`,
            '--bounce-height': `${ice.bounceHeight}px`,
            '--rotation': `${ice.rotation}deg`
          }}
        >
          {ice.type === 'cube' ? (
            <div className="ice-cube">
              <div className="cube-face front"></div>
              <div className="cube-face back"></div>
              <div className="cube-face right"></div>
              <div className="cube-face left"></div>
              <div className="cube-face top"></div>
              <div className="cube-face bottom"></div>
            </div>
          ) : (
            <div className="ice-circle">
              <div className="circle-inner"></div>
              <div className="circle-shine"></div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default FallingIce;
