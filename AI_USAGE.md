AI tools used: GEMINI, COPILOT
I have used copilot to right the code easily it recommend us the code.
Prompts1: When a customer places an order, the warehouse team needs to know which shipping box should be used
Prompts2: Each product has dimensions and weight
Prompts3: Each box has internal dimensions, maximum weight capacity, and cost
Mistake identified: Then imported the models in views.py
AI intially generated(1): In the first response, _can_fit_items sorted each item's dimensions and checked item_dims[i] <= box_dims[i] inside a for loop without tracking cumulative occupied space across multiple items.
Mistake identified: Order contained 4 books (each 18 x 12 x 3 cm = 648 cm, total 2,592 cm), each book fit inside a 20 x 15 x 10 cm (3,000 cm) Small Mailer. If we do vertically (4 × 3 cm = 12 cm), they exceed height 10cm of the Small Mailer—and cannot be placed in a 20 × 15 cm footprint. This produced a false positive.
Fixes: Replaced _can_fit_items with _can_fit_items_3d_shelf, implementing a 3D Next-Fit Decreasing Height, shelf-packing with 6-way item rotation and a 0.90 volumetric efficiency
AI generated(2): order.save() without update_fields, and order.items.all() without select_related('product')
Fixes: Updated views.py to use order.save(update_fields=['recommended_box']) to prevent race conditions on concurrent warehouse updates (e.g., is_packed), and added .select_related('product') in calculate_total_order_metrics to eliminate N+1 database queries.
AI intially generated(3): Setup instructions refer to add product and other models into admin but admin.py module is ommitted in first step
Fixes: Added admin.py to register in admin panel and requiremt.txt also
AI Initial APIView-based DRF Implementation: Replaced with DRF generics views because raw APIView classes do not automatically render HTML form input fields in the DRF Browsable API.
Issue: Using APIView forced users to manually type JSON keys in the raw data editor when testing POST and PUT requests.
Fix: Migrated endpoints to generics.ListCreateAPIView and generics.RetrieveUpdateDestroyAPIView with explicit serializer_class definitions.