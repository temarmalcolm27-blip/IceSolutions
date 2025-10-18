import React, { useState, useEffect, useRef } from 'react';
import { X, Send, MessageCircle, Minimize2 } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card } from './ui/card';
import './ChatWidget.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [leadInfo, setLeadInfo] = useState({
    name: '',
    phone: '',
    email: '',
    businessName: '',
    productInterest: '10lb Party Ice Bags',
    quantity: 1
  });
  const [isMinimized, setIsMinimized] = useState(false);
  
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      // Initial greeting from Temar
      setMessages([{
        id: 1,
        text: "Hi! I'm Temar Malcolm, owner of IceSolutions. How can I help you with your ice needs today? 🧊",
        sender: 'agent',
        timestamp: new Date()
      }]);
    }
  }, [isOpen]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: messages.length + 1,
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          conversationHistory: messages.map(m => ({
            role: m.sender === 'user' ? 'user' : 'assistant',
            content: m.text
          }))
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      
      const agentMessage = {
        id: messages.length + 2,
        text: data.response,
        sender: 'agent',
        timestamp: new Date(),
        showLeadForm: data.requestLeadInfo
      };

      setMessages(prev => [...prev, agentMessage]);
      
      // If agent is requesting lead information, show the form
      if (data.requestLeadInfo) {
        setShowLeadForm(true);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: messages.length + 2,
        text: "I apologize, I'm having trouble connecting right now. Please try calling us at (876) 490-7208 or email orders@icesolutions.com",
        sender: 'agent',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitLeadInfo = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/leads/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...leadInfo,
          inquiry: messages[messages.length - 2]?.text || 'Chat inquiry',
          conversationHistory: messages.map(m => m.text).join('\n')
        })
      });

      if (!response.ok) {
        throw new Error('Failed to submit lead');
      }

      const successMessage = {
        id: messages.length + 1,
        text: `Thank you ${leadInfo.name}! I've saved your information and you'll be hearing from us soon. Is there anything else I can help you with?`,
        sender: 'agent',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, successMessage]);
      setShowLeadForm(false);
      
      // Reset form
      setLeadInfo({
        name: '',
        phone: '',
        email: '',
        businessName: '',
        productInterest: '10lb Party Ice Bags',
        quantity: 1
      });

    } catch (error) {
      console.error('Error submitting lead:', error);
      const errorMessage = {
        id: messages.length + 1,
        text: "I had trouble saving your information. Please try again or call us at (876) 490-7208.",
        sender: 'agent',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    setIsMinimized(false);
  };

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  return (
    <div className="chat-widget-container">
      {/* Chat Button */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="chat-toggle-button"
          aria-label="Open chat"
        >
          <MessageCircle size={24} />
          <span className="chat-badge">Chat with Temar</span>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <Card className={`chat-window ${isMinimized ? 'minimized' : ''}`}>
          {/* Header */}
          <div className="chat-header">
            <div className="chat-header-info">
              <div className="agent-avatar">TM</div>
              <div>
                <div className="agent-name">Temar Malcolm</div>
                <div className="agent-status">
                  <span className="status-dot"></span>
                  Online
                </div>
              </div>
            </div>
            <div className="chat-header-actions">
              <button 
                onClick={toggleMinimize}
                className="chat-header-button"
                aria-label={isMinimized ? "Maximize" : "Minimize"}
              >
                <Minimize2 size={18} />
              </button>
              <button 
                onClick={toggleChat}
                className="chat-header-button"
                aria-label="Close chat"
              >
                <X size={18} />
              </button>
            </div>
          </div>

          {/* Messages Container */}
          {!isMinimized && (
            <>
              <div className="chat-messages" ref={chatContainerRef}>
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`message ${message.sender === 'user' ? 'message-user' : 'message-agent'}`}
                  >
                    <div className="message-content">
                      {message.text}
                    </div>
                    <div className="message-time">
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="message message-agent">
                    <div className="message-content">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Lead Form */}
              {showLeadForm && (
                <div className="lead-form-container">
                  <form onSubmit={handleSubmitLeadInfo} className="lead-form">
                    <div className="form-title">Let me get your information</div>
                    
                    <input
                      type="text"
                      placeholder="Your Name *"
                      value={leadInfo.name}
                      onChange={(e) => setLeadInfo({...leadInfo, name: e.target.value})}
                      required
                      className="lead-input"
                    />
                    
                    <input
                      type="tel"
                      placeholder="Phone Number *"
                      value={leadInfo.phone}
                      onChange={(e) => setLeadInfo({...leadInfo, phone: e.target.value})}
                      required
                      className="lead-input"
                    />
                    
                    <input
                      type="email"
                      placeholder="Email Address *"
                      value={leadInfo.email}
                      onChange={(e) => setLeadInfo({...leadInfo, email: e.target.value})}
                      required
                      className="lead-input"
                    />
                    
                    <input
                      type="text"
                      placeholder="Business Name (optional)"
                      value={leadInfo.businessName}
                      onChange={(e) => setLeadInfo({...leadInfo, businessName: e.target.value})}
                      className="lead-input"
                    />
                    
                    <select
                      value={leadInfo.productInterest}
                      onChange={(e) => setLeadInfo({...leadInfo, productInterest: e.target.value})}
                      required
                      className="lead-input"
                    >
                      <option value="10lb Party Ice Bags">10lb Party Ice Bags</option>
                      <option value="50lb Commercial Ice Bags">50lb Commercial Ice Bags (Coming Soon)</option>
                      <option value="100lb Industrial Ice Bags">100lb Industrial Ice Bags (Coming Soon)</option>
                      <option value="Bulk Order">Bulk Order</option>
                      <option value="Event Planning">Event Planning</option>
                    </select>
                    
                    <input
                      type="number"
                      placeholder="Quantity Needed"
                      value={leadInfo.quantity}
                      onChange={(e) => setLeadInfo({...leadInfo, quantity: parseInt(e.target.value)})}
                      min="1"
                      required
                      className="lead-input"
                    />
                    
                    <div className="form-actions">
                      <button
                        type="button"
                        onClick={() => setShowLeadForm(false)}
                        className="btn-secondary"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        disabled={isLoading}
                        className="btn-primary"
                      >
                        Submit
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {/* Input Area */}
              <div className="chat-input-container">
                <Input
                  type="text"
                  placeholder="Type your message..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  disabled={isLoading}
                  className="chat-input"
                />
                <Button
                  onClick={handleSendMessage}
                  disabled={isLoading || !inputMessage.trim()}
                  className="chat-send-button"
                  size="icon"
                >
                  <Send size={18} />
                </Button>
              </div>
            </>
          )}
        </Card>
      )}
    </div>
  );
};

export default ChatWidget;
