from .models import Box

class BoxRecommendationService:
    # 10% void-fill buffer by default to account for realistic packing gaps & dunnage[cite: 5]
    PACKING_EFFICIENCY_FACTOR = 0.90

    @staticmethod
    def calculate_total_order_metrics(order):
        total_weight = 0.0
        total_volume = 0.0
        items_list = []

        # Optimized with select_related to eliminate N+1 query overhead[cite: 5, 14]
        for item in order.items.select_related('product').all():
            for _ in range(item.quantity):
                total_weight += item.product.weight
                total_volume += (item.product.length * item.product.width * item.product.height)
                items_list.append({
                    'l': item.product.length,
                    'w': item.product.width,
                    'h': item.product.height
                })
        return total_weight, total_volume, items_list

    @classmethod
    def recommend_box(cls, order):
        total_weight, total_volume, items = cls.calculate_total_order_metrics(order)

        if not items:
            return None

        # Fetch active boxes sorted by cost ascending, then volume ascending[cite: 5]
        available_boxes = sorted(
            Box.objects.filter(is_active=True),
            key=lambda b: (b.cost, b.volume)
        )

        for box in available_boxes:
            # 1. Weight Check[cite: 5]
            if total_weight > box.max_weight:
                continue

            # 2. Volumetric Check (with packing efficiency buffer)[cite: 5]
            if total_volume > (box.volume * cls.PACKING_EFFICIENCY_FACTOR):
                continue

            # 3. 3D Shelf/Layer Geometric Fit Check with 6-way orientation rotation[cite: 5]
            if cls._can_fit_items_3d_shelf(items, box):
                return box

        return None

    @staticmethod
    def _get_orientations(item):
        dims = [item['l'], item['w'], item['h']]
        from itertools import permutations
        return list(set(permutations(dims)))

    @classmethod
    def _can_fit_items_3d_shelf(cls, items, box):
        """
        3D Next-Fit Decreasing Height (NFDH) Shelf-Packing heuristic with 6-way item rotation.
        Places items onto 2D shelves within 3D layers inside the box, preventing false positives
        where multiple items pass individual bounds checks but exceed cumulative dimensions[cite: 5].
        """
        sorted_items = sorted(items, key=lambda x: x['l'] * x['w'] * x['h'], reverse=True)

        box_L, box_W, box_H = box.inner_length, box.inner_width, box.inner_height

        curr_x = 0.0
        curr_y = 0.0
        curr_z = 0.0
        row_max_w = 0.0
        layer_max_h = 0.0

        for item in sorted_items:
            placed = False
            orientations = sorted(cls._get_orientations(item), key=lambda o: (o[2], o[1], o[0]))

            for (il, iw, ih) in orientations:
                if il > box_L or iw > box_W or ih > box_H:
                    continue

                # Case A: Fits in current row on current layer[cite: 5]
                if curr_x + il <= box_L and curr_y + iw <= box_W and curr_z + ih <= box_H:
                    curr_x += il
                    row_max_w = max(row_max_w, iw)
                    layer_max_h = max(layer_max_h, ih)
                    placed = True
                    break

                # Case B: Start a new row on the current layer[cite: 5]
                next_y = curr_y + row_max_w
                if il <= box_L and next_y + iw <= box_W and curr_z + ih <= box_H:
                    curr_x = il
                    curr_y = next_y
                    row_max_w = iw
                    layer_max_h = max(layer_max_h, ih)
                    placed = True
                    break

                # Case C: Start a new vertical layer[cite: 5]
                next_z = curr_z + layer_max_h
                if il <= box_L and iw <= box_W and next_z + ih <= box_H:
                    curr_x = il
                    curr_y = 0.0
                    curr_z = next_z
                    row_max_w = iw
                    layer_max_h = ih
                    placed = True
                    break

            if not placed:
                return False

        return True