import React, { useState } from 'react';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Card, CardContent } from '../components/ui/card';
import { HelpCircle, ChevronDown, ChevronUp } from 'lucide-react';

const FAQPage = () => {
  const [openIndex, setOpenIndex] = useState(null);

  const faqs = [
    {
      question: "What type of ice do you sell?",
      answer: "We specialize in premium cube ice made from purified water. It's the same crystal-clear, restaurant-quality ice used by top restaurants and bars across Kingston. Currently, we offer Quick Fix (10lb bags), with Party Solution (50lb) and Mega Solution (100lb) coming soon."
    },
    {
      question: "How fast can you deliver?",
      answer: "We offer same-day delivery! Just order at least 2 hours before you need your ice. We deliver Monday-Sunday, 7AM-9PM. For urgent orders, call us at (876) 490-7208 and we'll do our best to accommodate you."
    },
    {
      question: "What are your delivery areas?",
      answer: "We deliver throughout Kingston and surrounding areas. Delivery is FREE in Washington Gardens! All other areas have a small JMD $300 delivery fee."
    },
    {
      question: "Do you offer bulk discounts?",
      answer: "Yes! Bulk discounts are applied automatically: 5-9 bags get 5% off, 10-19 bags get 10% off, and 20+ bags get 15% off. The more you order, the more you save!"
    },
    {
      question: "How much ice do I need for my event?",
      answer: "Use our Event Planning Calculator on the website! As a general rule: plan for about 1-2 pounds of ice per guest for a 4-hour event. For 50 guests, you'd need about 5-10 bags (50-100 lbs). Bars and longer events need more."
    },
    {
      question: "What payment methods do you accept?",
      answer: "We accept all major credit and debit cards through our secure Stripe payment system. Payment is processed online when you place your order."
    },
    {
      question: "Can I cancel my order?",
      answer: "Yes! You can cancel or modify your order up to 1 hour before the scheduled delivery time. Just call us at (876) 490-7208. Refunds are processed within 5-7 business days."
    },
    {
      question: "What if I'm not satisfied with the ice quality?",
      answer: "We have a 100% satisfaction guarantee! If there's any issue with ice quality, let us know within 24 hours and we'll offer a replacement delivery or full refund. No returns needed - we trust your feedback."
    },
    {
      question: "Is there a minimum order?",
      answer: "No minimum order required! Whether you need 1 bag or 100 bags, we'll deliver. However, ordering 5 or more bags gets you our bulk discount starting at 5% off."
    },
    {
      question: "How should I store the ice?",
      answer: "Keep the bags in a freezer until needed. Our bags are designed to stack easily and stay fresh. For events, transfer to coolers with insulation about 1-2 hours before the event starts."
    },
    {
      question: "Do you offer recurring deliveries for businesses?",
      answer: "Yes! For restaurants, bars, and businesses that need regular ice deliveries, we offer recurring delivery services with priority scheduling. Contact us at (876) 490-7208 to set up a business account."
    },
    {
      question: "When will 50lb and 100lb bags be available?",
      answer: "We're working on adding these sizes soon! Click 'Notify When Available' on the Products page to get an email alert when they're ready to order."
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <div className="inline-block p-3 bg-cyan-100 rounded-full">
              <HelpCircle className="h-8 w-8 text-cyan-600" />
            </div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">Frequently Asked Questions</h1>
            <p className="text-lg text-gray-600">Everything you need to know about our ice delivery service</p>
          </div>
        </div>
      </section>

      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto space-y-4">
            {faqs.map((faq, index) => (
              <Card key={index} className="cursor-pointer hover:shadow-lg transition-shadow" onClick={() => setOpenIndex(openIndex === index ? null : index)}>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start">
                    <h3 className="text-lg font-semibold text-gray-900 pr-4">{faq.question}</h3>
                    {openIndex === index ? (
                      <ChevronUp className="h-5 w-5 text-cyan-600 flex-shrink-0" />
                    ) : (
                      <ChevronDown className="h-5 w-5 text-gray-400 flex-shrink-0" />
                    )}
                  </div>
                  {openIndex === index && (
                    <p className="mt-4 text-gray-600 leading-relaxed">{faq.answer}</p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="mt-16 max-w-3xl mx-auto">
            <Card className="bg-gradient-to-br from-cyan-50 to-blue-50">
              <CardContent className="p-8 text-center">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Still Have Questions?</h3>
                <p className="text-gray-600 mb-6">We're here to help! Contact us anytime.</p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <a href="tel:+18764907208" className="inline-block px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg hover:shadow-lg transition-all">Call (876) 490-7208</a>
                  <a href="mailto:temarmalcolm27@gmail.com" className="inline-block px-6 py-3 bg-white text-cyan-600 border-2 border-cyan-600 rounded-lg hover:bg-cyan-50 transition-all">Email Us</a>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default FAQPage;