# HVIA Task 01 — Olist Business Discovery

**Data Analysis Internship**
Submitted by Andrew Emad Luis

---











Olist is growing
        ↓
More orders create more operational exposure
        ↓
Late delivery is strongly linked to dissatisfaction
        ↓
Why are orders late?
        ↓
Seller supply is concentrated geographically
        ↓
Customers are distributed nationally
        ↓
Cross-state shipping creates additional friction
        ↓
Small sellers add another operational challenge
        ↓
Reviews show the customer impact
        ↓
Therefore: predict delivery risk
        ↓
Then: understand customer complaints
        ↓
Then: identify sellers needing intervention
        ↓
Then: automate inventory synchronization
        ↓
SEE → PREDICT → ACT



























## 1. Company Research Summary

### Overview
Olist is a Brazilian technology company founded in 2015 in Curitiba by Tiago Dalvi. It pioneered a "marketplace of marketplaces" model: instead of small and medium merchants having to integrate separately with each of Brazil's dominant e-commerce platforms (and navigate tax rules across 27 states), Olist provides one integration point that connects them to many marketplaces at once.

### Business Model & Ecosystem
Olist generates revenue through transaction fees, subscriptions, and financial products for merchants, aligning its growth with that of its sellers. Its ecosystem spans three pillars:

- **Commerce:** Olist Store (sell across marketplaces) and Olist Shops (own online storefront)
- **Logistics:** Olist Pax, a cloud-based logistics and fulfillment network
- **Capital:** Olist Credit and Olist Pay, financial services for merchants

This ecosystem was expanded through the 2021 acquisitions of Tiny (ERP) and Vnda (e-commerce platform). Conceptually, the business moves in one connected loop: sellers list products through Olist, Olist routes them to 170+ marketplaces and channels, orders flow back through products/inventory, payments, and shipping, and customer feedback loops back to drive growth.

### Scale & Growth
Olist now serves roughly 50,000 businesses, has raised a total of $314M across eight funding rounds, and reached a $1.5B valuation after a $186M Series E round led by Wellington Management, with participation from SoftBank and Goldman Sachs.

### Target Customers
Small and medium merchants — brick-and-mortar shopkeepers going online for the first time, or existing online sellers seeking better placement and reach across Brazil's fragmented marketplace landscape.

### Known Pain Points (from public reviews)
Independent reviews of Olist's ERP integration (Shopify App Store) surface recurring themes: inventory sync failures between Olist and connected storefronts, integration/login errors, and support experienced as slow or bot-driven rather than human. These operational frictions are relevant context for the solution proposed in Section 4.

---

## 2. Dataset Understanding & Key Findings

### Structure
The public Olist Store dataset (Kaggle) contains 9 linked tables covering ~100,000 real, anonymized orders placed between September 2016 and October 2018:

| Table | Rows | Role |
|---|---|---|
| orders | 99,441 | Core order records — status, timestamps |
| customers | 99,441 | Customer id + location |
| order_items | 112,650 | Line items — links product, seller, price, freight |
| order_payments | 103,886 | Payment method, installments, value |
| order_reviews | 99,224 | Review score, comments |
| products | 32,951 | Product category, dimensions, weight |
| sellers | 3,095 | Seller id + location |
| geolocation | 1,000,163 | Zip-code-level lat/long |
| category_name_translation | 71 | PT → EN category names |

The tables connect through a clear chain: customer → order → order_items → (product + seller) → payment + review, with both customers and sellers geolocated via zip-code prefix.

### Business Overview Charts

![Order status distribution](charts/01_order_status.png)

*Figure 1 — Order status distribution. The vast majority (97%) of orders reach "delivered" status.*

![Monthly order volume](charts/02_monthly_orders_trend.png)

*Figure 2 — Monthly order volume. Olist shows healthy, steady growth from late 2016 through mid-2018.*

---

## 3. Analysis & Business Story

The data tells a consistent story: Olist's core value proposition — connecting small sellers to national demand — works, but the physical distance between where sellers are based and where customers live creates a structural logistics tax. That tax shows up as longer delivery times, higher freight cost, and materially worse customer reviews whenever an order crosses state lines or misses its estimate.

### Finding 1 — Delivery delay is the strongest driver of dissatisfaction
6.8% of delivered orders arrive later than the estimated delivery date, with an average delay of 10.6 days among late orders. The effect on customer sentiment is stark:

![Delay vs review score](charts/03_delay_vs_review_score.png)

*Figure 3 — Average review score: on-time orders (4.29/5) vs late orders (2.27/5).*

### Finding 2 — Sellers are concentrated far from most customers
60% of sellers are based in São Paulo state, while customers are spread nationwide (SP is only 42% of customers):

![Customers vs sellers by state](charts/06_customers_vs_sellers_geography.png)

*Figure 4 — Customer distribution by state (left) vs seller distribution by state (right).*

This mismatch has a direct, measurable cost. 63.8% of orders ship across state lines, and cross-state orders take almost twice as long and cost ~75% more in freight than same-state orders:

![Same vs cross state](charts/07_same_vs_cross_state.png)

*Figure 5 — Delivery time and freight cost: same-state vs cross-state shipments.*

The regional impact varies widely — customers in Bahia, Rio Grande do Sul and Rio de Janeiro wait 15-19 days on average, versus 8.3 days for customers in São Paulo:

![Delivery time by state](charts/08_delivery_time_by_state.png)

*Figure 6 — Average delivery time by customer state (top 8 states by order volume).*

### Finding 3 — The seller base is a long tail
61% of the 3,095 sellers placed 10 or fewer orders over roughly two years, while the top 10% of sellers generate 67.5% of total revenue:

![Seller concentration](charts/05_seller_concentration.png)

*Figure 7 — Revenue share: top 10% of sellers vs the remaining 90%.*

### Finding 4 — Overall satisfaction is high, but with a visible gap
58% of reviews are 5-star, but 14.7% are 1-2 star — consistent with the delivery-delay pattern above. Only 41% of reviews include a written comment, leaving a large pool of qualitative feedback uncaptured beyond the numeric score.

![Review score distribution](charts/09_review_score_distribution.png)

*Figure 8 — Customer review score distribution (1-5 stars).*

### Finding 5 — Revenue concentration by category and payment behavior
health_beauty, watches_gifts, bed_bath_table, sports_leisure and computers_accessories are the top five categories by revenue:

![Top categories by revenue](charts/04_top_categories_revenue.png)

*Figure 9 — Top 10 product categories by total revenue.*

74% of orders are paid by credit card, with an average of 2.85 installments — installment payment is a normal and expected part of the Brazilian buying journey:

![Payment methods](charts/10_payment_methods.png)

*Figure 10 — Payment method distribution.*

### Business Story Summary
This is not a demand problem — order volume grew steadily throughout the dataset's window — it is an operational/logistics problem layered on top of healthy growth. It disproportionately affects customers outside the Southeast, and disproportionately involves the long tail of small, low-volume sellers who are least likely to have their own logistics sophistication. Three questions this points to for Olist's leadership:

1. Which lanes (seller state → customer state) drive most of the late-delivery volume, and are freight/carrier choices on those lanes optimized?
2. Should small, long-tail sellers be routed through Olist's own fulfillment network (Olist Pax) by default, rather than handling logistics themselves?
3. What is hiding in the 59% of reviews with no written comment — are there recurring complaint themes in the 41% that do, that a scaled text-analysis pass would surface?

---

## 4. Solution Proposal — What HVIA Could Offer Olist

Rather than proposing a generic analytics tool, the data points to one clear, evidence-backed opportunity: reducing the delivery-delay/dissatisfaction loop, with two supporting workstreams.

### Core proposal: Predictive Delivery Risk Scoring (Logistics Intelligence + Forecasting)
A model that scores every order's late-delivery risk at the moment it is placed, using seller state, customer state, category, carrier, and seasonality — enabling Olist to proactively re-route, expedite, or set more accurate customer expectations before a complaint happens rather than after.
تنبو وصول الطلب 

### Supporting workstream 1: Customer Intelligence
Sentiment and topic extraction across the written-review text (41% of reviews) to surface complaint themes not visible in the star rating alone, and to estimate what similar themes might exist in the unwritten 59%.
41% بس من المراجعات فيها تعليق مكتوب (نص فعلي، مش رقم بس)
59% الباقيين بس حطوا تقييم بالنجوم من غير ما يكتبوا سبب

المشكلة إن الرقم لوحده (1-5 نجوم) مش بيقول السبب. يعني لو عميل حط نجمة واحدة، احنا عارفين إنه مش راضي، لكن مش عارفين ليه بالظبط — التأخير؟ المنتج وصل تالف؟ خدمة العملاء وحشة؟

الحل المقترح هنا:

Sentiment Analysis (تحليل المشاعر): نظام بياخد النص المكتوب ويحدد هل الكلام ده إيجابي، سلبي، أو محايد
Topic Extraction (استخراج المواضيع): نظام يكتشف إيه "الموضوع" الأساسي في كل تعليق — مثلاً "شحن"، "جودة منتج"، "تغليف"، "خدمة عملاء"

ليه مهم؟

بدل ما Olist تعرف بس "في ناس مش راضية"، تقدر تعرف بالظبط إيه أكتر سبب بيتكرر للشكوى
وبما إن عندنا الـ 41% بس فيهم نص، نقدر نستخدمهم كـ "عينة" نتعلم منها الأنماط، وبعدين نحاول نخمن (نقدّر) هل نفس الأنماط دي موجودة في الـ 59% الباقيين (اللي معندهمش نص) بناءً على معلومات تانية زي رقم التقييم نفسه أو حالة الطلب.

خلاصة بسيطة: ده اقتراح إن HVIA تستخدم تقنيات معالجة اللغة الطبيعية (NLP) عشان تحول التعليقات النصية لمعلومات مفيدة ومنظمة، بدل ما تفضل مجرد كلام مكتوب محدش بيحلله.

### Supporting workstream 2: Seller Performance Analytics
A dashboard tracking the long tail of small sellers (61% of the base) against top-performer benchmarks, to identify which sellers would benefit most from being migrated onto Olist's own fulfillment network.

This is deliberately framed as a problem to solve, not a tool to sell — every recommendation above traces directly back to a specific, quantified pattern in Section 3.

عمل "لوحة متابعة" (dashboard) بتقارن أداء كل بائع صغير بأداء أفضل البائعين (زي: سرعة الشحن، نسبة الشكاوى، تقييمات العملاء)
البائعين اللي أداءهم ضعيف، نقترح عليهم ينتقلوا لنظام Olist Pax (شبكة التوصيل الخاصة بـ Olist نفسها) بدل ما يدبروا الشحن بنفسهم
كده Olist تحسن تجربة العملاء حتى مع البائعين الصغار، من غير ما تضطرهم يتعلموا لوجستيات معقدة بنفسهم
---

**أتمتة تزامن المخزون (Inventory Sync Automation)**

نظام آلي بيحافظ على تطابق كميات المخزون لحظيًا عبر كل المنصات والمتاجر المتصلة بـ Olist. ده بيعالج مباشرة مشكلة عدم تزامن المخزون اللي ظهرت في مراجعات تكامل نظام Olist (القسم 1) — شكوى متكررة من تجار بيلاقوا كمية مخزونهم مش متطابقة بين القنوات، وده بيأدي لبيع منتجات غير متوفرة فعليًا وإلغاء الطلبات. أتمتة الخطوة دي بتقلل عدد الطلبات "غير المتاحة" أو "الملغاة" (اللي ظهرت في القسم 2)، وكمان بتقلل العبء على فريق الدعم الفني.

## 5. Outreach Message Draft

**Channel:** LinkedIn (direct message to a relevant Operations/Data leader at Olist).

> Hi [Name],
>
> I've been looking at Olist's marketplace-of-marketplaces model, and ran some analysis on the public order data. One pattern stood out: orders that arrive later than the estimated delivery date average a 2.3/5 review score, cross-state shipments (64% of all orders) take almost twice as long and cost ~75% more in freight than same-state ones,this maybe cause churn نسبة مغادرة.
>
> At HVIA, we build predictive systems that flag delivery risk at the moment an order is placed, so it can be addressed before it turns into a bad review,Automation for markets stock,AI-Driven Customer Complaint handling & Churn Prevention Platform,Marketing automated agent And more AI Solutions for any case.                    I'd love to share the approach in a quick 15-minute call this week, if you're open to it.
>
> Best,
> Andrew HVIA-Member

---

**Understand → Analyze → Propose → Pitch**
