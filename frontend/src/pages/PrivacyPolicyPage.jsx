import React from 'react';
import Header from '../components/Header';
import RunningBanner from '../components/RunningBanner';
import Footer from '../components/Footer';
import { Card, CardContent } from '../components/ui/card';
import { Shield } from 'lucide-react';

const PrivacyPolicyPage = () => {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <RunningBanner />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-cyan-50 py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-4">
            <div className="inline-block p-3 bg-cyan-100 rounded-full">
              <Shield className="h-8 w-8 text-cyan-600" />
            </div>
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Privacy Policy
            </h1>
            <p className="text-lg text-gray-600">
              Last updated: {new Date().toLocaleDateString()}
            </p>
          </div>
        </div>
      </section>

      {/* Policy Content */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <Card>
              <CardContent className="p-8 space-y-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">1. Information We Collect</h2>
                  <p className="text-gray-600 mb-4">
                    We collect information you provide directly to us when using our ice delivery service:
                  </p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li><strong>Personal Information:</strong> Name, email address, phone number, delivery address</li>
                    <li><strong>Order Information:</strong> Order details, payment information (processed securely through Stripe)</li>
                    <li><strong>Communication:</strong> Messages you send us through contact forms or email</li>
                    <li><strong>Product Notifications:</strong> Email addresses for product availability alerts</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">2. How We Use Your Information</h2>
                  <p className="text-gray-600 mb-4">We use the information we collect to:</p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>Process and deliver your ice orders</li>
                    <li>Send order confirmations and delivery updates</li>
                    <li>Respond to your inquiries and provide customer support</li>
                    <li>Send product availability notifications (if you subscribed)</li>
                    <li>Improve our services and website experience</li>
                    <li>Comply with legal obligations</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">3. Information Sharing</h2>
                  <p className="text-gray-600 mb-4">
                    We do not sell your personal information. We may share your information with:
                  </p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li><strong>Service Providers:</strong> Payment processors (Stripe), email service (SendGrid), delivery partners</li>
                    <li><strong>Legal Requirements:</strong> When required by law or to protect our rights</li>
                    <li><strong>Business Transfers:</strong> In connection with a merger, sale, or acquisition</li>
                  </ul>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">4. Data Security</h2>
                  <p className="text-gray-600">
                    We implement appropriate security measures to protect your personal information. Payment information is encrypted and processed securely through Stripe. However, no method of transmission over the internet is 100% secure.
                  </p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">5. Your Rights</h2>
                  <p className="text-gray-600 mb-4">You have the right to:</p>
                  <ul className="list-disc pl-6 space-y-2 text-gray-600">
                    <li>Access, update, or delete your personal information</li>
                    <li>Opt-out of marketing communications</li>
                    <li>Unsubscribe from product notification emails</li>
                    <li>Request a copy of your data</li>
                  </ul>
                  <p className="text-gray-600 mt-4">
                    To exercise these rights, contact us at <a href="mailto:icesolutions.mybusiness@gmail.com" className="text-cyan-600 hover:underline">icesolutions.mybusiness@gmail.com</a>
                  </p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">6. Cookies</h2>
                  <p className="text-gray-600">
                    We use essential cookies to ensure proper website functionality. We do not use tracking or advertising cookies.
                  </p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">7. Children's Privacy</h2>
                  <p className="text-gray-600">
                    Our services are not directed to children under 13. We do not knowingly collect personal information from children.
                  </p>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">8. Changes to This Policy</h2>
                  <p className="text-gray-600">
                    We may update this privacy policy from time to time. Changes will be posted on this page with an updated date.
                  </p>
                </div>

                <div className="bg-cyan-50 border-l-4 border-cyan-600 p-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Contact Us</h3>
                  <p className="text-gray-600 mb-4">
                    If you have questions about this Privacy Policy, please contact us:
                  </p>
                  <div className="space-y-2 text-gray-600">
                    <p><strong>Email:</strong> <a href="mailto:icesolutions.mybusiness@gmail.com" className="text-cyan-600 hover:underline">icesolutions.mybusiness@gmail.com</a></p>
                    <p><strong>Phone:</strong> <a href="tel:+18764907208" className="text-cyan-600 hover:underline">(876) 490-7208</a></p>
                    <p><strong>Address:</strong> Rosend Avenue, Washington Gardens, Kingston 20, Jamaica</p>
                  </div>
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

export default PrivacyPolicyPage;
