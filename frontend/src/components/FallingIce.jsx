import React, { useEffect, useState } from 'react';
import './FallingIce.css';

const FallingIce = () => {
  const [iceElements, setIceElements] = useState([]);

  useEffect(() => {
    // Create only 3D ice cubes
    const elements = [];
    
    // Generate 15 HD 3D ice cubes
    for (let i = 0; i < 15; i++) {
      elements.push({
        id: i,
        left: Math.random() * 100, // Random horizontal position (%)
        delay: Math.random() * 5, // Random delay (0-5s)
        duration: 3 + Math.random() * 2, // Random fall duration (3-5s)
        size: 40 + Math.random() * 40, // Random size (40-80px) - larger for HD
        rotationX: Math.random() * 360, // Random X rotation
        rotationY: Math.random() * 360, // Random Y rotation
        rotationZ: Math.random() * 360, // Random Z rotation
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
          className="ice-element"
          style={{
            left: `${ice.left}%`,
            animationDelay: `${ice.delay}s`,
            animationDuration: `${ice.duration}s`,
            '--bounce-height': `${ice.bounceHeight}px`,
            '--rotation-x': `${ice.rotationX}deg`,
            '--rotation-y': `${ice.rotationY}deg`,
            '--rotation-z': `${ice.rotationZ}deg`,
            '--size': `${ice.size}px`
          }}
        >
          <div className="ice-cube-3d">
            <div className="cube-face front"></div>
            <div className="cube-face back"></div>
            <div className="cube-face right"></div>
            <div className="cube-face left"></div>
            <div className="cube-face top"></div>
            <div className="cube-face bottom"></div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default FallingIce;
