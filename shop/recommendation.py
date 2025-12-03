# shop/recommendation.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from .models import Product, UserInteraction

class RecommendationEngine:
    def __init__(self):
        self.scaler = StandardScaler()
    
    def get_product_features(self):
        products = Product.objects.all()
        features = []
        product_ids = []
        
        for product in products:
            feature_vector = [
                float(product.price) / 1000,
                product.popularity_score,
                product.rating / 5.0,
                float(product.category.id)
            ]
            features.append(feature_vector)
            product_ids.append(product.id)
        
        return np.array(features), product_ids
    
    def get_user_interactions_matrix(self, user):
        interactions = UserInteraction.objects.filter(user=user)
        weights = {'view': 1, 'cart': 3, 'purchase': 5, 'like': 4, 'dislike': -2}
        
        product_scores = {}
        for interaction in interactions:
            product_id = interaction.product.id
            weight = weights.get(interaction.interaction_type, 1)
            
            if product_id in product_scores:
                product_scores[product_id] += weight
            else:
                product_scores[product_id] = weight
        
        return product_scores
    
    def calculate_content_similarity(self, product_id, all_features, product_ids):
        try:
            target_idx = product_ids.index(product_id)
            target_features = all_features[target_idx].reshape(1, -1)
            similarities = cosine_similarity(target_features, all_features)[0]
            return similarities
        except ValueError:
            return np.zeros(len(product_ids))
    
    def get_recommendations(self, user, num_recommendations=6, exclude_products=None):
        if exclude_products is None:
            exclude_products = []
        
        all_features, product_ids = self.get_product_features()
        if len(product_ids) == 0:
            return []
        
        all_features = self.scaler.fit_transform(all_features)
        user_scores = self.get_user_interactions_matrix(user)
        recommendation_scores = np.zeros(len(product_ids))
        
        if user_scores:
            for interacted_product_id, interaction_score in user_scores.items():
                if interacted_product_id in product_ids:
                    similarities = self.calculate_content_similarity(
                        interacted_product_id, all_features, product_ids
                    )
                    recommendation_scores += similarities * interaction_score
        else:
            for idx, product_id in enumerate(product_ids):
                product = Product.objects.get(id=product_id)
                recommendation_scores[idx] = product.popularity_score * product.rating
        
        product_score_pairs = list(zip(product_ids, recommendation_scores))
        product_score_pairs.sort(key=lambda x: x[1], reverse=True)
        
        recommended_ids = []
        for product_id, score in product_score_pairs:
            if product_id not in exclude_products and product_id not in user_scores:
                recommended_ids.append(product_id)
                if len(recommended_ids) >= num_recommendations:
                    break
        
        return Product.objects.filter(id__in=recommended_ids)
    
    def get_similar_products(self, product_id, num_recommendations=4):
        all_features, product_ids = self.get_product_features()
        if product_id not in product_ids:
            return []
        
        all_features = self.scaler.fit_transform(all_features)
        similarities = self.calculate_content_similarity(product_id, all_features, product_ids)
        
        product_score_pairs = list(zip(product_ids, similarities))
        product_score_pairs.sort(key=lambda x: x[1], reverse=True)
        
        similar_ids = [pid for pid, score in product_score_pairs[1:num_recommendations+1]]
        return Product.objects.filter(id__in=similar_ids)