import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ProductsPage from "./pages/ProductsPage";
import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";
import QuotePage from "./pages/QuotePage";
import SimpleQuotePage from "./pages/SimpleQuotePage";
import QuickOrderPage from "./pages/QuickOrderPage";
import EventPlanningPage from "./pages/EventPlanningPage";
import BulkOrdersPage from "./pages/BulkOrdersPage";
import BulkOrderFormPage from "./pages/BulkOrderFormPage";
import CheckoutPage from "./pages/CheckoutPage";
import OrderConfirmationPage from "./pages/OrderConfirmationPage";
import PrivacyPolicyPage from "./pages/PrivacyPolicyPage";
import TermsConditionsPage from "./pages/TermsConditionsPage";
import RefundPolicyPage from "./pages/RefundPolicyPage";
import FAQPage from "./pages/FAQPage";
import OrderTrackingPage from "./pages/OrderTrackingPage";
import NotFoundPage from "./pages/NotFoundPage";
import ScrollToTop from "./components/ScrollToTop";
import ChatWidget from "./components/ChatWidget";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <ScrollToTop />
        <Toaster position="top-right" />
        <ChatWidget />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/quote" element={<SimpleQuotePage />} />
          <Route path="/quote-old" element={<QuotePage />} />
          <Route path="/event-planning" element={<EventPlanningPage />} />
          <Route path="/bulk-orders" element={<BulkOrdersPage />} />
          <Route path="/bulk-order-form" element={<BulkOrderFormPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/order-confirmation" element={<OrderConfirmationPage />} />
          <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />
          <Route path="/terms" element={<TermsConditionsPage />} />
          <Route path="/refund-policy" element={<RefundPolicyPage />} />
          <Route path="/faq" element={<FAQPage />} />
          <Route path="/track-order" element={<OrderTrackingPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;