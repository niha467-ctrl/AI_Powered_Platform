# AI NEGOTIATION STRATEGY ENGINE (Single File)

import random
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any

# -----------------------------
# Data Models
# -----------------------------

@dataclass
class Offer:
    price: float
    concessions: Dict[str, Any] = field(default_factory=dict)
    timestamp: int = 0


@dataclass
class OpponentProfile:
    aggressiveness: float = 0.5   # 0 = passive, 1 = aggressive
    flexibility: float = 0.5      # willingness to compromise
    budget_sensitivity: float = 0.5
    history: List[Offer] = field(default_factory=list)


# -----------------------------
# Strategy Engine
# -----------------------------

class NegotiationEngine:
    def __init__(self, base_price: float):
        self.base_price = base_price
        self.current_round = 0
        self.opponent = OpponentProfile()
        self.my_min_threshold = base_price * 0.7
        self.my_max_threshold = base_price * 1.2

    # -------------------------
    # Opponent Modeling
    # -------------------------
    def update_opponent_model(self, offer: Offer):
        self.opponent.history.append(offer)

        if len(self.opponent.history) > 1:
            deltas = [
                self.opponent.history[i].price - self.opponent.history[i+1].price
                for i in range(len(self.opponent.history)-1)
            ]
            avg_change = sum(deltas) / len(deltas)

            # Infer aggressiveness & flexibility
            self.opponent.aggressiveness = min(1.0, max(0.0, abs(avg_change) / self.base_price))
            self.opponent.flexibility = 1.0 - self.opponent.aggressiveness

    # -------------------------
    # Strategy Selection
    # -------------------------
    def choose_strategy(self):
        if self.opponent.aggressiveness > 0.7:
            return "defensive"
        elif self.opponent.flexibility > 0.6:
            return "collaborative"
        else:
            return "balanced"

    # -------------------------
    # Offer Generator
    # -------------------------
    def generate_offer(self):
        strategy = self.choose_strategy()
        self.current_round += 1

        if strategy == "defensive":
            price = self.base_price * (1.05 + random.uniform(0, 0.1))
        elif strategy == "collaborative":
            price = self.base_price * (0.95 + random.uniform(-0.05, 0.05))
        else:
            price = self.base_price * (1.0 + random.uniform(-0.08, 0.08))

        price = max(self.my_min_threshold, min(self.my_max_threshold, price))

        return Offer(price=round(price, 2), timestamp=self.current_round)

    # -----------------------------
    # Offer Evaluation
    # -----------------------------
    def evaluate_offer(self, offer: Offer):
        utility = (self.base_price - offer.price) / self.base_price

        if offer.price < self.my_min_threshold:
            return "reject"
        elif utility > 0.15:
            return "accept"
        elif utility > 0.05:
            return "counter"
        else:
            return "negotiate"

    # -----------------------------
    # Counter Offer Logic
    # -----------------------------
    def counter_offer(self, offer: Offer):
        adjustment_factor = (self.opponent.flexibility + 0.3) / 2
        counter_price = offer.price + (self.base_price - offer.price) * adjustment_factor

        counter_price = max(self.my_min_threshold, min(self.my_max_threshold, counter_price))

        return Offer(price=round(counter_price, 2), timestamp=self.current_round)

    # -----------------------------
    # Simulation Step
    # -----------------------------
    def step(self, opponent_offer: Offer):
        self.update_opponent_model(opponent_offer)

        decision = self.evaluate_offer(opponent_offer)

        if decision == "accept":
            return {"status": "accepted", "offer": opponent_offer}
        elif decision == "reject":
            return {"status": "rejected", "offer": opponent_offer}
        else:
            counter = self.counter_offer(opponent_offer)
            return {"status": "counter", "offer": counter}

    # -----------------------------
    # Run Full Negotiation
    # -----------------------------
    def negotiate(self, opponent_offers: List[float]):
        logs = []

        for price in opponent_offers:
            offer = Offer(price=price, timestamp=self.current_round)
            result = self.step(offer)

            logs.append({
                "round": self.current_round,
                "opponent_offer": price,
                "decision": result["status"],
                "response_price": result["offer"].price
            })

            if result["status"] == "accepted":
                break

        return logs


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":
    engine = NegotiationEngine(base_price=1000)

    opponent_prices = [1200, 1150, 1100, 1050, 1020, 1005]

    results = engine.negotiate(opponent_prices)

    for r in results:
        print(r)