# 🧪 Marcus Sales Agent Testing Plan

## Goal
Test the improved voice message with real businesses to measure effectiveness before investing in full conversational AI.

---

## Phase 1: Friendly Testing (Week 1)

### Target: 5-10 Known Contacts
- Friends with businesses
- Family members who own businesses
- Contacts who won't mind a test call
- Previous customers or warm leads

### Purpose
- Get honest feedback on voice quality
- Test if message is professional enough
- Identify any issues before calling cold leads
- Gather suggestions for improvement

### Add Test Contacts to Google Sheet

| Business Name | Phone | Address | Type | Area | Status |
|--------------|-------|---------|------|------|--------|
| Friend's Bar | 876-XXX-XXXX | Address | bar | Area | New |
| Family Restaurant | 876-XXX-XXXX | Address | restaurant | Area | New |
| Known Caterer | 876-XXX-XXXX | Address | caterer | Area | New |

### Call Schedule
- **Monday 10 AM - 12 PM**: Call 3 contacts
- **Tuesday 2 PM - 4 PM**: Call 3 contacts
- **Wednesday 10 AM - 12 PM**: Call remaining contacts

### After Each Call
1. Wait 30 minutes
2. Call them personally to ask for feedback:
   - "Did you get a call from Marcus?"
   - "How did it sound?"
   - "Was the message clear?"
   - "Would you have been interested?"
   - "Any suggestions to improve it?"

### Success Metrics
- [ ] All contacts received the call
- [ ] Voice quality rated 7+ out of 10
- [ ] Message was clear and understandable
- [ ] At least 3 contacts said they'd be interested
- [ ] No technical issues

---

## Phase 2: Semi-Warm Leads (Week 2)

### Target: 10-15 Real Businesses (Not Cold)
- Businesses you've interacted with before
- Referrals from friends
- Businesses that know of Ice Solutions
- LinkedIn connections

### Purpose
- Test on real prospects
- Measure actual interest rate
- See if anyone places an order
- Refine messaging based on feedback

### Selection Criteria
- Businesses that likely need ice (bars, restaurants, caterers)
- Located in target areas (Washington Gardens, Half Way Tree, etc.)
- Currently in operation
- Reachable during business hours

### Call Schedule
- **Monday-Friday 10 AM - 4 PM**
- No more than 5 calls per day
- Space out calls by 1-2 hours

### Track Results

| Business | Called | Answered | Interested | Order | Notes |
|----------|--------|----------|-----------|-------|-------|
| Business 1 | ✅ | ✅ | ⚠️ | ❌ | Asked to call back |
| Business 2 | ✅ | ❌ | - | - | Voicemail |

### Success Metrics
- [ ] 60%+ answer rate (9+ out of 15 answer or hear voicemail)
- [ ] 20%+ interest rate (3+ express interest)
- [ ] 1-2 actual orders or follow-ups
- [ ] Positive feedback on professionalism

---

## Phase 3: Cold Outreach (Week 3+)

### Target: 50+ Cold Businesses
Only proceed to this phase if Phase 2 shows promise:
- Interest rate > 15%
- At least 1 order from Phase 2
- Positive feedback on message quality

### Purpose
- Scale up lead generation
- Measure true conversion rates
- Build customer pipeline
- Optimize calling process

### Generate Leads
```bash
# Generate 50 leads
curl -X POST "http://localhost:8001/api/leads/scrape?count=50"

# View stats
curl "http://localhost:8001/api/leads/stats"
```

### Call Schedule
- **Monday-Friday 10 AM - 4 PM**
- 10-15 calls per day
- Focus on high-potential areas first (Washington Gardens, Half Way Tree)

### Track Conversions

**Key Metrics to Track**:
- Total calls made
- Calls answered
- Voicemails left
- Interested responses
- Follow-up requests
- Actual orders
- Revenue generated

### Success Metrics
- [ ] 50%+ calls answered or voicemail delivered
- [ ] 10%+ interest rate
- [ ] 5%+ conversion to orders
- [ ] ROI positive (revenue > calling costs)

---

## Response Tracking Template

After each call, update the lead:

```bash
# Example for answered call
curl -X POST "http://localhost:8001/api/leads/update/876-XXX-XXXX" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Contacted",
    "call_notes": "Spoke with manager, interested in weekly deliveries",
    "result": "Follow up Friday to place first order"
  }'

# Example for voicemail
curl -X POST "http://localhost:8001/api/leads/update/876-XXX-XXXX" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Contacted",
    "call_notes": "Left voicemail with full message",
    "result": "Awaiting callback"
  }'

# Example for not interested
curl -X POST "http://localhost:8001/api/leads/update/876-XXX-XXXX" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Not Interested",
    "call_notes": "Have existing supplier, not looking to switch",
    "result": "No follow-up needed"
  }'

# Example for interested
curl -X POST "http://localhost:8001/api/leads/update/876-XXX-XXXX" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Interested",
    "call_notes": "Manager interested, wants pricing for 15 bags weekly",
    "result": "Send quote via email, follow up Monday"
  }'
```

---

## Feedback Form

After Phase 1 (Friendly Testing), ask each contact:

### Voice Quality (1-10)
- How natural did Marcus sound? _____
- Was the audio clear? _____
- Any issues with choppiness? _____

### Message Content (1-10)
- Was the purpose clear? _____
- Did it sound professional? _____
- Would you be interested based on the message? _____

### Suggestions
- What would you change about the script? _________________
- What did you like most? _________________
- What was confusing or unclear? _________________

---

## Decision Points

### After Phase 1 (Friendly Testing):
**If voice quality < 7/10**: 
- Adjust script and pacing
- Try different Polly voices
- Get more feedback

**If voice quality >= 7/10**: 
→ Proceed to Phase 2

### After Phase 2 (Semi-Warm Leads):
**If interest rate < 10%**:
- Message not resonating
- Consider conversational AI
- Revise script significantly

**If interest rate 10-20%**:
- Message is working!
- Continue with current setup
- Optimize based on feedback

**If interest rate > 20%**:
- Excellent results!
- Scale up to cold outreach
- Consider conversational AI to increase conversion further

### After Phase 3 (Cold Outreach):
**If conversion rate < 3%**:
- Reevaluate approach
- Consider conversational AI
- May need different strategy

**If conversion rate 3-5%**:
- Good results for cold outreach
- Continue and optimize
- Track ROI carefully

**If conversion rate > 5%**:
- Excellent performance!
- Scale up significantly
- Invest in conversational AI for even better results
- Hire team to handle follow-ups

---

## Cost Tracking

### Per Call Cost
- Twilio: ~$0.01/minute
- Average call: 1 minute
- **Cost per call: ~$0.01**

### Per Order Cost
Example calculation:
- 100 calls made
- 15 answered/voicemail (15% answer rate)
- 3 interested (20% of answered)
- 1 order (33% of interested)

**Cost per order: $1.00** (100 calls × $0.01)

If average order value is JMD $3,500 (10 bags):
**ROI: 3,500% (massive win!)**

---

## Weekly Review Template

Every Friday, review:

### Calls Made This Week
- Total calls: _____
- Answered: _____
- Voicemails: _____
- No answer: _____

### Results
- Interested: _____
- Not interested: _____
- Orders placed: _____
- Revenue generated: JMD $_____

### Costs
- Total calling costs: $_____
- Cost per order: $_____
- ROI: _____%

### What Worked
- Best performing areas: _____
- Best time to call: _____
- Most effective script points: _____

### What Didn't Work
- Low response areas: _____
- Common objections: _____
- Technical issues: _____

### Action Items for Next Week
1. _____
2. _____
3. _____

---

## Tips for Success

### Best Calling Times
- **Best**: Tuesday-Thursday, 10 AM - 12 PM, 2 PM - 4 PM
- **Good**: Monday-Friday, 9 AM - 5 PM
- **Avoid**: Before 9 AM, after 5 PM, weekends, holidays

### Follow-up Protocol
- If interested: Follow up within 24 hours
- If voicemail: Follow up in 2-3 days
- If no answer: Try again different time/day
- Maximum 3 attempts per lead

### Red Flags to Watch
- Consistent complaints about voice quality
- Businesses asking not to be called
- Very low interest rate (< 5%)
- Technical issues with calls

### Green Flags (Success Indicators)
- Businesses asking for more information
- Positive feedback on voice message
- Multiple orders from different sources
- Referrals from called businesses

---

## Tools to Help

### Interactive Helper Script
```bash
/app/test_calls_helper.sh
```
Use this for easy calling and tracking.

### View Dashboard
```
file:///app/lead_management_dashboard.html
```
Visual overview of all leads and stats.

### Quick Commands
```bash
# Sync from Google Sheets
curl "http://localhost:8001/api/leads/sync"

# Make a call
curl -X POST "http://localhost:8001/api/leads/call/876-XXX-XXXX?lead_name=Business%20Name"

# Check stats
curl "http://localhost:8001/api/leads/stats"
```

---

## When to Upgrade to Conversational AI

Consider upgrading if:
- ✅ Current system generating 5+ orders/week
- ✅ Interest rate > 15% consistently
- ✅ ROI is strongly positive
- ✅ Ready to invest $40-100/month for better results
- ✅ Want to increase conversion rate 2-3x

Signs you're ready:
- Businesses asking questions you can't answer
- Missing opportunities due to no conversation
- Competitors have better calling systems
- Want to scale to 100+ calls/day

---

## Success!

By following this plan, you'll:
1. Validate the system works
2. Gather real feedback
3. Measure actual conversion rates
4. Build initial customer base
5. Make data-driven decision on conversational AI

**Start with Phase 1 this week! 🚀**
